#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_usecase_diagram.py
生成溯源系统用例图（图5-1）
直接运行即可在 ../pic/ 目录生成 PNG 图片
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Ellipse
import matplotlib.patheffects as pe
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(1, 1, figsize=(16, 12))
ax.set_xlim(0, 16)
ax.set_ylim(0, 12)
ax.axis('off')
ax.set_facecolor('#f8f9fa')
fig.patch.set_facecolor('#f8f9fa')

# ---- 标题 ----
ax.text(8, 11.5, '农产品溯源系统 用例图', fontsize=18, fontweight='bold',
        ha='center', va='center', color='#1a3a5c')

# ---- 系统边界框 ----
system_box = FancyBboxPatch((2.5, 1.0), 11, 9.8,
                             boxstyle="round,pad=0.1",
                             linewidth=2, edgecolor='#2c7be5',
                             facecolor='#eaf3fb', alpha=0.5)
ax.add_patch(system_box)
ax.text(8, 10.6, '农产品溯源系统', fontsize=13, ha='center', va='center',
        color='#2c7be5', fontweight='bold')

# ---- 角色定义（Actor）----
actors = [
    {'name': '种植户', 'x': 0.8, 'y': 8.5, 'color': '#27ae60'},
    {'name': '质检员', 'x': 0.8, 'y': 6.0, 'color': '#2980b9'},
    {'name': '物流商', 'x': 0.8, 'y': 3.5, 'color': '#8e44ad'},
    {'name': '销售商', 'x': 0.8, 'y': 1.5, 'color': '#e67e22'},
    {'name': '消费者', 'x': 15.2, 'y': 6.5, 'color': '#c0392b'},
    {'name': '管理员', 'x': 15.2, 'y': 3.5, 'color': '#16a085'},
]

def draw_actor(ax, x, y, name, color):
    """绘制 UML 小人"""
    # 头
    head = plt.Circle((x, y + 0.55), 0.22, color=color, zorder=5)
    ax.add_patch(head)
    # 身体
    ax.plot([x, x], [y + 0.33, y - 0.15], color=color, lw=2, zorder=5)
    # 手臂
    ax.plot([x - 0.3, x + 0.3], [y + 0.1, y + 0.1], color=color, lw=2, zorder=5)
    # 腿
    ax.plot([x, x - 0.25], [y - 0.15, y - 0.55], color=color, lw=2, zorder=5)
    ax.plot([x, x + 0.25], [y - 0.15, y - 0.55], color=color, lw=2, zorder=5)
    # 名称
    ax.text(x, y - 0.75, name, fontsize=10, ha='center', va='center',
            color=color, fontweight='bold')

for actor in actors:
    draw_actor(ax, actor['x'], actor['y'], actor['name'], actor['color'])

# ---- 用例椭圆 ----
use_cases = [
    # 种植户相关
    {'text': '录入种植信息', 'x': 5.0, 'y': 9.2, 'w': 2.2, 'h': 0.5},
    {'text': '记录采收信息', 'x': 5.0, 'y': 8.2, 'w': 2.2, 'h': 0.5},
    {'text': '创建产品批次', 'x': 5.0, 'y': 7.2, 'w': 2.2, 'h': 0.5},
    # 质检员相关
    {'text': '上传质检报告', 'x': 8.0, 'y': 6.8, 'w': 2.2, 'h': 0.5},
    {'text': '录入质检结果', 'x': 8.0, 'y': 5.8, 'w': 2.2, 'h': 0.5},
    # 物流商相关
    {'text': '记录运输信息', 'x': 5.0, 'y': 4.5, 'w': 2.2, 'h': 0.5},
    {'text': '更新物流状态', 'x': 5.0, 'y': 3.5, 'w': 2.2, 'h': 0.5},
    # 销售商相关
    {'text': '上架产品信息', 'x': 5.0, 'y': 2.3, 'w': 2.2, 'h': 0.5},
    # 消费者相关
    {'text': '扫码溯源查询', 'x': 11.0, 'y': 7.5, 'w': 2.2, 'h': 0.5},
    {'text': '查看溯源时间轴', 'x': 11.0, 'y': 6.5, 'w': 2.4, 'h': 0.5},
    {'text': '验证区块链哈希', 'x': 11.0, 'y': 5.5, 'w': 2.4, 'h': 0.5},
    # 管理员相关
    {'text': '用户权限管理', 'x': 11.0, 'y': 4.0, 'w': 2.2, 'h': 0.5},
    {'text': '系统数据监控', 'x': 11.0, 'y': 3.0, 'w': 2.2, 'h': 0.5},
    {'text': '区块链浏览器', 'x': 11.0, 'y': 2.0, 'w': 2.2, 'h': 0.5},
    # 共用
    {'text': '国密SM3上链存证', 'x': 8.0, 'y': 4.0, 'w': 2.6, 'h': 0.5},
    {'text': 'IPFS文件存储', 'x': 8.0, 'y': 2.8, 'w': 2.2, 'h': 0.5},
]

