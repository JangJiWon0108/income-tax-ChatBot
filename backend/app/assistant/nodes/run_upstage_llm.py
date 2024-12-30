# run_upstage_llm.py
# Upstage Solar Pro LLM 을 통해 답변을 생성하는 노드

# 라이브러리
from langchain_core.output_parsers import StrOutputParser
from langchain_upstage import ChatUpstage

import sys
sys.path.append("/home/jjw/work/backend")

# 모듈
from config import get_settings
from app.assistant.templates import llm_answer_prompt
from app.assistant.state import RagState

config = get_settings()

# ==================== Upstage solar pro LLM 로딩 ====================
def load_solar_pro() -> ChatUpstage:
    solar_pro = ChatUpstage(
        api_key=config.UPSTAGE_API, 
        model="solar-pro"
        )
    return solar_pro

# ==================== run_solar_node 노드 정의 ====================
# 질문에 대해 solar pro 답변 생성
def run_solar_node(state : RagState) -> RagState:
    solar_pro = load_solar_pro()                                            # solar pro LLM 로딩
    question = state["question"]                                            # 질문
    context = state["context"]                                              # 리트리브 결과로 나온 chunk
    history = state["history"]                                              # 히스토리
    prompt = llm_answer_prompt()                                            # 프롬프트

    chain = prompt | solar_pro | StrOutputParser()                          # chain 구성

    answer = chain.invoke({"history":history, "question":question, "context":context})         # 답변 생성
    
    print("="*50)
    print("solar pro 답변 :")
    print(answer)
    print("="*50, end="\n\n")

    return RagState(solar_answer=answer)                                     # 업데이트된 상태 반환





# import sys
# import os
# def add_all_parent_and_subdirs():
#     current_dir = os.path.dirname(os.path.abspath(__file__))
    
#     # 상위 디렉토리 추가 (루트까지 올라가기)
#     while current_dir != os.path.dirname(current_dir):  # 루트 디렉토리까지 올라간다
#         if current_dir not in sys.path:
#             sys.path.append(current_dir)
#         current_dir = os.path.dirname(current_dir)
    
#     # 하위 디렉토리들 추가 (현재 디렉토리부터 시작해서 모든 하위 디렉토리 순회)
#     def add_subdirs(path):
#         for subdir in os.listdir(path):
#             subdir_path = os.path.join(path, subdir)
#             if os.path.isdir(subdir_path) and subdir_path not in sys.path:
#                 sys.path.append(subdir_path)
#                 add_subdirs(subdir_path)  # 재귀적으로 하위 디렉토리 순회
    
#     add_subdirs(os.path.dirname(os.path.abspath(__file__)))

# add_all_parent_and_subdirs()




# top 3 df, question, prompt 을 받아 solar pro 답변 return
# def generage_solar_answer(question, df)->str:
    
#     context = "\n\n".join(df["content"])

#     prompt = get_kor_prompt()
#     gpt_4o = load_solar_pro()

#     chain = prompt | gpt_4o | StrOutputParser()

#     answer = chain.invoke({"question":question, "context":context})

#     return answer