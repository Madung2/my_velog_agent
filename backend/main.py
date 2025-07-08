from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import json

app = FastAPI(title="My Velog Agent API", version="0.1.0")

# Gmail API 설정
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CREDENTIALS_FILE = 'credentials.json'  # Google Cloud Console에서 다운로드
TOKEN_FILE = 'token.json'

@app.get("/")
async def root():
    return {"message": "🚀 My Velog Agent API가 실행 중입니다!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "backend"}

# Gmail 인증 시작
@app.get("/auth/gmail")
async def gmail_auth():
    """Gmail OAuth 인증을 시작합니다."""
    try:
        flow = Flow.from_client_secrets_file(
            CREDENTIALS_FILE,
            scopes=SCOPES,
            redirect_uri='http://localhost:8000/auth/gmail/callback'
        )
        
        auth_url, _ = flow.authorization_url(prompt='consent')
        return {"auth_url": auth_url, "message": "이 URL로 이동해서 인증하세요"}
        
    except FileNotFoundError:
        raise HTTPException(
            status_code=404, 
            detail="credentials.json 파일이 없습니다. Google Cloud Console에서 다운로드하세요."
        )

# Gmail 인증 콜백
@app.get("/auth/gmail/callback")
async def gmail_callback(code: str):
    """Gmail OAuth 콜백을 처리합니다."""
    try:
        flow = Flow.from_client_secrets_file(
            CREDENTIALS_FILE,
            scopes=SCOPES,
            redirect_uri='http://localhost:8000/auth/gmail/callback'
        )
        
        flow.fetch_token(code=code)
        
        # 토큰 저장
        creds = flow.credentials
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
        
        return {"message": "✅ Gmail 인증 완료!", "status": "success"}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"인증 실패: {str(e)}")

# Gmail 이메일 목록 조회
@app.get("/gmail/messages")
async def get_gmail_messages(max_results: int = 10):
    """Gmail 이메일 목록을 가져옵니다."""
    creds = None
    
    # 저장된 토큰 로드
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # 토큰이 없거나 만료된 경우
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise HTTPException(
                status_code=401, 
                detail="인증이 필요합니다. /auth/gmail 엔드포인트를 먼저 호출하세요."
            )
    
    try:
        # Gmail API 서비스 생성
        service = build('gmail', 'v1', credentials=creds)
        
        # 이메일 목록 조회
        results = service.users().messages().list(
            userId='me', 
            maxResults=max_results
        ).execute()
        
        messages = results.get('messages', [])
        
        # 각 메시지의 상세 정보 가져오기
        email_list = []
        for message in messages:
            msg = service.users().messages().get(
                userId='me', 
                id=message['id']
            ).execute()
            
            # 헤더에서 제목과 발신자 추출
            headers = msg['payload'].get('headers', [])
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
            
            email_list.append({
                "id": message['id'],
                "subject": subject,
                "sender": sender,
                "snippet": msg.get('snippet', '')
            })
        
        return {
            "total_messages": len(email_list),
            "messages": email_list
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gmail API 오류: {str(e)}")

# 특정 이메일 내용 조회
@app.get("/gmail/messages/{message_id}")
async def get_gmail_message(message_id: str):
    """특정 Gmail 이메일의 전체 내용을 가져옵니다."""
    creds = None
    
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    if not creds or not creds.valid:
        raise HTTPException(status_code=401, detail="인증이 필요합니다.")
    
    try:
        service = build('gmail', 'v1', credentials=creds)
        
        # 메시지 상세 정보 조회
        message = service.users().messages().get(
            userId='me', 
            id=message_id,
            format='full'
        ).execute()
        
        return {
            "id": message_id,
            "message": message
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"이메일 조회 오류: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 