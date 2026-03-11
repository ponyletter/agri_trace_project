-- ==========================================================
-- 农产品溯源系统数据库初始化脚本
-- 遵循《GB/T 29373-2012 农产品追溯要求 果蔬》标准
-- 尽量通用，适用于各类农产品溯源场景
-- ==========================================================

CREATE DATABASE IF NOT EXISTS agri_trace DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE agri_trace;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- 1. 用户角色表 (users)
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `username` varchar(64) NOT NULL COMMENT '登录账号',
  `password_hash` varchar(255) NOT NULL COMMENT '密码哈希',
  `real_name` varchar(64) NOT NULL COMMENT '真实姓名/企业名称',
  `role` varchar(32) NOT NULL COMMENT '角色标识(admin:管理员, farmer:种植户, inspector:质检员, transporter:物流商, retailer:销售商)',
  `phone` varchar(20) DEFAULT NULL COMMENT '联系电话',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户角色表';

-- ----------------------------
-- 2. 农产品批次表 (agri_batches)
-- ----------------------------
DROP TABLE IF EXISTS `agri_batches`;
CREATE TABLE `agri_batches` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `batch_no` varchar(64) NOT NULL COMMENT '溯源批次号(全局唯一)',
  `product_name` varchar(128) NOT NULL COMMENT '产品名称',
  `product_type` varchar(64) NOT NULL COMMENT '产品类型(如: 果蔬类)',
  `quantity` decimal(10,2) NOT NULL COMMENT '产品数量',
  `unit` varchar(16) NOT NULL COMMENT '计量单位(如: kg, 箱)',
  `origin_info` varchar(255) NOT NULL COMMENT '产地基础信息',
  `farmer_id` bigint(20) NOT NULL COMMENT '关联种植户ID',
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '批次状态(0:种植中, 1:已采收, 2:已质检, 3:运输中, 4:已上架)',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_batch_no` (`batch_no`),
  KEY `idx_farmer_id` (`farmer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='农产品批次表';

-- ----------------------------
-- 3. 溯源节点流转表 (trace_records)
-- ----------------------------
DROP TABLE IF EXISTS `trace_records`;
CREATE TABLE `trace_records` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `batch_id` bigint(20) NOT NULL COMMENT '关联批次ID',
  `node_type` varchar(32) NOT NULL COMMENT '节点类型(planting:种植, harvesting:采收, inspecting:质检, packing:装箱, transporting:运输, retailing:上架)',
  `operator_id` bigint(20) NOT NULL COMMENT '操作人ID',
  `operation_time` datetime NOT NULL COMMENT '操作发生时间',
  `location` varchar(255) NOT NULL COMMENT '操作地点(如: 某果园、某质检中心)',
  `env_data` json DEFAULT NULL COMMENT '环境与业务扩展数据(如:温度、湿度、施肥记录、质检结果等)',
  `tx_hash` varchar(128) DEFAULT NULL COMMENT '区块链交易哈希(国密SM3)',
  `block_height` bigint(20) DEFAULT NULL COMMENT '区块高度',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_batch_id` (`batch_id`),
  KEY `idx_node_type` (`node_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='溯源节点流转表';

