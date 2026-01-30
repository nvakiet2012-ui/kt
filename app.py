import streamlit as st
import google.generativeai as genai
import json
import os

# 1. Cấu hình API
GEMINI_API_KEY = "AIzaSyCQFGrPYS_7PkbniYFwy1Vx4YSlk3kMBmI"
genai.configure(api_key=GEMINI_API_KEY)

# Chiến thuật: Thử lần lượt các model, cái nào sống thì đá bản đó
def get_working_model():
    models_to_try = ['gemini-1.5-pro', 'gemini-1.5-flash', 'gemini-1.0-pro']
    for m in models_to_try:
        try:
            model = genai.GenerativeModel(m)
            model.generate_content("test", generation_config={"max_output_tokens": 1})
            return model
        except:
            continue
    return genai.GenerativeModel('gemini-1.5-flash') # Default

model = get_working_model()

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

# Nút dọn rác nếu JSON bị lỗi (Fix ảnh image_724b59.png)
if st.sidebar.button("Reset Trí Nhớ"):
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
        response = model.generate_content(full_prompt)
        if response.text:
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            save_history(st.session_state.messages)
    except Exception as e:
        st.error(f"Vẫn lỗi 404 à? Nhấn nút Reset bên trái thử xem bro! Lỗi: {e}")