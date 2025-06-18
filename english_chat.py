# 영어 회화 연습 챗봇
import os
import streamlit as st
from streamlit_chat import message
import openai

# API 키 설정
openai.api_key = "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"  

st.set_page_config(page_title="영어 회화 파트너", layout="centered")
st.title("🗣️ 영어 회화 연습 파트너 챗봇")
st.write("영어 문장으로 대화하며 실시간 교정을 받고 연습하세요.")

# 채팅 히스토리 초기화
if "history" not in st.session_state:
    st.session_state.history = []

# 사용자 입력
user_input = st.text_input("영어로 메시지를 입력하세요:")

if st.button("전송") and user_input.strip():
    # 사용자 메시지 추가
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.spinner("GPT가 응답 중..."):
        try:
            resp = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "너는 영어 회화 교정 도우미야. "
                            "사용자의 문장을 자연스럽게 교정하고, "
                            "그 다음 이어질 질문을 제안해줘."
                        )
                    },
                    *st.session_state.history
                ],
                temperature=0.5,
                max_tokens=300,
            )
            # OpenAI 응답에서 assistant 메시지 추출
            reply = resp.choices[0].message.content.strip()
            st.session_state.history.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"응답 중 오류가 발생했습니다: {e}")

# 대화 UI 렌더링
for chat in st.session_state.history:
    if chat["role"] == "user":
        message(chat["content"], is_user=True)
    else:
        message(chat["content"])