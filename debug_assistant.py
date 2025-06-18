# 코드 디버깅 도우미 챗봇
import os
import streamlit as st
from streamlit_chat import message
import openai

# API 키 설정
openai.api_key = "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"  

st.set_page_config(page_title="코드 디버깅 도우미", layout="centered")
st.title("🐞 코드 디버깅 도우미 챗봇")
st.write("파이썬 코드를 입력하면 GPT가 디버깅 아이디어와 수정 제안을 제공합니다.")

# 세션 상태 초기화
if "history" not in st.session_state:
    st.session_state.history = []

# 사용자 입력
user_code = st.text_area("디버깅이 필요한 코드를 입력하세요:", height=200)

if st.button("전송") and user_code.strip():
    # 사용자 메시지 히스토리에 추가
    st.session_state.history.append({"role": "user", "content": user_code})
    with st.spinner("GPT가 분석 중..."):
        try:
            resp = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "너는 친절한 파이썬 코드 디버깅 도우미야."},
                    *st.session_state.history
                ],
                temperature=0.2,
                max_tokens=500,
            )
            reply = resp.choices[0].message.content.strip()
            st.session_state.history.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"분석 중 오류가 발생했습니다: {e}")

# 채팅 UI 렌더링
for chat in st.session_state.history:
    if chat["role"] == "user":
        message(chat["content"], is_user=True)
    else:
        message(chat["content"])