#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
火山引擎集成验证脚本
用于验证火山引擎 API 是否已正确配置和集成
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """检查 Python 版本"""
    print("🔍 检查 Python 版本...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - 符合要求")
        return True
    else:
        print(f"❌ Python 版本过低：{version.major}.{version.minor}")
        print("   需要 Python 3.8 或更高版本")
        return False


def check_env_file():
    """检查 .env 文件是否存在和配置"""
    print("\n🔍 检查 .env 文件...")
    if not Path('.env').exists():
        print("❌ .env 文件不存在")
        print("   建议：复制 .env.example 为 .env")
        return False
    
    with open('.env', 'r', encoding='utf-8') as f:
        content = f.read()
    
    volcano_key = None
    for line in content.splitlines():
        line = line.strip()
        # 跳过注释行
        if line.startswith('#'):
            continue
        if line.startswith('VOLCANOENGINE_API_KEY'):
            parts = line.split('=', 1)
            if len(parts) == 2:
                volcano_key = parts[1].strip()
                # 去除可能的引号
                if (volcano_key.startswith('"') and volcano_key.endswith('"')) or \
                   (volcano_key.startswith("'") and volcano_key.endswith("'")):
                    volcano_key = volcano_key[1:-1]
                break
    
    if volcano_key is not None:
        if 'your-' in volcano_key or 'your_' in volcano_key or not volcano_key:
            print("⚠️  VOLCANOENGINE_API_KEY 未配置（仍为示例值）")
            return False
        else:
            print("✅ VOLCANOENGINE_API_KEY 已配置")
            return True
    else:
        print("❌ .env 文件中未找到 VOLCANOENGINE_API_KEY")
        return False


def check_modules():
    """检查所需的 Python 模块"""
    print("\n🔍 检查 Python 依赖包...")
    required_packages = [
        'streamlit',
        'streamlit_option_menu',
        'beautifulsoup4',
        'requests',
        'plotly',
        'pandas',
        'dotenv'
    ]
    
    # 映射 pip 包名到 Python 导入模块名
    import_mapping = {
        'beautifulsoup4': 'bs4'
    }
    
    missing = []
    for package in required_packages:
        import_name = import_mapping.get(package, package.replace('-', '_'))
        try:
            __import__(import_name)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - 未安装")
            missing.append(package)
    
    if missing:
        print(f"\n💡 安装缺失的依赖包：")
        print(f"   pip install {' '.join(missing)}")
        return False
    
    return True


def check_source_files():
    """检查源代码文件是否包含火山引擎支持"""
    print("\n🔍 检查源代码集成...")
    
    files_to_check = {
        'utils/config.py': ['VOLCANOENGINE_API_KEY', 'VOLCANOENGINE_API_URL', 'volcanoengine'],
        'llm_analyzer.py': ['_call_volcanoengine_api', 'volcanoengine'],
        'app.py': ['volcanoengine', '🎵']
    }
    
    all_good = True
    for filepath, keywords in files_to_check.items():
        if not Path(filepath).exists():
            print(f"❌ 文件不存在：{filepath}")
            all_good = False
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        found = all(keyword in content for keyword in keywords)
        if found:
            print(f"✅ {filepath} - 已集成火山引擎支持")
        else:
            missing_kw = [kw for kw in keywords if kw not in content]
            print(f"❌ {filepath} - 缺失：{missing_kw}")
            all_good = False
    
    return all_good


def check_api_key():
    """检查 API Key 格式"""
    print("\n🔍 检查 API Key...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("⚠️  python-dotenv 未安装，跳过此检查")
        return None
    
    api_key = os.getenv('VOLCANOENGINE_API_KEY')
    
    if not api_key:
        print("❌ VOLCANOENGINE_API_KEY 未设置")
        return False
    
    if api_key.startswith('your-') or api_key.startswith('your_'):
        print("❌ VOLCANOENGINE_API_KEY 仍为示例值")
        return False
    
    if len(api_key) < 10:
        print("⚠️  API Key 可能格式不正确（太短）")
        return False
    
    print(f"✅ API Key 已配置（长度：{len(api_key)} 字符）")
    return True


def check_documentation():
    """检查文档文件"""
    print("\n🔍 检查文档...")
    
    doc_files = [
        'VOLCANOENGINE_GUIDE.md',
        'VOLCANOENGINE_INTEGRATION.md',
        'VOLCANOENGINE_QUICK_REFERENCE.md',
        'README.md'
    ]
    
    all_exist = True
    for doc in doc_files:
        if Path(doc).exists():
            print(f"✅ {doc}")
        else:
            print(f"❌ {doc} - 文件不存在")
            all_exist = False
    
    return all_exist


def test_import():
    """测试模块导入"""
    print("\n🔍 测试模块导入...")
    
    try:
        from utils.config import Config
        print("✅ 导入 Config 成功")
        
        # 检查是否有火山引擎的配置
        if hasattr(Config, 'VOLCANOENGINE_API_KEY'):
            print("✅ Config.VOLCANOENGINE_API_KEY 已定义")
        else:
            print("❌ Config.VOLCANOENGINE_API_KEY 未定义")
            return False
        
        # 检查模型配置
        if 'volcanoengine' in Config.MODEL_CONFIG:
            print("✅ 豆包模型配置已定义")
        else:
            print("❌ 豆包模型配置未定义")
            return False
        
        return True
    except Exception as e:
        print(f"⚠️  导入测试跳过：{str(e)}")
        return None


def generate_report(results):
    """生成验证报告"""
    print("\n" + "="*60)
    print("📊 集成验证报告")
    print("="*60)
    
    # 计算通过的检查项（排除 None）
    passed = sum(1 for v in results.values() if v is True)
    total = sum(1 for v in results.values() if v is not None)
    
    if total > 0:
        percentage = (passed / total) * 100
    else:
        percentage = 0
    
    print(f"\n总体完成度：{percentage:.0f}% ({passed}/{total})")
    
    if percentage == 100:
        print("\n🎉 恭喜！火山引擎已完全集成！")
        print("\n下一步：")
        print("1. 编辑 .env 文件，填入你的 API Key")
        print("2. 运行 pip install -r requirements.txt")
        print("3. 运行 streamlit run app.py")
        print("4. 在应用中选择 🎵 抖音豆包 模型")
        print("\n详细指南请查看 VOLCANOENGINE_GUIDE.md")
    elif percentage >= 80:
        print("\n⚠️  集成基本完成，但有几项需要注意")
        for check, passed in results.items():
            if passed is False:
                print(f"  - {check}")
    else:
        print("\n❌ 集成未完成，请检查上述错误")
    
    print("\n" + "="*60)


def main():
    """主函数"""
    print("\n" + "="*60)
    print("🔧 火山引擎集成验证工具 v1.0")
    print("="*60)
    
    # 运行所有检查
    results = {
        'Python 版本': check_python_version(),
        '环境配置': check_env_file(),
        'Python 依赖': check_modules(),
        '源代码集成': check_source_files(),
        'API Key': check_api_key(),
        '文档文件': check_documentation(),
        '模块导入': test_import()
    }
    
    # 生成报告
    generate_report(results)
    
    # 返回状态码
    return 0 if all(results.values()) else 1


if __name__ == '__main__':
    sys.exit(main())
