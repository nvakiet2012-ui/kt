import streamlit as st
import google.generativeai as genai
import json
import os

# 1. Cấu hình API - Dùng gemini-1.5-flash là bản 'quốc dân' ổn định nhất
GEMINI_API_KEY = "AIzaSyCQFGrPYS_7PkbniYFwy1Vx4YSlk3kMBmI"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Hàm đọc/ghi bộ nhớ có bảo vệ (Fix lỗi JSONDecodeError)
def load_history():
    if os.path.exists("history.json"):
        try:
            with open("history.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except:
            return [] # Nếu file lỗi, tự động reset về [] để app không sập
    return []

def save_history(messages):
    with open("history.json", "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

if "messages" not in st.session_state:
    st.session_state.messages = load_history()

st.title("⚽ CR7 AI - BỘ NÃO TỰ HỌC 24/7")

# Hiển thị lịch sử
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Xử lý chat và ép AI tuân thủ luật C++ của bro
if prompt := st.chat_input("Nói gì đi bro..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    instruction = "Bạn là CR7. Quy tắc C++: TUYỆT ĐỐI không dùng // và không dùng #include <bits/stdc++.h>. Luôn thân thiện."
    full_prompt = f"{instruction}\nLịch sử chat: {str(st.session_state.messages)}"

    try:
        response = model.generate_content(full_prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        save_history(st.session_state.messages)
    except Exception as e:
        st.error(f"Lỗi rồi bro: {e}")