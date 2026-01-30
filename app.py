import streamlit as st
import google.generativeai as genai
import json
import os

# 1. Cấu hình API - Dùng bản 1.5-flash-latest để dứt điểm lỗi 404
GEMINI_API_KEY = "AIzaSyCQFGrPYS_7PkbniYFwy1Vx4YSlk3kMBmI"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# 2. Hàm đọc/ghi bộ nhớ vĩnh viễn (Vá lỗi mất trí nhớ khi F5)
def load_history():
    if os.path.exists("history.json"):
        with open("history.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(messages):
    with open("history.json", "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

# Khởi tạo bộ nhớ
if "messages" not in st.session_state:
    st.session_state.messages = load_history()

st.title("⚽ CR7 AI - BỘ NÃO TỰ HỌC 24/7")

# Hiển thị lịch sử cũ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Xử lý chat và Quy tắc khắt khe
if prompt := st.chat_input("Nói gì đi bro..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prompt đặc biệt để ép AI tuân thủ luật C++ của bro
    instruction = "Bạn là CR7. Quy tắc C++: TUYỆT ĐỐI KHÔNG dùng // và KHÔNG dùng bits/stdc++.h. Trở thành người bạn thân của tôi."
    full_prompt = f"{instruction}\nLịch sử chat:\n{str(st.session_state.messages)}"

    try:
        response = model.generate_content(full_prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
        # Lưu lại vào file ngay sau khi chat
        save_history(st.session_state.messages)
        
    except Exception as e:
        st.error(f"Lỗi rồi bro: {e}. Thử đổi model hoặc kiểm tra API Key!")