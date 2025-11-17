# kimi_ppt.py
from openai import OpenAI
import streamlit as st
import json

def generate_ppt_with_kimi(title: str, markdown: str, style="business"):
    """
    调用 Kimi Chat+Tool 接口生成 PPT，返回 ppt_url
    """
    kimi_client = OpenAI(
        api_key=st.secrets["KIMI_API_KEY"],
        base_url="https://api.moonshot.cn/v1"
    )

    tools = [{
        "type": "function",
        "function": {
            "name": "ppt_generator",
            "description": "生成PPT",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "outline": {"type": "string"},
                    "theme": {"type": "string", "enum": ["business", "minimal", "academic"]}
                },
                "required": ["title", "outline"]
            }
        }
    }]

    messages = [
        {"role": "user", "content": f"请把以下教案做成PPT，标题为《{title}》，主题风格{style}：\n{markdown}"}
    ]

    # 第一次请求，让模型决定调用工具
    resp1 = kimi_client.chat.completions.create(
        model="kimi-k2-turbo-preview",
        messages=messages,
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "ppt_generator"}}
    )
    assistant_msg = resp1.choices[0].message
    messages.append(assistant_msg)

    # 第二条 tool 消息只表示“函数已执行”，内容随意
    tool_call = assistant_msg.tool_calls[0]
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "name": tool_call.function.name,
        "content": "{}"
    })

    # 再次请求获取 ppt_url
    resp2 = kimi_client.chat.completions.create(
        model="kimi-k2-turbo-preview",
        messages=messages
    )

    raw = resp2.choices[0].message.content
    if raw.startswith("http"):
        return raw
    try:
        return json.loads(raw)["ppt_url"]
    except Exception:
        return raw