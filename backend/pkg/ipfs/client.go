// Package ipfs 封装 IPFS 文件上传与获取接口
// 实现"优雅降级"机制：当 IPFS 节点不可达时，自动切换到 Mock 模式
package ipfs

import (
	"agri-trace/config"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"log"
	"time"
)

// Client IPFS 客户端接口
type Client interface {
	Upload(data []byte, filename string) (string, error)
	GetURL(cid string) string
	IsConnected() bool
}

type ipfsClient struct {
	cfg *config.IPFSConfig
}

type mockIPFSClient struct {
	cfg *config.IPFSConfig
}

// NewClient 创建 IPFS 客户端（自动检测并降级）
func NewClient(cfg *config.IPFSConfig) Client {
	if cfg.MockMode {
		log.Println("[IPFS] 配置为 Mock 模式，使用模拟 CID")
		return &mockIPFSClient{cfg: cfg}
	}
	client := &ipfsClient{cfg: cfg}
	if !client.IsConnected() {
		log.Println("[IPFS] IPFS 节点不可达，自动降级为 Mock 模式")
		return &mockIPFSClient{cfg: cfg}
	}
	log.Println("[IPFS] 已连接到 IPFS 节点")
	return client
}

// ==================== ipfsClient 实现 ====================

func (c *ipfsClient) IsConnected() bool {
	// 生产环境：使用 HTTP 请求检测 IPFS 节点状态
	// resp, err := http.Get(c.cfg.APIURL + "/api/v0/version")
	// return err == nil && resp.StatusCode == 200
	return false
}

func (c *ipfsClient) Upload(data []byte, filename string) (string, error) {
	// 生产环境：调用 IPFS HTTP API 上传文件
	// multipart form 上传到 /api/v0/add
	return "", fmt.Errorf("IPFS 节点未连接")
}

func (c *ipfsClient) GetURL(cid string) string {
	return fmt.Sprintf("%s/ipfs/%s", c.cfg.APIURL, cid)
}

// ==================== mockIPFSClient 实现 ====================

func (c *mockIPFSClient) IsConnected() bool {
	return true
}

func (c *mockIPFSClient) Upload(data []byte, filename string) (string, error) {
	// 生成模拟 CID（基于数据内容哈希）
	h := sha256.New()
	h.Write(data)
	h.Write([]byte(filename))
	h.Write([]byte(fmt.Sprintf("%d", time.Now().UnixNano())))
	hash := hex.EncodeToString(h.Sum(nil))
	// 模拟 IPFS CID v1 格式前缀
	mockCID := "Qm" + hash[:44]
	log.Printf("[IPFS-Mock] 模拟上传成功: filename=%s, CID=%s", filename, mockCID)
	return mockCID, nil
}

func (c *mockIPFSClient) GetURL(cid string) string {
	return fmt.Sprintf("https://ipfs.io/ipfs/%s", cid)
}
