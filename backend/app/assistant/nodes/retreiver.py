# retreiver.py
# 사용자 질문에 대해 벡터DB에서 가장 유사한 문서를 찾는 리트리버 노드 정의

import sys
sys.path.append("/home/jjw/work/backend")

# 모듈
from app.rag.rag_job import connect_vectordb, load_upstage_embedding_model
from app.assistant.state import RagState
from app.history.save_history import connect_db, get_history

# ==================== 리트리버 노드 정의 ====================
def retreive_node(state : RagState) -> RagState:
    

    question = state["question"]                                                  # 질문
    embedding_model=load_upstage_embedding_model()                                # 임베딩 모델 로딩
    vector_db=connect_vectordb(embedding_model)                                   # 벡터DB 객체
    retreive_result=vector_db.similarity_search(question, k=2)                    # 가장 유사한 2개 문서 반환 (코사인 유사도)
    result_str="\n\n".join([chunk.page_content for chunk in retreive_result])     # \n\n 로 연결해 문자열화
    meta_data=[chunk.metadata for chunk in retreive_result]                       # 메타데이터 저장 (리스트)


    # history 업데이트
    conn=connect_db()
    history_db=get_history(conn)
    history_str=""
    for row in history_db[:
                          5]:
        history_str+=str(row[1])+":"+str(row[2])+"\n"
    print("히스토리")
    print(history_str)

    # 결과 출력
    print("="*50)
    print("리트리브 결과 :")
    print(retreive_result)
    print("="*50, end="\n\n")

    return RagState(context=result_str, metadata=meta_data, history=history_str)           # 업데이트된 상태 반환










# 테스트
# if __name__=="__main__":
#     question="연봉이 5000만원인 사람의 소득세를 계산해줘"
#     # conn=connect_postgreSQL()
#     # embedding=load_upstage_embedding_model()
#     # df=get_db_and_return_dataframe(conn)
#     # top_3=retreive_top_3(df, question, embedding)

#     embedding_model=load_upstage_embedding_model()
#     vector_db=connect_vectordb(embedding_model)
#     retreive_result=retreive_top_2(vector_db, question)

#     print(retreive_result)
#     print("끝")







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



# def vector_length(vec):
#     return sum([point**2 for point in vec])**(1/2)

# def vector_dot_product(ver1, vec2):
#     return sum(np.array(ver1)*np.array(vec2))

# def cosine_similarity(vec1, vec2):
#     return vector_dot_product(vec1, vec2) / (vector_length(vec1)*vector_length(vec2))

# def apply_cosine_similarity_to_df(row, question):
#     return cosine_similarity(row, question)


# # db 조회 후 df 로 반환
# def get_db_and_return_dataframe(conn):
#     with conn.cursor() as cursor:
#         cursor.execute("""
#             SELECT * FROM a5.vector_table;
#         """)
#         rows=cursor.fetchall()
#         df=pd.DataFrame(
#             rows,
#             columns=["id", "vector", "content", "page_number", "source"],
#         )
    
#     return df

# # 사용자 질문에 대해 코사인 유사도 계산 후 상위 3개 반환
# def retreive_top_3(df, question, embedding_model):
#     df["cosine_similarity"]=df["vector"].apply(lambda row : apply_cosine_similarity_to_df(
#         [float(value) for value in row.replace("[", "").replace("]", "").split(",")],
#         embedding_model.embed_query(question)
#     ))
#     df_top_3=df.sort_values(by=["cosine_similarity"], ascending=False).head(3).reset_index(drop=True)

#     return df_top_3
