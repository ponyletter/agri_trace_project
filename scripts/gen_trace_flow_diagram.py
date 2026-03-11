#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_trace_flow_diagram.py
生成溯源业务流程图（图5-4）和国密上链时序图（图5-5）
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patches as mpatches

plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# ============================================================
# 图5-4: 溯源业务流程图（苹果全生命周期）
# ============================================================
fig, ax = plt.subplots(figsize=(18, 10))
ax.set_xlim(0, 18)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_facecolor('#f8f9fa')
fig.patch.set_facecolor('#f8f9fa')

ax.text(9, 9.6, '阿克苏苹果溯源全生命周期业务流程图', fontsize=17, fontweight='bold',
        ha='center', va='center', color='#1a3a5c')

# 定义节点
nodes = [
    {'label': '🌱 种植\n(4月)', 'x': 1.5, 'y': 7.0, 'color': '#27ae60', 'actor': '种植户'},
    {'label': '🍎 采收\n(10月)', 'x': 4.0, 'y': 7.0, 'color': '#f39c12', 'actor': '种植户'},
    {'label': '🔬 质检\n(10月底)', 'x': 6.5, 'y': 7.0, 'color': '#2980b9', 'actor': '质检员'},
    {'label': '📦 装箱\n(10月底)', 'x': 9.0, 'y': 7.0, 'color': '#8e44ad', 'actor': '种植户'},
    {'label': '🚛 运输\n(11月)', 'x': 11.5, 'y': 7.0, 'color': '#16a085', 'actor': '物流商'},
    {'label': '🏪 上架\n(12月)', 'x': 14.0, 'y': 7.0, 'color': '#e74c3c', 'actor': '销售商'},
    {'label': '📱 消费者\n溯源查询', 'x': 16.5, 'y': 7.0, 'color': '#c0392b', 'actor': '消费者'},
]

# 绘制节点
for node in nodes:
    circle = plt.Circle((node['x'], node['y']), 0.75,
                          color=node['color'], zorder=4, alpha=0.9)
    ax.add_patch(circle)
    ax.text(node['x'], node['y'], node['label'], fontsize=8.5, ha='center', va='center',
            color='white', fontweight='bold', zorder=5)
    ax.text(node['x'], node['y'] - 1.1, node['actor'], fontsize=9, ha='center',
            color=node['color'], fontweight='bold')

# 节点间连接箭头
for i in range(len(nodes) - 1):
    x1, x2 = nodes[i]['x'] + 0.75, nodes[i + 1]['x'] - 0.75
    ax.annotate('', xy=(x2, 7.0), xytext=(x1, 7.0),
                arrowprops=dict(arrowstyle='->', color='#555', lw=2.0))

# 区块链上链说明（下方）
chain_y = 4.5
ax.text(9, 5.3, '区块链上链流程（每个节点操作均触发）', fontsize=12, ha='center',
        color='#1a3a5c', fontweight='bold')

chain_steps = [
    {'text': '① 业务数据\n采集', 'x': 2.0, 'color': '#ecf0f1'},
    {'text': '② SM3哈希\n计算', 'x': 5.0, 'color': '#d5f5e3'},
    {'text': '③ SM2签名\n背书', 'x': 8.0, 'color': '#d6eaf8'},
    {'text': '④ Fabric\n共识排序', 'x': 11.0, 'color': '#fdebd0'},
    {'text': '⑤ 区块\n写入账本', 'x': 14.0, 'color': '#fadbd8'},
    {'text': '⑥ TxHash\n返回存储', 'x': 17.0, 'color': '#e8daef'},
]

for step in chain_steps:
    box = FancyBboxPatch((step['x'] - 1.2, chain_y - 0.5), 2.4, 1.0,
                          boxstyle="round,pad=0.08",
                          facecolor=step['color'], edgecolor='#aaa', lw=1.2, zorder=3)
    ax.add_patch(box)
    ax.text(step['x'], chain_y, step['text'], fontsize=9, ha='center', va='center',
            color='#333', zorder=4)

for i in range(len(chain_steps) - 1):
    x1 = chain_steps[i]['x'] + 1.2
    x2 = chain_steps[i + 1]['x'] - 1.2
    ax.annotate('', xy=(x2, chain_y), xytext=(x1, chain_y),
                arrowprops=dict(arrowstyle='->', color='#c0392b', lw=1.5))

# IPFS 说明
ax.text(9, 2.8, 'IPFS 文件存储流程（质检报告、现场图片等）', fontsize=12, ha='center',
        color='#1a3a5c', fontweight='bold')
ipfs_steps = [
    {'text': '文件上传\n至IPFS节点', 'x': 3.5},
    {'text': '获取\nCID', 'x': 7.0},
    {'text': 'CID存入\nMySQL', 'x': 10.5},
    {'text': 'CID上链\n存证', 'x': 14.0},
]
for step in ipfs_steps:
    box = FancyBboxPatch((step['x'] - 1.5, 1.6), 3.0, 0.9,
                          boxstyle="round,pad=0.08",
                          facecolor='#fef9e7', edgecolor='#f39c12', lw=1.2, zorder=3)
    ax.add_patch(box)
    ax.text(step['x'], 2.05, step['text'], fontsize=9, ha='center', va='center',
            color='#333', zorder=4)

