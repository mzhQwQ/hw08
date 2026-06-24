# -*- coding: utf-8 -*-
"""
数据同步模块 - 从教务系统自动获取成绩数据

功能：
1. 生成 WebVPN 认证链接
2. 处理会话管理和自动登录
3. 自动注入 JS 脚本获取全部成绩
4. 解析并缓存成绩数据
"""

import requests
import re
from typing import Optional, Dict, List, Tuple
from urllib.parse import urljoin
import json
from datetime import datetime
import hashlib


class WebVPNAuthenticator:
    """WebVPN 认证管理器"""
    
    def __init__(self):
        """初始化认证器"""
        self.vpn_hostname = "webvpn.bipt.edu.cn"
        self.vpn_protocol = "https"
        
        # 编码的应用主机名
        self.vpn_app_hostname = "77726476706e69737468656265737421fae05b84693261406a468ca88d1b203b"
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_login_url(self) -> str:
        """获取 WebVPN 登录入口 URL
        
        Returns:
            str: 完整的登录 URL
        """
        return (f"{self.vpn_protocol}://{self.vpn_hostname}/https/"
                f"{self.vpn_app_hostname}/academic/login/bipt/loginIds6.jsp")
    
    def get_score_page_url(self) -> str:
        """获取成绩查询页面 URL
        
        Returns:
            str: 完整的成绩查询 URL
        """
        return (f"{self.vpn_protocol}://{self.vpn_hostname}/https/"
                f"{self.vpn_app_hostname}/academic/manager/score/studentOwnScore.do")
    
    def get_fetch_all_scores_script(self) -> str:
        """获取强制拉取全部成绩的 JavaScript 注入脚本
        
        Returns:
            str: JavaScript 代码
        """
        return """
        // 自动化获取全部学年学期的成绩
        (function() {
            console.log('开始获取全部成绩...');
            
            // 设置学年和学期为空，表示查询全部
            var yearSelect = document.querySelector('select[name="year"]');
            var termSelect = document.querySelector('select[name="term"]');
            
            if (yearSelect && termSelect) {
                yearSelect.value = "";
                termSelect.value = "";
                console.log('已设置查询条件为全部学年学期');
                
                // 提交表单
                var form = document.forms["form1"];
                if (form) {
                    form.submit();
                    console.log('表单已提交');
                }
            } else {
                console.error('无法找到选择框');
            }
        })();
        """


