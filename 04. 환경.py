import streamlit as st
from PIL import Image
import os

# 앱 제목
st.title("환경 탐험 챗봇 🌍")

# 사용자 입력
st.write("안녕하세요! 저는 환경 탐험 챗봇이에요. 환경에 대해 알고 싶은 걸 물어보세요!")
user_input = st.text_input("질문을 입력하세요:")

# 챗봇 응답
def chatbot_response(user_input):
    responses = {
        "지구 온난화": "지구 온난화는 온실가스 배출로 지구 평균 온도가 상승하는 현상이에요. 이를 막기 위해 에너지를 절약하고 나무를 심는 게 중요해요.",
        "재활용": "재활용은 쓰레기를 새롭게 사용하는 방법이에요. 캔, 병, 종이를 분리수거하면 자원을 아낄 수 있어요!",
        "에너지 절약": "에너지를 절약하려면 불필요한 전기 사용을 줄이고, 대중교통을 이용해보세요.",
    }
    return responses.get(user_input, "그 내용은 아직 공부 중이에요. 다른 질문을 해볼래요?")

if user_input:
    response = chatbot_response(user_input)
    st.write(f"챗봇: {response}")

# 퀴즈 섹션
st.subheader("환경 퀴즈 🧠")
quiz_question = "플라스틱 쓰레기를 줄이는 가장 좋은 방법은 무엇일까요?"
quiz_options = ["플라스틱 제품 사용 줄이기", "분리수거 안 하기", "플라스틱 더 많이 사용하기"]
answer = st.radio("선택하세요:", quiz_options)

if st.button("제출"):
    if answer == "플라스틱 제품 사용 줄이기":
        st.success("정답이에요! 플라스틱 사용을 줄이는 게 가장 중요해요.")
    else:
        st.error("다시 생각해보세요. 플라스틱을 줄이는 방법이 중요해요!")

# 실천 과제 제안
st.subheader("오늘의 실천 과제 🌱")
st.write("오늘은 전자제품의 플러그를 뽑고 에너지를 절약해보세요!")

# 학생 활동 사진 업로드
st.subheader("나의 환경 활동 공유하기 📸")

# 업로드 폴더 설정
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

uploaded_file = st.file_uploader("환경 활동 사진을 업로드하세요", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # 저장 경로 설정
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    
    # 파일 저장
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success("사진이 성공적으로 업로드되었습니다!")
    st.image(Image.open(file_path), caption="업로드한 사진", use_column_width=True)

# 업로드된 사진 갤러리
st.subheader("친구들의 환경 활동 🌍")
uploaded_files = os.listdir(UPLOAD_FOLDER)

if uploaded_files:
    for file_name in uploaded_files:
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        st.image(Image.open(file_path), caption=file_name, use_column_width=True)
else:
    st.write("아직 업로드된 사진이 없어요. 첫 번째로 공유해보세요!")
