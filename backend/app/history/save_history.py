# save_history.py
# 대화 기록 관련된 DB 작업 수행

import psycopg   # PostgreSQL 데이터베이스와 상호작용할 수 있게 해주는 라이브러리
import sys
sys.path.append("/home/jjw/work/backend")

from config import get_settings

# 환경변수 가져오기
config = get_settings()

# ==================== PostgreSQL DB 에 연결 ====================
# 결과가 Connection 객체인데, 이 클래스에 들어가 보면 __ enter __ 과 __ exit __ 메서드가 존재함, cursor() 메서드도 존재함.
def connect_db()->psycopg.Connection:
    connection = psycopg.connect(
            dbname=config.vectordb_DB,
            user=config.vectordb_USER,
            password=config.vectordb_PW,
            host=config.vectordb_HOST,
            port=config.vectordb_PORT
        )   
    
    return connection

# ==================== history 테이블 생성 (1번 만 실행) ====================
# with 구문은 컨텍스트 매니저를 사용하는 구문으로, 자원의 할당과 해제를 자동으로 관리
# with 구문 시작에서 `conn.cursor()` 는 커서 객체를 생성하는 메서드이고 해당 객체가 cursor 변수에 저장됨
# with 구문이 끝나는 시점에서 exit 메서드가 호출되어 `cursor.close()` 가 실행되어 자원 해제
def create_history_table(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE SCHEMA IF NOT EXISTS history_schema;
            CREATE TABLE IF NOT EXISTS history_schema.history_table (
            id SERIAL PRIMARY KEY,
            question TEXT,
            answer TEXT
        );
        """)

        conn.commit()


# ==================== 질문과 답변을 받아 테이블에 데이터 insert ====================
def insert_history(conn, question, answer):
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO history_schema.history_table (question, answer) VALUES (%s, %s); 
        """, (question, answer))

        conn.commit()

# ==================== db 조회하는 함수 ====================
def get_history(conn)->list[tuple]:
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM history_schema.history_table;
        """)
        results=cursor.fetchall()

        return results

# ==================== db 내용 삭제 함수 ====================
# 데이터를 삭제(delete 문)해도 id 는 계속 증가하는 이슈 (원인은 아직 파악X)
# 이를 해결하기 위해 ALTER 구문 수행 (1부터 재시작 하도록)
def delete_history(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            DELETE FROM history_schema.history_table;
            ALTER SEQUENCE history_schema.history_table_id_seq RESTART WITH 1;
        """)

        conn.commit()




# if __name__=="__main__":
#     conn=connect_db()
#     print("db 연결 완료", end="\n\n")
#     # create_history_table(conn)
#     # print("history 테이블 생성 완료")
#     data=get_history(conn)


#     # 최대 출력 길이 설정
#     max_answer_length = 40  # Answer 열 제한 길이
#     max_question_length = 20  # Question 열 제한 길이

#     # 헤더 출력
#     print(f"{'ID':<5} {'Question':<45} {'Answer':<50}")
#     print("-" * 95)

#     # 데이터 출력
#     for row in data:
#         id_, question, answer = row  # 각 요소를 언팩
        
#         # Question이 너무 길면 자르고 "..." 추가
#         if len(question) > max_question_length:
#             question = question[:max_question_length] + "..."
        
#         # Answer를 자르기
#         if len(answer) > max_answer_length:
#             answer = answer[:max_answer_length] + "..."
        
#         # 각 행 출력
#         if id_==1:
#             print(f"{id_:<5} {question:<29} {answer:<50}")
#         elif id_==2:
#             print(f"{id_:<5} {question:<36} {answer:<50}")
#         else:
#             print(f"{id_:<5} {question:<30} {answer:<50}")
    # conn=connect_db()
    # re=get_history(conn)
    # print(re)

