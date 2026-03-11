package controller

import (
	"agri-trace/model"
	"agri-trace/pkg/blockchain"
	"agri-trace/pkg/ipfs"
	"fmt"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"gorm.io/gorm"
)

// TraceController 溯源核心控制器
type TraceController struct {
	DB              *gorm.DB
	BlockchainClient blockchain.Client
	IPFSClient      ipfs.Client
}

// ==================== 批次管理 ====================

// CreateBatchRequest 创建批次请求体
type CreateBatchRequest struct {
	ProductName string  `json:"product_name" binding:"required"`
	ProductType string  `json:"product_type" binding:"required"`
	Quantity    float64 `json:"quantity" binding:"required,gt=0"`
	Unit        string  `json:"unit" binding:"required"`
	OriginInfo  string  `json:"origin_info" binding:"required"`
}

// CreateBatch 创建农产品批次
// @Summary 创建农产品批次
// @Tags 溯源管理
// @Security BearerAuth
// @Accept json
// @Produce json
// @Router /api/v1/batches [post]
func (ctrl *TraceController) CreateBatch(c *gin.Context) {
	var req CreateBatchRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"code": 400, "msg": err.Error()})
		return
	}

	farmerID, _ := c.Get("user_id")
	// 生成唯一批次号
	batchNo := fmt.Sprintf("BATCH-%s-%s",
		time.Now().Format("20060102"),
		uuid.New().String()[:8])

	batch := model.AgriBatch{
		BatchNo:     batchNo,
		ProductName: req.ProductName,
		ProductType: req.ProductType,
		Quantity:    req.Quantity,
		Unit:        req.Unit,
		OriginInfo:  req.OriginInfo,
		FarmerID:    farmerID.(uint),
		Status:      0,
	}

	if err := ctrl.DB.Create(&batch).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"code": 500, "msg": "批次创建失败"})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"code": 200,
		"msg":  "批次创建成功",
		"data": gin.H{"batch_no": batchNo, "batch_id": batch.ID},
	})
}

// ListBatches 获取批次列表
func (ctrl *TraceController) ListBatches(c *gin.Context) {
	var batches []model.AgriBatch
	query := ctrl.DB.Model(&model.AgriBatch{})

	// 角色过滤：种植户只能看自己的批次
	role, _ := c.Get("role")
	if role == "farmer" {
		userID, _ := c.Get("user_id")
		query = query.Where("farmer_id = ?", userID)
	}

	if err := query.Find(&batches).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"code": 500, "msg": "查询失败"})
		return
	}
	c.JSON(http.StatusOK, gin.H{"code": 200, "data": batches})
}

// ==================== 溯源记录管理 ====================

// AddTraceRecordRequest 添加溯源记录请求体
type AddTraceRecordRequest struct {
	BatchID       uint                   `json:"batch_id" binding:"required"`
	NodeType      string                 `json:"node_type" binding:"required,oneof=planting harvesting inspecting packing transporting retailing"`
	OperationTime string                 `json:"operation_time" binding:"required"`
	Location      string                 `json:"location" binding:"required"`
	EnvData       map[string]interface{} `json:"env_data"`
}

// AddTraceRecord 添加溯源节点记录并上链
// @Summary 添加溯源节点记录
// @Tags 溯源管理
// @Security BearerAuth
// @Router /api/v1/trace/records [post]
func (ctrl *TraceController) AddTraceRecord(c *gin.Context) {
	var req AddTraceRecordRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"code": 400, "msg": err.Error()})
		return
	}

	// 查询批次
	var batch model.AgriBatch
	if err := ctrl.DB.First(&batch, req.BatchID).Error; err != nil {
		c.JSON(http.StatusNotFound, gin.H{"code": 404, "msg": "批次不存在"})
		return
	}

	// 解析操作时间
	opTime, err := time.Parse("2006-01-02 15:04:05", req.OperationTime)
	if err != nil {
		opTime = time.Now()
	}

	operatorID, _ := c.Get("user_id")

	// 构建上链数据
	payload := blockchain.TracePayload{
		BatchNo:       batch.BatchNo,
		NodeType:      req.NodeType,
		OperatorID:    operatorID.(uint),
		OperationTime: opTime,
		Location:      req.Location,
		EnvData:       req.EnvData,
	}

	// 调用区块链（含降级机制）
	txResult, err := ctrl.BlockchainClient.SubmitTrace(payload)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"code": 500, "msg": "上链失败: " + err.Error()})
		return
	}

	// 写入 MySQL
	record := model.TraceRecord{
		BatchID:       req.BatchID,
		NodeType:      req.NodeType,
		OperatorID:    operatorID.(uint),
		OperationTime: opTime,
		Location:      req.Location,
		EnvData:       model.JSONMap(req.EnvData),
		TxHash:        txResult.TxHash,
		BlockHeight:   txResult.BlockHeight,
	}
	if err := ctrl.DB.Create(&record).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"code": 500, "msg": "记录保存失败"})
		return
	}

	// 更新批次状态
	statusMap := map[string]int8{
		"planting": 0, "harvesting": 1, "inspecting": 2,
		"packing": 2, "transporting": 3, "retailing": 4,
	}
	if newStatus, ok := statusMap[req.NodeType]; ok {
		ctrl.DB.Model(&batch).Update("status", newStatus)
	}

	c.JSON(http.StatusOK, gin.H{
		"code": 200,
		"msg":  "溯源记录添加成功",
		"data": gin.H{
			"record_id":    record.ID,
			"tx_hash":      txResult.TxHash,
			"block_height": txResult.BlockHeight,
			"is_mock":      txResult.IsMock,
		},
	})
}

