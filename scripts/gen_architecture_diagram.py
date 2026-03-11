#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_architecture_diagram.py
生成系统整体架构图（图5-2）
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(18, 13))
ax.set_xlim(0, 18)
ax.set_ylim(0, 13)
ax.axis('off')
ax.set_facecolor('#f0f4f8')
fig.patch.set_facecolor('#f0f4f8')

# 标题
ax.text(9, 12.5, '农产品溯源系统整体架构图', fontsize=20, fontweight='bold',
        ha='center', va='center', color='#1a3a5c')

def draw_box(ax, x, y, w, h, text, bg, border, fontsize=10, bold=False, sub=None):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                          linewidth=1.8, edgecolor=border, facecolor=bg, zorder=3)
    ax.add_patch(box)
    weight = 'bold' if bold else 'normal'
    ty = y + h / 2 + (0.12 if sub else 0)
    ax.text(x + w / 2, ty, text, fontsize=fontsize, ha='center', va='center',
            color='#1a3a5c', fontweight=weight, zorder=4)
    if sub:
        ax.text(x + w / 2, y + h / 2 - 0.22, sub, fontsize=8, ha='center',
                va='center', color='#666', zorder=4)

def draw_layer_bg(ax, x, y, w, h, label, color, alpha=0.15):
    bg = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                         linewidth=2, edgecolor=color, facecolor=color, alpha=alpha, zorder=1)
    ax.add_patch(bg)
    ax.text(x + 0.2, y + h - 0.25, label, fontsize=11, color=color,
            fontweight='bold', va='top', zorder=2)

# ======= 层次背景 =======
draw_layer_bg(ax, 0.3, 10.8, 17.4, 1.5, '接入层', '#27ae60')
draw_layer_bg(ax, 0.3, 8.5, 17.4, 2.0, '应用层 (Go 1.22 · Gin · GORM)', '#2980b9')
draw_layer_bg(ax, 0.3, 5.8, 17.4, 2.4, '数据存储层', '#8e44ad')
draw_layer_bg(ax, 0.3, 2.5, 17.4, 3.0, '区块链底层 (Hyperledger Fabric v2.2 国密版)', '#c0392b')
draw_layer_bg(ax, 0.3, 0.3, 17.4, 1.9, '基础设施层 (Docker · Linux)', '#16a085')

# ======= 接入层 =======
draw_box(ax, 1.0, 11.0, 2.8, 1.0, 'Web 管理端', '#d5f5e3', '#27ae60', bold=True, sub='Vue3 + Element Plus')
draw_box(ax, 4.2, 11.0, 2.8, 1.0, '微信小程序', '#d5f5e3', '#27ae60', bold=True, sub='WXML + JS')
draw_box(ax, 7.4, 11.0, 2.8, 1.0, 'REST API', '#d5f5e3', '#27ae60', bold=True, sub='HTTP/HTTPS')
draw_box(ax, 10.6, 11.0, 2.8, 1.0, '二维码溯源', '#d5f5e3', '#27ae60', bold=True, sub='QR Code')
draw_box(ax, 13.8, 11.0, 2.8, 1.0, 'Nginx 反向代理', '#d5f5e3', '#27ae60', bold=True, sub='负载均衡')

# ======= 应用层 =======
draw_box(ax, 1.0, 8.8, 2.4, 1.4, '认证模块', '#d6eaf8', '#2980b9', sub='JWT + RBAC')
draw_box(ax, 3.7, 8.8, 2.4, 1.4, '批次管理', '#d6eaf8', '#2980b9', sub='CRUD + 状态机')
draw_box(ax, 6.4, 8.8, 2.4, 1.4, '溯源记录', '#d6eaf8', '#2980b9', sub='节点流转')
draw_box(ax, 9.1, 8.8, 2.4, 1.4, '链码调用', '#d6eaf8', '#2980b9', sub='降级Mock')
draw_box(ax, 11.8, 8.8, 2.4, 1.4, 'IPFS上传', '#d6eaf8', '#2980b9', sub='文件存证')
draw_box(ax, 14.5, 8.8, 2.4, 1.4, '区块浏览器', '#d6eaf8', '#2980b9', sub='可视化')

