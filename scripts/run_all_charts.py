#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all_charts.py
一键运行所有图表生成脚本
使用方法：
    cd scripts
    python3 run_all_charts.py
"""

import subprocess
import sys
import os

scripts = [
    'gen_usecase_diagram.py',
    'gen_architecture_diagram.py',
    'gen_er_diagram.py',
    'gen_trace_flow_diagram.py',
    'gen_performance_charts.py',
]

os.chdir(os.path.dirname(os.path.abspath(__file__)))
print('=' * 60)
print('农产品溯源系统 - 论文图表批量生成工具')
print('=' * 60)

success = 0
failed = 0
for script in scripts:
    print(f'\n[运行] {script}')
    result = subprocess.run([sys.executable, script], capture_output=True, text=True)
    if result.returncode == 0:
        print(result.stdout.strip())
        success += 1
    else:
        print(f'[错误] {result.stderr.strip()}')
        failed += 1

print('\n' + '=' * 60)
print(f'完成！成功: {success} 个，失败: {failed} 个')
print(f'图片已保存至: {os.path.abspath("../pic/")}')
print('=' * 60)
