# socratic_ai.py
from openai import OpenAI
import streamlit as st

api_key = st.secrets.get("DEEPSEEK_API_KEY", "").strip()

deepseek_client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

def ask_socratic(lesson_text: str, question: str) -> str:
    """
    根据教学内容进行苏格拉底式问答
    """
    messages = [
        {"role": "system",
         "content": (
            "你是一名苏格拉底式中文教师助手，根据提供的教学内容"
            "（包括教学目标、教学重点、教学难点）进行引导式提问。"
            "回答时不要直接告诉学生答案，而是通过逐步启发，帮助学生自己推理出结论。"
            "每次提问不超过 1-2 个关键问题。"
                    ),},
        {"role": "user",
         "content": f"教学内容:\n{lesson_text}\n学生问题: {question}"}
    ]
    resp = deepseek_client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        temperature=0.7
    )
    return resp.choices[0].message.content