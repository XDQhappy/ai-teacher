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

def generate_lesson_plan(
    lesson_title, subject, grade, duration,
    key_vocab, supporting_material,
    teaching_goals="", teaching_focus="", teaching_difficulties=""
):
    user_msg = f"""
课程名称：{lesson_title}
学科：{subject}
年级：{grade}
课时：{duration}

关键词：{key_vocab}
辅助材料：{supporting_material}

教学目标：{teaching_goals}
教学重点：{teaching_focus}
教学难点：{teaching_difficulties}


请根据以上内容生成完整教学方案，包括：
- 对老师填写的教学目标、教学重点、教学难点的评估
- 教学过程（包括五个环节，情景引学，探究真学，明理深学，例题促学，小结思考）
- 老师需要关注的课堂反思
    """

    messages = [
        {"role": "system", "content": "你是一名专业中文AI教师助手"},
        {"role": "user", "content": user_msg}
    ]

    # 新版 openai==1.x 调用方法
    resp = deepseek_client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        temperature=0.7
    )

    # 取内容也必须用 ["content"]
    return resp.choices[0].message["content"]