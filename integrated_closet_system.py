import anthropic
import base64
import io
import json
import os
import requests
import random
from PIL import Image
import matplotlib.pyplot as plt

# ==========================================
# 1. 설정 (API 키 및 클라이언트)
# ==========================================
CLAUDE_API_KEY = "YOUR_CLAUDE_API_KEY_HERE"
WEATHER_API_KEY = "YOUR_WEATHER_KEY_HERE"
client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
# ==========================================
# 🛡️ 2. [신규] 의도 분석 트리거 (패션 질문 여부 검증)
# ==========================================
def is_valid_fashion_query(situation, mood):
    """사용자의 입력이 패션과 관련 있는지 검증"""
    # 1차 키워드 검사 (속도 최적화)
    fashion_keywords = ["코디", "패션", "옷", "추천", "스타일", "결혼식", "등교", "데이트", "일상", "외출", "룩", "입을", "어울리는", "출근", "소개팅", "학교", "장소"]
    combined_input = (situation + mood).lower()
    
    if any(keyword in combined_input for keyword in fashion_keywords):
        return True

    # 2차 AI 검사 (키워드 없을 시 의도 파악)
    prompt = f"사용자 입력 상황: '{situation}', 분위기: '{mood}'. 이 질문이 옷 코디나 스타일 추천과 관련이 있나요? 관련 있으면 'yes', 관련 없으면 'no'라고만 대답해줘."
    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=10,
            messages=[{"role": "user", "content": prompt}]
        )
        return "yes" in response.content[0].text.lower()
    except:
        return True # 에러 시 일단 통과

# ==========================================
# 3. [입력] 옷 사진 분석 및 저장
# ==========================================
def analyze_and_save(image_path):
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
            model="claude-sonnet-4-6",
            max_tokens=1024,
            messages=[{"role": "user", "content": [{"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": image_data}}, {"type": "text", "text": prompt}]}]
        )

        raw_text = message.content[0].text.strip().replace("'", '"')
        if "```json" in raw_text: raw_text = raw_text.split("```json")[1].split("```")[0].strip()
        
        new_item = json.loads(raw_text)
        new_item['image_path'] = image_path 
        
        closet = []
        if os.path.exists("closet.json"):
            with open("closet.json", "r", encoding="utf-8") as f: closet = json.load(f)
        
        closet.append(new_item)
        with open("closet.json", "w", encoding="utf-8") as f: json.dump(closet, f, indent=4, ensure_ascii=False)
        print(f"✅ '{new_item['sub_category']}' 등록 완료!")
    except Exception as e:
        print(f"❌ 분석 실패: {e}")

# ==========================================
# 4. [환경] 실시간 날씨 정보 가져오기
# ==========================================
def get_current_temp():
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={WEATHER_API_KEY}&units=metric&lang=kr"
    try:
        res = requests.get(url).json()
        return res["main"]["temp"], res["weather"][0]["description"]
    except:
        return 20.0, "맑음"

# ==========================================
# 🖼️ 5. [시각화] 중복 제거 및 이미지 출력 함수
# ==========================================
def show_recommendation_images(recommendation):
    """추천된 아이템을 중복 이미지 없이 화면에 출력"""
    items = recommendation['items']
    unique_paths = []
    for item in items:
        path = item.get('image_path')
        if path and path not in unique_paths:
            unique_paths.append(path)

    num_images = len(unique_paths)
    fig, axes = plt.subplots(1, num_images, figsize=(6 * num_images, 7))
    fig.suptitle(f"🌟 [AI 추천 코디 조합]: {recommendation['ref_name']}", fontsize=16, fontweight='bold')

    if num_images == 1: axes = [axes]

    for i, path in enumerate(unique_paths):
        if os.path.exists(path):
            img = Image.open(path).convert("RGB")
            axes[i].imshow(img)
            # 해당 사진에서 추천된 모든 아이템 태그 표시
            contained = [f"[{it['category']}] {it['sub_category']}" for it in items if it['image_path'] == path]
            axes[i].set_title("\n".join(contained), fontsize=11)
            axes[i].axis('off')

    plt.tight_layout()
    print("📸 코디 이미지를 출력합니다...")
    plt.show()

