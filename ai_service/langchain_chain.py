import os
from langchain.chat_models import init_chat_model

# OpenAI API 키 체크 (환경변수에서만)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY:
    # LLM 모델 초기화
    model = init_chat_model("gpt-4o-mini", model_provider="openai")
    
    # 텍스트 요약 함수
    def summarize_text(text: str) -> str:
        try:
            response = model.invoke(f"다음 텍스트를 한국어로 요약해주세요:\n\n{text}")
            return response.content
        except Exception as e:
            return f"요약 중 오류 발생: {str(e)}"
    
    # 간단한 벡터 검색 함수 (FAISS 없이 우선 구현)
    def store_and_search(texts: list[str], query: str):
        # 임시로 간단한 키워드 매칭
        results = []
        for text in texts:
            if query.lower() in text.lower():
                results.append(text)
        return results[:3]  # 최대 3개 결과

else:
    print("⚠️  OPENAI_API_KEY가 설정되지 않았습니다.")
    
    def summarize_text(text: str) -> str:
        return "API 키가 설정되지 않아 요약을 수행할 수 없습니다."
    
    def store_and_search(texts: list[str], query: str):
        return ["API 키가 설정되지 않아 검색을 수행할 수 없습니다."]

# 테스트 코드
if __name__ == "__main__":
    sample_text = "LangChain은 LLM 기반 애플리케이션을 쉽게 만들 수 있는 파이썬 프레임워크입니다."
    print("[요약 결과]")
    print(summarize_text(sample_text))
    
    print("\n[검색 결과]")
    results = store_and_search([sample_text], "LangChain")
    for r in results:
        print("-", r)
