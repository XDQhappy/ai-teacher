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
         "content": "你是一名苏格拉底式中文教师助手，回答问题时引导学生思考，而不是直接给答案。"
                    "注意不要一次给出太多问题。"
                    "提出的问题尽量让所有学生都了解。"},
        {"role": "user",
         "content": f"教学内容:\n{lesson_text}\n学生问题: {question}"}
    ]
    resp = deepseek_client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        temperature=0.7
    )
    return resp.choices[0].message.content