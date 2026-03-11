// Package main 农产品溯源链码
// 部署于 Hyperledger Fabric v2.2（国密版）
// Channel: agrichannel
package main

import (
	"encoding/json"
	"fmt"
	"log"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

// AgriTraceContract 溯源链码合约
type AgriTraceContract struct {
	contractapi.Contract
}

// TraceRecord 链上溯源记录结构
type TraceRecord struct {
	BatchNo       string                 `json:"batch_no"`
	NodeType      string                 `json:"node_type"`
	OperatorID    uint                   `json:"operator_id"`
	OperationTime string                 `json:"operation_time"`
	Location      string                 `json:"location"`
	EnvData       map[string]interface{} `json:"env_data"`
	TxID          string                 `json:"tx_id"`
	Timestamp     int64                  `json:"timestamp"`
}

// CreateTrace 创建溯源记录（写入账本）
func (c *AgriTraceContract) CreateTrace(ctx contractapi.TransactionContextInterface,
	batchNo, nodeType string, operatorID uint, operationTime, location, envDataJSON string) error {

	// 解析扩展数据
	var envData map[string]interface{}
	if envDataJSON != "" {
		if err := json.Unmarshal([]byte(envDataJSON), &envData); err != nil {
			return fmt.Errorf("envData 解析失败: %v", err)
		}
	}

	// 构建链上记录
	record := TraceRecord{
		BatchNo:       batchNo,
		NodeType:      nodeType,
		OperatorID:    operatorID,
		OperationTime: operationTime,
		Location:      location,
		EnvData:       envData,
		TxID:          ctx.GetStub().GetTxID(),
	}

	// 序列化并写入账本
	recordBytes, err := json.Marshal(record)
	if err != nil {
		return fmt.Errorf("序列化失败: %v", err)
	}

	// Key 格式：TRACE_{batchNo}_{nodeType}_{txID[:8]}
	key := fmt.Sprintf("TRACE_%s_%s_%s", batchNo, nodeType, ctx.GetStub().GetTxID()[:8])
	return ctx.GetStub().PutState(key, recordBytes)
}

// QueryTraceByBatch 查询指定批次的所有溯源记录
func (c *AgriTraceContract) QueryTraceByBatch(ctx contractapi.TransactionContextInterface,
	batchNo string) ([]*TraceRecord, error) {

	// 使用范围查询
	prefix := fmt.Sprintf("TRACE_%s_", batchNo)
	iterator, err := ctx.GetStub().GetStateByRange(prefix, prefix+"~")
	if err != nil {
		return nil, fmt.Errorf("查询失败: %v", err)
	}
	defer iterator.Close()

	var records []*TraceRecord
	for iterator.HasNext() {
		result, err := iterator.Next()
		if err != nil {
			return nil, err
		}
		var record TraceRecord
		if err := json.Unmarshal(result.Value, &record); err != nil {
			continue
		}
		records = append(records, &record)
	}
	return records, nil
}

// GetTraceHistory 查询指定 Key 的历史记录（防篡改验证）
func (c *AgriTraceContract) GetTraceHistory(ctx contractapi.TransactionContextInterface,
	key string) (string, error) {

	iterator, err := ctx.GetStub().GetHistoryForKey(key)
	if err != nil {
		return "", err
	}
	defer iterator.Close()

	var history []map[string]interface{}
	for iterator.HasNext() {
		modification, err := iterator.Next()
		if err != nil {
			return "", err
		}
		history = append(history, map[string]interface{}{
			"tx_id":     modification.TxId,
			"value":     string(modification.Value),
			"timestamp": modification.Timestamp.Seconds,
			"is_delete": modification.IsDelete,
		})
	}

	historyBytes, err := json.Marshal(history)
	if err != nil {
		return "", err
	}
	return string(historyBytes), nil
}

func main() {
	chaincode, err := contractapi.NewChaincode(&AgriTraceContract{})
	if err != nil {
		log.Panicf("链码初始化失败: %v", err)
	}
	if err := chaincode.Start(); err != nil {
		log.Panicf("链码启动失败: %v", err)
	}
}
