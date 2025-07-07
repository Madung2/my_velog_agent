# LangChain + FAISS gRPC AI 서비스 서버용 Dockerfile
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# pyproject.toml 복사
COPY pyproject.toml ./

# 의존성만 설치 (패키지 빌드 없이)
RUN uv pip install --system --no-cache \
    fastapi \
    uvicorn \
    "langchain[openai]" \
    openai \
    faiss-cpu \
    grpcio \
    grpcio-tools \
    python-dotenv \
    pydantic \
    httpx

# ai_service 소스 코드 복사
COPY ai_service/ ./

# gRPC 서버 실행 예시 (main.py)
CMD ["python", "main.py"]
