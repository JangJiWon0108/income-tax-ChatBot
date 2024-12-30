# schema.py
# FastAPI 스키마 정의

from pydantic import BaseModel

class UserQuestion(BaseModel):
    question : str
