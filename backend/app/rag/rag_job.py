# rag_job.py
# rag 관련 (pdf ocr, 스플릿, 임베딩, 벡터DB 저장)

# 라이브러리
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_upstage import UpstageEmbeddings
from langchain_postgres.vectorstores import PGVector  # PostgreSQL 기반 벡터 데이터베이스와 상호작용
from sqlalchemy import create_engine                  # 데이터베이스와의 연결을 설정 
import requests

# 모듈
from config import get_settings

# 환경변수 
config = get_settings()


# ==================== Upstage OCR 을 통해 pdf 읽어오는 함수 ====================
def load_with_upstage_ocr(file_name_1:str, file_name_2:str)->Document:
    # 아래 코드는 Upstage 공식 문서에서 제공
    api=config.UPSTAGE_API
    url = "https://api.upstage.ai/v1/document-ai/ocr"   
    headers = {"Authorization": f"Bearer {api}"}

    # 한 번에 받아올 수 있는 page 가 최대 20 이라서, 2번 나눠서 받음
    files_1 = {"document": open(file_name_1, "rb")}
    files_2 = {"document": open(file_name_2, "rb")}

    response_1 = requests.post(url, headers=headers, files=files_1) 
    response_2 = requests.post(url, headers=headers, files=files_2) 

    # 결과를 json(딕셔너리) 형태로
    ocr_result_1 = response_1.json()
    ocr_result_2 = response_2.json()

    # 결과를 저장할 변수
    documents = []

    # pages 에 각 페이지마다의 정보가 저장되어있음, page는 페이지 번호(0부터 시작), text는 해당 페이지 텍스트
    for page in ocr_result_1['pages']:
        page_number = page['id'] + 1    # 페이지 번호는 0부터 시작하므로 1을 더함
        page_content = page['text']     # 텍스트 추출
        
        # Document 형식으로 변환
        documents.append(Document(
            metadata = {
                "source" : "소득세법 [시행 2024. 7. 1.] [법률 제19933호, 2023. 12. 31., 일부개정]", 
                "page_number":page_number
            },
            page_content = page_content
        ))
    
    for page in ocr_result_2['pages']:
        page_number = page['id'] + 21    # 21페이지 부터 저장
        page_content = page['text']
        
        documents.append(Document(
            metadata = {
                "source" : "소득세법 [시행 2024. 7. 1.] [법률 제19933호, 2023. 12. 31., 일부개정]", 
                "page_number":page_number
            },
            page_content = page_content
        ))


    return documents

# ==================== 텍스트 스플릿 함수 ====================
# 토큰 제한이 있는 LLM 에 여러 문장을 참고해 답변할 수 있도록 문서를 스플릿
# chunk_size : 청크 길이 len
# chunk_overlap : 각 청크 간 겹치는 부분의 크기
def text_split(documents:Document)->Document:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200,
    )
    chunks = text_splitter.split_documents(documents)

    return chunks


# ==================== Upstage 임베딩 모델 로딩 ====================
def load_upstage_embedding_model()->UpstageEmbeddings:
    embedding_model = UpstageEmbeddings(
        api_key=config.UPSTAGE_API,
        model="solar-embedding-1-large",
    )

    return embedding_model


# ==================== 벡터 db 연결 및 생성 ====================
# postgreSQL DB에 연결 후 pgvector 생성
# postgreSQL 에 접속해 DB 는 이미 만들었다는 가정
def connect_vectordb(embedding_model)->PGVector:

    # 데이터베이스 연결 문자열
    connection_string = (
        f"postgresql+psycopg://{config.vectordb_USER}:{config.vectordb_PW}@"
        f"{config.vectordb_HOST}:{config.vectordb_PORT}/{config.vectordb_DB}"
        f"?options=-c search_path={config.vectordb_search_path}"
    )
    
    # create_engine : 데이터베이스 연결을 설정하는 함수
    # 연결은 애플리케이션과 DB간의 통신 세션을 의미
    # 연결을 정의
    engine = create_engine(
        connection_string,
        pool_size=10,                    # 기본적으로 유지할 연결의 수
        max_overflow=20,                 # 기본 풀 크기를 초과하여 추가로 생성할 수 있는 연결의 수 (10+20=30 개 가능)
        pool_timeout=30,                 # 연결 풀이 고갈되었을 때 새 연결을 얻기 위해 대기할 최대 시간 설정(30초 넘으면 에러)
        pool_pre_ping=True,              # 연결이 유효한지 미리 확인하도록 설정. 유효하지 않은 경우 새로운 연결을 생성
        pool_recycle=1800,               # 일정 시간(30분) 동안 사용되지 않은 연결을 자동으로 새 연결로 교체 (연결이 끊어지지 않도록)
        pool_reset_on_return='rollback'  # 커밋되지 않은 사항이 있다면, 반환 시 커밋하지 않고 롤백(초기화)
    )

    # PGVector 객체 생성
    # collection_name 은 벡터 데이터를 논리적으로 그룹화하기 위한 이름
    # 소득세법 pdf 데이터를 'rag_collection' 에 저장
    vectordb =  PGVector(
        connection=engine,
        embeddings=embedding_model,
        collection_name="rag_collection"
    )   

    return vectordb



