import os
import streamlit as st
import openai
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import json

# 한글 폰트 설정 (맑은 고딕)
mpl.rc('font', family='Malgun Gothic')
# 음수 부호 깨짐 방지
mpl.rcParams['axes.unicode_minus'] = False

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

st.set_page_config(page_title="감정 분석 데모 (OpenAI)", layout="centered")
st.title("🧐 감정 분석 데모 (OpenAI)")
st.write("입력된 텍스트의 긍정/중립/부정 확률을 계산하여 막대 그래프로 시각화합니다.")

# 사용자 입력
text = st.text_area("분석할 문장을 입력하세요:", placeholder="예: 이 영화 정말 재미있었어요.")

if st.button("분석"):
    if not text.strip():
        st.error("분석할 문장을 입력해주세요.")
    else:
        with st.spinner("분석 중..."):
            # OpenAI로 감정 분석 요청
            prompt = (
                "다음 문장의 감정을 분석하여 JSON 형식으로 긍정, 중립, 부정 확률을 반환해줘."
                f"\n문장: '{text}'"
                "\n출력 예시: {\"positive\": 0.70, \"neutral\": 0.20, \"negative\": 0.10}"
            )
            try:
                # openai v1.0.0+ 인터페이스 사용
                resp = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "당신은 정확한 감정 분석 결과를 JSON으로만 응답하는 도우미입니다."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0,
                    max_tokens=100,
                )
                content = resp.choices[0].message.content.strip()
                # JSON 파싱
                data = json.loads(content)
                # DataFrame 생성
                df = pd.DataFrame({
                    '감정': ['긍정', '중립', '부정'],
                    '확률': [data.get('positive', 0), data.get('neutral', 0), data.get('negative', 0)]
                })
                # 시각화
                st.subheader("분석 결과")
                fig, ax = plt.subplots()
                ax.bar(df['감정'], df['확률'])
                ax.set_ylim(0, 1)
                ax.set_ylabel('확률')
                st.pyplot(fig)
                # 원본 JSON
                st.markdown("**원본 응답 JSON**")
                st.json(data)
            except Exception as e:
                st.error(f"분석 중 오류가 발생했습니다: {e}")

