package model

import (
	"database/sql/driver"
	"encoding/json"
	"fmt"
	"time"
)

// JSONMap 自定义JSON类型，用于存储env_data等动态字段
type JSONMap map[string]interface{}

func (j JSONMap) Value() (driver.Value, error) {
	if j == nil {
		return nil, nil
	}
	b, err := json.Marshal(j)
	return string(b), err
}

func (j *JSONMap) Scan(value interface{}) error {
	if value == nil {
		*j = nil
		return nil
	}
	var bytes []byte
	switch v := value.(type) {
	case []byte:
		bytes = v
	case string:
		bytes = []byte(v)
	default:
		return fmt.Errorf("JSONMap: 不支持的类型 %T", value)
	}
	return json.Unmarshal(bytes, j)
}

// User 用户角色表
type User struct {
	ID           uint      `gorm:"primaryKey;autoIncrement" json:"id"`
	Username     string    `gorm:"uniqueIndex;size:64;not null" json:"username"`
	PasswordHash string    `gorm:"size:255;not null" json:"-"`
	RealName     string    `gorm:"size:64;not null" json:"real_name"`
	Role         string    `gorm:"size:32;not null" json:"role"`
	Phone        string    `gorm:"size:20" json:"phone"`
	CreatedAt    time.Time `json:"created_at"`
	UpdatedAt    time.Time `json:"updated_at"`
}

func (User) TableName() string { return "users" }

// AgriBatch 农产品批次表
type AgriBatch struct {
	ID          uint      `gorm:"primaryKey;autoIncrement" json:"id"`
	BatchNo     string    `gorm:"uniqueIndex;size:64;not null" json:"batch_no"`
	ProductName string    `gorm:"size:128;not null" json:"product_name"`
	ProductType string    `gorm:"size:64;not null" json:"product_type"`
	Quantity    float64   `gorm:"type:decimal(10,2);not null" json:"quantity"`
	Unit        string    `gorm:"size:16;not null" json:"unit"`
	OriginInfo  string    `gorm:"size:255;not null" json:"origin_info"`
	FarmerID    uint      `gorm:"not null;index" json:"farmer_id"`
	Status      int8      `gorm:"default:0;not null" json:"status"`
	CreatedAt   time.Time `json:"created_at"`
	UpdatedAt   time.Time `json:"updated_at"`
}

func (AgriBatch) TableName() string { return "agri_batches" }

// TraceRecord 溯源节点流转表
type TraceRecord struct {
	ID            uint      `gorm:"primaryKey;autoIncrement" json:"id"`
	BatchID       uint      `gorm:"not null;index" json:"batch_id"`
	NodeType      string    `gorm:"size:32;not null;index" json:"node_type"`
	OperatorID    uint      `gorm:"not null" json:"operator_id"`
	OperationTime time.Time `gorm:"not null" json:"operation_time"`
	Location      string    `gorm:"size:255;not null" json:"location"`
	EnvData       JSONMap   `gorm:"type:json" json:"env_data"`
	TxHash        string    `gorm:"size:128" json:"tx_hash"`
	BlockHeight   int64     `json:"block_height"`
	CreatedAt     time.Time `json:"created_at"`
}

func (TraceRecord) TableName() string { return "trace_records" }

// IPFSFile IPFS文件关联表
type IPFSFile struct {
	ID        uint      `gorm:"primaryKey;autoIncrement" json:"id"`
	RecordID  uint      `gorm:"not null;index" json:"record_id"`
	FileName  string    `gorm:"size:128;not null" json:"file_name"`
	FileType  string    `gorm:"size:32;not null" json:"file_type"`
	CID       string    `gorm:"size:128;not null" json:"cid"`
	CreatedAt time.Time `json:"created_at"`
}

func (IPFSFile) TableName() string { return "ipfs_files" }
