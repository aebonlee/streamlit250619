import os
import streamlit as st
import openai

# ==================== 설정 방법 ====================
# 1) 환경변수 사용 시:
#    터미널에서:
#      export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"  # Windows: set OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
#    아래 주석 해제:
# openai.api_key = os.getenv("OPENAI_API_KEY")

# 2) 직접 키값 입력 시 (VS Code에서 사용):
openai.api_key = "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"  
# 실제 API 키로 변경하세요
# ===================================================

st.set_page_config(page_title="AI 자기소개서 생성기", layout="centered")
st.title("✍️ AI 기반 자기소개서 생성기")
st.write("이력서 정보를 입력하면 자기소개서를 자동으로 생성해줍니다.")

# 사용자 입력 폼
with st.form(key="resume_form"):
    name = st.text_input("이름")
    cellphone = st.text_input("전화번호")
    email = st.text_input("이메일")
    address = st.text_input("주소")
    education = st.text_area("학력 (예: 학교명, 전공, 기간)")
    experience = st.text_area("경력 (예: 회사명, 직무, 기간 및 주요 업무)")
    skills = st.text_area("기술 및 역량 (예: 프로그래밍 언어, 도구, 자격증)")
    submitted = st.form_submit_button("자기소개서 생성")

if submitted:
    # API 키 확인
    if openai.api_key in (None, "", "YOUR_OPENAI_API_KEY"):
        st.error("OpenAI API 키가 설정되지 않았습니다. 소스 코드에서 직접 입력하거나 환경변수를 설정해주세요.")
    else:
        # 프롬프트 구성
        prompt = (
            f"다음 이력서 정보를 바탕으로 한국어로 자기소개서를 작성해줘.\n"
            f"이름: {name}\n"
            f"전화번호: {cellphone}\n"
            f"이메일: {email}\n"
            f"주소: {address}\n"
            f"학력: {education}\n"
            f"경력: {experience}\n"
            f"기술 및 역량: {skills}\n"
            f"자기소개서는 3~4문단으로 구성하고, 지원 동기와 강점을 부각시켜 작성해줘."
        )
        with st.spinner("자기소개서를 생성 중입니다..."):
            try:
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "친절한 이력서 및 자기소개서 작성 도우미입니다."},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.7,
                    max_tokens=800,
                )
                cover_letter = response.choices[0].message.content.strip()
                st.subheader("📝 생성된 자기소개서")
                st.write(cover_letter)
            except Exception as e:
                st.error(f"자기소개서 생성 중 오류가 발생했습니다: {e}")
