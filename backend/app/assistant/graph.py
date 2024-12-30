# graph.py
# LangGraph 노드 추가, 엣지 연결, 컴파일 

from langgraph.graph import StateGraph, END 

import sys
sys.path.append("/home/jjw/work/backend")

from app.assistant.state import RagState
from app.assistant.nodes.retreiver import retreive_node
from app.assistant.nodes.run_gpt import run_gpt_node
from app.assistant.nodes.run_upstage_llm import run_solar_node
from app.assistant.nodes.answer_evaluate import solar_answer_evaluate_node, gpt_answer_evaluate_node
from app.assistant.nodes.result_comparison import result_comparison_node

# ==================== 그래프(노드, 엣지) 정의 및 컴파일 ===================
def compile_graph() -> StateGraph:

    # StateGraph 객체 생성
    workflow=StateGraph(RagState)

    # 노드 추가
    workflow.add_node("retrieve", retreive_node)                                # 리트리브 노드
    workflow.add_node("run_solar_pro", run_solar_node)                          # solar pro 답변 생성 노드 
    workflow.add_node("run_GPT", run_gpt_node)                                  # gpt 답변 생성 노드
    workflow.add_node("solar_pro_evaluate", solar_answer_evaluate_node)         # solar pro 답변 평가 노드 
    workflow.add_node("GPT_evaluate", gpt_answer_evaluate_node)                 # gpt 답변 평가 노드
    workflow.add_node("result_compare", result_comparison_node)                 # 결과 비교 노드
    
    # 엣지 연결
    workflow.add_edge("retrieve", "run_solar_pro")                              
    workflow.add_edge("retrieve", "run_GPT")
    workflow.add_edge("run_solar_pro", "solar_pro_evaluate")
    workflow.add_edge("run_GPT", "GPT_evaluate")
    workflow.add_edge("solar_pro_evaluate", "result_compare")
    workflow.add_edge("GPT_evaluate", "result_compare")
    workflow.add_edge("result_compare", END)

    # 시작점 설정
    workflow.set_entry_point("retrieve")

    # 그래프 컴파일 
    app = workflow.compile()

    # 그래프 이미지 저장
    # graph_image = app.get_graph().draw_mermaid_png()
    # image_path = "graph_image.png"  # 저장할 경로 지정
    # with open(image_path, "wb") as f:
    #     f.write(graph_image)

    return app








# if __name__=="__main__":

#     user_question = "거주자와 비거주자의 차이점은 무엇이며, 이들이 부담하는 소득세 납세의무(과세 범위)에는 어떤 차이가 있는지 자세하고 자세하게 설명해줘"

#     app=compile_graph()

#     graph_image = app.get_graph().draw_mermaid_png()

#     # 이미지를 파일로 저장
#     image_path = "graph_image.png"  # 저장할 경로 지정
#     with open(image_path, "wb") as f:
#         f.write(graph_image)

#     inputs = RagState(question=user_question)

#     outputs = app.invoke(input=inputs)

#     # 결과 출력
#     print(outputs["gpt_answer"])
#     print("Question : \t", outputs["question"])
#     print("HCX Answer : \t", outputs["solar_answer"])
#     print("HCX Score : \t", outputs["solar_score"])
#     print("GPT Answer : \t", outputs["gpt_answer"])
#     print("GPT Score : \t", outputs["gpt_score"])
#     print("Winner : \t", outputs["winner"])
    
    # final_answer=outputs["solar_answer"] if outputs["winner"]=="SOLAR" else outputs["gpt_answer"]
    
    # print("리트리버 결과")
    # print(outputs["context"])
    # print(outputs["metadata"])
    # print("\n최종 답변")
    # print(final_answer)

    # print(outputs["solar_answer"])
    # print(outputs["solar_score"])
    # print(outputs["gpt_answer"])
    # print(outputs["gpt_score"])





