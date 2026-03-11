// Package router 注册 Gin 路由
package router

import (
	"agri-trace/controller"
	"agri-trace/middleware"

	"github.com/gin-gonic/gin"
)

// Setup 注册所有路由
func Setup(
	authCtrl *controller.AuthController,
	traceCtrl *controller.TraceController,
) *gin.Engine {
	r := gin.Default()

	// 全局中间件
	r.Use(middleware.CORS())

	// 健康检查
	r.GET("/health", func(c *gin.Context) {
		c.JSON(200, gin.H{"status": "ok", "service": "agri-trace-backend"})
	})

	// API v1 路由组
	v1 := r.Group("/api/v1")
	{
		// ---- 认证接口（无需鉴权）----
		auth := v1.Group("/auth")
		{
			auth.POST("/login", authCtrl.Login)
		}

		// ---- 溯源公开查询接口（无需鉴权，供微信小程序使用）----
		v1.GET("/trace/:trace_code", traceCtrl.QueryByTraceCode)
		v1.GET("/block/info", traceCtrl.GetBlockInfo)

		// ---- 需要鉴权的接口 ----
		authorized := v1.Group("/")
		authorized.Use(middleware.JWTAuth())
		{
			// 用户信息
			authorized.GET("/auth/profile", authCtrl.GetProfile)
			// 仅管理员可注册新用户
			authorized.POST("/auth/register", middleware.RoleRequired("admin"), authCtrl.Register)

			// 批次管理
			authorized.POST("/batches", middleware.RoleRequired("farmer", "admin"), traceCtrl.CreateBatch)
			authorized.GET("/batches", traceCtrl.ListBatches)

			// 溯源记录管理
			authorized.POST("/trace/records", middleware.RoleRequired("farmer", "inspector", "transporter", "retailer", "admin"), traceCtrl.AddTraceRecord)
			authorized.GET("/trace/records", traceCtrl.ListTraceRecords)
		}
	}

	return r
}
