#!/usr/bin/env python3
"""
动态矩阵生成脚本
根据文件变更自动生成测试矩阵
"""
import json
import sys
import os
from pathlib import Path


def get_changed_files(base_ref="HEAD~1"):
    """获取变更的文件列表"""
    import subprocess
    
    try:
        # 获取变更的文件
        result = subprocess.run(
            ["git", "diff", "--name-only", base_ref, "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().split('\n') if result.stdout.strip() else []
    except subprocess.CalledProcessError:
        # 如果无法获取变更文件，返回空列表（运行所有测试）
        return []


def should_run_full_matrix(changed_files):
    """判断是否需要运行完整矩阵"""
    critical_paths = [
        "src/gpu_driver.py",
        "src/gpu_compute.py",
        "tests/",
    ]
    
    # 如果变更了关键文件，运行完整矩阵
    for file in changed_files:
        for critical in critical_paths:
            if critical in file:
                return True
    return False


def generate_matrix(changed_files=None):
    """生成测试矩阵"""
    if changed_files is None:
        changed_files = get_changed_files()
    
    # 基础矩阵配置
    matrix = {
        "os": ["ubuntu-latest"],
        "python-version": ["3.10"],
        "gpu-driver-version": ["2.0"]
    }
    
    # 如果需要完整矩阵
    if should_run_full_matrix(changed_files) or not changed_files:
        matrix = {
            "os": ["ubuntu-latest", "windows-latest"],
            "python-version": ["3.9", "3.10", "3.11"],
            "gpu-driver-version": ["1.0", "2.0"],
            "exclude": [
                {
                    "os": "windows-latest",
                    "gpu-driver-version": "2.0"
                }
            ]
        }
    
    return matrix


def main():
    """主函数"""
    base_ref = sys.argv[1] if len(sys.argv) > 1 else "HEAD~1"
    changed_files = get_changed_files(base_ref)
    
    matrix = generate_matrix(changed_files)
    
    # 输出 JSON 格式的矩阵
    print(json.dumps(matrix, indent=2))
    
    # 也输出变更文件信息（用于调试）
    if changed_files:
        print(f"\nChanged files: {len(changed_files)}", file=sys.stderr)
        for file in changed_files[:5]:  # 只显示前5个
            print(f"  - {file}", file=sys.stderr)
        if len(changed_files) > 5:
            print(f"  ... and {len(changed_files) - 5} more", file=sys.stderr)


if __name__ == "__main__":
    main()

