import anthropic
import base64
import io
import json
import os
import requests
import random
from PIL import Image
import matplotlib.pyplot as plt
from color_ai_service import get_final_fashion_score
import platform
import warnings

# ==========================================
# 1. 설정 및 한글 폰트 환경 구축
# ==========================================
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "YOUR_CLAUDE_API_KEY_HERE")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "YOUR_WEATHER_KEY_HERE")

client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

# 경고 메시지 무시 및 한글 폰트 설정
warnings.filterwarnings("ignore", category=UserWarning)
from matplotlib import font_manager, rc
if platform.system() == 'Windows':
    font_path = "c:/Windows/Fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font_name)

# ==========================================
# 2. 의도 분석 및 날씨 정보
# ==========================================
def is_valid_fashion_query(situation, mood):
    fashion_keywords = ["코디", "패션", "옷", "추천", "스타일", "결혼식", "등교", "데이트", "일상", "외출", "룩", "입을", "어울리는", "출근", "소개팅", "학교", "장소"]
    combined_input = (situation + mood).lower()
    return any(keyword in combined_input for keyword in fashion_keywords)

def get_current_temp():
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={WEATHER_API_KEY}&units=metric&lang=kr"
    try:
        res = requests.get(url).json()
        return res["main"]["temp"], res["weather"][0]["description"]
    except:
        return 20.0, "맑음"

# ==========================================
# 3. 데이터 분석 및 시각화
# ==========================================
def analyze_and_save(image_path):
    # (기존 analyze_and_save 코드와 동일 - 업로드된 파일 내용 유지)
    print(f"🔍 '{image_path}' 분석 중...")
    try:
        img = Image.open(image_path)
        img.thumbnail((1024, 1024))
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        image_data = base64.b64encode(buffer.getvalue()).decode("utf-8")

        prompt = """이 옷 사진을 분석해서 정해진 형식의 JSON으로만 출력해줘. 
        {"category": "상의/하의/아우터/원피스", "sub_category": "구체적명칭", "color": "색상", 
        "thickness": 1~5, "formal_level": 1~5, "style": "스타일", "season": ["계절"]}"""

        message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1024,
            messages=[{"role": "user", "content": [{"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": image_data}}, {"type": "text", "text": prompt}]}]
        )
        raw_text = message.content[0].text.strip()
        new_item = json.loads(raw_text)
        new_item['image_path'] = image_path 
        
        closet = []
        if os.path.exists("closet.json"):
            with open("closet.json", "r", encoding="utf-8") as f: closet = json.load(f)
        closet.append(new_item)
        with open("closet.json", "w", encoding="utf-8") as f: json.dump(closet, f, indent=4, ensure_ascii=False)
        print(f"✅ '{new_item['sub_category']}' 등록 완료!")
    except Exception as e: print(f"❌ 분석 실패: {e}")

def show_recommendation_images(recommendation):
    items = recommendation['items']
    unique_paths = list(set([item.get('image_path') for item in items if item.get('image_path')]))

    num_images = len(unique_paths)
    if num_images == 0: return
    
    fig, axes = plt.subplots(1, num_images, figsize=(5 * num_images, 6))
    fig.suptitle(f"🌟 [AI 추천 코디 조합]: {recommendation['ref_name']} (매칭률: {recommendation['score']}%)", fontsize=14, fontweight='bold')

    if num_images == 1: axes = [axes]
    for i, path in enumerate(unique_paths):
        if os.path.exists(path):
            img = Image.open(path).convert("RGB")
            axes[i].imshow(img)
            contained = [f"[{it['category']}] {it['sub_category']}" for it in items if it['image_path'] == path]
            axes[i].set_title("\n".join(contained), fontsize=10)
            axes[i].axis('off')
    plt.tight_layout()
    plt.show()