uc_colors = {
    '录入': '#d5f5e3', '记录': '#d5f5e3', '创建': '#d5f5e3',
    '上传': '#d6eaf8', '录入质': '#d6eaf8',
    '更新': '#e8daef', '上架': '#fdebd0',
    '扫码': '#fadbd8', '查看': '#fadbd8', '验证': '#fadbd8',
    '用户': '#d1f2eb', '系统': '#d1f2eb', '区块链浏': '#d1f2eb',
    '国密': '#fef9e7', 'IPFS': '#fef9e7',
}

def get_uc_color(text):
    for k, v in uc_colors.items():
        if text.startswith(k):
            return v
    return '#fff9c4'

for uc in use_cases:
    ellipse = Ellipse((uc['x'], uc['y']), uc['w'], uc['h'],
                      facecolor=get_uc_color(uc['text']),
                      edgecolor='#555', linewidth=1.2, zorder=4)
    ax.add_patch(ellipse)
    ax.text(uc['x'], uc['y'], uc['text'], fontsize=8.5, ha='center', va='center',
            color='#333', zorder=5)

# ---- 连接线（Actor → 用例）----
connections = [
    # 种植户
    (0.8, 8.5, 3.9, 9.2), (0.8, 8.5, 3.9, 8.2), (0.8, 8.5, 3.9, 7.2),
    # 质检员
    (0.8, 6.0, 6.9, 6.8), (0.8, 6.0, 6.9, 5.8),
    # 物流商
    (0.8, 3.5, 3.9, 4.5), (0.8, 3.5, 3.9, 3.5),
    # 销售商
    (0.8, 1.5, 3.9, 2.3),
    # 消费者
    (15.2, 6.5, 12.2, 7.5), (15.2, 6.5, 12.2, 6.5), (15.2, 6.5, 12.2, 5.5),
    # 管理员
    (15.2, 3.5, 12.2, 4.0), (15.2, 3.5, 12.2, 3.0), (15.2, 3.5, 12.2, 2.0),
    # 共用
    (6.1, 7.2, 6.9, 4.0), (6.1, 4.5, 6.9, 4.0),
    (6.9, 5.8, 6.9, 2.8),
]

for x1, y1, x2, y2 in connections:
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='-', color='#666', lw=1.0))

# ---- 包含关系（虚线）----
includes = [
    (8.0, 6.8, 8.0, 4.5),  # 上传质检报告 <<include>> 国密上链
    (8.0, 5.8, 8.0, 4.5),  # 录入质检结果 <<include>> 国密上链
]
for x1, y1, x2, y2 in includes:
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='#999', lw=1.0,
                                linestyle='dashed'))
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ax.text(mx + 0.15, my, '<<include>>', fontsize=7, color='#999', ha='left')

plt.tight_layout()
output_path = '../pic/图5-1 溯源系统用例图.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight',
            facecolor='#f8f9fa', edgecolor='none')
plt.close()
print(f'[OK] 用例图已保存: {output_path}')