-- ----------------------------
-- 4. IPFS文件关联表 (ipfs_files)
-- ----------------------------
DROP TABLE IF EXISTS `ipfs_files`;
CREATE TABLE `ipfs_files` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `record_id` bigint(20) NOT NULL COMMENT '关联的溯源记录ID',
  `file_name` varchar(128) NOT NULL COMMENT '文件原始名称',
  `file_type` varchar(32) NOT NULL COMMENT '文件类型(image:图片, report:报告, video:视频)',
  `cid` varchar(128) NOT NULL COMMENT 'IPFS网络CID',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '上传时间',
  PRIMARY KEY (`id`),
  KEY `idx_record_id` (`record_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='IPFS文件关联表';

-- ==========================================================
-- 初始模拟数据 (INSERT)
-- 场景：2025年12月 优质红富士苹果（参考阿克苏苹果生长周期）
-- 包含：管理员、种植户、质检员、物流商、销售商
-- ==========================================================

-- 1. 插入用户数据 (密码统一为 123456 的哈希值，此处用明文模拟或简单哈希表示，实际后端需校验)
-- 实际Go后端使用 bcrypt，这里直接用假哈希替代，仅供参考。
INSERT INTO `users` (`id`, `username`, `password_hash`, `real_name`, `role`, `phone`) VALUES
(1, 'admin', '$2a$10$7/x.o4k9aZ1tV5w6x7y8.O9z0A1b2C3d4E5f6G7h8I9j0K1l2M3n4', '系统管理员', 'admin', '13800000000'),
(2, 'farmer01', '$2a$10$7/x.o4k9aZ1tV5w6x7y8.O9z0A1b2C3d4E5f6G7h8I9j0K1l2M3n4', '张三果园专业合作社', 'farmer', '13800000001'),
(3, 'inspector01', '$2a$10$7/x.o4k9aZ1tV5w6x7y8.O9z0A1b2C3d4E5f6G7h8I9j0K1l2M3n4', '农产品质量检测中心-李四', 'inspector', '13800000002'),
(4, 'transporter01', '$2a$10$7/x.o4k9aZ1tV5w6x7y8.O9z0A1b2C3d4E5f6G7h8I9j0K1l2M3n4', '冷链物流有限公司', 'transporter', '13800000003'),
(5, 'retailer01', '$2a$10$7/x.o4k9aZ1tV5w6x7y8.O9z0A1b2C3d4E5f6G7h8I9j0K1l2M3n4', '生鲜连锁超市', 'retailer', '13800000004');

-- 2. 插入农产品批次数据
-- 苹果生长周期：4月开花/坐果，10月底采收，11月运输，12月上架
INSERT INTO `agri_batches` (`id`, `batch_no`, `product_name`, `product_type`, `quantity`, `unit`, `origin_info`, `farmer_id`, `status`, `created_at`) VALUES
(1, 'BATCH-APPLE-20251025-001', '优质冰糖心苹果', '果蔬类', 5000.00, 'kg', '优质苹果种植示范基地', 2, 4, '2025-04-10 08:00:00');

-- 3. 插入溯源节点流转数据
-- 节点1: 种植 (2025-04-10)
INSERT INTO `trace_records` (`id`, `batch_id`, `node_type`, `operator_id`, `operation_time`, `location`, `env_data`, `tx_hash`, `block_height`, `created_at`) VALUES
(1, 1, 'planting', 2, '2025-04-10 10:30:00', '优质苹果种植示范基地A区', 
 '{"temperature": "15°C", "humidity": "45%", "soil_ph": "7.2", "fertilizer": "有机农家肥", "pesticide": "无"}', 
 '0x8b3a4f9e2d1c5b7a6f8e9d0c1b2a3f4e5d6c7b8a9f0e1d2c3b4a5f6e7d8c9b0a', 1001, '2025-04-10 10:35:00');

-- 节点2: 采收 (2025-10-25)
INSERT INTO `trace_records` (`id`, `batch_id`, `node_type`, `operator_id`, `operation_time`, `location`, `env_data`, `tx_hash`, `block_height`, `created_at`) VALUES
(2, 1, 'harvesting', 2, '2025-10-25 09:00:00', '优质苹果种植示范基地A区', 
 '{"weather": "晴", "method": "人工采摘", "sugar_content": "18%"}', 
 '0x1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b', 1502, '2025-10-25 09:30:00');

-- 节点3: 质检 (2025-10-28)
INSERT INTO `trace_records` (`id`, `batch_id`, `node_type`, `operator_id`, `operation_time`, `location`, `env_data`, `tx_hash`, `block_height`, `created_at`) VALUES
(3, 1, 'inspecting', 3, '2025-10-28 14:00:00', '农产品质量检测中心', 
 '{"pesticide_residue": "合格", "heavy_metal": "未检出", "appearance": "优级", "inspector": "李四"}', 
 '0x2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c', 1588, '2025-10-28 14:30:00');

-- 节点4: 装箱 (2025-10-29)
INSERT INTO `trace_records` (`id`, `batch_id`, `node_type`, `operator_id`, `operation_time`, `location`, `env_data`, `tx_hash`, `block_height`, `created_at`) VALUES
(4, 1, 'packing', 2, '2025-10-29 10:00:00', '基地包装车间', 
 '{"pack_type": "环保纸箱", "spec": "5kg/箱", "total_boxes": 1000}', 
 '0x3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d', 1605, '2025-10-29 10:15:00');

-- 节点5: 运输 (2025-11-05)
INSERT INTO `trace_records` (`id`, `batch_id`, `node_type`, `operator_id`, `operation_time`, `location`, `env_data`, `tx_hash`, `block_height`, `created_at`) VALUES
(5, 1, 'transporting', 4, '2025-11-05 08:00:00', '国道G314-高速干线', 
 '{"vehicle_no": "新A·12345", "driver": "王五", "temp_control": "0-4°C冷链"}', 
 '0x4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e', 1850, '2025-11-05 08:10:00');

-- 节点6: 上架 (2025-12-01)
INSERT INTO `trace_records` (`id`, `batch_id`, `node_type`, `operator_id`, `operation_time`, `location`, `env_data`, `tx_hash`, `block_height`, `created_at`) VALUES
(6, 1, 'retailing', 5, '2025-12-01 09:00:00', '生鲜连锁超市(中心店)', 
 '{"shelf_no": "A-01", "storage_temp": "4°C", "retail_price": "15.8元/kg"}', 
 '0x5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f', 2100, '2025-12-01 09:15:00');

-- 4. 插入IPFS文件关联数据
INSERT INTO `ipfs_files` (`id`, `record_id`, `file_name`, `file_type`, `cid`, `created_at`) VALUES
(1, 1, 'planting_site.jpg', 'image', 'QmXoypizjW3WknFiJnKLwHCnL72vedxjQkDDP1mXWo6uco', '2025-04-10 10:35:00'),
(2, 3, 'inspection_report.pdf', 'report', 'QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG', '2025-10-28 14:30:00'),
(3, 5, 'transport_vehicle.jpg', 'image', 'QmZTR5bcpQD7cFgTorxoPcqTEbpZfPz4o6Zq4N7v9E2kQW', '2025-11-05 08:10:00');

SET FOREIGN_KEY_CHECKS = 1;
