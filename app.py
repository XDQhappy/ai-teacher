import streamlit as st
from lesson_plan_generator import generate_lesson_plan
from socratic_ai import ask_socratic
from kimi_ppt import generate_ppt_with_kimi
from datetime import date

# ======================
# Streamlit 页面配置
# ======================
st.set_page_config(page_title="教学方案 + 苏格拉底问答", layout="wide")
st.title("📚 AI 教学方案 + 苏格拉底问答")

col1, col2 = st.columns(2)

# ----------------------
# 左侧：教案 + Kimi PPT
# ----------------------
with col1:
    st.header("生成教案")

    lesson_title = st.text_input("课程名称", placeholder="例如：光合作用", key="lesson_title_input")
    subject = st.text_input("学科", placeholder="例如：生物", key="subject_input")
    grade = st.number_input("年级", min_value=1, max_value=12, key="grade_input")
    duration = st.number_input("课时数", min_value=1, max_value=10, key="duration_input")
    key_vocab = st.text_input("关键词汇，用逗号分隔", key="key_vocab_input")
    teaching_goals = st.text_area("教学目标（可选）", key="teaching_goals_input")
    teaching_focus = st.text_area("教学重点（可选）", key="teaching_focus_input")
    teaching_difficulties = st.text_area("教学难点（可选）", key="teaching_difficulties_input")
    supporting_materials = st.text_area("辅助材料与资源，用逗号分隔", key="supporting_materials_input")

    # 生成教案按钮
    if st.button("🚀 生成教案", key="generate_lesson_btn"):
        if not lesson_title or not subject:
            st.warning("请填写课程名称和学科")
        else:
            with st.spinner("🧠 AI 正在生成教案，请稍候..."):
                lesson_text = generate_lesson_plan(
                    lesson_title, subject, grade, duration,
                    key_vocab, supporting_materials,
                    teaching_goals, teaching_focus, teaching_difficulties
                )
                st.session_state["lesson_text"] = lesson_text
            st.success("✅ 教案生成完成！")

    # 清空按钮（教案未生成）
    if "lesson_text" not in st.session_state:
        if st.button("🗑️ 清空教案与 PPT", key="clear_before"):
            st.session_state.clear()
            st.success("已清空，可重新生成。")

    # 显示教案
    if "lesson_text" in st.session_state:
        st.subheader("📘 教学方案")
        st.markdown(st.session_state["lesson_text"])

        st.download_button(
            "📥 下载教案文本",
            data=st.session_state["lesson_text"],
            file_name=f"教学方案_{date.today()}.txt",
            mime="text/plain",
            key="download_lesson"
        )

        # Kimi PPT 生成按钮
        if st.button("🎨 生成 PPT（Kimi）", key="generate_ppt"):
            with st.spinner("正在生成 PPT…"):
                ppt_url = generate_ppt_with_kimi(
                    lesson_title, st.session_state["lesson_text"]
                )
                st.session_state["ppt_url"] = ppt_url
            st.success("✅ PPT 已生成！")

        # 清空按钮（教案已生成）
        if st.button("🗑️ 清空教案与 PPT", key="clear_after"):
            st.session_state.clear()
            st.success("已清空，可重新生成。")

        # 下载 PPT
        if "ppt_url" in st.session_state:
            st.markdown(f"[📥 点击下载 PPT]({st.session_state['ppt_url']})", unsafe_allow_html=True)

# ----------------------
# 右侧：苏格拉底式问答
# ----------------------
with col2:
    st.header("苏格拉底式问答")

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # 1️⃣ 提问表单（顶部）
    with st.form(key="socratic_form_top"):
        user_question = st.text_input(
            "向AI提问",
            placeholder="在此输入问题...",
            key="user_question_top"
        )
        ask_button = st.form_submit_button("💬 提问")

        if ask_button and user_question.strip():
            with st.spinner("🧠 AI 正在思考中，请稍候..."):
                answer = ask_socratic(
                    st.session_state.get("lesson_text", ""),
                    user_question
                )
            st.session_state["chat_history"].append((user_question, answer))

    # 2️⃣ 对话记录（最新在上）
    if st.session_state["chat_history"]:
        st.subheader("对话记录")
        for idx, (q, a) in enumerate(reversed(st.session_state["chat_history"])):
            st.markdown(f"**学生:** {q}")
            st.markdown(f"**AI:** {a}")
            st.markdown("---")