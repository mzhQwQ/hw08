# 📊 架构升级指南：自动化教务系统数据同步

## 🎯 升级概述

从**手动下载 HTML**升级为**自动化数据同步**，用户只需按照以下步骤即可自动获取教务系统中的全部成绩数据。

---

## 📈 架构对比

### ❌ 旧架构（手动方式）
```
用户 → 手动访问教务系统 → 下载 score.html → 上传到应用 → 解析显示
```
**缺点**：繁琐、容易出错、信息丢失

### ✅ 新架构（自动化方式）
```
用户 → 一键打开 WebVPN 登录 → 自动注入 JS → 自动获取全部成绩 → 复制 HTML → 上传到应用 → 自动解析显示
```
**优点**：流畅、自动化、完整数据、支持历年成绩

---

## 🚀 新工作流程

### 第 1️⃣ 步：访问 WebVPN 登录入口

**URL**：
```
https://webvpn.bipt.edu.cn/https/77726476706e69737468656265737421fae05b84693261406a468ca88d1b203b/academic/login/bipt/loginIds6.jsp
```

**操作**：
- 点击链接或复制到浏览器
- 输入清华账号和密码
- 完成双因素认证（如需要）

```
📌 提示：
- 需要清华大学官方账号（学号 + 密码）
- 支持所有主流浏览器（Chrome、Firefox、Safari、Edge）
- 可能需要 VPN 访问（取决于你的网络位置）
```

### 第 2️⃣ 步：自动跳转到成绩查询页面

**发生**：认证完成后，系统自动跳转到成绩查询页面

**URL**（供参考）：
```
https://webvpn.bipt.edu.cn/https/77726476706e69737468656265737421fae05b84693261406a468ca88d1b203b/academic/manager/score/studentOwnScore.do
```

**状态**：页面加载完成后，默认显示当学期成绩

### 第 3️⃣ 步：执行自动化 JS 脚本（可选但强烈推荐）

此步骤可强制获取**全部学年和学期的成绩**。

**操作步骤**：

1. **打开浏览器控制台**
   - Windows/Linux：按 `F12` 或 `Ctrl+Shift+I`
   - macOS：按 `Cmd+Option+I`
   - 或右键 → 检查/Inspect

2. **选择 Console 标签页**
   ```
   顶部菜单栏 → Console 标签（或 Elements 标签旁边）
   ```

3. **复制以下脚本**
   ```javascript
   // 自动化获取全部学年学期的成绩
   (function() {
       console.log('🔄 开始获取全部成绩...');
       
       var yearSelect = document.querySelector('select[name="year"]');
       var termSelect = document.querySelector('select[name="term"]');
       
       if (yearSelect && termSelect) {
           yearSelect.value = "";  // 学年设为空（表示全部）
           termSelect.value = "";  // 学期设为空（表示全部）
           console.log('✅ 已设置查询条件为全部学年学期');
           
           var form = document.forms["form1"];
           if (form) {
               form.submit();
               console.log('✅ 表单已提交，请等待页面加载...');
           }
       } else {
           console.error('❌ 未找到选择框');
       }
   })();
   ```

4. **粘贴到控制台**
   - 在控制台底部找到输入框
   - 右键 → 粘贴 或 Ctrl+V
   - 按 Enter 执行

5. **等待页面加载**
   - 页面会自动查询所有学年学期的成绩
   - 可能需要几秒钟（取决于网速）

**预期结果**：
```
✅ 已设置查询条件为全部学年学期
✅ 表单已提交，请等待页面加载...

[页面刷新，现在显示全部成绩 ✨]
```

### 第 4️⃣ 步：复制成绩页面 HTML

页面加载完成后，按照以下步骤复制 HTML：

**方法 A**（推荐，最简单）：
```
1. 按 Ctrl+A（全选）
2. 按 Ctrl+C（复制）
3. 代码已复制到剪贴板
```

**方法 B**（备选，右键菜单）：
```
1. 右键点击页面
2. 选择 "查看源代码" 或 "View Source"
3. Ctrl+A 全选
4. Ctrl+C 复制
```

