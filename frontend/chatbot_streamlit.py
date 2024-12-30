# chatbot_streamlit.py
# /run 경로로 요청하고 답변 받아오는 과정 streamlit으로 front 작성

import streamlit as st
import time
import requests
import sys
sys.path.append("/home/jjw/work")

from backend.app.history.save_history import connect_db, get_history, delete_history

# 스트림형식으로 바꾸기
def stream_data():
     for word in answer.split(" "):
        yield word + " "
        time.sleep(0.06) 


st.set_page_config(page_title="소득세챗봇", page_icon="🤖", layout="centered")

CHAT_API_URL = "http://localhost:8080/run"

with st.sidebar:
    with st.expander("🔎질문 예시", expanded=True):
        que_sample = """
                <style>
                    .text {
                        font-size: 15px; /* 폰트 크기를 20px로 설정 */
                        color: #7C00A0; /* 텍스트 색상 설정 (옵션) */
                    }
                </style>
                <p class='text'>소득세법의 목적은 무엇인가요?</p>
                <p class='text'>거주자와 비거주자의 차이점을 설명해 주세요.</p>
                <p class='text'>7년 근무한 사람의 퇴직소득공제액을 계산해 주세요.</p> 
                <p class='text'>연봉이 5000만원인 사람의 소득세를 계산해 주세요.</p> 
                <p class='text'>뇌물은 어떤 종류의 소득으로 분류되나요?</p> 
            """
        st.markdown(que_sample, unsafe_allow_html=True)

    
title_col1, title_col2, title_col3 = st.columns([1, 0.8, 1])

# 첫 번째 열에 이미지 추가
with title_col1:
    st.image("frontend/chatbot.jpg")

# 두 번째 열에 제목 추가
with title_col2:
    st.markdown(
        """
        <h4 style='color: black;'>📚소득세법 전문 AI 어시스턴트</h4>
        """, 
        unsafe_allow_html=True
    )

with title_col3:
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    if st.button("🍀대화내용삭제(리셋)🍀"):
        conn=connect_db()
        delete_history(conn)
        st.session_state.message_list=[]


# st.session_state 는 전역변수 느낌 
# 비어있다면 빈 리스트를 저장하고, 채팅 할때마다 "role" 과 "content"를 딕셔너리로 append함
if "message_list" not in st.session_state:
    st.session_state.message_list=[]
    conn=connect_db()
    history=get_history(conn)
    print(history)
    for row in history:
        st.session_state.message_list.append({"role":"user", "content":row[1]})
        st.session_state.message_list.append({"role":"ai", "content":row[2]})

# ========================== session_state 를 돌면서 내용을 write함 =============================
for i, message in enumerate(st.session_state.message_list):
    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])
    elif message["role"] == "ai":
        with st.chat_message("ai"):
            st.write(message["content"])
    elif message["role"] == "toggle":
        # 고유 키를 지정한 checkbox 생성
        toggle_state = st.checkbox("출처 보기", key=f"checkbox_{i}")
        if toggle_state:
            st.markdown(message["content"], unsafe_allow_html=True)
        


 # ================================== 사용자 입력 및 LLM 답변 출력 ===============================
# 사용자 입력창 추가
# user_question 에 저장됨
# st.chat_message("user") 를 통해 user의 바 생성하고 st.wrie()를 통해 텍스트 출력
# user은 "role" 로 저장됨
# with를 사용해써 해당 바 안에 텍스트 넣음
if user_question := st.chat_input(placeholder="소득세에 대해 질문해 주세요😀"):
    with st.chat_message("user"):
        st.write(user_question)
        st.session_state.message_list.append({"role":"user", "content":user_question})

    with st.spinner("답변을 생성하는 중입니다😊"):
        try:
            response = requests.post(CHAT_API_URL, json={"question":user_question})
            response_json=response.json()
            
            answer=response_json["chatbot_answer"]
            meta_data=response_json["meta_data"]
            print(meta_data)
            # print(meta_data)

        except:
            print("요청 실패!")

    with st.chat_message("ai"):
        st.write_stream(stream_data)
        st.session_state.message_list.append({"role": "ai", "content": answer})
    
    toggle_state=st.checkbox("출처 보기")
    page_number=[x["page_number"] for x in meta_data]
    if page_number[0]==page_number[1]:
        page_number=page_number[0]
    else:
        page_number=str(page_number[0])+", "+str(page_number[1])

    meta_data_str = """
            <b>➡️ 출처 : </b>{}<br><br>
            <b>➡️ 페이지 번호 : </b>{}
        """.format(meta_data[0]["source"], page_number)
    
    if toggle_state:
        st.markdown(meta_data_str, unsafe_allow_html=True)


    st.session_state.message_list.append({"role":"toggle", "content" : meta_data_str})

    

        
    