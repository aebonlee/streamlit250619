import os
import streamlit as st
import openai
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import json

# ---------- (기존 설정 부분 동일) ----------
mpl.rc('font', family='Malgun Gothic')
mpl.rcParams['axes.unicode_minus'] = False
openai.api_key = "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"  
# 실제 API 키로 변경하세요

st.set_page_config(page_title="감정 분석 데모 (OpenAI)", layout="centered")
st.title("🧐 감정 분석 데모 (OpenAI)")
st.write("입력된 텍스트의 긍정/중립/부정 확률을 계산하여 막대 그래프로 시각화합니다.")

text = st.text_area("분석할 문장을 입력하세요:", placeholder="예: 이 영화 정말 재미있었어요.")

if st.button("분석"):
    if not text.strip():
        st.error("분석할 문장을 입력해주세요.")
    else:
        with st.spinner("분석 중..."):
            # ------- ① 문장 전체 감정 확률 요청 -------
            prob_prompt = (
                "다음 문장의 감정을 분석하여 JSON 형식으로 긍정, 중립, 부정 확률을 반환해줘.\n"
                f"문장: '{text}'\n"
                '출력 예시: {"positive": 0.70, "neutral": 0.20, "negative": 0.10}'
            )
            try:
                prob_resp = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "당신은 정확한 감정 분석 결과를 JSON으로만 응답하는 도우미입니다."},
                        {"role": "user", "content": prob_prompt}
                    ],
                    temperature=0,
                    max_tokens=100
                )
                prob_json = json.loads(prob_resp.choices[0].message.content.strip())

                # ------- ② 단어별 감정 태깅 요청(추가) -------
                tag_prompt = (
                    "다음 문장의 각 단어를 긍정, 중립, 부정 중 하나로 분류해서 "
                    "아래 JSON 스키마에 맞게만 응답해줘.\n"
                    f"문장: '{text}'\n"
                    '스키마 예시: {"positive": ["행복", "좋다"], "neutral": ["영화"], "negative": ["지루했다"]}'
                )
                tag_resp = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "당신은 단어별 감정 태깅을 JSON으로만 응답하는 도우미입니다."},
                        {"role": "user", "content": tag_prompt}
                    ],
                    temperature=0,
                    max_tokens=200
                )
                tag_json = json.loads(tag_resp.choices[0].message.content.strip())

                # ------- ③ 확률 시각화 -------
                df_prob = pd.DataFrame({
                    "감정": ["긍정", "중립", "부정"],
                    "확률": [
                        prob_json.get("positive", 0),
                        prob_json.get("neutral", 0),
                        prob_json.get("negative", 0)
                    ]
                })
                st.subheader("① 문장 전체 감정 확률")
                fig, ax = plt.subplots()
                ax.bar(df_prob["감정"], df_prob["확률"])
                ax.set_ylim(0, 1)
                ax.set_ylabel("확률")
                st.pyplot(fig)
                st.json(prob_json)

                # ------- ④ 단어별 감정 결과 표시 -------
                st.subheader("② 단어별 감정 분류")
                # 표 형태
                df_tag = (
                    pd.DataFrame([
                        {"단어": w, "감정": "긍정"} for w in tag_json.get("positive", [])] +
                        [{"단어": w, "감정": "중립"} for w in tag_json.get("neutral", [])] +
                        [{"단어": w, "감정": "부정"} for w in tag_json.get("negative", [])]
                    )
                    .sort_values("감정")
                    .reset_index(drop=True)
                )
                st.dataframe(df_tag, hide_index=True, use_container_width=True)
                # 리스트 형태(가독성용)
                st.markdown("**단어 리스트**")
                st.markdown(f"- 긍정: {', '.join(tag_json.get('positive', []) or ['(없음)'])}")
                st.markdown(f"- 중립: {', '.join(tag_json.get('neutral', []) or ['(없음)'])}")
                st.markdown(f"- 부정: {', '.join(tag_json.get('negative', []) or ['(없음)'])}")

            except Exception as e:
                st.error(f"분석 중 오류가 발생했습니다: {e}")
