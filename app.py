import streamlit as st
import google.generativeai as genai

# Cấu hình API - Key của bro
genai.configure(api_key="AIzaSyCQFGrPYS_7PkbniYFwy1Vx4YSlk3kMBmI")

# Thử dùng model Pro thay vì Flash để phá lỗi 404
model = genai.GenerativeModel('gemini-1.5-pro')

st.title("⚽ CR7 AI - SIUUU")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Nói gì đi bro..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Ép AI tuân thủ luật C++ ngay trong câu hỏi
        full_p = f"Bạn là CR7. Luật C++: KO dùng // và KO dùng bits/stdc++.h. Chat: {prompt}"
        response = model.generate_content(full_p)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Lỗi: {e}")