# lesson_plan_generator.py
from openai import OpenAI
import streamlit as st
import json

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
    teaching_goals="", teaching_focus="", teaching_difficulties=""
):
    user_prompt = f"""
课程名称: {title}
学科: {subject}
年级: {grade}
课时: {duration}

关键词汇: {key_vocab}

教学目标:
{teaching_goals}

教学重点:
{teaching_focus}

教学难点:
{teaching_difficulties}

请根据以上内容生成完整教学方案，包括：
- 对老师填写的教学目标、教学重点、教学难点的评估（如果老师没有填写，则自动生成这几个部分）
- 教学过程（包括五个环节，情景引学，探究真学，明理深学，例题促学，小结思考）
- 尽量使用提供的教材中的例题和内容
- 老师需要关注的课堂反思
请结合我上传的教辅材料文本。
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





