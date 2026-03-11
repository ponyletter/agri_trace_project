#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_er_diagram.py
生成数据库 E-R 图（图5-3）
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(18, 12))
ax.set_xlim(0, 18)
ax.set_ylim(0, 12)
ax.axis('off')
ax.set_facecolor('#f8f9fa')
fig.patch.set_facecolor('#f8f9fa')

ax.text(9, 11.6, '农产品溯源系统 数据库 E-R 图', fontsize=18, fontweight='bold',
        ha='center', va='center', color='#1a3a5c')

def draw_entity(ax, x, y, w, h, title, fields, header_color, field_color):
    """绘制实体框"""
    # 标题栏
    header = FancyBboxPatch((x, y + h - 0.55), w, 0.55,
                             boxstyle="round,pad=0.02",
                             facecolor=header_color, edgecolor='#333', lw=1.5, zorder=3)
    ax.add_patch(header)
    ax.text(x + w / 2, y + h - 0.28, title, fontsize=11, ha='center', va='center',
            color='white', fontweight='bold', zorder=4)
    # 字段区
    body = FancyBboxPatch((x, y), w, h - 0.55,
                           boxstyle="round,pad=0.02",
                           facecolor=field_color, edgecolor='#333', lw=1.5, zorder=3)
    ax.add_patch(body)
    # 字段列表
    field_h = (h - 0.55) / len(fields)
    for i, (fname, ftype, is_pk, is_fk) in enumerate(fields):
        fy = y + h - 0.55 - (i + 1) * field_h + field_h / 2
        prefix = '🔑 ' if is_pk else ('🔗 ' if is_fk else '   ')
        color = '#c0392b' if is_pk else ('#2980b9' if is_fk else '#333')
        ax.text(x + 0.15, fy, f'{prefix}{fname}', fontsize=8.5, va='center', color=color, zorder=4)
        ax.text(x + w - 0.1, fy, ftype, fontsize=7.5, va='center', ha='right', color='#888', zorder=4)
        if i < len(fields) - 1:
            ax.plot([x, x + w], [fy - field_h / 2, fy - field_h / 2],
                    color='#ddd', lw=0.8, zorder=4)

# ---- 实体定义 ----
# users 表
draw_entity(ax, 0.5, 7.5, 4.0, 3.8, 'users (用户表)',
            [('id', 'BIGINT PK', True, False),
             ('username', 'VARCHAR(64)', False, False),
             ('password_hash', 'VARCHAR(255)', False, False),
             ('real_name', 'VARCHAR(64)', False, False),
             ('role', 'VARCHAR(32)', False, False),
             ('phone', 'VARCHAR(20)', False, False),
             ('created_at', 'TIMESTAMP', False, False),
             ('updated_at', 'TIMESTAMP', False, False)],
            '#27ae60', '#f0fff4')

# agri_batches 表
draw_entity(ax, 6.5, 7.0, 4.5, 4.5, 'agri_batches (批次表)',
            [('id', 'BIGINT PK', True, False),
             ('batch_no', 'VARCHAR(64) UK', False, False),
             ('product_name', 'VARCHAR(128)', False, False),
             ('product_type', 'VARCHAR(64)', False, False),
             ('quantity', 'DECIMAL(10,2)', False, False),
             ('unit', 'VARCHAR(16)', False, False),
             ('origin_info', 'VARCHAR(255)', False, False),
             ('farmer_id', 'BIGINT FK', False, True),
             ('status', 'TINYINT', False, False),
             ('created_at', 'TIMESTAMP', False, False)],
            '#2980b9', '#eaf3fb')

# trace_records 表
draw_entity(ax, 0.5, 1.5, 4.5, 5.5, 'trace_records (溯源记录表)',
            [('id', 'BIGINT PK', True, False),
             ('batch_id', 'BIGINT FK', False, True),
             ('node_type', 'VARCHAR(32)', False, False),
             ('operator_id', 'BIGINT FK', False, True),
             ('operation_time', 'DATETIME', False, False),
             ('location', 'VARCHAR(255)', False, False),
             ('env_data', 'JSON', False, False),
             ('tx_hash', 'VARCHAR(128)', False, False),
             ('block_height', 'BIGINT', False, False),
             ('created_at', 'TIMESTAMP', False, False)],
            '#8e44ad', '#f5eef8')

# ipfs_files 表
draw_entity(ax, 6.5, 1.5, 4.0, 3.5, 'ipfs_files (IPFS文件表)',
            [('id', 'BIGINT PK', True, False),
             ('record_id', 'BIGINT FK', False, True),
             ('file_name', 'VARCHAR(128)', False, False),
             ('file_type', 'VARCHAR(32)', False, False),
             ('cid', 'VARCHAR(128)', False, False),
             ('created_at', 'TIMESTAMP', False, False)],
            '#e67e22', '#fef9e7')

# ---- 关系说明框 ----
draw_entity(ax, 12.5, 7.5, 5.0, 3.5, '关系说明',
            [('users 1:N agri_batches', '种植户创建批次', False, False),
             ('users 1:N trace_records', '用户操作溯源节点', False, False),
             ('agri_batches 1:N trace_records', '批次包含多个节点', False, False),
             ('trace_records 1:N ipfs_files', '节点关联多个文件', False, False),
             ('tx_hash', '国密SM3链上存证', False, False),
             ('env_data(JSON)', '扩展业务数据字段', False, False)],
            '#c0392b', '#fdf2f2')

# ---- 关系连接线 ----
# users → agri_batches (farmer_id)
ax.annotate('', xy=(6.5, 9.5), xytext=(4.5, 9.5),
            arrowprops=dict(arrowstyle='->', color='#27ae60', lw=2))
ax.text(5.5, 9.7, '1:N', fontsize=10, ha='center', color='#27ae60', fontweight='bold')

# users → trace_records (operator_id)
ax.annotate('', xy=(0.5, 5.5), xytext=(1.5, 7.5),
            arrowprops=dict(arrowstyle='->', color='#27ae60', lw=2,
                            connectionstyle='arc3,rad=0.3'))
ax.text(0.3, 6.5, '1:N', fontsize=10, ha='center', color='#27ae60', fontweight='bold')

# agri_batches → trace_records (batch_id)
ax.annotate('', xy=(4.5, 4.5), xytext=(6.5, 7.0),
            arrowprops=dict(arrowstyle='->', color='#2980b9', lw=2,
                            connectionstyle='arc3,rad=-0.2'))
ax.text(5.8, 5.8, '1:N', fontsize=10, ha='center', color='#2980b9', fontweight='bold')

# trace_records → ipfs_files (record_id)
ax.annotate('', xy=(6.5, 3.5), xytext=(5.0, 3.5),
            arrowprops=dict(arrowstyle='->', color='#8e44ad', lw=2))
ax.text(5.75, 3.7, '1:N', fontsize=10, ha='center', color='#8e44ad', fontweight='bold')

plt.tight_layout()
output_path = '../pic/图5-3 数据库ER图.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight',
            facecolor='#f8f9fa', edgecolor='none')
plt.close()
print(f'[OK] ER图已保存: {output_path}')
