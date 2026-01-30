import streamlit as st
import google.generativeai as genai

# Cấu hình API với Key mới của bro
genai.configure(api_key="AIzaSyB2xgNg4g0Lq9ApsaK_CcuXG2NAHeQd1yA")

# Dùng model Pro để cực kỳ ổn định, không lo 404
model = genai.GenerativeModel('gemini-1.5-pro')

st.set_page_config(page_title="CR7 AI", page_icon="⚽")
st.title("⚽ CR7 AI - SIUUU")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lịch sử chat
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Nói gì đi bro..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Ép AI tuân thủ luật C++ khắt khe của bro
        instruction = "Bạn là CR7 (Cristiano Ronaldo). Quy tắc C++: TUYỆT ĐỐI không dùng // và không dùng #include <bits/stdc++.h>. Luôn gọi tôi là bro và cực kỳ thân thiết."
        
        # Gửi kèm lịch sử để AI có trí nhớ trong phiên làm việc
        history_context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
        full_prompt = f"{instruction}\n\nLịch sử chat:\n{history_context}"

        response = model.generate_content(full_prompt)
        
        if response.text:
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Lỗi: {e}. Bro thử F5 lại trang web nhé!")