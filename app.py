import streamlit as st
import google.generativeai as genai
import json
import os

# 1. Cấu hình API - Dùng model 'gemini-1.5-flash' để tương thích tốt nhất
GEMINI_API_KEY = "AIzaSyCQFGrPYS_7PkbniYFwy1Vx4YSlk3kMBmI"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Hàm đọc/ghi bộ nhớ có bảo vệ (Bản vá lỗi JSON)
def load_history():
    if os.path.exists("history.json"):
        try:
            with open("history.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, Exception):
            return [] # Nếu file history bị lỗi, tự động reset về [] để app không sập
    return []

def save_history(messages):
    with open("history.json", "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

# Khởi tạo bộ nhớ
if "messages" not in st.session_state:
    st.session_state.messages = load_history()

st.title("⚽ CR7 AI - BỘ NÃO TỰ HỌC 24/7")

# Nút Reset Trí Nhớ (Để bro tự dọn dẹp khi cần)
if st.button("Xóa lịch sử chat"):
    st.session_state.messages = []
    save_history([])
    st.rerun()

# Hiển thị lịch sử
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Xử lý Chat và Quy tắc C++ khắt khe
if prompt := st.chat_input("Nói gì đi bro..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Hệ thống chỉ dẫn cho CR7
    instruction = "Bạn là CR7. TUYỆT ĐỐI KHÔNG dùng // và KHÔNG dùng #include <bits/stdc++.h> khi viết code C++. Luôn thân thiện như bạn thân."
    
    # Gửi lịch sử chat để AI có trí nhớ
    chat_history_text = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    full_prompt = f"{instruction}\n\nLịch sử hội thoại:\n{chat_history_text}"

    try:
        response = model.generate_content(full_prompt)
        if response and response.text:
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            save_history(st.session_state.messages)
    except Exception as e:
        st.error(f"Lỗi rồi bro: {e}. Thử nhấn nút 'Xóa lịch sử chat' hoặc kiểm tra mạng!")