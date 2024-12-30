# answer_evaluate.py
# LLM 답변을 평가하는 노드 (1~4점으로 평가)

# 라이브러리
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

import sys
sys.path.append("/home/jjw/work/backend")

# 모듈
from app.assistant.state import RagState
from app.assistant.templates import llm_answer_evaluate_prompt
from config import get_settings

config = get_settings()

# GPT-4 로딩 (JUDGE LLM)
def load_judge_llm()->ChatOpenAI:
    judge_llm=ChatOpenAI(
        api_key = config.OPENAI_API,
        model="gpt-4o"
    )
    return judge_llm

# ==================== solar pro 답변 평가 노드 정의  (JUDGE LLM : GPT-4o) ====================
def solar_answer_evaluate_node(state:RagState) -> RagState:
    question = state["question"]                                       # 질문
    answer=state["solar_answer"]                                       # solar llm 답변
    prompt=llm_answer_evaluate_prompt()                                # 답변 평가 프롬프트
    judge_llm=load_judge_llm()                                         # judge llm 로딩

    chain = prompt | judge_llm | StrOutputParser()                     # chain 구성

    score=chain.invoke({"question":question, "answer":answer})         # 답변 생성 (1~4점 사이의 점수)

    print("="*50)
    print("solar pro 평가 점수 : {}".format(score))
    print("="*50, end="\n\n")

    return RagState(solar_score=score)                                 # 업데이트된 상태 반환

# ==================== gpt 답변 평가 노드 정의 (JUDGE LLM : GPT-4o) ====================
def gpt_answer_evaluate_node(state:RagState) -> RagState:
    question = state["question"]                                       # 질문
    answer=state["gpt_answer"]                                         # gpt 답변
    prompt=llm_answer_evaluate_prompt()                                # 답변 평가 프롬프트
    judge_llm=load_judge_llm()                                         # jugde llm 로딩

    chain = prompt | judge_llm | StrOutputParser()                     # chain 구성

    score=chain.invoke({"question":question, "answer":answer})         # 답변 생성 (1~4점 사이의 점수)

    print("="*50)
    print("gpt 평가 점수 : {}".format(score))
    print("="*50, end="\n\n")
 
    return RagState(gpt_score=score)                                   # 업데이트된 상태 반환








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