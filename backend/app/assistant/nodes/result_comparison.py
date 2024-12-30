# result_comparison.py
# 2개 LLM 답변에 대해 최종 답변을 선택하는 노드
from app.history.save_history import connect_db, insert_history, get_history

import sys
sys.path.append("/home/jjw/work/backend")

# 모듈
from app.assistant.state import RagState

# ==================== 답변 score 비교 노드 정의 ====================
def result_comparison_node(state:RagState)->RagState:

    solar_score=state["solar_score"]                                 # solar pro 답변에 대한 점수
    gpt_score=state["gpt_score"]                                     # gpt 답변에 대한 점수

    result_winner="GPT" if gpt_score>=solar_score else "SOLAR"       # gpt 가 크거나 같으면 gpt 를 winner 로 채택
    final_answer=state["gpt_answer"] if result_winner=="GPT" else state["solar_answer"]
    
    # history 저장 
    conn=connect_db()
    insert_history(conn, state["question"], final_answer)

    return RagState(winner=result_winner)                    # 업데이트된 상태 반환











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