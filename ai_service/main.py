import time
import os
from langchain_chain import summarize_text, store_and_search
from ai_service.langchain_tool_test import test_tools, run_agent_with_query

def main():
    print("🚀 AI Service 시작됨!")
    print("LangChain 테스트 중...")
    
    # OpenAI API 키 확인
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY가 설정되지 않았습니다.")
        print("환경변수를 설정하거나 .env 파일을 생성해주세요.")
    else:
        print("✅ OPENAI_API_KEY 확인됨")
        
        # 기본 LangChain 테스트
        sample_text = "LangChain은 LLM 기반 애플리케이션을 쉽게 만들 수 있는 프레임워크입니다."
        try:
            print("\n[기본 요약 테스트]")
            summary = summarize_text(sample_text)
            print(f"요약 결과: {summary}")
            
            print("\n[기본 FAISS 벡터 검색 테스트]")
            results = store_and_search([sample_text], "LangChain")
            print(f"검색 결과: {results}")
            
        except Exception as e:
            print(f"❌ 기본 테스트 에러: {e}")
        
        # LangChain Tools 테스트
        try:
            print("\n" + "="*50)
            print("🔧 LangChain Tools 테스트 시작")
            print("="*50)
            
            # 간단한 툴 테스트
            test_query = "5와 3의 합을 계산해주세요"
            print(f"\n[툴 테스트] {test_query}")
            result = run_agent_with_query(test_query)
            print(f"결과: {result}")
            
        except Exception as e:
            print(f"❌ 툴 테스트 에러: {e}")
    
    print("\n🔄 AI Service 대기 중... (Ctrl+C로 종료)")
    
    # 서비스 유지를 위한 무한 루프
    try:
        while True:
            time.sleep(10)
            print("💡 AI Service 실행 중...")
    except KeyboardInterrupt:
        print("\n👋 AI Service 종료")

if __name__ == "__main__":
    main()
