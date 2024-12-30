# config.py
# .env 파일에서 값을 로드하여 설정을 초기화 하여서
# 여러 외부 서비스와의 통합을 지원하는 설정 관리 모듈

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Pydantic 의 BaseSettings 클래스를 상속
# 예를 들어 app_name 은 str 타입으로 설정되어 있으므로,
# 다른 타입이 주어지면 로드 시 오류가 발생
# 각 항목은 .env 파일에서 값을 로드함
class Settings(BaseSettings):

    # Hyper Clover X 관련
    hcx_api_base : str
    hcx_clovastudio_api_key : str
    hcx_apigw_api_key : str
    hcx_max_output_tokens : int

    # Naver 임베딩 관련
    emb_api_base : str
    emb_clovastudio_api_key : str
    emb_apigw_api_key : str
    emb_app_id : str

    # pgvector 접속 관련 (벡터DB)
    vectordb_schema_name = 'abc'
    vectordb_HOST : str
    vectordb_PORT : int
    vectordb_DB : str
    vectordb_USER : str
    vectordb_PW : str
    vectordb_search_path : str
    vectordb_schema_name : str

    # Upstage API 키
    UPSTAGE_API : str

    # OpenAI API 키
    OPENAI_API : str
    
    # Pydantic의 SettingsConfigDict를 사용하여
    # .env 파일을 읽을 때 사용할 설정을 정의
    # .env 파일의 인코딩 방식을 utf-8 로 설정해
    # 해당 파일을 통해 환경 변수를 로드
    model_config = SettingsConfigDict(
            env_file=".env", 
            env_file_encoding="utf-8",
        )
    
    # hash 메서드
    # 객체를 해시 가능한 형태로 만들기 위해 사용
    # lru_cache는 입력값을 기준으로 함수의 결과를 캐싱
    # 이때 입력값이 해시 가능한 객체여야 효율적으로 캐싱할 수 있습니다.
    def __hash__(self):
        return hash((self.name, ...))
    

# lru_cache 데코레이터가 적용된 함수는
# 설정을 한 번 로드한 후에는 캐시하여 성능을 최적화
@lru_cache
def get_settings():
    load_dotenv()
    return Settings()