# ==================== 벡터 db에 데이터 삽입 ====================
# add_documents() 메서드를 이용
def insert_data(vectordb, chunks):

    vectordb.add_documents(chunks)


# ==================== 벡터 db 구축 ====================
# rag_job.py 파일이 직접 실행될 때, 아래 실행
# 벡터DB 구축하는 과정을 수행하기 위함
if __name__=="__main__":
    print("벡터DB 구축 시작")
    documents=load_with_upstage_ocr(
        "/home/jjw/work/backend/app/rag/소득세법(1_55)_1.pdf",
        "/home/jjw/work/backend/app/rag/소득세법(1_55)_2.pdf"
    )
    print("PDF OCR 완료")

    chunks=text_split(documents)
    print("text split 완료")

    em=load_upstage_embedding_model()
    vector_db=connect_vectordb(em)
    print("db 연결 완료")
    
    insert_data(vector_db, chunks)
    print("데이터 insert 완료")

    print("유사도 검색 테스트")
    chunk=vector_db.similarity_search("거주자의 종합소득에 대한 소득세", k=1)
    page_content=chunk[0].page_content[500:700]
    source=chunk[0].metadata["source"]
    page=chunk[0].metadata["page_number"]

    print("="*50)
    print("page content")
    print("="*50)
    print(page_content, end="\n\n")

    print("="*50)
    print("source")
    print("="*50)
    print(source, end="\n\n")

    print("="*50)
    print("page number")
    print("="*50)
    print(page)




    # insert_data(vector_db, chunks)

    # conn=connect_postgreSQL()
    # create_vector_table(conn)
    # insert_vetcor_data(conn, chunks, em)

    # cursor = connect_postgreSQL().cursor()
    # cursor.execute("""
    #     SELECT * FROM a5.vector_table;
    # """)

    # rows = cursor.fetchall()
    # for row in rows:
    #     print(row)


# # 데이터베이스 연결
# def connect_postgreSQL():
#     conn = psycopg.connect(
#         dbname="PostgreSQL_db",
#         user="postgres",
#         password="0108",
#         host="localhost"
#     )   
    
#     return conn

# # 벡터 테이블 생성
# def create_vector_table(conn):
#     with conn.cursor() as cursor:
#         cursor.execute("""
#                 CREATE EXTENSION IF NOT EXISTS vector;
#                 DROP SCHEMA IF EXISTS a5 CASCADE;
#                 CREATE SCHEMA a5;
#                 CREATE TABLE a5.vector_table (
#                 id SERIAL PRIMARY KEY,
#                 vector VECTOR(4096),
#                 content TEXT,
#                 page_number INT,
#                 source TEXT
#             );
#         """)
#         conn.commit()

# # 벡터 테이블에 값 INSERT
# def insert_vetcor_data(conn, documents, embedding_model):
#     with conn.cursor() as cursor:
#         count=1
#         for chunk in documents:
#             cursor.execute("""
#                     INSERT INTO a5.vector_table (vector, content, page_number, source)
#                     VALUES (%s, %s, %s, %s);
#             """,
#               (
#                   embedding_model.embed_query(chunk.page_content),
#                   chunk.page_content,
#                   chunk.metadata["page_number"],
#                   chunk.metadata["source"]
#               )
#             )
#             print("{} ...  완료".format(count))
#             count+=1
#         conn.commit()

    
# import sys
# sys.path.append('/home/jjw/work')
# # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


# PDF 로딩 및 텍스트 스플릿
# def load_and_split(file_name:str)->list:
#     # 1. pdf 로딩
#     load_pdf = PyPDFium2Loader(file_name)
#     documents = load_pdf.load()

#     # 2. 텍스트 스플릿
#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=1000, 
#         chunk_overlap=200,
#     )


#     chunks = text_splitter.split_documents(documents)

#     return chunks



# # 임베딩 모델 로딩
# # hcx는 1024 차원으로 임베딩
# def load_embedding_model():
#     max_tokens=2048
#     embedding_model = HCXEmbeddings(
#         api_base=config.emb_api_base,
#         clovastudio_api_key=config.emb_clovastudio_api_key,
#         apigw_api_key=config.emb_apigw_api_key,
#         app_id=config.emb_app_id,
#         max_tokens=max_tokens
#     )

#     return embedding_model