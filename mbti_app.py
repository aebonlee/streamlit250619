import streamlit as st

# MBTI Quiz: 스트림릿 앱 (5문제씩 순차 진행)
st.set_page_config(page_title="MBTI 테스트", layout="centered")
st.title("🔮 간단한 MBTI 테스트")
st.write("5개의 질문에 답변 후 '다음' 버튼을 눌러주세요.")

# MBTI 질문 리스트: (질문, 지표, {키: 라벨})
questions = [
    ("새로운 사람들과 함께 시간을 보내는 것이 더 즐겁다.", "EI", {"E": "외향(E)", "I": "내향(I)"}),
    ("조용한 환경에서 혼자 생각하는 시간이 필요하다.", "EI", {"E": "외향(E)", "I": "내향(I)"}),
    ("대규모 모임에서 활기를 느낀다.", "EI", {"E": "외향(E)", "I": "내향(I)"}),
    ("한 사람과 깊이 있는 대화를 선호한다.", "EI", {"E": "외향(E)", "I": "내향(I)"}),
    ("혼자 있을 때 에너지가 충전된다.", "EI", {"E": "외향(E)", "I": "내향(I)"}),

    ("구체적인 사실과 경험에 집중하는 편이다.", "SN", {"S": "감각(S)", "N": "직관(N)"}),
    ("전체적인 그림과 가능성에 대해 생각하는 것이 편하다.", "SN", {"S": "감각(S)", "N": "직관(N)"}),
    ("실제 관찰 가능한 것을 중요하게 여긴다.", "SN", {"S": "감각(S)", "N": "직관(N)"}),
    ("미래의 가능성을 상상하는 것이 흥미롭다.", "SN", {"S": "감각(S)", "N": "직관(N)"}),
    ("현재의 세세한 정보에 집중하는 편이다.", "SN", {"S": "감각(S)", "N": "직관(N)"}),

    ("결정을 내릴 때 논리적이고 객관적인 기준을 중시한다.", "TF", {"T": "사고(T)", "F": "감정(F)"}),
    ("다른 사람의 감정과 조화를 고려하여 결정을 내린다.", "TF", {"T": "사고(T)", "F": "감정(F)"}),
    ("논리적인 분석이 의사결정의 핵심이라고 생각한다.", "TF", {"T": "사고(T)", "F": "감정(F)"}),
    ("다른 사람의 기분에 민감하게 반응한다.", "TF", {"T": "사고(T)", "F": "감정(F)"}),
    ("사실과 감정보다 원칙을 우선시한다.", "TF", {"T": "사고(T)", "F": "감정(F)"}),

    ("계획을 세우고 정리된 상태에서 움직이는 것이 좋다.", "JP", {"J": "판단(J)", "P": "인식(P)"}),
    ("유연하게 상황에 따라 행동하는 것을 선호한다.", "JP", {"J": "판단(J)", "P": "인식(P)"}),
    ("계획 없는 일정은 불안하다.", "JP", {"J": "판단(J)", "P": "인식(P)"}),
    ("즉흥적으로 계획을 변경하는 것을 좋아한다.", "JP", {"J": "판단(J)", "P": "인식(P)"}),
    ("항상 할 일을 미리 정해두는 편이다.", "JP", {"J": "판단(J)", "P": "인식(P)"}),
]
block_size = 5

# 퀴즈 초기화 함수
def reset_quiz():
    st.session_state.current_idx = 0
    st.session_state.scores = {k: 0 for k in ["E","I","S","N","T","F","J","P"]}

# 세션 상태 초기화
def initialize():
    if "scores" not in st.session_state or "current_idx" not in st.session_state:
        reset_quiz()

initialize()
start = st.session_state.current_idx
end = min(start + block_size, len(questions))

# 블록별 질문 표시
if start < len(questions):
    with st.form(key=f"form_{start}"):
        for i in range(start, end):
            q_text, _, opts = questions[i]
            st.radio(f"Q{i+1}. {q_text}", list(opts.values()), key=f"choice_{i}")
        if st.form_submit_button("다음"):
            # 점수 합산
            for i in range(start, end):
                selected = st.session_state.get(f"choice_{i}")
                for key, label in questions[i][2].items():
                    if label == selected:
                        st.session_state.scores[key] += 1
                        break
            # 다음 블록 인덱스 업데이트
            st.session_state.current_idx += block_size
# 마지막 블록: 결과 표시
else:
    # 마지막 블록 점수 합산
    for i in range(start, end):
        selected = st.session_state.get(f"choice_{i}")
        for key, label in questions[i][2].items():
            if label == selected:
                st.session_state.scores[key] += 1
                break
    # MBTI 유형 계산
    sc = st.session_state.scores
    mbti = (
        "E" if sc["E"] >= sc["I"] else "I"
    ) + (
        "S" if sc["S"] >= sc["N"] else "N"
    ) + (
        "T" if sc["T"] >= sc["F"] else "F"
    ) + (
        "J" if sc["J"] >= sc["P"] else "P"
    )
    st.subheader("🧩 결과")
    st.write(f"당신의 MBTI 유형은 **{mbti}** 입니다!")
    # 유형 설명
    descriptions = {
        "ISTJ":"논리적이고 신중한 관리자 유형","ISFJ":"책임감 있고 세심한 수호자 유형",
        "INFJ":"통찰력 있고 창의적인 통역자 유형","INTJ":"전략적이고 독립적인 설계자 유형",
        "ISTP":"유연하고 분석적인 해결사 유형","ISFP":"따뜻하고 예술적인 탐험가 유형",
        "INFP":"이상주의적이고 충실한 중재자 유형","INTP":"호기심 많고 논리적인 사색가 유형",
        "ESTP":"에너지 넘치고 현실적인 활동가 유형","ESFP":"친근하고 낙천적인 연예인 유형",
        "ENFP":"열정적이고 창의적인 활동가 유형","ENTP":"영리하고 독창적인 발명가 유형",
        "ESTJ":"현실적이고 조직적인 관리자 유형","ESFJ":"친절하고 협력적인 제공자 유형",
        "ENFJ":"이해심 많고 카리스마 있는 지도자 유형","ENTJ":"결단력 있고 대담한 지휘관 유형"
    }
    st.write(descriptions.get(mbti, "유형 설명이 없습니다."))
    # 다시 시작 버튼
    if st.button("다시 시작"):
        reset_quiz()
# 세션 상태 초기화