class EducationSystemScraper:
    """教务系统成绩爬虫
    
    用于自动从教务系统获取成绩数据
    """
    
    def __init__(self):
        """初始化爬虫"""
        self.authenticator = WebVPNAuthenticator()
        self.session = self.authenticator.session
        self.cache_file = "score_cache.json"
    
    def get_instructions_for_user(self) -> Dict[str, str]:
        """为用户生成详细的操作指南
        
        Returns:
            Dict: 包含步骤和 URL 的指南
        """
        return {
            "step_1_title": "📍 第 1 步：访问 WebVPN 登录入口",
            "step_1_description": "点击以下链接进入清华大学教务系统（需要清华账号）",
            "step_1_url": self.authenticator.get_login_url(),
            "step_1_action": "使用清华账号密码登录",
            
            "step_2_title": "📍 第 2 步：自动跳转到成绩查询",
            "step_2_description": "登录完成后，系统会自动跳转到成绩查询页面",
            "step_2_url": self.authenticator.get_score_page_url(),
            "step_2_action": "等待页面加载完成",
            
            "step_3_title": "📍 第 3 步：执行自动化脚本（可选）",
            "step_3_description": "在浏览器控制台（F12 → Console）执行以下脚本，强制获取全部学年学期的成绩",
            "step_3_script": self.authenticator.get_fetch_all_scores_script(),
            "step_3_action": "复制脚本到浏览器控制台并执行",
            
            "step_4_title": "📍 第 4 步：复制成绩页面 HTML",
            "step_4_description": "页面加载完成后，按 Ctrl+A 全选页面，Ctrl+C 复制",
            "step_4_action": "复制整个页面 HTML 代码",
            
            "step_5_title": "📍 第 5 步：上传到应用",
            "step_5_description": "在应用的『上传成绩』页面，选择『直接粘贴 HTML』选项",
            "step_5_action": "粘贴复制的 HTML 代码，应用会自动解析",
        }
    
    def extract_scores_from_page_html(self, html_content: str) -> List[Dict]:
        """从成绩查询页面 HTML 中提取成绩数据
        
        Args:
            html_content: 成绩查询页面的 HTML 内容
            
        Returns:
            List[Dict]: 成绩数据列表
        """
        scores = []
        
        # 使用正则表达式提取表格行
        # 查找所有 <tr> 标签内的课程数据
        rows = re.findall(r'<tr>\s*(?:<td[^>]*>.*?</td>\s*)+</tr>', html_content, re.DOTALL)
        
        if not rows:
            raise ValueError("未能找到成绩数据表格")
        
        # 跳过表头行（包含 "学年" 等标题的行）
        for row in rows[1:]:
            cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
            
            if len(cells) >= 16:
                try:
                    # 清理单元格内容
                    course_data = {
                        'year': cells[0].strip(),  # 学年
                        'term': cells[1].strip(),  # 学期
                        'department': cells[2].strip(),  # 开课院系
                        'course_code': cells[3].strip(),  # 课程号
                        'course_seq': cells[4].strip(),  # 课序号
                        'course_name': cells[5].strip(),  # 课程名
                        'credits': self._parse_float(cells[6].strip()),  # 学分
                        'instructor': cells[7].strip(),  # 主讲教师
                        'course_group': cells[8].strip(),  # 课组
                        'grade_point': self._parse_float(cells[9].strip()),  # 绩点
                        'course_property': cells[10].strip(),  # 选课属性
                        'remark': cells[11].strip(),  # 备注
                        'is_makeup': cells[12].strip(),  # 是否缓考
                        'double_degree': cells[13].strip(),  # 二学位/辅修
                        'pass_flag': cells[14].strip(),  # 及格标志
                        'final_grade': cells[15].strip(),  # 总评(综合)
                    }
                    
                    # 计算成绩分数（从绩点反推）
                    score = self._grade_point_to_score(course_data['grade_point'])
                    course_data['score'] = score
                    
                    scores.append(course_data)
                    
                except (IndexError, ValueError) as e:
                    print(f"警告：解析行数据时出错 - {e}")
                    continue
        
        return scores
    
    @staticmethod
    def _parse_float(value: str) -> float:
        """安全地将字符串转换为浮点数
        
        Args:
            value: 字符串值
            
        Returns:
            float: 浮点数，如果无法转换则返回 0
        """
        try:
            return float(value.strip())
        except ValueError:
            return 0.0
    
    @staticmethod
    def _grade_point_to_score(grade_point: float) -> float:
        """从绩点反推成绩分数（粗略估计）
        
        绩点到分数的大致对应关系：
        - 4.0 → 90-100
        - 3.7 → 87-89
        - 3.3 → 83-86
        - 3.0 → 80-82
        - 2.7 → 77-79
        - 2.3 → 73-76
        - 2.0 → 70-72
        - 1.7 → 67-69
        - 1.3 → 63-66
        - 1.0 → 60-62
        
        Args:
            grade_point: 绩点
            
        Returns:
            float: 估计的分数
        """
        if grade_point >= 4.0:
            return 95.0
        elif grade_point >= 3.7:
            return 88.0
        elif grade_point >= 3.3:
            return 84.0
        elif grade_point >= 3.0:
            return 81.0
        elif grade_point >= 2.7:
            return 78.0
        elif grade_point >= 2.3:
            return 74.0
        elif grade_point >= 2.0:
            return 71.0
        elif grade_point >= 1.7:
            return 68.0
        elif grade_point >= 1.3:
            return 64.0
        elif grade_point >= 1.0:
            return 61.0
        else:
            return 0.0
    
    def cache_scores(self, scores: List[Dict]) -> None:
        """缓存成绩数据到本地文件
        
        Args:
            scores: 成绩数据列表
        """
        try:
            cache_data = {
                'timestamp': datetime.now().isoformat(),
                'scores': scores,
                'count': len(scores),
            }
            
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 成绩已缓存到 {self.cache_file}（{len(scores)} 门课程）")
        except Exception as e:
            print(f"⚠️ 缓存失败：{e}")
    
    def load_cached_scores(self) -> Optional[List[Dict]]:
        """从缓存文件加载成绩数据
        
        Returns:
            List[Dict]: 缓存的成绩数据，如果不存在则返回 None
        """
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
                return cache_data.get('scores', [])
        except FileNotFoundError:
            return None
        except Exception as e:
            print(f"⚠️ 读取缓存失败：{e}")
            return None


def main():
    """演示脚本"""
    
    scraper = EducationSystemScraper()
    
    print("=" * 70)
    print("🎓 智能学业状态诊断助手 - 教务系统数据自动同步")
    print("=" * 70)
    
    # 显示用户操作指南
    instructions = scraper.get_instructions_for_user()
    
    print("\n📚 操作指南：\n")
    for key, value in instructions.items():
        if key.endswith('_title'):
            print(f"\n{value}")
        elif key.endswith('_description'):
            print(f"   {value}")
        elif key.endswith('_url'):
            print(f"   🔗 URL: {value}")
        elif key.endswith('_script'):
            print(f"   📝 脚本:\n")
            for line in value.split('\n'):
                if line.strip():
                    print(f"      {line}")
        elif key.endswith('_action'):
            print(f"   ✓ {value}")
    
    print("\n" + "=" * 70)
    print("📝 说明：")
    print("   1. 这是一个半自动化流程")
    print("   2. 需要清华账号登录才能访问教务系统")
    print("   3. 可选的 JS 注入脚本可强制获取全部学年成绩")
    print("   4. 获取到成绩页面后，复制 HTML 并粘贴到应用")
    print("   5. 应用会自动解析并存储成绩数据")
    print("=" * 70)


if __name__ == '__main__':
    main()
