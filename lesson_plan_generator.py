# lesson_plan_generator.py
from openai import OpenAI
import streamlit as st

# 从 Streamlit secrets 获取 DeepSeek API Key
api_key = st.secrets.get("DEEPSEEK_API_KEY", "").strip()

# 正确写法：base_url 必须加 /v1
deepseek_client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com/v1"
)

def generate_lesson_plan_with_text_chunks(
    title, subject, grade, duration,
    key_vocab, text_chunks,
    teaching_goals="", teaching_focus="", teaching_difficulties="",
    lesson_type="新授课"
):
    user_prompt = f"""
【核心指令】
你是一位特级教师，需根据我提供的所有信息，生成一节可立即执行的、以学生为中心的精品课教案。**严格引用我后续上传的教材内容**，并据此调整所有教学环节和例题。忽略教材视为失败。

【基础信息】
*   课程名称: {title}
*   授课类型: {lesson_type}
*   学科: {subject}
*   年级: {grade}
*   课时: {duration}
*   关键词汇: {key_vocab}
*   教学目标: {teaching_goals}
*   教学重点: {teaching_focus}
*   教学难点: {teaching_difficulties}

【核心规则与禁区】
1.  **授课类型逻辑**：
    *   若为“新授课”：必须有“知识回顾”环节（需引用教材上一章节内容）。
    *   若为“复习课”：**删除“知识回顾”**，强化“例题促学”和“错因反思”。
    *   若为“习题课”：少量回顾核心知识，大量设计分层习题（普通生+尖子生）。
2.  **教案结构**：严格按顺序生成以下八大板块，不得增减调换：
    *   一、教学目标（仅含“知识与技能”“过程与方法”，须可验证）
    *   二、教学重难点（若已提供，则直接使用）
    *   三、易错点提示（预判具体思维误区，如“误将分母含x的方程当整式方程”）
    *   四、教学过程（**详见下文的【教学过程模板】**）
    *   五、课堂小结（用提问引导学生总结）
    *   六、布置作业（**分层设计**：※基础巩固题 / ☆拓展探究题，用任务描述而非页码）
    *   七、板书设计（结构化表格，含【辅助简笔画】描述、【红笔标注区】和【黑板快照】）
    *   八、思维导图（如适用则给出）
3.  **语言与风格**：
    *   使用初中生能懂的生动语言（如“把话变成式子”而非“数学建模”）。
    *   不是老师一句，学生一句的对话式，这是老师的教案
    *   在关键话术后插入简短`[动作：...]`指令。
    *   禁止出现“情感态度与价值观”、你的角色自述、具体教材页码、不正式标题、课后留白。

【教学过程模板 - 根据授课类型动态选择】

if lesson_type == "新授课":
    
    1. 知识回顾（--- 约X分钟 ---） *必须引用教材上一章节内容*
    2. 情景引学（--- 约X分钟 ---）
    3. 探究真学（--- 约X分钟 ---）
    4. 明理深学（--- 约X分钟 ---）
    5. 例题促学（--- 约X分钟 ---）
    6. 小结思考（--- 约X分钟 ---）

elif lesson_type == "复习课":
    
    1. 目标导学（--- 约X分钟 ---）
    2. 体系构建（--- 约X分钟 ---）
    3. 典例深化（--- 约X分钟 ---） *剖析课本或作业中的例题，讲联系、易错点和方法*
    4. 疑点突破（--- 约X分钟 ---） *解决共性问题和疑难杂症*
    5. 综合应用（--- 约X分钟 ---）
    6. 反思提升（--- 约X分钟 ---）
    
elif lesson_type == "习题课":
    
    1. 目标定向（--- 约X分钟 ---） *明确训练重点和技能*
    2. 基础热身（--- 约X分钟 ---） *设计3-5道核心知识热身题*
    3. 典例悟法（--- 约X分钟 ---） *精讲一道题，展示“审题-分析-解答-回顾”全过程，提炼解题模型*
    4. 合作探学（--- 约X分钟 ---） *设计有梯度的题组（基础+中档），组织小组合作*
    5. 展评提炼（--- 约X分钟 ---） *组织学生讲题，师生共评，关注多解与错误*
    6. 巩固拓展（--- 约X分钟 ---） *含“当堂检测题”和“尖子生挑战题”*
    

【最终执行】
请基于以上所有指令，尤其是我后续上传的教材文本，开始生成教案内容。不要有任何前置回复。必须结合我上传的教材，就是以下分块上传的内容来生成
"""

    # messages 中加入所有文本块
    user_content = [{"type": "text", "text": user_prompt}]
    for chunk in text_chunks:
        user_content.append({"type": "text", "text": chunk})

    messages = [
        {"role": "system", "content": "你是一名专业中文AI教师助手。"},
        {"role": "user", "content": user_content}
    ]

    resp = deepseek_client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )

    return resp.choices[0].message.content





