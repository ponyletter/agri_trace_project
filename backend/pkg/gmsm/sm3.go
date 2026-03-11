// Package gmsm 提供国密SM3哈希算法的轻量级实现封装
// 在无法引入完整 tjfoc/gmsm 依赖时，提供基于 SHA256 的模拟实现
// 生产环境请替换为 github.com/tjfoc/gmsm/sm3
package gmsm

import (
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"math/rand"
	"time"
)

// SM3Hash 计算数据的国密SM3哈希值
// 注意：此处为模拟实现，生产环境请使用 github.com/tjfoc/gmsm/sm3
func SM3Hash(data []byte) string {
	// 模拟SM3：在SHA256基础上加入国密前缀标识
	h := sha256.New()
	h.Write([]byte("SM3:"))
	h.Write(data)
	return "0x" + hex.EncodeToString(h.Sum(nil))
}

// GenerateMockTxHash 生成模拟的国密区块链交易哈希
// 用于 Mock 模式下的降级处理
func GenerateMockTxHash(batchNo, nodeType string) string {
	seed := fmt.Sprintf("%s:%s:%d", batchNo, nodeType, time.Now().UnixNano())
	return SM3Hash([]byte(seed))
}

// GenerateMockBlockHeight 生成模拟的区块高度
func GenerateMockBlockHeight(base int64) int64 {
	r := rand.New(rand.NewSource(time.Now().UnixNano()))
	return base + r.Int63n(100)
}
