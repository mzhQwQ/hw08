"""
数据处理模块
负责解析 HTML 教务成绩单和数据清洗
"""
import pandas as pd
from bs4 import BeautifulSoup
from typing import Optional, Dict, List
import re
from utils.helpers import clean_text, safe_float, calculate_gpa, grade_point_to_score, score_to_grade_level


class ScoreDataProcessor:
    """教务成绩数据处理器"""
    
    def __init__(self):
        self.df = None
        self.raw_html = None
    
    def parse_score_html(self, html_content: str) -> Optional[pd.DataFrame]:
        """
        解析教务系统导出的 HTML 成绩单
        
        支持多种常见的 HTML 表格结构，包括：
        1. 新版教务系统格式（含学年、学期、绩点等详细信息）
        2. 简化格式（仅含课程名、学分、成绩）
        
        Args:
            html_content: HTML 文件内容
        
        Returns:
            包含课程信息的 DataFrame，如果解析失败则返回 None
        """
        self.raw_html = html_content
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 查找所有表格
            tables = soup.find_all('table', class_='datalist')
            if not tables:
                tables = soup.find_all('table')
            
            if not tables:
                return None
            
            # 使用数据表格（通常是成绩表）
            table = tables[0]
            
            rows = []
            tr_list = table.find_all('tr')
            
            # 检测表格格式
            if len(tr_list) > 0:
                header_tds = tr_list[0].find_all('th')
                if header_tds:
                    # 新版教务系统格式（16+ 列）
                    if len(header_tds) >= 14:
                        return self._parse_new_format(html_content)
            
            # 解析数据行
            for tr in tr_list[1:]:  # 跳过表头
                tds = tr.find_all('td')
                
                if len(tds) < 3:
                    continue
                
                # 检测是否为新格式（含绩点列）
                if len(tds) >= 10:
                    # 新格式：学年、学期、院系、课程号、课序号、课程名、学分、教师、课组、绩点...
                    return self._parse_new_format(html_content)
                
                # 旧格式解析
                course_name = clean_text(tds[0].get_text())
                credits_str = clean_text(tds[1].get_text())
                score_str = clean_text(tds[2].get_text()) if len(tds) > 2 else '0'
                
                # 类型转换
                credits = safe_float(credits_str, 0)
                
                # 支持字母记分制或二级分制
                try:
                    score = float(score_str)
                    gpa = calculate_gpa(score)
                except ValueError:
                    # 如果不是纯数字，可能是等第或通过/不通过等
                    gpa = calculate_gpa(score_str)
                    score = grade_point_to_score(gpa)
                
                # 跳过无效数据
                if not course_name or score < 0 or score > 100:
                    continue
                
                rows.append({
                    '课程名': course_name,
                    '学分': credits,
                    '成绩': score,
                    '绩点': gpa,
                    '等级': score_to_grade_level(score)
                })
            
            if not rows:
                return None
            
            self.df = pd.DataFrame(rows)
            return self.df
        
        except Exception as e:
            print(f"HTML 解析错误: {str(e)}")
            return None
    
    def _parse_new_format(self, html_content: str) -> Optional[pd.DataFrame]:
        """
        解析新版教务系统格式（含学年、学期、绩点等信息）
        
        Args:
            html_content: HTML 文件内容
        
        Returns:
            DataFrame 或 None
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            tables = soup.find_all('table', class_='datalist')
            if not tables:
                tables = soup.find_all('table')
            
            if not tables:
                return None
            
            table = tables[0]
            rows = []
            
            tr_list = table.find_all('tr')
            for tr in tr_list[1:]:  # 跳过表头
                tds = tr.find_all('td')
                
                if len(tds) < 10:
                    continue
                
                try:
                    # 新格式列顺序：
                    # 0:学年, 1:学期, 2:院系, 3:课程号, 4:课序号, 
                    # 5:课程名, 6:学分, 7:教师, 8:课组, 9:绩点, ...
                    
                    course_name = clean_text(tds[5].get_text())
                    credits_str = clean_text(tds[6].get_text())
                    grade_point_str = clean_text(tds[9].get_text())
                    year = clean_text(tds[0].get_text())
                    term = clean_text(tds[1].get_text())
                    
                    # 类型转换
                    credits = safe_float(credits_str, 0)
                    grade_point = safe_float(grade_point_str, 0)
                    
                    # 从绩点推算成绩
                    score = grade_point_to_score(grade_point)
                    
                    # 跳过无效数据
                    if not course_name or score < 0:
                        continue
                    
                    rows.append({
                        '课程名': course_name,
                        '学分': credits,
                        '成绩': score,
                        '绩点': grade_point,
                        '等级': score_to_grade_level(score),
                        '学年': year,
                        '学期': term
                    })
                    
                except (IndexError, ValueError):
                    continue
            
            if not rows:
                return None
            
            self.df = pd.DataFrame(rows)
            return self.df
            
        except Exception as e:
            print(f"新格式解析错误: {str(e)}")
            return None
    
    @staticmethod
    def _grade_point_to_score(grade_point: float) -> float:
        """
        从绩点反推成绩分数 (向后兼容委托函数)
        """
        return grade_point_to_score(grade_point)
    
    def _get_grade_level(self, score: float) -> str:
        """
        根据分数获取等级 (向后兼容委托函数)
        """
        return score_to_grade_level(score)
    
    def get_statistics(self) -> Dict:
        """
        获取成绩统计信息
        
        Returns:
            包含统计信息的字典
        """
        if self.df is None or len(self.df) == 0:
            return {}
        
        scores = self.df['成绩'].tolist()
        credits = self.df['学分'].tolist()
        gpas = self.df['绩点'].tolist()
        
        total_credit = sum(credits)
        
        # 计算加权 GPA
        if total_credit > 0:
            weighted_gpa = sum(g * c for g, c in zip(gpas, credits)) / total_credit
        else:
            weighted_gpa = sum(gpas) / len(gpas) if gpas else 0
        
        return {
            '总课程数': len(self.df),
            '平均成绩': sum(scores) / len(scores) if scores else 0,
            '最高成绩': max(scores) if scores else 0,
            '最低成绩': min(scores) if scores else 0,
            '总学分': total_credit,
            '平均绩点': sum(gpas) / len(gpas) if gpas else 0,
            '加权绩点': weighted_gpa,
            'A 等级课程': len(self.df[self.df['等级'] == 'A']),
            'B 等级课程': len(self.df[self.df['等级'] == 'B']),
            'C 等级课程': len(self.df[self.df['等级'] == 'C']),
            'D 等级课程': len(self.df[self.df['等级'] == 'D']),
            'F 等级课程': len(self.df[self.df['等级'] == 'F'])
        }
    
    def get_subject_analysis(self) -> Dict[str, Dict]:
        """
        分析课程的学科分类
        
        返回按学科分类的成绩分析
        
        Returns:
            按学科分类的分析结果
        """
        if self.df is None or len(self.df) == 0:
            return {}
        
        # 课程分类映射（基于课程名称的关键词）
        math_keywords = ['数学', '微积分', '线性代数', '概率', '统计']
        english_keywords = ['英语', '大学英语', 'English']
        programming_keywords = ['程序', '编程', '计算机', 'Python', 'C++', 'Java', '算法']
        
        subjects = {
            '数学': [],
            '英语': [],
            '专业课': [],
            '其他': []
        }
        
        for _, row in self.df.iterrows():
            course = row['课程名']
            score = row['成绩']
            
            classified = False
            
            for keyword in math_keywords:
                if keyword in course:
                    subjects['数学'].append(score)
                    classified = True
                    break
            
            if not classified:
                for keyword in english_keywords:
                    if keyword in course:
                        subjects['英语'].append(score)
                        classified = True
                        break
            
            if not classified:
                for keyword in programming_keywords:
                    if keyword in course:
                        subjects['专业课'].append(score)
                        classified = True
                        break
            
            if not classified:
                subjects['其他'].append(score)
        
        # 计算每个学科的统计
        result = {}
        for subject, scores in subjects.items():
            if scores:
                result[subject] = {
                    '课程数': len(scores),
                    '平均成绩': sum(scores) / len(scores),
                    '最高成绩': max(scores),
                    '最低成绩': min(scores)
                }
        
        return result
    
    def get_dataframe(self) -> Optional[pd.DataFrame]:
        """获取处理后的 DataFrame"""
        return self.df
    
    def export_csv(self, filepath: str) -> bool:
        """
        导出成绩数据为 CSV 文件
        
        Args:
            filepath: 输出文件路径
        
        Returns:
            成功与否
        """
        try:
            if self.df is None:
                return False
            self.df.to_csv(filepath, index=False, encoding='utf-8-sig')
            return True
        except Exception as e:
            print(f"导出 CSV 失败: {str(e)}")
            return False


def create_sample_html() -> str:
    """
    生成示例 HTML 成绩单（用于测试）
    
    Returns:
        HTML 字符串
    """
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>教务成绩单</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>学生成绩单</h1>
        <table border="1">
            <tr>
                <th>课程名称</th>
                <th>学分</th>
                <th>成绩</th>
            </tr>
            <tr>
                <td>高等数学 I</td>
                <td>4</td>
                <td>87</td>
            </tr>
            <tr>
                <td>线性代数</td>
                <td>3</td>
                <td>92</td>
            </tr>
            <tr>
                <td>大学英语</td>
                <td>4</td>
                <td>78</td>
            </tr>
            <tr>
                <td>数据结构</td>
                <td>4</td>
                <td>88</td>
            </tr>
            <tr>
                <td>Python 程序设计</td>
                <td>3</td>
                <td>91</td>
            </tr>
            <tr>
                <td>数据库原理</td>
                <td>3</td>
                <td>85</td>
            </tr>
            <tr>
                <td>Web 前端技术</td>
                <td>3</td>
                <td>89</td>
            </tr>
            <tr>
                <td>算法设计</td>
                <td>4</td>
                <td>82</td>
            </tr>
            <tr>
                <td>操作系统</td>
                <td>4</td>
                <td>86</td>
            </tr>
            <tr>
                <td>计算机网络</td>
                <td>3</td>
                <td>79</td>
            </tr>
            <tr>
                <td>人工智能导论</td>
                <td>3</td>
                <td>90</td>
            </tr>
            <tr>
                <td>概率论与数理统计</td>
                <td>3</td>
                <td>84</td>
            </tr>
            <tr>
                <td>离散数学</td>
                <td>3</td>
                <td>80</td>
            </tr>
        </table>
    </body>
    </html>
    """
    return html


if __name__ == '__main__':
    # 测试数据处理
    processor = ScoreDataProcessor()
    
    # 使用示例 HTML
    sample_html = create_sample_html()
    df = processor.parse_score_html(sample_html)
    
    if df is not None:
        print("成绩数据:")
        print(df)
        print("\n统计信息:")
        print(processor.get_statistics())
        print("\n学科分析:")
        print(processor.get_subject_analysis())
    else:
        print("解析失败")
