# 👔 Mapsee (개인 취향 반영 AI 스마트 옷장)

이 프로젝트는 사용자의 옷장 데이터를 분석하고, 날씨와 상황에 맞는 코디를 추천해주는 AI 패션 어시스턴트입니다.

---

## 🚀 시작하기 (Execution Guide)

애플리케이션을 실행하려면 **백엔드(FastAPI)**와 **프론트엔드(Next.js)** 서버를 각각 실행해야 합니다.

### 1. 백엔드 서버 실행 (Backend - FastAPI)
백엔드는 데이터 분석 및 AI 추천 로직을 담당합니다.

```bash
# 1. Backend 디렉토리로 이동
cd Backend

# 2. 가상환경 활성화 (Mac/Linux)
source .venv/bin/activate

# 3. 서버 실행
uvicorn main_api:app --reload

# 4. env 설정
Backend에 .env 파일을 만들고 아래 키들을 설정해야 정상 작동합니다.
WEATHER_API_KEY=API 키
CLAUDE_API_KEY=API 키

```
*   서버 주소: `http://localhost:8000`
*   API 문서: `http://localhost:8000/docs`


### 2. 프론트엔드 서버 실행 (Frontend - Next.js)
프론트엔드는 사용자 대화형 인터페이스 및 마이페이지를 제공합니다. 프로젝트 **루트 디렉토리**에서 다음을 실행하세요.

```bash
# 1. 의존성 설치 (최초 1회)
npm install

# 2. 개발 서버 실행
npm run dev
```
*   접속 주소: `http://localhost:3000`

---

## ⚙️ 설정 (Configuration)

### API 키 설정
`Backend/.env` 파일을 만들고 아래 키들을 설정해야 정상 작동합니다.
- `CLAUDE_API_KEY`: Anthropic Claude API 키
- `WEATHER_API_KEY`: OpenWeatherMap API 키

### 주요 기능
- **AI 코디 추천**: 날씨와 사용자 기분(mood)을 분석하여 맞춤 스타일 제안
- **스마트 옷장 등록**: 사진 업로드 시 AI가 카테고리, 색상, 소재 자동 분석
- **마이페이지**: 등록된 옷들을 카테고리별로 관리

---

## 🛠 기술 스택
- **Frontend**: Next.js (App Router), TypeScript, Vanilla CSS
- **Backend**: FastAPI (Python), Claude 3.5 Sonnet, OpenWeather API
- **Tooling**: Uvicorn, NPM, Python venv
