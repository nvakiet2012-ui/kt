import streamlit as st
import google.generativeai as genai
import json
import os

# 1. Cấu hình API
GEMINI_API_KEY = "AIzaSyCQFGrPYS_7PkbniYFwy1Vx4YSlk3kMBmI"
genai.configure(api_key=GEMINI_API_KEY)
# Dùng model này để tương thích 100% với thư viện mới bro vừa cài
model = genai.GenerativeModel('gemini-1.5-flash')

def load_history():
    if os.path.exists("history.json"):
        try:
            with open("history.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except:
            return []
    return []

def save_history(messages):
    with open("history.json", "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

if "messages" not in st.session_state:
    st.session_state.messages = load_history()

st.title("⚽ CR7 AI - BỘ NÃO TỰ HỌC 24/7")

if st.button("Xóa lịch sử chat"):
    st.session_state.messages = []
    save_history([])
    st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Nói gì đi bro..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    instruction = "Bạn là CR7. Quy tắc C++: KHÔNG dùng // và KHÔNG dùng #include <bits/stdc++.h>."
    full_prompt = f"{instruction}\nLịch sử: {str(st.session_state.messages)}"

    try:
        # Vá lỗi: Kiểm tra phản hồi có tồn tại không
        response = model.generate_content(full_prompt)
        if response.text:
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            save_history(st.session_state.messages)
    except Exception as e:
        st.error(f"Lỗi API (Có thể do Key hoặc Model): {e}")