"""
工具函数模块
包含各种通用的辅助函数
"""
import json
import re
from typing import Any, Dict, List, Optional


def calculate_gpa(score: Any) -> float:
    """
    根据分数、等级或二级分制计算绩点
    
    Args:
        score: 分数（0-100）或等级（A, A-, P, F, 等）
    
    Returns:
        绩点（0-4.0）
    """
    # 尝试将输入转换为浮点数（百分制）
    try:
        val = float(score)
        if val >= 90:
            return 4.00
        elif val >= 86:
            return 3.67
        elif val >= 83:
            return 3.33
        elif val >= 80:
            return 3.00
        elif val >= 76:
            return 2.67
        elif val >= 73:
            return 2.33
        elif val >= 70:
            return 2.00
        elif val >= 66:
            return 1.67
        elif val >= 63:
            return 1.33
        elif val >= 60:
            return 1.00
        else:
            return 0.00
    except (ValueError, TypeError):
        pass

    # 无法直接转换为浮点数，处理为字符串（字母记分制或二级分制）
    if not isinstance(score, str):
        score = str(score)
    
    grade = score.strip().upper()
    
    # 字母记分制映射
    grade_map = {
        'A': 4.00,
        'A-': 3.67,
        'B+': 3.33,
        'B': 3.00,
        'B-': 2.67,
        'C+': 2.33,
        'C': 2.00,
        'C-': 1.67,
        'D+': 1.33,
        'D': 1.00,
        'F': 0.00
    }
    if grade in grade_map:
        return grade_map[grade]
        
    # 二级分制映射
    if grade in ['通过', 'P', 'PASS', '及格']:
        return 3.00
    if grade in ['不通过', 'F', 'FAIL', '不及格']:
        return 0.00
        
    return 0.00


def grade_point_to_score(grade_point: float) -> float:
    """
    从绩点反推成绩分数
    
    对应关系：
    - 4.00 → 95.0
    - 3.67 → 88.0
    - 3.33 → 84.0
    - 3.00 → 81.0
    - 2.67 → 78.0
    - 2.33 → 74.0
    - 2.00 → 71.0
    - 1.67 → 68.0
    - 1.33 → 64.0
    - 1.00 → 61.0
    - 0.00 → 50.0
    
    Args:
        grade_point: 绩点
    
    Returns:
        推算的分数
    """
    if grade_point >= 3.95:
        return 95.0
    elif grade_point >= 3.65:
        return 88.0
    elif grade_point >= 3.30:
        return 84.0
    elif grade_point >= 2.95:
        return 81.0
    elif grade_point >= 2.65:
        return 78.0
    elif grade_point >= 2.30:
        return 74.0
    elif grade_point >= 1.95:
        return 71.0
    elif grade_point >= 1.65:
        return 68.0
    elif grade_point >= 1.30:
        return 64.0
    elif grade_point >= 0.95:
        return 61.0
    else:
        return 50.0  # 不及格的分数代表值


def score_to_grade_level(score: float) -> str:
    """
    根据分数获取等级 (A, A-, B+, B, B-, C+, C, C-, D+, D, F)
    
    Args:
        score: 分数
    
    Returns:
        等级字符串
    """
    if score >= 90:
        return 'A'
    elif score >= 86:
        return 'A-'
    elif score >= 83:
        return 'B+'
    elif score >= 80:
        return 'B'
    elif score >= 76:
        return 'B-'
    elif score >= 73:
        return 'C+'
    elif score >= 70:
        return 'C'
    elif score >= 66:
        return 'C-'
    elif score >= 63:
        return 'D+'
    elif score >= 60:
        return 'D'
    else:
        return 'F'


def calculate_avg_gpa(scores: List[float]) -> float:
    """
    计算平均绩点
    
    Args:
        scores: 分数列表
    
    Returns:
        平均绩点
    """
    if not scores:
        return 0.0
    gpas = [calculate_gpa(score) for score in scores]
    return sum(gpas) / len(gpas)


