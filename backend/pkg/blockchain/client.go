// Package blockchain 封装 Hyperledger Fabric 链码调用层
// 实现"优雅降级"机制：当 Fabric 网络不可达时，自动切换到 Mock 模式
// 生产环境需配置 fabric-sdk-go 并将 MockMode 设为 false
package blockchain

import (
	"agri-trace/config"
	"agri-trace/pkg/gmsm"
	"encoding/json"
	"fmt"
	"log"
	"time"
)

// TracePayload 上链数据结构
type TracePayload struct {
	BatchNo       string                 `json:"batch_no"`
	NodeType      string                 `json:"node_type"`
	OperatorID    uint                   `json:"operator_id"`
	OperationTime time.Time              `json:"operation_time"`
	Location      string                 `json:"location"`
	EnvData       map[string]interface{} `json:"env_data"`
}

// TxResult 链码调用结果
type TxResult struct {
	TxHash      string `json:"tx_hash"`
	BlockHeight int64  `json:"block_height"`
	Timestamp   int64  `json:"timestamp"`
	IsMock      bool   `json:"is_mock"`
}

// BlockInfo 区块信息
type BlockInfo struct {
	BlockHeight  int64  `json:"block_height"`
	TxCount      int    `json:"tx_count"`
	DataHash     string `json:"data_hash"`
	PreviousHash string `json:"previous_hash"`
}

// Client 区块链客户端接口
type Client interface {
	SubmitTrace(payload TracePayload) (*TxResult, error)
	QueryTrace(batchNo string) ([]TracePayload, error)
	GetBlockInfo(height int64) (*BlockInfo, error)
	IsConnected() bool
}

// fabricClient 真实 Fabric 客户端（需要 fabric-sdk-go）
type fabricClient struct {
	cfg *config.BlockchainConfig
}

// mockClient Mock 模式客户端
type mockClient struct {
	cfg *config.BlockchainConfig
}

// NewClient 创建区块链客户端（自动检测并降级）
func NewClient(cfg *config.BlockchainConfig) Client {
	if cfg.MockMode {
		log.Println("[Blockchain] 配置为 Mock 模式，使用模拟区块链数据")
		return &mockClient{cfg: cfg}
	}
	// 尝试连接真实 Fabric 网络
	client := &fabricClient{cfg: cfg}
	if !client.IsConnected() {
		log.Println("[Blockchain] Fabric 网络不可达，自动降级为 Mock 模式")
		return &mockClient{cfg: cfg}
	}
	log.Println("[Blockchain] 已连接到 Fabric 网络")
	return client
}

// ==================== fabricClient 实现 ====================

func (c *fabricClient) IsConnected() bool {
	// 实际生产环境：使用 fabric-sdk-go 检测网络连通性
	// 此处简化为检测配置文件是否存在
	// 生产环境示例：
	// sdk, err := fabsdk.New(config.FromFile(c.cfg.ConfigPath))
	// return err == nil
	return false // 演示环境默认不连接
}

func (c *fabricClient) SubmitTrace(payload TracePayload) (*TxResult, error) {
	// 生产环境：调用 fabric-sdk-go 提交交易
	// channelClient, err := channel.New(sdk.ChannelContext(c.cfg.ChannelName, ...))
	// response, err := channelClient.Execute(channel.Request{ChaincodeID: c.cfg.ChaincodeName, Fcn: "CreateTrace", Args: ...})
	return nil, fmt.Errorf("Fabric 网络未连接")
}

func (c *fabricClient) QueryTrace(batchNo string) ([]TracePayload, error) {
	return nil, fmt.Errorf("Fabric 网络未连接")
}

func (c *fabricClient) GetBlockInfo(height int64) (*BlockInfo, error) {
	return nil, fmt.Errorf("Fabric 网络未连接")
}

// ==================== mockClient 实现 ====================

func (c *mockClient) IsConnected() bool {
	return true // Mock 模式始终"在线"
}

func (c *mockClient) SubmitTrace(payload TracePayload) (*TxResult, error) {
	// 生成模拟国密 SM3 交易哈希
	dataBytes, _ := json.Marshal(payload)
	txHash := gmsm.SM3Hash(dataBytes)
	blockHeight := gmsm.GenerateMockBlockHeight(1000)

	log.Printf("[Blockchain-Mock] 模拟上链成功: BatchNo=%s, NodeType=%s, TxHash=%s",
		payload.BatchNo, payload.NodeType, txHash)

	return &TxResult{
		TxHash:      txHash,
		BlockHeight: blockHeight,
		Timestamp:   time.Now().Unix(),
		IsMock:      true,
	}, nil
}

func (c *mockClient) QueryTrace(batchNo string) ([]TracePayload, error) {
	// Mock 模式下返回空列表，由上层从 MySQL 读取
	return []TracePayload{}, nil
}

func (c *mockClient) GetBlockInfo(height int64) (*BlockInfo, error) {
	// 生成模拟区块信息
	return &BlockInfo{
		BlockHeight:  height,
		TxCount:      int(height%10) + 1,
		DataHash:     gmsm.SM3Hash([]byte(fmt.Sprintf("block:%d", height))),
		PreviousHash: gmsm.SM3Hash([]byte(fmt.Sprintf("block:%d", height-1))),
	}, nil
}