# ==========================================
# 6. [알고리즘] 12만 전문가 데이터 매칭 및 폴백 로직
# ==========================================
def expert_recommend_algorithm(temp, situation, mood):
    # --- [트리거 검사] ---
    if not is_valid_fashion_query(situation, mood):
        return "⚠️ 죄송합니다. 저는 패션 전문 AI입니다. 코디와 관련 없는 질문에는 답변드리기 어렵습니다! 😊"

    if not os.path.exists("closet.json") or not os.path.exists("reference_fashion.json"):
        return "❌ 데이터 파일이 없습니다."

    with open("closet.json", "r", encoding="utf-8") as f: my_closet = json.load(f)
    with open("reference_fashion.json", "r", encoding="utf-8") as f: references = json.load(f)

    if not my_closet: return "❌ 옷장이 비어있습니다."

    mood_map = {
        "러블리/로맨틱": ["로맨틱", "페미닌", "큐트", "러블리"],
        "캐주얼": ["캐주얼", "데일리", "내추럴", "아메카지"],
        "단정한/포멀": ["모던", "오피스", "비즈니스", "정장", "미니멀", "클래식"],
        "힙한/스트릿": ["스트릿", "힙합", "펑크", "고프코어", "스트리트"],
        "빈티지": ["레트로", "빈티지", "워크웨어"]
    }
    target_styles = mood_map.get(mood, ["캐주얼"])

    # 1단계: 3중 필터링 (기온 범위를 +-10도로 확장하여 유연하게 검색)
    possible_refs = [ref for ref in references if (ref['temp_range'][0]-10 <= temp <= ref['temp_range'][1]+10) and any(s in ref['set_name'] for s in target_styles)]
    
    # [폴백] 스타일 데이터가 부족하면 기본 스타일로 확장
    if not possible_refs:
        print(f"⚠️ {mood} 스타일 부족으로 대안 코디를 탐색합니다.")
        backup_styles = ["모던", "캐주얼", "미니멀", "데일리"]
        possible_refs = [ref for ref in references if (ref['temp_range'][0]-10 <= temp <= ref['temp_range'][1]+10) and any(s in ref['set_name'] for s in backup_styles)]

    if not possible_refs: return "❌ 현재 날씨에 맞는 전문가 데이터를 찾지 못했습니다."
    if len(possible_refs) > 3000: possible_refs = random.sample(possible_refs, 3000)

    target_thick = 5 if temp < 5 else 4 if temp < 12 else 3 if temp < 20 else 1.5
    best_total_score = -1
    best_recommendation = None

    for ref in possible_refs:
        slots = {"상의": None, "하의": None, "아우터": None, "원피스": None}
        current_ref_score = 0
        for ref_item in ref['items']:
            cat = ref_item['category']
            if cat not in slots: continue 
            best_item = None
            max_score = -1
            for my_item in my_closet:
                if my_item['category'] == cat:
                    score = (50 if my_item['sub_category'] == ref_item['sub_category'] else 0) + \
                            (30 if my_item['color'] in ref_item['color'] else 0) + \
                            ((5 - abs(my_item['thickness'] - target_thick)) * 10)
                    if score > max_score: max_score = score; best_item = my_item
            if best_item: slots[cat] = best_item; current_ref_score += max_score

        # 상하의 세트 필수 (단, 25도 이상이면 아우터 제외)
        if temp >= 25: slots["아우터"] = None
        if (slots["상의"] and slots["하의"]) or slots["원피스"]:
            if current_ref_score > best_total_score:
                best_total_score = current_ref_score
                best_recommendation = {"ref_name": ref['set_name'], "items": [v for v in slots.values() if v]}

    return best_recommendation

# ==========================================
# 7. 메인 제어부
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

        print(f"\n🧪 분석 중: {temp}도 | 상황: {sit} | 희망 스타일: {mood}")
        result = expert_recommend_algorithm(temp, sit, mood)
        
        if isinstance(result, dict):
            print(f"✨ [추천 결과: {result['ref_name']}]")
            for item in result['items']:
                print(f"👉 {item['category']}: {item['color']} {item['sub_category']}")
            show_recommendation_images(result)
        else:
            print(result)