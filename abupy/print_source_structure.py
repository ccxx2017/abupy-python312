#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
源代码文件结构打印工具

该脚本用于打印 abupy 量化投资项目的源代码文件结构，帮助开发者快速了解项目结构。
支持打印核心模块、业务模块、工具模块或完整项目结构。
"""

import os
import sys
from pathlib import Path
from typing import List, Set


class SourceStructurePrinter:
    """源代码结构打印器"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        
        # 核心模块目录
        self.core_dirs = ['CoreBu', 'UtilBu', 'ExtBu']
        
        # 业务功能模块目录（以Bu结尾的目录）
        self.business_dirs = [
            'AlphaBu', 'BetaBu', 'FactorBuyBu', 'FactorSellBu', 'TradeBu',
            'MarketBu', 'IndicatorBu', 'MLBu', 'MetricsBu', 'UmpBu',
            'TLineBu', 'SimilarBu', 'SlippageBu', 'PickStockBu', 'CheckBu',
            'CrawlBu', 'DLBu', 'WidgetBu'
        ]
        
        # 数据和配置目录
        self.data_dirs = ['RomDataBu']
        
        # Python 项目源代码文件扩展名
        self.source_extensions = {'.py', '.pyx', '.pyi'}
        
        # 配置和文档文件扩展名
        self.config_extensions = {'.md', '.txt', '.yaml', '.yml', '.json', '.toml', '.cfg', '.ini'}
        
        # 数据文件扩展名
        self.data_extensions = {'.csv', '.db', '.sqlite', '.json', '.txt', '.zip'}
        
        # 所有相关文件扩展名
        self.all_extensions = self.source_extensions | self.config_extensions | self.data_extensions
        
        # 需要忽略的目录
        self.ignore_dirs = {
            '__pycache__', '.pytest_cache', '.git', '.vscode', '.idea', 
            'dist', 'build', 'coverage', '.nyc_output', '.trae', '.cursor',
            'ui_photos', 'tests_backup_20250817_211730', '.ipynb_checkpoints'
        }
        
        # 需要忽略的文件
        self.ignore_files = {
            '.DS_Store', 'Thumbs.db', '.gitkeep', '.gitignore', '.pyc',
            'uv.lock', '.coverage', 'coverage.xml'
        }
    
    def should_ignore_path(self, path: Path) -> bool:
        """判断是否应该忽略该路径"""
        # 检查目录名
        if path.is_dir() and path.name in self.ignore_dirs:
            return True
        
        # 检查文件名
        if path.is_file() and path.name in self.ignore_files:
            return True
        
        # 检查是否是隐藏文件/目录（以.开头，但不包括特定的配置文件）
        if path.name.startswith('.') and path.name not in {'.editorconfig', '.python-version'}:
            return True
        
        return False
    
    def is_source_file(self, file_path: Path, extensions: Set[str]) -> bool:
        """判断是否是源代码文件"""
        return file_path.suffix.lower() in extensions
    
    def print_tree(self, directory: Path, prefix: str = "", extensions: Set[str] = None, 
                   target_dirs: List[str] = None, max_depth: int = 10, current_depth: int = 0) -> None:
        """打印目录树结构"""
        if current_depth >= max_depth:
            return
        
        if self.should_ignore_path(directory):
            return
        
        try:
            items = sorted(directory.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
        except PermissionError:
            return
        
        # 过滤项目
        filtered_items = []
        for item in items:
            if self.should_ignore_path(item):
                continue
            
            # 如果指定了目标目录，只显示这些目录及其内容
            if target_dirs and current_depth == 0:
                if item.is_dir() and item.name not in target_dirs:
                    continue
            
            # 如果指定了扩展名，只显示匹配的文件
            if extensions and item.is_file():
                if not self.is_source_file(item, extensions):
                    continue
            
            filtered_items.append(item)
        
        for i, item in enumerate(filtered_items):
            is_last = i == len(filtered_items) - 1
            current_prefix = "└── " if is_last else "├── "
            
            print(f"{prefix}{current_prefix}{item.name}{'/' if item.is_dir() else ''}")
            
            if item.is_dir():
                next_prefix = prefix + ("    " if is_last else "│   ")
                self.print_tree(item, next_prefix, extensions, target_dirs, max_depth, current_depth + 1)
    
    def print_core_structure(self):
        """打印核心模块结构"""
        print("\n" + "="*60)
        print("🔧 核心模块源代码结构")
        print("="*60)
        print(f"📁 根目录: {self.project_root}")
        print(f"📋 核心模块: {', '.join(self.core_dirs)}")
        print(f"📄 文件类型: {', '.join(sorted(self.source_extensions))}")
        print("-"*60)
        
        self.print_tree(self.project_root, "", self.source_extensions, self.core_dirs)
        print("-"*60)
        print("✅ 核心模块结构打印完成\n")
    
    def print_business_structure(self):
        """打印业务模块结构"""
        print("\n" + "="*60)
        print("💼 业务模块源代码结构")
        print("="*60)
        print(f"📁 根目录: {self.project_root}")
        print(f"📋 业务模块: {', '.join(self.business_dirs[:5])}... (共{len(self.business_dirs)}个)")
        print(f"📄 文件类型: {', '.join(sorted(self.source_extensions))}")
        print("-"*60)
        
        self.print_tree(self.project_root, "", self.source_extensions, self.business_dirs)
        print("-"*60)
        print("✅ 业务模块结构打印完成\n")
    
    def print_data_structure(self):
        """打印数据模块结构"""
        print("\n" + "="*60)
        print("📊 数据模块结构")
        print("="*60)
        print(f"📁 根目录: {self.project_root}")
        print(f"📋 数据模块: {', '.join(self.data_dirs)}")
        print(f"📄 文件类型: {', '.join(sorted(self.data_extensions))}")
        print("-"*60)
        
        self.print_tree(self.project_root, "", self.data_extensions, self.data_dirs)
        print("-"*60)
        print("✅ 数据模块结构打印完成\n")
    
    def print_full_structure(self):
        """打印完整项目结构"""
        print("\n" + "="*60)
        print("🏗️  完整 abupy 项目源代码结构")
        print("="*60)
        print(f"📁 根目录: {self.project_root}")
        print(f"📄 文件类型: {', '.join(sorted(self.all_extensions))}")
        print("-"*60)
        
        # 打印核心模块
        print("\n🔧 核心模块:")
        self.print_tree(self.project_root, "  ", self.source_extensions, self.core_dirs, max_depth=6)
        
        # 打印业务模块
        print("\n💼 业务模块:")
        self.print_tree(self.project_root, "  ", self.source_extensions, self.business_dirs, max_depth=6)
        
        # 打印数据模块
        print("\n📊 数据模块:")
        self.print_tree(self.project_root, "  ", self.data_extensions, self.data_dirs, max_depth=6)
        
        print("-"*60)
        print("✅ 完整项目结构打印完成\n")
    
    def print_source_only_structure(self):
        """只打印源代码文件结构（不包含数据文件）"""
        print("\n" + "="*60)
        print("📝 源代码文件结构（仅 .py 文件）")
        print("="*60)
        print(f"📁 根目录: {self.project_root}")
        print(f"📄 文件类型: {', '.join(sorted(self.source_extensions))}")
        print("-"*60)
        
        # 所有模块目录
        all_dirs = self.core_dirs + self.business_dirs
        self.print_tree(self.project_root, "", self.source_extensions, all_dirs)
        print("-"*60)
        print("✅ 源代码结构打印完成\n")


def get_user_choice() -> str:
    """获取用户选择"""
    print("\n" + "="*60)
    print("📂 abupy 量化投资项目源代码结构打印工具")
    print("="*60)
    print("请选择要打印的结构类型:")
    print("  1️⃣  核心模块结构 (CoreBu, UtilBu, ExtBu)")
    print("  2️⃣  业务模块结构 (AlphaBu, BetaBu, TradeBu 等)")
    print("  3️⃣  数据模块结构 (RomDataBu)")
    print("  4️⃣  源代码结构 (仅 .py 文件)")
    print("  5️⃣  完整项目结构 (所有模块)")
    print("  0️⃣  退出程序")
    print("-"*60)
    
    while True:
        try:
            choice = input("请输入选择 (0-5): ").strip()
            if choice in ['0', '1', '2', '3', '4', '5']:
                return choice
            else:
                print("❌ 无效选择，请输入 0-5 之间的数字")
        except KeyboardInterrupt:
            print("\n\n👋 程序已退出")
            sys.exit(0)
        except EOFError:
            print("\n\n👋 程序已退出")
            sys.exit(0)


def main():
    """主函数"""
    # 获取项目根目录（当前脚本所在目录就是项目根目录）
    script_dir = Path(__file__).parent
    project_root = script_dir
    
    # 验证项目根目录
    if not project_root.exists():
        print(f"❌ 项目根目录不存在: {project_root}")
        sys.exit(1)
    
    printer = SourceStructurePrinter(str(project_root))
    
    # 检查命令行参数，支持非交互模式
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ['core', 'c', '1']:
            printer.print_core_structure()
            return
        elif arg in ['business', 'b', '2']:
            printer.print_business_structure()
            return
        elif arg in ['data', 'd', '3']:
            printer.print_data_structure()
            return
        elif arg in ['source', 's', '4']:
            printer.print_source_only_structure()
            return
        elif arg in ['full', 'all', 'a', '5']:
            printer.print_full_structure()
            return
        elif arg in ['help', 'h', '--help', '-h']:
            print("\n使用方法:")
            print("  python print_source_structure.py [选项]")
            print("\n选项:")
            print("  core, c, 1        - 打印核心模块结构")
            print("  business, b, 2    - 打印业务模块结构")
            print("  data, d, 3        - 打印数据模块结构")
            print("  source, s, 4      - 打印源代码结构（仅 .py 文件）")
            print("  full, all, a, 5   - 打印完整项目结构")
            print("  help, h           - 显示此帮助信息")
            print("\n不提供参数时将进入交互模式")
            return
        else:
            print(f"❌ 未知参数: {sys.argv[1]}")
            print("使用 'python print_source_structure.py help' 查看帮助")
            return
    
    # 交互模式
    while True:
        choice = get_user_choice()
        
        if choice == '0':
            print("\n👋 感谢使用，再见！")
            break
        elif choice == '1':
            printer.print_core_structure()
        elif choice == '2':
            printer.print_business_structure()
        elif choice == '3':
            printer.print_data_structure()
        elif choice == '4':
            printer.print_source_only_structure()
        elif choice == '5':
            printer.print_full_structure()
        
        # 询问是否继续
        print("\n" + "-"*30)
        try:
            continue_choice = input("是否继续使用？(y/n): ").strip().lower()
            if continue_choice not in ['y', 'yes', '是', '']:
                print("\n👋 感谢使用，再见！")
                break
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 感谢使用，再见！")
            break


if __name__ == "__main__":
    main()