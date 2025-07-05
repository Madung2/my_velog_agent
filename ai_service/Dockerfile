# LangChain + FAISS gRPC AI 서비스 서버용 Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY ../requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

# gRPC 서버 실행 예시 (main.py)
CMD ["python", "main.py"]
