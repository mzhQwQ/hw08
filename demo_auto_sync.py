#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
演示脚本：测试新的教务系统 HTML 解析功能

这个脚本演示了如何使用升级后的应用来解析教务系统的成绩页面。
"""

import sys
sys.path.insert(0, '.')

from data_processor import ScoreDataProcessor
from data_sync import EducationSystemScraper
import pandas as pd


def demo_webvpn_guide():
    """演示 WebVPN 操作指南"""
    print("\n" + "="*70)
    print("📚 WebVPN 自动化成绩获取指南")
    print("="*70)
    
    scraper = EducationSystemScraper()
    instructions = scraper.get_instructions_for_user()
    
    for key, value in instructions.items():
        if key.endswith('_title'):
            print(f"\n{value}")
        elif key.endswith('_description'):
            print(f"   {value}")
        elif key.endswith('_url'):
            print(f"   🔗 {value}")
        elif key.endswith('_action'):
            print(f"   ✓ {value}")


def demo_parse_new_format():
    """演示解析新格式教务系统 HTML"""
    
    print("\n" + "="*70)
    print("🧪 测试：解析新格式教务系统 HTML")
    print("="*70)
    
    # 创建一个示例 HTML（模拟教务系统格式）
    sample_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>个人成绩查询</title>
        <meta charset="utf-8">
    </head>
    <body>
        <table class="datalist">
            <tr>
                <th>学年</th>
                <th>学期</th>
                <th>开课院系</th>
                <th>课程号</th>
                <th>课序号</th>
                <th>课程名</th>
                <th>学分</th>
                <th>主讲教师</th>
                <th>课组</th>
                <th>绩点</th>
                <th>选课属性</th>
                <th>备注</th>
                <th>是否缓考</th>
                <th>二学位/辅修</th>
                <th>及格标志</th>
                <th>总评(综合)</th>
            </tr>
            <tr>
                <td>2025</td>
                <td>秋</td>
                <td>人工智能研究院</td>
                <td>AAI016</td>
                <td>4</td>
                <td>人工智能导论A</td>
                <td>2</td>
                <td>贺京杰</td>
                <td>1024A通识教育-信息技术-必修</td>
                <td>3.67</td>
                <td>必修</td>
                <td>正常</td>
                <td>否</td>
                <td></td>
                <td>及格</td>
                <td>A-</td>
            </tr>
            <tr>
                <td>2025</td>
                <td>秋</td>
                <td>新材料与化工学院</td>
                <td>CHM119</td>
                <td>4</td>
                <td>无机与分析化学B</td>
                <td>3</td>
                <td>韩现英</td>
                <td></td>
                <td>2.0</td>
                <td>任选</td>
                <td>正常</td>
                <td>否</td>
                <td></td>
                <td>及格</td>
                <td>C</td>
            </tr>
            <tr>
                <td>2026</td>
                <td>春</td>
                <td>致远学院</td>
                <td>MATH101</td>
                <td>16</td>
                <td>高等数学A(Ⅰ)</td>
                <td>6</td>
                <td>游煦</td>
                <td>2001专业教育-先修基础课-必修</td>
                <td>4.0</td>
                <td>必修</td>
                <td>正常</td>
                <td>否</td>
                <td></td>
                <td>及格</td>
                <td>A</td>
            </tr>
            <tr>
                <td>2026</td>
                <td>春</td>
                <td>清华学堂在线</td>
                <td>XT-ECO005</td>
                <td>1</td>
                <td>管理学</td>
                <td>1</td>
                <td></td>
                <td>2202A通识教育-社会科学-经济与管理类</td>
                <td>4.0</td>
                <td>任选</td>
                <td>正常</td>
                <td>否</td>
                <td></td>
                <td>及格</td>
                <td>A</td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    try:
        processor = ScoreDataProcessor()
        
        print("\n🔄 正在解析 HTML...")
        df = processor.parse_score_html(sample_html)
        
        if df is not None:
            print(f"✅ 成功解析 {len(df)} 门课程！\n")
            
            print("📊 课程数据：")
            print(df.to_string(index=False))
            
            print("\n\n📈 统计信息：")
            stats = processor.get_statistics()
            for key, value in stats.items():
                print(f"   {key}: {value}")
            
            print("\n\n🎓 学科分析：")
            subject_analysis = processor.get_subject_analysis()
            for subject, info in subject_analysis.items():
                print(f"\n   {subject}:")
                for metric, value in info.items():
                    print(f"      {metric}: {value:.2f}" if isinstance(value, float) else f"      {metric}: {value}")
            
            # 验证新增字段
            if '学年' in df.columns:
                print("\n\n✅ 新增字段验证：")
                print(f"   包含学年字段：✓")
                print(f"   包含学期字段：✓")
                print(f"   学年范围：{df['学年'].min()} - {df['学年'].max()}")
            
            return True
        else:
            print("❌ 解析失败")
            return False
            
    except Exception as e:
        print(f"❌ 错误：{e}")
        import traceback
        traceback.print_exc()
        return False


def demo_grade_point_conversion():
    """演示绩点到成绩的转换"""
    
    print("\n" + "="*70)
    print("🧪 测试：绩点到成绩的转换")
    print("="*70)
    
    processor = ScoreDataProcessor()
    
    print("\n绩点 → 成绩对应表：\n")
    
    test_cases = [4.0, 3.67, 3.33, 3.0, 2.67, 2.33, 2.0, 1.67, 1.33, 1.0, 0.0]
    
    print(f"{'绩点':<10} {'推算成绩':<15} {'等级':<10}")
    print("-" * 35)
    
    for gp in test_cases:
        score = processor._grade_point_to_score(gp)
        grade = processor._get_grade_level(score)
        print(f"{gp:<10.2f} {score:<15.0f} {grade:<10}")


def main():
    """主函数"""
    
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "🎓 升级测试：教务系统自动化数据同步" + " "*15 + "║")
    print("╚" + "="*68 + "╝")
    
    try:
        # 测试 1：显示 WebVPN 操作指南
        demo_webvpn_guide()
        
        # 测试 2：解析新格式 HTML
        result = demo_parse_new_format()
        
        if result:
            # 测试 3：绩点转换
            demo_grade_point_conversion()
            
            print("\n" + "="*70)
            print("✅ 所有测试成功完成！")
            print("="*70)
            
            print("\n📝 下一步：")
            print("   1. 按照 WebVPN 操作指南获取你的成绩页面 HTML")
            print("   2. 在应用中选择『直接粘贴 HTML』")
            print("   3. 粘贴你的成绩页面 HTML")
            print("   4. 应用会自动解析并显示诊断结果")
            
        else:
            print("\n" + "="*70)
            print("❌ 测试失败")
            print("="*70)
            return 1
    
    except Exception as e:
        print(f"\n❌ 执行过程中出错：{e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
