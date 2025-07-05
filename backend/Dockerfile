# FastAPI + LangChain + FAISS 백엔드용 Dockerfile
FROM python:3.12-slim

# 작업 디렉토리 생성
WORKDIR /app

# requirements.txt 복사 및 패키지 설치
COPY ../requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# FastAPI 서버 실행 (예시: main.py)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 