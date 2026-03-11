package main

import (
	"agri-trace/config"
	"agri-trace/controller"
	"agri-trace/pkg/blockchain"
	"agri-trace/pkg/ipfs"
	"agri-trace/router"
	"agri-trace/utils"
	"fmt"
	"log"
	"strings"

	"github.com/gin-gonic/gin"
)

func main() {
	// 1. 加载配置
	cfg := config.Load("config/config.yaml")

	// 2. 在代码内部设置 Gin 运行模式
	//    直接读取 config.yaml 中的 server.mode 字段，
	//    彻底规避 Windows 下 set GIN_MODE=release && 命令
	//    因空格导致的 "panic: gin mode unknown: release " 问题。
	mode := strings.TrimSpace(cfg.Server.Mode)
	switch mode {
	case gin.ReleaseMode, gin.TestMode:
		gin.SetMode(mode)
	default:
		gin.SetMode(gin.DebugMode)
	}

	// 3. 初始化数据库
	db := utils.InitDB(&cfg.Database)

	// 4. 初始化区块链客户端（含优雅降级）
	bcClient := blockchain.NewClient(&cfg.Blockchain)

	// 5. 初始化 IPFS 客户端（含优雅降级）
	ipfsClient := ipfs.NewClient(&cfg.IPFS)

	// 6. 初始化控制器
	authCtrl := &controller.AuthController{DB: db}
	traceCtrl := &controller.TraceController{
		DB:               db,
		BlockchainClient: bcClient,
		IPFSClient:       ipfsClient,
	}

	// 7. 注册路由
	r := router.Setup(authCtrl, traceCtrl)

	// 8. 启动服务
	addr := fmt.Sprintf(":%d", cfg.Server.Port)
	log.Printf("[Server] 农产品溯源系统后端启动，监听端口 %s，运行模式: %s", addr, gin.Mode())
	if err := r.Run(addr); err != nil {
		log.Fatalf("[Server] 启动失败: %v", err)
	}
}
