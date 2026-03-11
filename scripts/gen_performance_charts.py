#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_performance_charts.py
生成系统性能测试图表（图5-8 ~ 图5-11）
包含：
  1. 吞吐量 TPS 对比图（国密 vs 标准密码）
  2. 响应时间分布图（各接口延迟）
  3. 国密算法开销分析图（SM2/SM3/SM4）
  4. 并发压力测试图（TPS vs 并发数）
数据来源：模拟 Caliper 测试数据（已存入 CSV）
"""

import os
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

OUTPUT_DIR = '../pic'
DATA_DIR = '../data'
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# ============================================================
# 1. 生成模拟测试数据 CSV
# ============================================================

# 1.1 TPS 对比数据（国密 vs 标准密码）
tps_data = [
    ['scenario', 'concurrency', 'tps_gm', 'tps_std'],
    ['溯源记录上链', 10, 42.3, 68.5],
    ['溯源记录上链', 20, 78.6, 124.2],
    ['溯源记录上链', 50, 156.4, 248.7],
    ['溯源记录上链', 100, 198.2, 312.5],
    ['溯源记录上链', 200, 187.3, 298.1],
    ['溯源查询', 10, 185.4, 210.3],
    ['溯源查询', 20, 342.8, 398.5],
    ['溯源查询', 50, 621.5, 712.4],
    ['溯源查询', 100, 834.2, 956.8],
    ['溯源查询', 200, 812.6, 932.1],
]
with open(f'{DATA_DIR}/tps_comparison.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(tps_data)

# 1.2 接口响应时间数据（ms）
latency_data = [
    ['interface', 'avg_ms', 'p50_ms', 'p95_ms', 'p99_ms', 'max_ms'],
    ['用户登录', 8.2, 7.5, 15.3, 28.6, 45.2],
    ['创建批次', 12.4, 11.2, 22.8, 38.5, 62.1],
    ['添加溯源记录(Mock)', 45.6, 42.3, 78.5, 125.4, 198.3],
    ['添加溯源记录(Fabric)', 312.5, 298.4, 485.6, 623.8, 892.4],
    ['溯源查询(MySQL)', 18.3, 16.5, 32.4, 52.8, 85.6],
    ['溯源查询(链上)', 285.4, 268.2, 445.8, 578.3, 756.2],
    ['IPFS文件上传', 156.8, 142.5, 285.4, 398.6, 523.4],
]
with open(f'{DATA_DIR}/latency_distribution.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(latency_data)

# 1.3 国密算法开销数据（微秒）
gm_overhead_data = [
    ['algorithm', 'operation', 'time_us', 'std_time_us'],
    ['SM2', '密钥生成', 1245.6, 856.3],
    ['SM2', '签名', 985.4, 623.8],
    ['SM2', '验签', 1125.8, 712.5],
    ['SM2', '加密', 1356.2, 845.6],
    ['SM2', '解密', 1289.5, 798.4],
    ['SM3', '哈希(1KB)', 12.5, 8.3],
    ['SM3', '哈希(10KB)', 85.6, 58.4],
    ['SM3', '哈希(100KB)', 812.3, 548.6],
    ['SM4', '加密(1KB)', 45.8, 32.5],
    ['SM4', '解密(1KB)', 48.2, 34.8],
]
with open(f'{DATA_DIR}/gm_overhead.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(gm_overhead_data)

# 1.4 并发压力测试数据
stress_data = [
    ['concurrency', 'tps', 'avg_latency_ms', 'error_rate'],
    [1, 18.5, 54.2, 0.0],
    [5, 85.3, 58.6, 0.0],
    [10, 156.8, 63.8, 0.0],
    [20, 298.4, 67.1, 0.0],
    [50, 512.6, 97.5, 0.0],
    [100, 634.2, 157.8, 0.12],
    [150, 658.4, 228.3, 0.85],
    [200, 612.8, 326.5, 2.34],
    [250, 534.5, 468.2, 5.68],
    [300, 423.6, 712.4, 12.45],
]
with open(f'{DATA_DIR}/stress_test.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(stress_data)

print('[OK] 测试数据 CSV 已生成')

# ============================================================
# 2. 绘制图表
# ============================================================

COLORS = {
    'gm': '#e74c3c',
    'std': '#2980b9',
    'primary': '#1a5276',
    'success': '#27ae60',
    'warning': '#e67e22',
    'info': '#17a2b8',
}

# ---- 图5-8: TPS 对比折线图 ----
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('图5-8  系统吞吐量(TPS)对比测试', fontsize=15, fontweight='bold', color='#1a3a5c')

concurrencies = [10, 20, 50, 100, 200]
# 上链场景
tps_gm_write = [42.3, 78.6, 156.4, 198.2, 187.3]
tps_std_write = [68.5, 124.2, 248.7, 312.5, 298.1]
# 查询场景
tps_gm_read = [185.4, 342.8, 621.5, 834.2, 812.6]
tps_std_read = [210.3, 398.5, 712.4, 956.8, 932.1]

ax = axes[0]
ax.plot(concurrencies, tps_gm_write, 'o-', color=COLORS['gm'], lw=2.5,
        markersize=8, label='国密版 Fabric')
ax.plot(concurrencies, tps_std_write, 's--', color=COLORS['std'], lw=2.5,
        markersize=8, label='标准版 Fabric')
ax.fill_between(concurrencies, tps_gm_write, tps_std_write, alpha=0.1, color='gray')
ax.set_title('溯源记录上链 TPS', fontsize=12)
ax.set_xlabel('并发数', fontsize=11)
ax.set_ylabel('TPS (事务/秒)', fontsize=11)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_facecolor('#fafafa')
for i, (x, y) in enumerate(zip(concurrencies, tps_gm_write)):
    ax.annotate(f'{y}', (x, y), textcoords='offset points', xytext=(0, 8),
                fontsize=8, ha='center', color=COLORS['gm'])

ax = axes[1]
ax.plot(concurrencies, tps_gm_read, 'o-', color=COLORS['gm'], lw=2.5,
        markersize=8, label='国密版 Fabric')
ax.plot(concurrencies, tps_std_read, 's--', color=COLORS['std'], lw=2.5,
        markersize=8, label='标准版 Fabric')
ax.fill_between(concurrencies, tps_gm_read, tps_std_read, alpha=0.1, color='gray')
ax.set_title('溯源查询 TPS', fontsize=12)
ax.set_xlabel('并发数', fontsize=11)
ax.set_ylabel('TPS (事务/秒)', fontsize=11)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_facecolor('#fafafa')

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/图5-8 系统TPS对比测试.png', dpi=150, bbox_inches='tight')
plt.close()
print('[OK] 图5-8 TPS对比图已生成')

# ---- 图5-9: 接口响应时间分布图 ----
fig, ax = plt.subplots(figsize=(14, 7))
ax.set_title('图5-9  各接口响应时间分布（ms）', fontsize=15, fontweight='bold', color='#1a3a5c')

interfaces = ['用户登录', '创建批次', '溯源记录\n(Mock)', '溯源记录\n(Fabric)', '溯源查询\n(MySQL)', '溯源查询\n(链上)', 'IPFS\n文件上传']
avg_ms = [8.2, 12.4, 45.6, 312.5, 18.3, 285.4, 156.8]
p95_ms = [15.3, 22.8, 78.5, 485.6, 32.4, 445.8, 285.4]
p99_ms = [28.6, 38.5, 125.4, 623.8, 52.8, 578.3, 398.6]

x = np.arange(len(interfaces))
width = 0.25

bars1 = ax.bar(x - width, avg_ms, width, label='平均响应时间', color='#27ae60', alpha=0.85)
bars2 = ax.bar(x, p95_ms, width, label='P95 响应时间', color='#e67e22', alpha=0.85)
bars3 = ax.bar(x + width, p99_ms, width, label='P99 响应时间', color='#e74c3c', alpha=0.85)

ax.set_xlabel('接口名称', fontsize=12)
ax.set_ylabel('响应时间 (ms)', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(interfaces, fontsize=10)
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)
ax.set_facecolor('#fafafa')

# 添加数值标签
for bar in bars1:
    h = bar.get_height()
    if h < 50:
        ax.text(bar.get_x() + bar.get_width() / 2, h + 3, f'{h}', ha='center', fontsize=7.5)

# 添加参考线
ax.axhline(y=200, color='#c0392b', linestyle='--', alpha=0.5, lw=1.5)
ax.text(6.5, 205, '200ms 阈值', fontsize=9, color='#c0392b')

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/图5-9 接口响应时间分布.png', dpi=150, bbox_inches='tight')
plt.close()
print('[OK] 图5-9 响应时间分布图已生成')

# ---- 图5-10: 国密算法开销分析 ----
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('图5-10  国密算法性能开销分析', fontsize=15, fontweight='bold', color='#1a3a5c')

# SM2 操作对比
ax = axes[0]
sm2_ops = ['密钥生成', '签名', '验签', '加密', '解密']
sm2_gm = [1245.6, 985.4, 1125.8, 1356.2, 1289.5]
sm2_std = [856.3, 623.8, 712.5, 845.6, 798.4]
x = np.arange(len(sm2_ops))
ax.bar(x - 0.2, sm2_gm, 0.4, label='SM2 (国密)', color=COLORS['gm'], alpha=0.85)
ax.bar(x + 0.2, sm2_std, 0.4, label='RSA-2048 (对照)', color=COLORS['std'], alpha=0.85)
ax.set_title('SM2 vs RSA-2048 操作耗时', fontsize=12)
ax.set_xlabel('操作类型', fontsize=11)
ax.set_ylabel('耗时 (μs)', fontsize=11)
ax.set_xticks(x)
ax.set_xticklabels(sm2_ops, fontsize=10)
ax.legend(fontsize=10)
ax.grid(axis='y', alpha=0.3)
ax.set_facecolor('#fafafa')

# 计算开销比
overhead_ratio = [(g / s - 1) * 100 for g, s in zip(sm2_gm, sm2_std)]
ax2 = ax.twinx()
ax2.plot(x, overhead_ratio, 'D--', color='#8e44ad', lw=1.5, markersize=6, label='额外开销(%)')
ax2.set_ylabel('额外开销 (%)', fontsize=10, color='#8e44ad')
ax2.tick_params(axis='y', labelcolor='#8e44ad')
ax2.legend(loc='upper right', fontsize=9)

# SM3 哈希性能
ax = axes[1]
data_sizes = ['1KB', '10KB', '100KB', '1MB']
sm3_times = [12.5, 85.6, 812.3, 8234.5]
sha256_times = [8.3, 58.4, 548.6, 5612.8]
x = np.arange(len(data_sizes))
ax.bar(x - 0.2, sm3_times, 0.4, label='SM3 (国密)', color=COLORS['gm'], alpha=0.85)
ax.bar(x + 0.2, sha256_times, 0.4, label='SHA-256 (对照)', color=COLORS['std'], alpha=0.85)
ax.set_title('SM3 vs SHA-256 哈希耗时', fontsize=12)
ax.set_xlabel('数据大小', fontsize=11)
ax.set_ylabel('耗时 (μs)', fontsize=11)
ax.set_xticks(x)
ax.set_xticklabels(data_sizes, fontsize=10)
ax.legend(fontsize=10)
ax.grid(axis='y', alpha=0.3)
ax.set_facecolor('#fafafa')
ax.set_yscale('log')
ax.yaxis.set_major_formatter(mticker.ScalarFormatter())

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/图5-10 国密算法开销分析.png', dpi=150, bbox_inches='tight')
plt.close()
print('[OK] 图5-10 国密算法开销图已生成')

# ---- 图5-11: 并发压力测试图 ----
fig, ax1 = plt.subplots(figsize=(12, 6))
ax1.set_title('图5-11  系统并发压力测试结果', fontsize=15, fontweight='bold', color='#1a3a5c')

concurrencies_s = [1, 5, 10, 20, 50, 100, 150, 200, 250, 300]
tps_s = [18.5, 85.3, 156.8, 298.4, 512.6, 634.2, 658.4, 612.8, 534.5, 423.6]
latency_s = [54.2, 58.6, 63.8, 67.1, 97.5, 157.8, 228.3, 326.5, 468.2, 712.4]
error_s = [0.0, 0.0, 0.0, 0.0, 0.0, 0.12, 0.85, 2.34, 5.68, 12.45]

color1 = '#2980b9'
color2 = '#e74c3c'

ax1.plot(concurrencies_s, tps_s, 'o-', color=color1, lw=2.5, markersize=8, label='TPS')
ax1.fill_between(concurrencies_s, tps_s, alpha=0.1, color=color1)
ax1.set_xlabel('并发用户数', fontsize=12)
ax1.set_ylabel('TPS (事务/秒)', fontsize=12, color=color1)
ax1.tick_params(axis='y', labelcolor=color1)
ax1.set_facecolor('#fafafa')
ax1.grid(True, alpha=0.3)

# 标注最大TPS点
max_idx = tps_s.index(max(tps_s))
ax1.annotate(f'峰值 TPS: {max(tps_s)}',
             xy=(concurrencies_s[max_idx], max(tps_s)),
             xytext=(concurrencies_s[max_idx] + 20, max(tps_s) - 30),
             arrowprops=dict(arrowstyle='->', color='#333'),
             fontsize=10, color='#333')

ax2 = ax1.twinx()
ax2.plot(concurrencies_s, latency_s, 's--', color=color2, lw=2, markersize=7, label='平均延迟(ms)')
ax2.set_ylabel('平均响应时间 (ms)', fontsize=12, color=color2)
ax2.tick_params(axis='y', labelcolor=color2)

# 错误率柱状图
ax3 = ax1.twinx()
ax3.spines['right'].set_position(('outward', 60))
ax3.bar(concurrencies_s, error_s, width=8, alpha=0.3, color='#e67e22', label='错误率(%)')
ax3.set_ylabel('错误率 (%)', fontsize=11, color='#e67e22')
ax3.tick_params(axis='y', labelcolor='#e67e22')

# 合并图例
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/图5-11 并发压力测试结果.png', dpi=150, bbox_inches='tight')
plt.close()
print('[OK] 图5-11 并发压力测试图已生成')

print('\n[完成] 所有性能测试图表已生成到 ../pic/ 目录')
print('CSV 数据文件已保存到 ../data/ 目录')
