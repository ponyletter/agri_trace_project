# 农产品溯源系统 - 部署与使用指南

> **项目名称**：基于国密区块链的农产品溯源系统（以阿克苏苹果为例）
> **技术栈**：Go 1.22 + Gin + GORM + MySQL 8.0 + Redis + Hyperledger Fabric v2.2（国密版）+ IPFS + Vue3 + 微信小程序
> **论文支撑**：《基于区块链的农产品溯源关键技术研究》第五章

---

## 目录结构

```
agri_trace_project/
├── backend/                    # Go 后端项目
│   ├── main.go                 # 主程序入口
│   ├── go.mod / go.sum         # Go 模块依赖
│   ├── config/
│   │   ├── config.go           # 配置加载模块
│   │   └── config.yaml         # 配置文件（数据库/Redis/区块链/IPFS）
│   ├── controller/
│   │   ├── auth.go             # 用户认证控制器（登录/注册/获取信息）
│   │   └── trace.go            # 溯源核心控制器（批次/记录/查询）
│   ├── middleware/
│   │   ├── jwt.go              # JWT 鉴权中间件
│   │   └── cors.go             # CORS 跨域中间件
│   ├── model/
│   │   └── model.go            # GORM 数据模型定义
│   ├── pkg/
│   │   ├── blockchain/
│   │   │   └── client.go       # Fabric 链码调用（含优雅降级 Mock）
│   │   ├── ipfs/
│   │   │   └── client.go       # IPFS 文件上传（含优雅降级 Mock）
│   │   └── gmsm/
│   │       └── sm3.go          # 国密 SM3 哈希工具
│   ├── router/
│   │   └── router.go           # Gin 路由注册
│   ├── utils/
│   │   └── database.go         # 数据库初始化工具
│   └── Dockerfile              # 后端 Docker 镜像构建文件
├── frontend/                   # Vue3 前端项目
│   ├── src/
│   │   ├── main.ts             # 应用入口
│   │   ├── App.vue             # 根组件
│   │   ├── router/index.ts     # 路由配置
│   │   ├── api/
│   │   │   ├── request.ts      # Axios 请求封装（含 JWT 拦截器）
│   │   │   └── trace.ts        # API 接口定义
│   │   └── views/
│   │       ├── login/          # 登录页面
│   │       ├── DashboardView.vue # 系统概览
│   │       ├── batch/          # 批次管理页面
│   │       ├── trace/          # 溯源记录与公开查询页面
│   │       └── admin/          # 用户管理页面（管理员专用）
│   └── vite.config.ts          # Vite 构建配置
├── miniprogram/                # 微信小程序
│   ├── app.js / app.json       # 小程序全局配置
│   ├── utils/api.js            # 网络请求封装
│   └── pages/
│       ├── index/              # 溯源查询首页（扫码/手动输入）
│       └── result/             # 溯源结果展示页（时间轴）
├── db/
│   └── init.sql                # MySQL 初始化脚本（含模拟数据）
├── scripts/                    # Python 图表生成脚本
│   ├── run_all_charts.py       # 一键生成所有图表
│   ├── gen_usecase_diagram.py  # 用例图（图5-1）
│   ├── gen_architecture_diagram.py # 架构图（图5-2）
│   ├── gen_er_diagram.py       # 数据库ER图（图5-3）
│   ├── gen_trace_flow_diagram.py # 流程图（图5-4/5-5）
│   └── gen_performance_charts.py # 性能测试图（图5-8~5-11）
├── pic/                        # 生成的论文图片
├── data/                       # 性能测试 CSV 数据
├── docker-compose.yml          # Docker Compose 编排文件
├── nginx.conf                  # Nginx 反向代理配置
└── 第五章_系统实现与测试评估.md  # 第五章论文正文
```

---

## 快速启动（推荐：Docker Compose 一键部署）

### 前置条件

```bash
# 确保已安装以下工具
docker --version       # >= 24.0
docker compose version # >= 2.0
go version             # >= 1.22（本地开发时需要）
node --version         # >= 18（前端构建时需要）
python3 --version      # >= 3.9（生成图表时需要）
```

### 步骤一：构建前端静态文件

```bash
cd frontend
pnpm install
pnpm build
# 构建产物在 frontend/dist/ 目录
```

### 步骤二：修改后端配置

编辑 `backend/config/config.yaml`，根据实际环境修改以下配置：

```yaml
database:
  dsn: "root:你的密码@tcp(mysql:3306)/agri_trace?charset=utf8mb4&parseTime=True&loc=Local"

blockchain:
  mock_mode: true  # 无 Fabric 网络时设为 true，系统自动降级
  # mock_mode: false  # 连接真实 Fabric 网络时设为 false

ipfs:
  mock_mode: true  # 无 IPFS 节点时设为 true
```

### 步骤三：启动所有服务

```bash
# 在项目根目录执行
# 基础模式（不启动 IPFS，适合快速体验）
docker compose up -d

# 完整模式（含 IPFS 节点）
docker compose --profile full up -d

# 查看服务状态
docker compose ps

# 查看后端日志
docker compose logs -f backend
```

### 步骤四：访问系统

| 服务 | 地址 | 说明 |
| :--- | :--- | :--- |
| Web 管理端 | http://localhost:80 | Vue3 前端界面 |
| 后端 API | http://localhost:8080 | Go 后端服务 |
| 健康检查 | http://localhost:8080/health | 服务状态检查 |
| 溯源查询（示例） | http://localhost/trace/BATCH-APPLE-20251025-001 | 无需登录 |

**默认账号**（密码均为 `123456`，需先运行 init.sql）：

