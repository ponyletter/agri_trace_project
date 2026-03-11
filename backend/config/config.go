package config

import (
	"log"
	"sync"

	"github.com/spf13/viper"
)

// Config 全局配置结构体
type Config struct {
	Server     ServerConfig     `mapstructure:"server"`
	Database   DatabaseConfig   `mapstructure:"database"`
	Redis      RedisConfig      `mapstructure:"redis"`
	JWT        JWTConfig        `mapstructure:"jwt"`
	Blockchain BlockchainConfig `mapstructure:"blockchain"`
	IPFS       IPFSConfig       `mapstructure:"ipfs"`
}

type ServerConfig struct {
	Port int    `mapstructure:"port"`
	Mode string `mapstructure:"mode"`
}

type DatabaseConfig struct {
	DSN string `mapstructure:"dsn"`
}

type RedisConfig struct {
	Addr     string `mapstructure:"addr"`
	Password string `mapstructure:"password"`
	DB       int    `mapstructure:"db"`
}

type JWTConfig struct {
	Secret      string `mapstructure:"secret"`
	ExpireHours int    `mapstructure:"expire_hours"`
}

type BlockchainConfig struct {
	MockMode      bool   `mapstructure:"mock_mode"`
	ConfigPath    string `mapstructure:"config_path"`
	ChannelName   string `mapstructure:"channel_name"`
	ChaincodeName string `mapstructure:"chaincode_name"`
	OrgName       string `mapstructure:"org_name"`
	UserName      string `mapstructure:"user_name"`
}

type IPFSConfig struct {
	MockMode bool   `mapstructure:"mock_mode"`
	APIURL   string `mapstructure:"api_url"`
}

var (
	globalConfig *Config
	once         sync.Once
)

// Load 加载配置文件
func Load(path string) *Config {
	once.Do(func() {
		viper.SetConfigFile(path)
		viper.SetConfigType("yaml")
		if err := viper.ReadInConfig(); err != nil {
			log.Fatalf("[Config] 读取配置文件失败: %v", err)
		}
		globalConfig = &Config{}
		if err := viper.Unmarshal(globalConfig); err != nil {
			log.Fatalf("[Config] 解析配置文件失败: %v", err)
		}
		log.Printf("[Config] 配置加载成功, 区块链Mock模式: %v", globalConfig.Blockchain.MockMode)
	})
	return globalConfig
}

// Get 获取全局配置
func Get() *Config {
	if globalConfig == nil {
		log.Fatal("[Config] 配置未初始化，请先调用 Load()")
	}
	return globalConfig
}
