import os
from typing import List, Dict, Any
from langchain.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model



# OpenAI API 키 체크
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@tool
def calculate_sum(a: int, b: int) -> int:
    """두 숫자의 합을 계산합니다."""
    return a + b

@tool
def get_weather(city: str) -> str:
    """특정 도시의 날씨 정보를 가져옵니다."""
    # 실제로는 날씨 API를 호출하겠지만, 여기서는 예시로 고정값 반환
    weather_data = {
        "서울": "맑음, 15도",
        "부산": "흐림, 18도",
        "제주": "비, 12도"
    }
    return weather_data.get(city, f"{city}의 날씨 정보를 찾을 수 없습니다.")

@tool
def search_documents(query: str) -> List[str]:
    """문서에서 특정 키워드를 검색합니다."""
    # 예시 문서 데이터
    documents = [
        "LangChain은 LLM 기반 애플리케이션을 쉽게 만들 수 있는 프레임워크입니다.",
        "FastAPI는 Python으로 API를 빠르게 구축할 수 있는 웹 프레임워크입니다.",
        "Docker는 컨테이너 기반 가상화 플랫폼입니다.",
        "gRPC는 고성능 RPC 프레임워크입니다."
    ]
    
    # 키워드가 포함된 문서 검색
    results = [doc for doc in documents if query.lower() in doc.lower()]
    return results[:3]  # 최대 3개 결과

@tool
def create_summary(text: str) -> str:
    """주어진 텍스트를 요약합니다."""
    if len(text) > 100:
        return text[:100] + "... (요약됨)"
    return text

@tool
def translate_text(text: str, target_language: str) -> str:
    """텍스트를 다른 언어로 번역합니다."""
    # 실제로는 번역 API를 사용하겠지만, 여기서는 예시
    translations = {
        "english": f"[영어 번역] {text}",
        "japanese": f"[일본어 번역] {text}",
        "chinese": f"[중국어 번역] {text}"
    }
    return translations.get(target_language.lower(), f"{target_language}로 번역: {text}")

# 툴 리스트
tools = [
    calculate_sum,
    get_weather,
    search_documents,
    create_summary,
    translate_text
]

def create_agent_with_tools():
    """툴을 사용할 수 있는 LangChain 에이전트를 생성합니다."""
    if not OPENAI_API_KEY:
        print("⚠️  OPENAI_API_KEY가 설정되지 않았습니다.")
        return None
    
    # LLM 모델 초기화
    llm = init_chat_model("gpt-4o-mini", model_provider="openai")
    
    # 프롬프트 템플릿
    prompt = ChatPromptTemplate.from_messages([
        ("system", """당신은 다양한 도구를 사용할 수 있는 AI 어시스턴트입니다.
        사용자의 요청을 분석하고 적절한 도구를 선택해서 실행하세요.
        
        사용 가능한 도구들:
        - calculate_sum: 두 숫자의 합을 계산
        - get_weather: 도시의 날씨 정보 조회
        - search_documents: 문서에서 키워드 검색
        - create_summary: 텍스트 요약
        - translate_text: 텍스트 번역
        """),
        ("user", "{input}"),
        ("assistant", "{agent_scratchpad}")
    ])
    
    # 에이전트 생성
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    return agent_executor

def run_agent_with_query(query: str):
    """사용자 쿼리를 받아서 에이전트를 실행합니다."""
    agent_executor = create_agent_with_tools()
    
    if agent_executor is None:
        return "에이전트를 생성할 수 없습니다. API 키를 확인해주세요."
    
    try:
        result = agent_executor.invoke({"input": query})
        return result["output"]
    except Exception as e:
        return f"에러 발생: {str(e)}"

# 테스트 함수
def test_tools():
    """다양한 툴 테스트"""
    print("🔧 LangChain Tools 테스트 시작\n")
    
    test_queries = [
        "5와 3의 합을 계산해주세요",
        "서울의 날씨를 알려주세요",
        "LangChain에 대한 문서를 검색해주세요",
        "이 텍스트를 영어로 번역해주세요: 안녕하세요",
        "FastAPI는 Python으로 API를 빠르게 구축할 수 있는 웹 프레임워크입니다. 이 텍스트를 요약해주세요"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"[테스트 {i}] {query}")
        result = run_agent_with_query(query)
        print(f"결과: {result}\n")
        print("-" * 50)

if __name__ == "__main__":
    test_tools() 