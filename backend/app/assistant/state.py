# state.py
# LangGraph 상태(State) 정의

from typing import TypedDict

# 상태 정의
class RagState(TypedDict):
    question : str             # 사용자 질문
    context : str              # 리트리브 결과로 나온 chunk의 page_content
    metadata : list            # 리트리브 결과로 나온 chunk의 metadata
    solar_answer : str         # Upstage Solar Pro LLM 답변
    solar_score : str          # Upstage Solar Pro LLM 답변에 대한 점수
    gpt_answer : str           # GPT 답변
    gpt_score : str            # GPT 답변에 대한 점수
    winner : str               # 점수 비교해서 높은 LLM

    history : str             # 대화 기록









# 2
# Annotated[자료형, "설명"]
# class RagState(TypedDict):
#     question : Annotated[str, "설명"] 
#     context : Annotated[str, "설명"]
#     hcx_answer : Annotated[str, "설명"] 
#     hcx_score : Annotated[str, "설명"]
#     gpt_answer : Annotated[str, "설명"] 
#     gpt_score : Annotated[str, "설명"]
#     winner : Annotated[str, "설명"]