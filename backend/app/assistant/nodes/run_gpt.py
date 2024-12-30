# run_gpt.py
# GPT-4o 를 통해 답변을 생성하는 노드

# 라이브러리
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

import sys
sys.path.append("/home/jjw/work/backend")

# 모듈
from config import get_settings
from app.assistant.templates import llm_answer_prompt
from app.assistant.state import RagState

config = get_settings()

# ==================== gpt 4o 로딩 ====================
def load_gpt_4o() -> ChatOpenAI:
    gpt_4o=ChatOpenAI(
        api_key = config.OPENAI_API,
        model = "gpt-4o"
    )
    return gpt_4o

# ====================  run_gpt_node 노드 정의 ====================
# 질문에 대해 gpt 답변 생성
def run_gpt_node(state : RagState) -> RagState:
    gpt_4o = load_gpt_4o()                                                  # gpt 로딩
    question = state["question"]                                            # 질문
    context = state["context"]                                              # 리트리브 결과로 나온 chunk
    history = state["history"]                                              # 히스토리
    prompt = llm_answer_prompt()                                            # 프롬프트 로딩

    chain = prompt | gpt_4o | StrOutputParser()                              # chain 구성

    answer = chain.invoke({"history":history, "question":question, "context":context})      # 답변 생성

    print("="*50)
    print("gpt 답변 :")
    print(answer)
    print("="*50, end="\n\n")

    return RagState(gpt_answer=answer)                                   # 업데이트된 상태 반환






# 테스트
# if __name__=="__main__":
#     documents=load_and_split("/home/jjw/work/backend/app/rag/소득세법_55조.pdf")
#     em=load_embedding_model()
#     conn=connect_postgreSQL()
#     create_vector_table(conn)
#     insert_vetcor_data(conn, documents, em)

#     print(2)

#     cursor = connect_postgreSQL().cursor()
#     cursor.execute("""
#         SELECT * FROM a4.vector_table;
#     """)
#     rows = cursor.fetchall()
#     for row in rows:
#         print(row)

#     # 테스트
#     question="장기주택저당차입금 이자 상환액의 소득공제에 관한 경과조치"
#     conn=connect_postgreSQL()
#     embedding=load_embedding_model()
#     df=get_db_and_return_dataframe(conn)
#     top_3=retreive_top_3(df, question, embedding)


#     print(top_3[["content", "page_number", "cosine_similarity"]])

#     print("="*30)
#     print("리트리버 완료")

#     answer=generage_gpt_answer(question, top_3)
#     print("="*30)
#     print("답변")
#     print(answer)






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


# # top 3 df, question, prompt 을 받아 hcx 답변 return
# def generage_gpt_answer(question, df)->str:
    
#     context = "\n\n".join(df["content"])

#     prompt = get_kor_prompt()
#     gpt_4o = load_gpt_4o_mini()

#     chain = prompt | gpt_4o | StrOutputParser()

#     answer = chain.invoke({"question":question, "context":context})

#     return answer