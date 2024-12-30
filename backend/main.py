# main.py
# 메인 파일

# 깃허브 테스트
print("깃허브 테스트 입니다")

from fastapi import FastAPI
import uvicorn

from app.router.api_router import chat_router

# FastAPI 객체 생성
app = FastAPI()

# 라우터 include
app.include_router(chat_router)

# 이 스크립트가 직접 실행될때만 실행
# main 파일의 app 객체 실행
# 포트 8080
# reload=True => 코드변경 시 자동으로 서버 재시작
if __name__ == "__main__":
    
    uvicorn.run("main:app", port=8080, reload=True)