// ==================== 溯源查询（小程序接口）====================

// TraceNodeVO 溯源时间轴节点视图对象
type TraceNodeVO struct {
	ID            uint                   `json:"id"`
	NodeType      string                 `json:"node_type"`
	NodeLabel     string                 `json:"node_label"`
	OperationTime string                 `json:"operation_time"`
	Location      string                 `json:"location"`
	EnvData       map[string]interface{} `json:"env_data"`
	TxHash        string                 `json:"tx_hash"`
	BlockHeight   int64                  `json:"block_height"`
	IPFSFiles     []IPFSFileVO           `json:"ipfs_files"`
}

// IPFSFileVO IPFS文件视图对象
type IPFSFileVO struct {
	FileName string `json:"file_name"`
	FileType string `json:"file_type"`
	CID      string `json:"cid"`
	URL      string `json:"url"`
}

// TraceQueryResponse 溯源查询响应
type TraceQueryResponse struct {
	BatchNo     string        `json:"batch_no"`
	ProductName string        `json:"product_name"`
	ProductType string        `json:"product_type"`
	Quantity    float64       `json:"quantity"`
	Unit        string        `json:"unit"`
	OriginInfo  string        `json:"origin_info"`
	Status      int8          `json:"status"`
	StatusLabel string        `json:"status_label"`
	Timeline    []TraceNodeVO `json:"timeline"`
}

// nodeLabels 节点类型中文标签
var nodeLabels = map[string]string{
	"planting":     "种植",
	"harvesting":   "采收",
	"inspecting":   "质检",
	"packing":      "装箱",
	"transporting": "运输",
	"retailing":    "上架",
}

// statusLabels 批次状态中文标签
var statusLabels = map[int8]string{
	0: "种植中", 1: "已采收", 2: "已质检", 3: "运输中", 4: "已上架",
}

// QueryByTraceCode 根据溯源码查询完整溯源链（微信小程序接口）
// @Summary 溯源查询
// @Tags 溯源查询
// @Param trace_code path string true "溯源批次号"
// @Produce json
// @Router /api/v1/trace/{trace_code} [get]
func (ctrl *TraceController) QueryByTraceCode(c *gin.Context) {
	traceCode := c.Param("trace_code")
	if traceCode == "" {
		c.JSON(http.StatusBadRequest, gin.H{"code": 400, "msg": "溯源码不能为空"})
		return
	}

	// 查询批次
	var batch model.AgriBatch
	if err := ctrl.DB.Where("batch_no = ?", traceCode).First(&batch).Error; err != nil {
		c.JSON(http.StatusNotFound, gin.H{"code": 404, "msg": "溯源码无效或批次不存在"})
		return
	}

	// 查询溯源记录
	var records []model.TraceRecord
	ctrl.DB.Where("batch_id = ?", batch.ID).Order("operation_time ASC").Find(&records)

	// 构建时间轴
	timeline := make([]TraceNodeVO, 0, len(records))
	for _, r := range records {
		// 查询关联的 IPFS 文件
		var files []model.IPFSFile
		ctrl.DB.Where("record_id = ?", r.ID).Find(&files)

		fileVOs := make([]IPFSFileVO, 0, len(files))
		for _, f := range files {
			fileVOs = append(fileVOs, IPFSFileVO{
				FileName: f.FileName,
				FileType: f.FileType,
				CID:      f.CID,
				URL:      ctrl.IPFSClient.GetURL(f.CID),
			})
		}

		node := TraceNodeVO{
			ID:            r.ID,
			NodeType:      r.NodeType,
			NodeLabel:     nodeLabels[r.NodeType],
			OperationTime: r.OperationTime.Format("2006-01-02 15:04:05"),
			Location:      r.Location,
			EnvData:       map[string]interface{}(r.EnvData),
			TxHash:        r.TxHash,
			BlockHeight:   r.BlockHeight,
			IPFSFiles:     fileVOs,
		}
		timeline = append(timeline, node)
	}

	resp := TraceQueryResponse{
		BatchNo:     batch.BatchNo,
		ProductName: batch.ProductName,
		ProductType: batch.ProductType,
		Quantity:    batch.Quantity,
		Unit:        batch.Unit,
		OriginInfo:  batch.OriginInfo,
		Status:      batch.Status,
		StatusLabel: statusLabels[batch.Status],
		Timeline:    timeline,
	}

	c.JSON(http.StatusOK, gin.H{"code": 200, "data": resp})
}

// GetBlockInfo 查询区块信息
func (ctrl *TraceController) GetBlockInfo(c *gin.Context) {
	var height int64
	if err := c.ShouldBindQuery(&struct {
		Height int64 `form:"height"`
	}{Height: height}); err == nil {
	}
	heightParam := c.Query("height")
	if heightParam == "" {
		c.JSON(http.StatusBadRequest, gin.H{"code": 400, "msg": "请提供区块高度参数"})
		return
	}
	var h int64
	fmt.Sscanf(heightParam, "%d", &h)

	info, err := ctrl.BlockchainClient.GetBlockInfo(h)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"code": 500, "msg": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{"code": 200, "data": info})
}

// ListTraceRecords 获取溯源记录列表（管理端）
func (ctrl *TraceController) ListTraceRecords(c *gin.Context) {
	batchID := c.Query("batch_id")
	var records []model.TraceRecord
	query := ctrl.DB.Model(&model.TraceRecord{})
	if batchID != "" {
		query = query.Where("batch_id = ?", batchID)
	}
	query.Order("operation_time ASC").Find(&records)
	c.JSON(http.StatusOK, gin.H{"code": 200, "data": records})
}