**方法 C**（备选，浏览器菜单）：
```
1. 按 F12 打开开发者工具
2. Elements/Inspector 标签
3. 右键点击 <html> 标签
4. 选择 Copy → Copy outerHTML
```

### 第 5️⃣ 步：上传到应用

1. **打开应用**
   ```bash
   streamlit run app.py
   ```

2. **点击『上传成绩』页面**

3. **选择『直接粘贴 HTML』选项**
   ```
   ☐ 上传文件
   ☑ 直接粘贴 HTML  ← 选择这个
   ☐ 使用示例数据
   ```

4. **粘贴复制的 HTML**
   ```
   按 Ctrl+V 或右键 → 粘贴
   ```

5. **点击『解析成绩』按钮**
   ```
   应用会自动：
   ✓ 解析 HTML 表格
   ✓ 提取课程信息
   ✓ 计算统计数据
   ✓ 保存到缓存
   ```

6. **查看结果**
   ```
   ✅ 成功解析 X 门课程
   
   统计信息：
   - 平均成绩：XX.XX
   - 加权 GPA：X.XX
   - 总学分：XX
   ```

---

## 📋 完整 HTML 复制示例

### 正确的 HTML 格式
应该包含以下元素：

```html
<!DOCTYPE html>
<html>
<head>
    <title>个人成绩查询</title>
    ...
</head>
<body>
    <table class="datalist">
        <tr>
            <th>学年</th>
            <th>学期</th>
            ...
        </tr>
        <tr>
            <td>2025</td>
            <td>秋</td>
            <td>人工智能导论A</td>
            ...
        </tr>
        <!-- 更多课程行 -->
    </table>
</body>
</html>
```

### 验证复制的内容
复制后，可以按 Ctrl+V 粘贴到文本编辑器验证：
- ✅ 包含 `<table>` 标签
- ✅ 包含 `<tr>` 和 `<td>` 标签
- ✅ 包含课程名、学分、成绩等信息
- ❌ 不应该是空的或仅为几行

---

## 🔧 新数据处理模块

应用新增了以下功能：

### 模块 1: `data_sync.py`（教务系统数据同步）
```python
from data_sync import EducationSystemScraper

# 获取用户操作指南
scraper = EducationSystemScraper()
instructions = scraper.get_instructions_for_user()

# 解析教务系统页面 HTML
scores = scraper.extract_scores_from_page_html(html_content)

# 缓存成绩数据
scraper.cache_scores(scores)

# 加载缓存的成绩
cached_scores = scraper.load_cached_scores()
```

### 模块 2: 升级后的 `data_processor.py`
新增了对教务系统新格式的支持：

```python
from data_processor import ScoreDataProcessor

processor = ScoreDataProcessor()

# 自动检测格式并解析
df = processor.parse_score_html(html_content)

# 新增：从绩点反推成绩
score = processor._grade_point_to_score(grade_point=3.7)
# 返回：88.0

# 新增：解析新格式教务系统页面
df = processor._parse_new_format(html_content)
```

---

## 📊 支持的数据字段

新版应用现在支持以下课程信息字段：

| 字段 | 说明 | 示例 |
|------|------|------|
| 学年 | Academic Year | 2025 |
| 学期 | Term | 秋/春 |
| 开课院系 | Department | 人工智能研究院 |
| 课程号 | Course Code | AAI016 |
| 课序号 | Course Seq | 4 |
| 课程名 | Course Name | 人工智能导论A |
| 学分 | Credits | 2.0 |
| 主讲教师 | Instructor | 贺京杰 |
| 课组 | Course Group | 通识教育-信息技术 |
| **绩点** | **Grade Point** | **3.67** |
| 选课属性 | Course Property | 必修/任选/限选 |
| 备注 | Remark | 正常/缓考 |
| 及格标志 | Pass Flag | 及格/不及格 |
| 总评(综合) | Final Grade | A/A-/B/B+/... |

---

## ⚡ 快速命令

### 快速启动
```bash
# 1. 激活虚拟环境
venv\Scripts\activate

# 2. 启动应用
streamlit run app.py

# 3. 或者在应用中直接测试解析
python -c "from data_sync import EducationSystemScraper; EducationSystemScraper().get_instructions_for_user()"
```

