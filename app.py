import streamlit as st
import google.generativeai as genai
import asyncio
import edge_tts

# Lắp não Gemini với Key của bro
GEMINI_API_KEY = "AIzaSyCQFGrPYS_7PkbniYFwy1Vx4YSlk3kMBmI"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Khởi tạo bộ nhớ hội thoại
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("⚽ CR7 AI - BỘ NÃO TỰ HỌC 24/7")

# Hiển thị lại lịch sử để AI không bị "mất trí nhớ"
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Ô nhập liệu chat
if prompt := st.chat_input("Nói gì đi bro..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gửi kèm lịch sử để AI học từ câu trước
    full_prompt = "Bạn là CR7. Quy tắc C++: không // và không bits/stdc++.h. Trở thành người bạn thân của tôi. Lịch sử: "
    for m in st.session_state.messages:
        full_prompt += f"\n{m['role']}: {m['content']}"

    response = model.generate_content(full_prompt)
    
    with st.chat_message("assistant"):
        st.markdown(response.text)
    
    st.session_state.messages.append({"role": "assistant", "content": response.text})