# api_router.py
# run 경로 post 요청 시 처리
# 사용자 질문에 대해 LLM 답변을 return

from fastapi import APIRouter

import sys
sys.path.append("/home/jjw/work/backend")

from schema import UserQuestion
from app.assistant.graph import compile_graph
from app.assistant.state import RagState

# 라우터 객체 생성
chat_router = APIRouter()

# /run 경로 post 요청 시 수행
@chat_router.post("/run")
async def chatbot_run(user_question : UserQuestion) -> dict:
    
    # LangGraph 컴파일된 객체
    app = compile_graph()
    
    # invoke 로 실행
    inputs = RagState(question=user_question.question)
    outputs = app.invoke(input=inputs)

    # 최종 답변 선택
    chatbot_answer=outputs["gpt_answer"] if outputs["winner"]=="GPT" else outputs["solar_answer"]

    # 메타 데이터
    meta_data=outputs["metadata"]

    return {"chatbot_answer": chatbot_answer, "meta_data": meta_data}