# ==========================================
# 4. [수정됨] 100점 만점 기반 추천 알고리즘
# ==========================================
def expert_recommend_algorithm(temp, situation, mood):
    if not is_valid_fashion_query(situation, mood):
        return "⚠️ 패션 관련 질문이 아니신 것 같아요! 코디 고민을 말씀해 주세요. 😊"

    if not os.path.exists("closet.json") or not os.path.exists("reference_fashion.json"):
        return "❌ 데이터 파일이 없습니다."

    with open("closet.json", "r", encoding="utf-8") as f: my_closet = json.load(f)
    with open("reference_fashion.json", "r", encoding="utf-8") as f: references = json.load(f)
    if not my_closet: return "❌ 옷장이 비어있습니다."

    mood_map = {
        "러블리/로맨틱": ["로맨틱", "페미닌", "러블리"],
        "캐주얼": ["캐주얼", "데일리", "아메카지"],
        "단정한/포멀": ["모던", "오피스", "비즈니스", "미니멀"],
        "힙한/스트릿": ["스트릿", "힙합", "고프코어"],
        "빈티지": ["레트로", "빈티지", "워크웨어"]
    }
    target_styles = mood_map.get(mood, ["캐주얼"])
    possible_refs = [ref for ref in references if (ref['temp_range'][0]-5 <= temp <= ref['temp_range'][1]+5) and any(s in ref['set_name'] for s in target_styles)]
    
    if not possible_refs:
        possible_refs = [ref for ref in references if (ref['temp_range'][0]-5 <= temp <= ref['temp_range'][1]+5)]

    target_thick = 5 if temp < 5 else 4 if temp < 12 else 3 if temp < 20 else 1.5
    best_total_score = -1
    best_recommendation = None

    for ref in possible_refs:
        slots = {"상의": None, "하의": None, "아우터": None, "원피스": None}
        style_match_raw = 0
        
        for ref_item in ref['items']:
            cat = ref_item['category']
            if cat not in slots: continue 
            best_item, max_item_score = None, -1
            for my_item in my_closet:
                if my_item['category'] == cat:
                    # 아이템별 일치도 계산
                    item_score = (50 if my_item['sub_category'] == ref_item['sub_category'] else 0) + \
                                 (30 if my_item['color'] in ref_item['color'] else 0)
                    if item_score > max_item_score:
                        max_item_score = item_score
                        best_item = my_item
            if best_item:
                slots[cat] = best_item
                style_match_raw += max_item_score

        # 상하의 필수 체크
        if (slots["상의"] and slots["하의"]) or slots["원피스"]:
            # --- [가중치 기반 100점 만점 계산] ---
            # 1. 스타일 일치도 (최대 40점)
            style_score = min((style_match_raw / 160) * 40, 40)
            
            # 2. AI 색상 조화도 (최대 30점)
            ai_harmony_score = 0
            if slots["상의"] and slots["하의"]:
                ai_point = get_final_fashion_score(slots["상의"]['color'], slots["하의"]['color'], temp)
                ai_harmony_score = ai_point * 30
            
            # 3. 날씨/두께 적합도 (최대 30점)
            weather_point = 30
            for it in [slots["상의"], slots["하의"]]:
                if it: weather_point -= abs(it['thickness'] - target_thick) * 4
            weather_score = max(0, weather_point)

            final_total = round(style_score + ai_harmony_score + weather_score, 1)
            if final_total > 100: final_total = 100.0

            # 추천 이유 생성
            top_c = slots["상의"]['color'] if slots["상의"] else "선택"
            bot_c = slots["하의"]['color'] if slots["하의"] else "선택"
            reason = f"{top_c}와 {bot_c}의 조합이 AI 분석 결과 최적이며, 현재 기온({temp}도)에 맞는 두께감을 고려했습니다."

            if final_total > best_total_score:
                best_total_score = final_total
                best_recommendation = {
                    "ref_name": ref['set_name'], 
                    "items": [v for v in slots.values() if v],
                    "score": final_total,
                    "reason": reason
                }

    return best_recommendation

# ==========================================
# 5. 메인 제어부
# ==========================================
if __name__ == "__main__":
    print("\n👔 [2조] 개인 취향 반영 AI 스마트 옷장")
    print("1: 새 옷 등록 / 2: 맞춤 코디 추천받기")
    mode = input("선택: ")

    if mode == "1":
        img_path = input("사진 파일명 입력: ")
        analyze_and_save(img_path)
    elif mode == "2":
        temp, desc = get_current_temp()
        print(f"\n🌡️ 현재 날씨: {temp}도 ({desc})")
        sit = input("어디 가시나요? (예: 결혼식, 대학교, 데이트): ")
        print("\n--- 원하는 분위기를 선택하세요 ---")
        print("1. 러블리/로맨틱 | 2. 캐주얼 | 3. 단정한/포멀 | 4. 힙한/스트릿 | 5. 빈티지")
        mood_choice = input("번호: ")
        mood_dict = {"1": "러블리/로맨틱", "2": "캐주얼", "3": "단정한/포멀", "4": "힙한/스트릿", "5": "빈티지"}
        mood = mood_dict.get(mood_choice, mood_choice)

        print(f"\n🧪 AI 분석 중: {temp}도 | 상황: {sit} | 희망 스타일: {mood}")
        result = expert_recommend_algorithm(temp, sit, mood)
        
        if isinstance(result, dict):
            print(f"\n✨ [추천 코디: {result['ref_name']}]")
            print(f"📊 AI 스타일 매칭률: {result['score']}%")
            print("-" * 45)
            for item in result['items']:
                print(f"👉 {item['category']}: {item['color']} {item['sub_category']}")
            print("-" * 45)
            print(f"📝 추천 근거: {result['reason']}")
            print("-" * 45)
            show_recommendation_images(result)
        else:
            print(f"\n❌ 안내: {result}")
        
        input("\n계속하려면 엔터를 누르세요...")