# ======= 数据存储层 =======
draw_box(ax, 1.2, 6.1, 3.2, 1.8, 'MySQL 8.0', '#e8daef', '#8e44ad', bold=True,
         sub='users/batches\ntrace_records')
draw_box(ax, 5.0, 6.1, 3.2, 1.8, 'Redis 7', '#e8daef', '#8e44ad', bold=True,
         sub='Session缓存\n热点数据')
draw_box(ax, 8.8, 6.1, 3.2, 1.8, 'IPFS', '#e8daef', '#8e44ad', bold=True,
         sub='图片/报告\nCID寻址')
draw_box(ax, 12.6, 6.1, 3.2, 1.8, 'LevelDB', '#e8daef', '#8e44ad', bold=True,
         sub='Fabric账本\n世界状态')

# ======= 区块链底层 =======
draw_box(ax, 0.6, 2.8, 2.6, 2.3, 'Orderer\n排序节点', '#fadbd8', '#c0392b', bold=True,
         sub='Raft共识')
draw_box(ax, 3.5, 2.8, 2.6, 2.3, 'Peer节点\nOrg1', '#fadbd8', '#c0392b', bold=True,
         sub='背书/提交')
draw_box(ax, 6.4, 2.8, 2.6, 2.3, 'Peer节点\nOrg2', '#fadbd8', '#c0392b', bold=True,
         sub='背书/提交')
draw_box(ax, 9.3, 2.8, 2.6, 2.3, '链码\nAgriTrace', '#fadbd8', '#c0392b', bold=True,
         sub='Go Chaincode')
draw_box(ax, 12.2, 2.8, 2.6, 2.3, '国密改造', '#fadbd8', '#c0392b', bold=True,
         sub='SM2/SM3/SM4')
draw_box(ax, 15.1, 2.8, 2.2, 2.3, 'CA服务\n国密证书', '#fadbd8', '#c0392b', bold=True,
         sub='SM2证书')

# ======= 基础设施层 =======
draw_box(ax, 1.0, 0.5, 3.0, 1.4, 'Docker Compose', '#d1f2eb', '#16a085', bold=True, sub='容器编排')
draw_box(ax, 4.5, 0.5, 3.0, 1.4, 'Linux Ubuntu 22.04', '#d1f2eb', '#16a085', bold=True, sub='宿主机')
draw_box(ax, 8.0, 0.5, 3.0, 1.4, 'Go 1.22 Runtime', '#d1f2eb', '#16a085', bold=True, sub='后端运行时')
draw_box(ax, 11.5, 0.5, 3.0, 1.4, 'Node.js 22 / pnpm', '#d1f2eb', '#16a085', bold=True, sub='前端构建')
draw_box(ax, 15.0, 0.5, 2.5, 1.4, 'Git / CI/CD', '#d1f2eb', '#16a085', bold=True, sub='版本管理')

# ======= 层间箭头 =======
arrow_props = dict(arrowstyle='->', color='#555', lw=1.5,
                   connectionstyle='arc3,rad=0')
for x in [2.4, 5.6, 8.8, 12.0, 15.2]:
    ax.annotate('', xy=(x, 10.8), xytext=(x, 10.0),
                arrowprops=arrow_props)
    ax.annotate('', xy=(x, 8.5), xytext=(x, 8.0),
                arrowprops=arrow_props)
    ax.annotate('', xy=(x, 5.8), xytext=(x, 5.2),
                arrowprops=arrow_props)
    ax.annotate('', xy=(x, 2.5), xytext=(x, 1.9),
                arrowprops=arrow_props)

plt.tight_layout()
output_path = '../pic/图5-2 系统整体架构图.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight',
            facecolor='#f0f4f8', edgecolor='none')
plt.close()
print(f'[OK] 架构图已保存: {output_path}')