def calculate_weighted_gpa(scores: List[float], credits: List[float]) -> float:
    """
    计算加权绩点（考虑学分）
    
    Args:
        scores: 分数列表
        credits: 学分列表
    
    Returns:
        加权绩点
    """
    if not scores or not credits or len(scores) != len(credits):
        return 0.0
    
    total_credit = sum(credits)
    if total_credit == 0:
        return 0.0
    
    weighted_sum = sum(calculate_gpa(s) * c for s, c in zip(scores, credits))
    return weighted_sum / total_credit


def clean_text(text: str) -> str:
    """
    清理文本：删除多余空格、换行等
    
    Args:
        text: 原始文本
    
    Returns:
        清理后的文本
    """
    if not isinstance(text, str):
        return str(text)
    
    # 替换多个空格为单个空格
    text = re.sub(r'\s+', ' ', text)
    # 去除首尾空格
    text = text.strip()
    return text


def safe_float(value: Any, default: float = 0.0) -> float:
    """
    安全的字符串转浮点数
    
    Args:
        value: 值（任意类型）
        default: 转换失败时的默认值
    
    Returns:
        转换后的浮点数
    """
    try:
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            return float(clean_text(value))
        return default
    except (ValueError, TypeError):
        return default


def parse_json_response(response_text: str) -> Optional[Dict]:
    """
    从大模型响应中提取 JSON 对象
    
    Args:
        response_text: 大模型返回的文本
    
    Returns:
        解析出的字典，或 None
    """
    try:
        # 尝试直接解析
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass
    
    # 尝试从代码块中提取 JSON
    json_match = re.search(r'```json\n(.*?)\n```', response_text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass
    
    # 尝试从 { 到 } 提取 JSON
    match = re.search(r'\{.*\}', response_text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    
    return None


def format_diagnosis_report(text: str) -> str:
    """
    格式化诊断报告，确保 Markdown 格式正确
    
    Args:
        text: 原始报告文本
    
    Returns:
        格式化后的报告
    """
    if not text:
        return "暂无诊断报告"
    
    # 确保换行符处理正确
    text = text.replace('\\n', '\n')
    
    return text


def highlight_key_metrics(metrics: Dict[str, float]) -> Dict[str, str]:
    """
    给关键指标添加可视化标记
    
    Args:
        metrics: 指标字典
    
    Returns:
        添加标记的指标字典
    """
    highlighted = {}
    for key, value in metrics.items():
        if value >= 0.85:
            highlighted[key] = f"🟢 {key}: {value:.2f}"
        elif value >= 0.70:
            highlighted[key] = f"🟡 {key}: {value:.2f}"
        else:
            highlighted[key] = f"🔴 {key}: {value:.2f}"
    return highlighted


if __name__ == '__main__':
    # 测试工具函数
    print("GPA 计算测试:")
    print(f"  95 分 -> {calculate_gpa(95)} 绩点 (期望: 4.0)")
    print(f"  88 分 -> {calculate_gpa(88)} 绩点 (期望: 3.67)")
    print(f"  85 分 -> {calculate_gpa(85)} 绩点 (期望: 3.33)")
    print(f"  80 分 -> {calculate_gpa(80)} 绩点 (期望: 3.0)")
    print(f"  78 分 -> {calculate_gpa(78)} 绩点 (期望: 2.67)")
    print(f"  '通过' -> {calculate_gpa('通过')} 绩点 (期望: 3.0)")
    print(f"  'A-' -> {calculate_gpa('A-')} 绩点 (期望: 3.67)")
    
    print("\n平均 GPA 测试:")
    scores = [85, 90, 75, 88]
    print(f"  分数: {scores} -> 平均 GPA: {calculate_avg_gpa(scores):.2f}")
    
    print("\n加权 GPA 测试:")
    scores = [85, 90, 75, 88]
    credits = [4, 3, 3, 4]
    print(f"  分数: {scores}, 学分: {credits} -> 加权 GPA: {calculate_weighted_gpa(scores, credits):.2f}")