| 账号 | 角色 | 说明 |
| :--- | :--- | :--- |
| admin | 管理员 | 全部权限 |
| farmer01 | 种植户 | 创建批次、录入种植/采收信息 |
| inspector01 | 质检员 | 录入质检结果 |
| transporter01 | 物流商 | 录入运输信息 |
| retailer01 | 销售商 | 录入上架信息 |

> **注意**：init.sql 中的密码哈希为占位符，首次使用请通过管理员账号的注册接口重置密码，或直接修改 SQL 中的 `password_hash` 字段为 bcrypt 哈希值。

---

## 本地开发模式（无 Docker）

### 启动后端

```bash
# 1. 确保 MySQL 和 Redis 已启动
# 2. 导入数据库
mysql -u root -p agri_trace < db/init.sql

# 3. 启动后端
cd backend
export PATH=$PATH:/usr/local/go/bin
go run main.go
# 后端监听 :8080
```

### 启动前端

```bash
cd frontend
pnpm install
pnpm dev
# 前端监听 :9528，API 请求自动代理至 :8080
```

---

## 连接真实 Fabric 网络

当 `config.yaml` 中 `blockchain.mock_mode` 设为 `false` 时，系统将尝试连接真实 Fabric 网络。

### 使用 fabric-gm（国密版）

本项目参考 [fabric-gm](https://github.com/ponyletter/fabric-gm) 进行国密改造。启动步骤如下：

```bash
# 1. 克隆国密 Fabric 项目
git clone https://github.com/ponyletter/fabric-gm.git
cd fabric-gm

# 2. 启动测试网络（需要 Docker）
cd test-network
./network.sh up createChannel -c agrichannel -ca

# 3. 部署链码（链码路径需根据实际调整）
./network.sh deployCC -ccn agritrace -ccp ../chaincode/agritrace -ccl go

# 4. 将 Fabric 连接配置文件复制到后端
cp organizations/peerOrganizations/org1.example.com/connection-org1.yaml \
   ../agri_trace_project/backend/config/fabric/config.yaml

# 5. 修改 backend/config/config.yaml
#    blockchain.mock_mode: false
#    blockchain.config_path: ./config/fabric/config.yaml
```

---

## 生成论文图表

```bash
# 安装 Python 依赖
pip3 install matplotlib numpy

# 一键生成所有图表
cd scripts
python3 run_all_charts.py

# 图片保存在 ../pic/ 目录
# CSV 数据保存在 ../data/ 目录
```

---

## API 接口文档

### 认证接口

| 方法 | 路径 | 说明 | 鉴权 |
| :--- | :--- | :--- | :--- |
| POST | `/api/v1/auth/login` | 用户登录，返回 JWT Token | 否 |
| GET | `/api/v1/auth/profile` | 获取当前用户信息 | 是 |
| POST | `/api/v1/auth/register` | 注册新用户（仅管理员） | 是（admin） |

### 批次管理接口

| 方法 | 路径 | 说明 | 鉴权 |
| :--- | :--- | :--- | :--- |
| POST | `/api/v1/batches` | 创建农产品批次 | 是（farmer/admin） |
| GET | `/api/v1/batches` | 获取批次列表 | 是 |

### 溯源接口

| 方法 | 路径 | 说明 | 鉴权 |
| :--- | :--- | :--- | :--- |
| POST | `/api/v1/trace/records` | 添加溯源节点记录（触发上链） | 是 |
| GET | `/api/v1/trace/records` | 获取溯源记录列表 | 是 |
| GET | `/api/v1/trace/:trace_code` | 根据溯源码查询完整溯源链 | **否**（供小程序使用） |
| GET | `/api/v1/block/info?height=N` | 查询区块信息 | 否 |

### 请求示例（添加溯源记录）

```bash
curl -X POST http://localhost:8080/api/v1/trace/records \
  -H "Authorization: Bearer <your_jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "batch_id": 1,
    "node_type": "harvesting",
    "operation_time": "2025-10-25 09:00:00",
    "location": "优质苹果种植示范基地A区",
    "env_data": {
      "weather": "晴",
      "method": "人工采摘",
      "sugar_content": "18%"
    }
  }'
```

---

## 微信小程序配置

1. 使用微信开发者工具打开 `miniprogram/` 目录
2. 修改 `app.js` 中的 `globalData.baseUrl` 为后端实际域名（需已备案 HTTPS）
3. 在微信公众平台配置合法域名
4. 编译并上传审核

---

## 常见问题

**Q: 启动后端报 "数据库连接失败"？**
A: 检查 MySQL 是否已启动，且 `config.yaml` 中的 DSN 配置正确。

**Q: 上链操作返回 "Fabric 网络未连接"？**
A: 将 `config.yaml` 中 `blockchain.mock_mode` 设为 `true`，系统将使用模拟数据，不影响业务功能演示。

**Q: 如何生成真实的 bcrypt 密码哈希？**
A: 使用以下 Go 代码生成：
```go
import "golang.org/x/crypto/bcrypt"
hash, _ := bcrypt.GenerateFromPassword([]byte("123456"), bcrypt.DefaultCost)
fmt.Println(string(hash))
```

---

## 技术参考

- [Hyperledger Fabric v2.2 官方文档](https://hyperledger-fabric.readthedocs.io/en/release-2.2/)
- [fabric-gm 国密改造版](https://github.com/ponyletter/fabric-gm)
- [tjfoc/gmsm 国密算法库](https://github.com/tjfoc/gmsm)
- [GB/T 29373-2012 农产品追溯要求 果蔬](https://std.samr.gov.cn/)
- [fabric-eCert-trace-ipfs_ok 参考项目](https://github.com/ponyletter/fabric-eCert-trace-ipfs_ok)
