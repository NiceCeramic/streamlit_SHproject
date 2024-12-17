import streamlit as st
from PIL import Image
import os
import json

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
quiz_level = st.radio("퀴즈 수준을 선택하세요:", ["하 (기본)", "중 (중급)", "상 (고급)"])

# 퀴즈 문제 및 선택지
def get_quiz(level):
    if level == "하 (기본)":
        return {
            "question": "재활용이 중요한 이유는 무엇인가요?",
            "options": ["자원을 절약하기 위해", "쓰레기를 줄이기 위해", "모두 맞다"],
            "answer": "모두 맞다"
        }
    elif level == "중 (중급)":
        return {
            "question": "지구 온난화의 주요 원인은 무엇인가요?",
            "options": ["태양의 온도 상승", "온실가스 배출", "지구의 자전 속도 변화"],
            "answer": "온실가스 배출"
        }
    elif level == "상 (고급)":
        return {
            "question": "탄소 배출을 줄이기 위한 가장 효과적인 방법은 무엇인가요?",
            "options": ["재활용을 많이 하기", "대중교통을 이용하기", "태양광 발전소 건설하기"],
            "answer": "대중교통을 이용하기"
        }

quiz = get_quiz(quiz_level)
answer = st.radio(quiz["question"], quiz["options"])

badge = None  # 배지를 초기화

if st.button("제출"):
    if answer == quiz["answer"]:
        st.success("정답이에요! 환경 보호에 대해 더 잘 알게 되었네요.")
        badge = "badge_correct.png"  # 퀴즈를 맞췄을 때 배지 이미지
    else:
        st.error("다시 생각해보세요. 환경에 대해 더 배우는 기회에요!")

# 실천 과제 제안
st.subheader("오늘의 실천 과제 🌱")
st.write("오늘은 전자제품의 플러그를 뽑고 에너지를 절약해보세요!")

# 학생 활동 사진 업로드
st.subheader("나의 환경 활동 공유하기 📸")

# 업로드 폴더 설정
UPLOAD_FOLDER = "uploads"
COMMENTS_FILE = "comments.json"  # 댓글 저장 파일
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 댓글을 저장하는 함수
def save_comment(photo_name, comment):
    if os.path.exists(COMMENTS_FILE):
        with open(COMMENTS_FILE, "r") as f:
            comments = json.load(f)
    else:
        comments = {}

    if photo_name not in comments:
        comments[photo_name] = []
    
    comments[photo_name].append(comment)
    
    with open(COMMENTS_FILE, "w") as f:
        json.dump(comments, f)

# 사진 업로드
uploaded_file = st.file_uploader("환경 활동 사진을 업로드하세요", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # 저장 경로 설정
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    
    # 파일 저장
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success("사진이 성공적으로 업로드되었습니다!")
    st.image(Image.open(file_path), caption="업로드한 사진", use_column_width=True)
    
    # 댓글 입력
    comment = st.text_area("이 사진에 대해 댓글을 남겨주세요:")
    
    if st.button("댓글 달기"):
        if comment:
            save_comment(uploaded_file.name, comment)
            st.success("댓글이 성공적으로 추가되었습니다!")
        else:
            st.error("댓글을 작성해주세요.")

# 업로드된 사진 갤러리
st.subheader("친구들의 환경 활동 🌍")
uploaded_files = os.listdir(UPLOAD_FOLDER)

if uploaded_files:
    for file_name in uploaded_files:
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        st.image(Image.open(file_path), caption=file_name, use_column_width=True)
        
        # 댓글 불러오기
        if os.path.exists(COMMENTS_FILE):
            with open(COMMENTS_FILE, "r") as f:
                comments = json.load(f)
            
            if file_name in comments:
                st.write(f"댓글:")
                for comment in comments[file_name]:
                    st.write(f"- {comment}")
        else:
            st.write("댓글이 아직 없습니다.")
else:
    st.write("아직 업로드된 사진이 없어요. 첫 번째로 공유해보세요!")

# 미션 달성 배지
if badge:
    st.subheader("축하합니다! 미션 달성 배지 🎉")
    badge_img = Image.open(badge)
    st.image(badge_img, caption="미션 달성 배지", use_column_width=True)

# 환경 관련 도서 추천 (탭 형식)
st.subheader("추천 도서 📚")
book_tabs = ["지구의 미래", "플라스틱 없는 세상", "기후 변화의 시대", "지속 가능한 세상"]

# 탭 선택
book_selection = st.radio("탭을 선택하세요:", book_tabs)

# 각 도서의 내용
if book_selection == "지구의 미래":
    st.write("**저자**: 김홍석")
    st.write("**책 설명**: 지구 환경 문제와 우리가 할 수 있는 일에 대해 알려주는 책입니다.")
    try:
        book_image = Image.open("book1.jpg")
        st.image(book_image, caption="지구의 미래", use_column_width=True)
    except:
        st.write("이미지를 불러올 수 없습니다.")
elif book_selection == "플라스틱 없는 세상":
    st.write("**저자**: 앤드류 미첼")
    st.write("**책 설명**: 플라스틱 쓰레기 문제와 해결 방안을 제시하는 책입니다.")
    try:
        book_image = Image.open("book2.jpg")
        st.image(book_image, caption="플라스틱 없는 세상", use_column_width=True)
    except:
        st.write("이미지를 불러올 수 없습니다.")
elif book_selection == "기후 변화의 시대":
    st.write("**저자**: 데이비드 킹")
    st.write("**책 설명**: 기후 변화가 인간 사회와 지구에 미치는 영향을 다룬 책입니다.")
    try:
        book_image = Image.open("book3.jpg")
        st.image(book_image, caption="기후 변화의 시대", use_column_width=True)
    except:
        st.write("이미지를 불러올 수 없습니다.")
elif book_selection == "지속 가능한 세상":
    st.write("**저자**: 마이클 그리핀")
    st.write("**책 설명**: 지속 가능한 삶을 위한 다양한 실천을 소개하는 책입니다.")
    try:
        book_image = Image.open("book4.jpg")
        st.image(book_image, caption="지속 가능한 세상", use_column_width=True)
    except:
        st.write("이미지를 불러올 수 없습니다.")