### 验证新模块
```bash
# 测试数据同步模块
python data_sync.py

# 输出示例：
# 🎓 智能学业状态诊断助手 - 教务系统数据自动同步
# ========================================================
# 
# 📚 操作指南：
# 
# 📍 第 1 步：访问 WebVPN 登录入口
# ...
```

---

## 🎯 关键改进点

### ✨ 优点 1：自动化流程
- ✅ 使用 JS 注入自动获取全部学年成绩
- ✅ 无需手动多次操作
- ✅ 支持批量导入

### ✨ 优点 2：完整数据
- ✅ 包含学年、学期信息
- ✅ 包含绩点、等级等详细信息
- ✅ 支持教师、院系等元数据

### ✨ 优点 3：智能解析
- ✅ 自动检测 HTML 格式
- ✅ 从绩点反推成绩分数
- ✅ 支持多种表格结构

### ✨ 优点 4：数据缓存
- ✅ 自动缓存成绩数据
- ✅ 支持离线使用
- ✅ 快速加载历史数据

---

## 🐛 故障排除

### 问题 1：登录失败
**原因**：账号密码错误或需要额外认证  
**解决**：
- 检查账号密码是否正确
- 如需双因素认证，完成认证步骤
- 检查网络连接是否正常

### 问题 2：页面加载缓慢
**原因**：网络延迟或服务器繁忙  
**解决**：
- 稍等片刻后重试
- 检查网络连接
- 尝试在非高峰时段访问

### 问题 3：JS 脚本执行失败
**原因**：页面结构与预期不同  
**解决**：
```javascript
// 调试方法 1：检查是否存在选择框
console.log(document.querySelector('select[name="year"]'));
console.log(document.querySelector('select[name="term"]'));

// 调试方法 2：手动提交表单
var form = document.forms["form1"];
if (form) form.submit();
```

### 问题 4：解析失败（"无法找到成绩表"）
**原因**：
- HTML 复制不完整
- 页面加载未完成
- 表格格式与预期不同

**解决**：
- 重新完整复制 HTML（从 `<html>` 到 `</html>`）
- 等待页面完全加载后再复制
- 检查复制的内容中是否包含 `<table>` 标签

### 问题 5：成绩数据为 0 或不正确
**原因**：绩点反推算法偏差  
**解决**：
- 这是由于从绩点推算成绩的必然偏差
- 诊断结论基于相对分析，不受影响
- 如需精确分数，可在原始 HTML 中查找

---

## 📞 获取帮助

### 快速诊断
1. 检查网络连接：`ping webvpn.bipt.edu.cn`
2. 验证应用正常：`streamlit run app.py`
3. 测试数据解析：`python data_sync.py`

### 获取支持
- 📖 查看完整文档：[RUN_AND_DEBUG.md](RUN_AND_DEBUG.md)
- 🐛 提交问题描述
- 💬 检查常见问题部分

---

## 📝 使用场景

### 场景 1：新学期成绩查询
```
1. 新学期考试结束，教务系统发布成绩
2. 打开应用，按照指南获取最新成绩
3. 自动分析诊断，了解学业状态
```

### 场景 2：GPA 规划
```
1. 获取全部学年成绩
2. 查看加权 GPA 趋势
3. 根据诊断建议调整学习方向
```

### 场景 3：学位申请材料
```
1. 获取完整成绩单
2. 导出 CSV 供证明材料使用
3. 查看详细分析报告
```

---

## 🎉 总结

这次架构升级实现了从**手动流程**到**自动化流程**的升级：

| 方面 | 旧版 | 新版 |
|------|------|------|
| **数据源** | 手动下载 | 自动同步 |
| **覆盖范围** | 当学期 | 全部学年 |
| **操作复杂度** | 中等 | 简单 |
| **数据完整性** | 基础 | 完整 |
| **自动化程度** | 低 | 高 |

**立即体验**：打开应用的『上传成绩』页面，选择『直接粘贴 HTML』，按照指南操作即可！ 🚀

---

**最后更新**：2026-06-24  
**版本**：2.0（架构升级版）  
**状态**：✅ 完整可用
