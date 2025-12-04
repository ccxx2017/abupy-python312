# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

# 读取文件所在的目录
here = os.path.abspath(os.path.dirname(__file__))

# 这是一个辅助函数，用来读取 __init__.py 里的版本号，
# 这样你就不用手动在 setup.py 里再写一次版本了
def get_version():
    init_file = os.path.join(here, 'abupy', '__init__.py')
    with open(init_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('__version__'):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
    return "0.0.1"

setup(
    name="abupy",
    version=get_version(),
    description="Abu quant for Python 3.12+",
    author="Abu (Ported by CCXX)", 
    packages=find_packages(), # 自动寻找 abupy 文件夹
    include_package_data=True,
    platforms="any",
    install_requires=[
        # 核心数据库 - 这些在 Py3.12 必须用新版
        "pandas>=2.0.0",   # 警告：abupy 以前用的是 pandas 0.19，这里会有大量 API 报错，这是你修复工作的重点
        "numpy>=1.26.0",
        "scipy",
        "matplotlib",
        "seaborn",
        "scikit-learn",
        "statsmodels",
        
        # 工具库
        "requests",
        "ipython",
        "tqdm", 
        "beautifulsoup4",
        "sqlalchemy",
        "tables", # 用于处理 HDF5 数据
        "joblib",
        
        # 兼容性补充
        "yfinance", # 替代雅虎财经旧接口
    ],
    # 这一行很重要，确保 zip_safe 为 False
    zip_safe=False,
)