import os
import streamlit as st
import openai
from duckduckgo_search import DDGS  # pip install duckduckgo-search

# ==================== 설정 방법 ====================
# 1) 환경변수 사용 시:
#    터미널에서:
#      export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"  # Windows: set OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
#    아래 주석 해제:
# openai.api_key = os.getenv("OPENAI_API_KEY")

# 2) 직접 키값 입력 시 (VS Code에서 사용):
openai.api_key = "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"  # 실제 API 키로 변경하세요
# ===================================================

st.set_page_config(page_title="AI 자기소개서 + 평판 조회기", layout="centered")
st.title("✍️ AI 기반 자기소개서 생성기")
st.write("이력서 정보를 입력하면 자기소개서와 함께 인터넷 평판과 출처를 자동으로 조회해 보여줍니다.")

# 사용자 입력 폼
with st.form(key="resume_form"):
    name = st.text_input("이름")
    cellphone = st.text_input("전화번호")
    email = st.text_input("이메일")
    address = st.text_input("주소")
    education = st.text_area("학력 (예: 학교명, 전공, 기간)")
    experience = st.text_area("경력 (예: 회사명, 직무, 기간 및 주요 업무)")
    skills = st.text_area("기술 및 역량 (예: 프로그래밍 언어, 도구, 자격증)")
    submitted = st.form_submit_button("자기소개서 생성 및 조회")

# 인터넷 평판 조회 함수
def fetch_reputation(name: str, max_results: int = 5):
    query = f"{name} 평판 후기 OR 리뷰"
    reputations = []
    try:
        with DDGS() as ddgs:
            for i, r in enumerate(ddgs.text(query, region='wt-wt', safesearch='Off', timelimit=None)):
                if i >= max_results:
                    break
                snippet = r.get('body', '')
                url = r.get('href', '')
                reputations.append({'snippet': snippet, 'url': url})
        return reputations
    except Exception:
        return []

if submitted:
    if not openai.api_key or openai.api_key == "YOUR_OPENAI_API_KEY":
        st.error("OpenAI API 키가 설정되지 않았습니다. 환경변수나 소스코드에 API 키를 설정해주세요.")
    else:
        # 자기소개서 생성 프롬프트
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
                    max_tokens=1000,
                )
                cover_letter = response.choices[0].message.content.strip()
                st.subheader("📝 생성된 자기소개서")
                st.write(cover_letter)
            except Exception as e:
                st.error(f"자기소개서 생성 중 오류가 발생했습니다: {e}")

        # 인터넷 평판 조회 및 출력
        reputations = fetch_reputation(name)
        st.subheader(f"🌐 인터넷 평판 ({len(reputations)}건)")
        if reputations:
            for idx, rep in enumerate(reputations, 1):
                snippet = rep['snippet']
                url = rep['url']
                if url:
                    st.markdown(f"**{idx}.** {snippet} [출처]({url})")
                else:
                    st.markdown(f"**{idx}.** {snippet}")
        else:
            st.write("평판 정보를 찾을 수 없습니다.")

        st.success("자기소개서와 평판 조회가 완료되었습니다.")
        st.balloons()
