from fastapi import FastAPI, Query, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import shutil
import json

# 사용자님이 만든 핵심 로직 파일에서 함수들을 가져옵니다.
from integrated_closet_system import expert_recommend_algorithm, get_current_temp, analyze_and_save

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
UPLOAD_DIR = "upload_images"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app.mount("/images", StaticFiles(directory=UPLOAD_DIR), name="images")

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
async def recommend_api(
    situation: str = "일상", 
    mood: str = "캐주얼", 
    bypass_filter: bool = Query(False)
):
    """
    Next.js에서 상황과 무드를 보내면 추천 결과를 JSON으로 반환합니다.
    bypass_filter가 true이면 패션 관련 질문인지 확인하는 트리거를 건너뜁니다.
    """
    temp, desc = get_current_temp()
    
    # 우리가 만든 12만 데이터 알고리즘 실행
    result = expert_recommend_algorithm(temp, situation, mood, bypass_filter=bypass_filter)
    
    # 결과가 딕셔너리(성공)인 경우 이미지 경로를 웹 주소(URL)로 바꿔줍니다.
    if isinstance(result, dict):
        for item in result['items']:
            file_name = item['image_path'].replace('\\', '/').split('/')[-1]
            item['image_url'] = f"http://localhost:8000/images/{file_name}"
        
        return {
            "status": "success",
            "weather": {"temp": temp, "desc": desc},
            "recommendation": result
        }
    else:
        return {
            "status": "error", 
            "message": result
        }

# ==========================================
# 5. 옷장 데이터 API
# ==========================================
@app.get("/closet")
async def get_closet():
    """등록된 모든 옷 목록을 반환합니다."""
    if not os.path.exists("closet.json"):
        return {"status": "success", "items": []}
        
    with open("closet.json", "r", encoding="utf-8") as f:
        closet = json.load(f)
        
    for item in closet:
        file_name = item['image_path'].replace('\\', '/').split('/')[-1]
        item['image_url'] = f"http://localhost:8000/images/{file_name}"
        
    return {"status": "success", "items": closet}

# ==========================================
# 6. 이미지 업로드 및 분석 API
# ==========================================
@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """이미지를 서버에 저장하고 Claude AI로 분석하여 옷장에 등록합니다."""
    # 1. 파일 저장
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 2. AI 분석 및 저장 실행
    try:
        # analyze_and_save 내부에서 closet.json에 기록함
        analyze_and_save(file_path)
        
        # 최신 등록된 아이템 정보 가져오기 (마지막 요소)
        with open("closet.json", "r", encoding="utf-8") as f:
            closet = json.load(f)
            new_item = closet[-1]
            
        file_name = new_item['image_path'].replace('\\', '/').split('/')[-1]
        new_item['image_url'] = f"http://localhost:8000/images/{file_name}"
        
        return {
            "status": "success",
            "message": f"'{new_item['sub_category']}' 등록 완료!",
            "item": new_item
        }
    except Exception as e:
        return {"status": "error", "message": f"분석 실패: {str(e)}"}

# 실행 방법: 터미널에 uvicorn main_api:app --reload 입력