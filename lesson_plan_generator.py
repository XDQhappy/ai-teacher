# lesson_plan_generator.py
from openai import OpenAI
import streamlit as st

api_key = st.secrets.get("DEEPSEEK_API_KEY", "").strip()

deepseek_client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

def generate_lesson_plan(title, subject, grade, duration, key_vocab="", supporting_materials=""):
    user_msg = f"""
课程名称: {title}
学科: {subject}
年级: {grade}
课时: {duration}
关键词汇: {key_vocab}
辅助材料: {supporting_materials}
"""
    messages = [
        {"role": "system", "content": "你是一名专业中文AI教师助手"},
        {"role": "user", "content": user_msg}
    ]
    resp = deepseek_client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        temperature=0.7
    )
    return resp.choices[0].message.content