for i in range(len(ipfs_steps) - 1):
    x1 = ipfs_steps[i]['x'] + 1.5
    x2 = ipfs_steps[i + 1]['x'] - 1.5
    ax.annotate('', xy=(x2, 2.05), xytext=(x1, 2.05),
                arrowprops=dict(arrowstyle='->', color='#f39c12', lw=1.5))

# 垂直连接线（业务节点 → 区块链）
for node in nodes[:6]:
    ax.annotate('', xy=(node['x'], chain_y + 0.5), xytext=(node['x'], node['y'] - 0.75),
                arrowprops=dict(arrowstyle='->', color='#bbb', lw=1.0,
                                linestyle='dashed'))

plt.tight_layout()
plt.savefig('../pic/图5-4 溯源业务流程图.png', dpi=150, bbox_inches='tight',
            facecolor='#f8f9fa', edgecolor='none')
plt.close()
print('[OK] 图5-4 溯源业务流程图已生成')

# ============================================================
# 图5-5: 国密上链时序图（简化版）
# ============================================================
fig, ax = plt.subplots(figsize=(16, 10))
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_facecolor('#fafbfc')
fig.patch.set_facecolor('#fafbfc')

ax.text(8, 9.6, '溯源数据国密上链时序图', fontsize=17, fontweight='bold',
        ha='center', va='center', color='#1a3a5c')

# 参与者
participants = [
    {'name': '用户/小程序', 'x': 1.5, 'color': '#27ae60'},
    {'name': 'Go后端\n(Gin)', 'x': 4.5, 'color': '#2980b9'},
    {'name': 'Fabric SDK\n(国密版)', 'x': 7.5, 'color': '#8e44ad'},
    {'name': 'Peer节点\n(Org1)', 'x': 10.5, 'color': '#e67e22'},
    {'name': 'Orderer\n排序节点', 'x': 13.5, 'color': '#c0392b'},
]

# 生命线
for p in participants:
    box = FancyBboxPatch((p['x'] - 0.9, 8.8), 1.8, 0.7,
                          boxstyle="round,pad=0.05",
                          facecolor=p['color'], edgecolor='#333', lw=1.5, zorder=3)
    ax.add_patch(box)
    ax.text(p['x'], 9.15, p['name'], fontsize=9, ha='center', va='center',
            color='white', fontweight='bold', zorder=4)
    ax.plot([p['x'], p['x']], [0.5, 8.8], color='#aaa', lw=1.0, linestyle='--', zorder=1)

# 消息序列
messages = [
    (1.5, 4.5, 8.2, '① POST /api/v1/trace/records', '#333'),
    (4.5, 7.5, 7.6, '② 构建 TracePayload', '#2980b9'),
    (7.5, 10.5, 7.0, '③ SM2签名 + 提案背书请求', '#8e44ad'),
    (10.5, 7.5, 6.4, '④ 背书响应 (SM2签名)', '#e67e22'),
    (7.5, 10.5, 5.8, '⑤ 广播交易至 Orderer', '#8e44ad'),
    (10.5, 13.5, 5.2, '⑥ Raft共识排序', '#e67e22'),
    (13.5, 10.5, 4.6, '⑦ 区块分发', '#c0392b'),
    (10.5, 7.5, 4.0, '⑧ 账本提交 + SM3哈希', '#e67e22'),
    (7.5, 4.5, 3.4, '⑨ TxHash 返回', '#8e44ad'),
    (4.5, 4.5, 2.8, '⑩ 写入MySQL (tx_hash)', '#2980b9'),
    (4.5, 1.5, 2.2, '⑪ 返回成功响应', '#2980b9'),
]

for x1, x2, y, label, color in messages:
    direction = 1 if x2 > x1 else -1
    ax.annotate('', xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.8))
    mx = (x1 + x2) / 2
    offset = 0.15
    ax.text(mx, y + offset, label, fontsize=8.5, ha='center', va='bottom', color=color)

# 激活框
for p_x, y_start, y_end in [(4.5, 2.2, 8.2), (7.5, 3.4, 7.6), (10.5, 4.0, 7.0)]:
    box = FancyBboxPatch((p_x - 0.15, y_start), 0.3, y_end - y_start,
                          boxstyle="square,pad=0",
                          facecolor='#d6eaf8', edgecolor='#2980b9', lw=1.0, zorder=2)
    ax.add_patch(box)

plt.tight_layout()
plt.savefig('../pic/图5-5 国密上链时序图.png', dpi=150, bbox_inches='tight',
            facecolor='#fafbfc', edgecolor='none')
plt.close()
print('[OK] 图5-5 国密上链时序图已生成')
