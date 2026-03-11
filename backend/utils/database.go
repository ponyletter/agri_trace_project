package utils

import (
	"agri-trace/config"
	"agri-trace/model"
	"log"

	"gorm.io/driver/mysql"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

// InitDB 初始化数据库连接
func InitDB(cfg *config.DatabaseConfig) *gorm.DB {
	db, err := gorm.Open(mysql.Open(cfg.DSN), &gorm.Config{
		Logger: logger.Default.LogMode(logger.Info),
	})
	if err != nil {
		log.Fatalf("[DB] 数据库连接失败: %v", err)
	}

	// 自动迁移表结构（不会删除已有数据）
	if err := db.AutoMigrate(
		&model.User{},
		&model.AgriBatch{},
		&model.TraceRecord{},
		&model.IPFSFile{},
	); err != nil {
		log.Printf("[DB] 表结构迁移警告: %v", err)
	}

	log.Println("[DB] 数据库连接成功")
	return db
}
