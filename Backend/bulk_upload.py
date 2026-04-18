import anthropic
import base64
import io
import json
import os
import time
from PIL import Image

# ==========================================
# 1. 설정 (본인의 API 키 입력)
# ==========================================
CLAUDE_API_KEY = "YOUR_CLAUDE_API_KEY_HERE"
client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

def analyze_and_get_items(image_path):
    """사진 한 장에서 여러 옷 정보를 추출하는 함수"""
    try:
        img = Image.open(image_path)
        img.thumbnail((1024, 1024))
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        image_data = base64.b64encode(buffer.getvalue()).decode("utf-8")

        # 인물 사진에서 모든 옷을 뽑아내기 위한 정교한 프롬프트
        prompt = """
        이 사진 속 인물이 입고 있는 모든 옷(상의, 하의, 아우터)을 분석해줘.
        각 아이템별로 JSON 객체를 만들어서 '리스트' 형태로 출력해줘.
        
        [출력 형식 예시]
        [
            {"category": "상의", "sub_category": "반팔 티셔츠", "color": "화이트", "thickness": 2, "formal_level": 1, "style": "캐주얼", "season": ["여름"]},
            {"category": "하의", "sub_category": "와이드 데님", "color": "중청", "thickness": 3, "formal_level": 2, "style": "캐주얼", "season": ["봄", "가을"]}
        ]
        설명 없이 오직 JSON 리스트만 출력해.
        """

        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            messages=[{"role": "user", "content": [{"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": image_data}}, {"type": "text", "text": prompt}]}]
        )

        raw_text = message.content[0].text.strip().replace("'", '"')
        if "```json" in raw_text: raw_text = raw_text.split("```json")[1].split("```")[0].strip()
        
        return json.loads(raw_text)
    except Exception as e:
        print(f"❌ {image_path} 분석 중 오류 발생: {e}")
        return []

def run_bulk_upload(folder_name):
    """폴더 내 모든 사진을 읽어서 closet.json 업데이트"""
    image_extensions = ('.jpg', '.jpeg', '.png')
    files = [f for f in os.listdir(folder_name) if f.lower().endswith(image_extensions)]
    
    print(f"🚀 총 {len(files)}장의 사진을 분석합니다. 잠시만 기다려주세요...")
    
    all_new_items = []
    
    for i, filename in enumerate(files):
        path = os.path.join(folder_name, filename)
        print(f"🔄 [{i+1}/{len(files)}] {filename} 분석 중...")
        
        items = analyze_and_get_items(path)
        if items:
            for item in items:
                item['image_path'] = path
            all_new_items.extend(items)
            print(f"   ✅ {len(items)}개의 아이템 발견!")
        
        # API 과부하 방지를 위해 아주 잠깐 쉬어줍니다 (선택사항)
        time.sleep(0.5)

    # 기존 데이터와 합치기
    closet = []
    if os.path.exists("closet.json"):
        with open("closet.json", "r", encoding="utf-8") as f:
            closet = json.load(f)
    
    closet.extend(all_new_items)
    
    with open("closet.json", "w", encoding="utf-8") as f:
        json.dump(closet, f, indent=4, ensure_ascii=False)
        
    print(f"\n✨ 모든 작업 완료! 총 {len(all_new_items)}개의 새 옷이 옷장에 등록되었습니다.")

# --- 실행 ---
if __name__ == "__main__":
    run_bulk_upload("upload_images")