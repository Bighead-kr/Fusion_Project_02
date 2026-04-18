from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# 사용자님이 만든 핵심 로직 파일에서 함수들을 가져옵니다.
from integrated_closet_system import expert_recommend_algorithm, get_current_temp

app = FastAPI()

# ==========================================
# 1. CORS 설정 (프론트엔드 Next.js 접속 허용)
# ==========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 모든 곳에서 접속 허용 (실습용)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 2. 이미지 폴더 개방 (Next.js에서 사진을 볼 수 있게 함)
# ==========================================
# http://localhost:8000/images/cloth1.jpg 식으로 접근 가능해집니다.
app.mount("/images", StaticFiles(directory="upload_images"), name="images")

# ==========================================
# 3. 날씨 정보 API
# ==========================================
@app.get("/weather")
async def weather_api():
    temp, desc = get_current_temp()
    return {
        "status": "success",
        "temp": temp,
        "description": desc
    }

# ==========================================
# 4. 코디 추천 API (핵심!)
# ==========================================
@app.get("/recommend")
async def recommend_api(situation: str = "일상", mood: str = "캐주얼"):
    """
    Next.js에서 상황과 무드를 보내면 추천 결과를 JSON으로 반환합니다.
    사용법: /recommend?situation=결혼식&mood=단정한/포멀
    """
    temp, desc = get_current_temp()
    
    # 우리가 만든 12만 데이터 알고리즘 실행
    result = expert_recommend_algorithm(temp, situation, mood)
    
    # 결과가 딕셔너리(성공)인 경우 이미지 경로를 웹 주소(URL)로 바꿔줍니다.
    if isinstance(result, dict):
        for item in result['items']:
            file_name = os.path.basename(item['image_path'])
            # Next.js가 읽을 수 있는 전체 URL 주소 생성
            item['image_url'] = f"http://localhost:8000/images/{file_name}"
        
        return {
            "status": "success",
            "weather": {"temp": temp, "desc": desc},
            "recommendation": result
        }
    else:
        # 에러 메시지(트리거 차단 등) 반환
        return {
            "status": "error", 
            "message": result
        }

# 실행 방법: 터미널에 uvicorn main_api:app --reload 입력