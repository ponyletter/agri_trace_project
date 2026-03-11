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
)

func main() {
	// 1. 加载配置
	cfg := config.Load("config/config.yaml")

	// 2. 初始化数据库
	db := utils.InitDB(&cfg.Database)

	// 3. 初始化区块链客户端（含优雅降级）
	bcClient := blockchain.NewClient(&cfg.Blockchain)

	// 4. 初始化 IPFS 客户端（含优雅降级）
	ipfsClient := ipfs.NewClient(&cfg.IPFS)

	// 5. 初始化控制器
	authCtrl := &controller.AuthController{DB: db}
	traceCtrl := &controller.TraceController{
		DB:               db,
		BlockchainClient: bcClient,
		IPFSClient:       ipfsClient,
	}

	// 6. 注册路由
	r := router.Setup(authCtrl, traceCtrl)

	// 7. 启动服务
	addr := fmt.Sprintf(":%d", cfg.Server.Port)
	log.Printf("[Server] 农产品溯源系统后端启动，监听端口 %s", addr)
	if err := r.Run(addr); err != nil {
		log.Fatalf("[Server] 启动失败: %v", err)
	}
}
