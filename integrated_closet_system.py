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
WEATHER_API_KEY = "b4338d604cce5469f235f8fe913e4188"

client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

# ==========================================
# 2. [입력] 옷 사진 분석 및 저장
# ==========================================
def analyze_and_save(image_path):
    print(f"🔍 '{image_path}' 분석 중...")
    try:
        img = Image.open(image_path)
        img.thumbnail((1024, 1024))
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        image_data = base64.b64encode(buffer.getvalue()).decode("utf-8")

        prompt = """
        이 옷 사진을 분석해서 아래 항목들을 정해진 형식의 JSON으로만 출력해줘. 
        1. category: (상의, 하의, 아우터, 원피스 중 선택)
        2. sub_category: (티셔츠, 셔츠, 슬랙스, 청바지, 코트 등 구체적으로)
        3. color: (메인 색상 하나)
        4. thickness: (1: 아주 얇음 ~ 5: 아주 두꺼움 중 숫자 선택)
        5. formal_level: (1: 아주 편함 ~ 5: 아주 격식있음 중 숫자 선택)
        6. style: (캐주얼, 포멀, 스트릿, 빈티지 등 하나 선택)
        7. season: (봄, 여름, 가을, 겨울 중 해당하는 것 모두 리스트로)
        """

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
            with open("closet.json", "r", encoding="utf-8") as f:
                closet = json.load(f)
        
        closet.append(new_item)
        with open("closet.json", "w", encoding="utf-8") as f:
            json.dump(closet, f, indent=4, ensure_ascii=False)
        print(f"✅ '{new_item['sub_category']}' 등록 완료!")
    except Exception as e:
        print(f"❌ 분석 실패: {e}")

# ==========================================
# 3. [환경] 실시간 날씨 정보 가져오기
# ==========================================
def get_current_temp():
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={WEATHER_API_KEY}&units=metric&lang=kr"
    try:
        res = requests.get(url).json()
        return res["main"]["temp"], res["weather"][0]["description"]
    except:
        return 20.0, "맑음"

# ==========================================
# 4. [시각화] 추천 결과 사진 띄우기 함수
# ==========================================
def show_recommendation_images(recommendation):
    """추천된 아이템들의 이미지를 중복 없이 화면에 띄움"""
    items = recommendation['items']
    
    # 중복된 이미지 경로 제거 (상의/하의가 같은 사진일 경우 한 장만 띄우기 위함)
    unique_paths = []
    display_items = []
    for item in items:
        path = item.get('image_path')
        if path and path not in unique_paths:
            unique_paths.append(path)
            display_items.append(item)

    # 출력할 이미지 개수에 맞춰 칸 생성
    num_images = len(unique_paths)
    if num_images == 0:
        print("❌ 표시할 이미지가 없습니다.")
        return

    fig, axes = plt.subplots(1, num_images, figsize=(6 * num_images, 7))
    fig.suptitle(f"🌟 [AI 추천 코디 조합]: {recommendation['ref_name']}", fontsize=16, fontweight='bold')

    # 이미지가 한 장일 때 axes가 리스트가 아닌 경우 처리
    if num_images == 1:
        axes = [axes]

    for i, path in enumerate(unique_paths):
        if os.path.exists(path):
            img = Image.open(path).convert("RGB")
            axes[i].imshow(img)
            
            # 해당 사진에 포함된 아이템 이름들 모으기
            contained_items = [f"[{it['category']}] {it['sub_category']}" for it in items if it['image_path'] == path]
            axes[i].set_title("\n".join(contained_items), fontsize=12)
            axes[i].axis('off')
        else:
            axes[i].text(0.5, 0.5, f"이미지 없음\n{path}", ha='center', va='center')
            axes[i].axis('off')

    plt.tight_layout()
    print("📸 코디 이미지를 화면에 띄웁니다...")
    plt.show()

# ==========================================
# 5. [업그레이드] 상황 + 분위기(Mood) 반영 및 유연한 검색 알고리즘
# ==========================================
def expert_recommend_algorithm(temp, situation, mood):
    if not os.path.exists("closet.json") or not os.path.exists("reference_fashion.json"):
        return "❌ 데이터 파일이 없습니다."

    with open("closet.json", "r", encoding="utf-8") as f:
        my_closet = json.load(f)
    with open("reference_fashion.json", "r", encoding="utf-8") as f:
        references = json.load(f)

    if not my_closet: return "❌ 옷장이 비어있습니다. 먼저 1번 메뉴로 옷을 등록해주세요."

    # 분위기(Mood) 매핑 사전 확장
    mood_map = {
        "러블리/로맨틱": ["로맨틱", "페미닌", "큐트", "러블리"],
        "캐주얼": ["캐주얼", "데일리", "내추럴", "아메카지"],
        "단정한/포멀": ["모던", "오피스", "비즈니스", "정장", "미니멀", "클래식"],
        "힙한/스트릿": ["스트릿", "힙합", "펑크", "고프코어", "스트리트"],
        "빈티지": ["레트로", "빈티지", "워크웨어"]
    }
    target_styles = mood_map.get(mood, ["캐주얼"])

    # 1단계: 날씨 & 분위기 필터링 (기온 범위를 ±10도로 유연하게 확장)
    possible_refs = []
    for ref in references:
        temp_match = ref['temp_range'][0]-10 <= temp <= ref['temp_range'][1]+10
        style_match = any(style in ref['set_name'] for style in target_styles)
        if temp_match and style_match:
            possible_refs.append(ref)
    
    # [지능형 폴백] 데이터가 없을 경우 기본 스타일로 자동 확장
    if not possible_refs:
        print(f"⚠️ '{mood}' 스타일 코디 데이터가 부족하여 상황에 맞는 대안 스타일을 탐색합니다.")
        backup_styles = ["모던", "캐주얼", "미니멀", "데일리"]
        for ref in references:
            if (ref['temp_range'][0]-10 <= temp <= ref['temp_range'][1]+10) and \
               any(style in ref['set_name'] for style in backup_styles):
                possible_refs.append(ref)

    if not possible_refs: return "❌ 현재 조건에 맞는 코디 데이터를 찾지 못했습니다."

    if len(possible_refs) > 3000:
        possible_refs = random.sample(possible_refs, 3000)

    # 기온별 최적 옷 두께 타겟 설정
    target_thick = 5 if temp < 5 else 4 if temp < 12 else 3 if temp < 20 else 1.5

    best_total_score = -1
    best_recommendation = None

    for ref in possible_refs:
        slots = {"상의": None, "하의": None, "아우터": None, "원피스": None}
        current_ref_score = 0
        
        for ref_item in ref['items']:
            cat = ref_item['category']
            if cat not in slots: continue 
            
            best_item_for_cat = None
            max_item_score = -1
            
            for my_item in my_closet:
                if my_item['category'] == cat:
                    score = 0
                    if my_item['sub_category'] == ref_item['sub_category']: score += 60
                    if my_item['color'] in ref_item['color']: score += 30
                    # 두께 가중치 강화 (기온에 맞는 옷이 최우선)
                    score += (5 - abs(my_item['thickness'] - target_thick)) * 10
                    
                    if score > max_item_score:
                        max_item_score = score
                        best_item_for_cat = my_item
            
            if best_item_for_cat:
                slots[cat] = best_item_for_cat
                current_ref_score += max_item_score

        # [코디 완성 규칙] 상하의 세트 필수 (단, 25도 이상이면 아우터는 자동 제외하여 시원하게 추천)
        if temp >= 25:
            slots["아우터"] = None # 고온일 때 아우터 강제 제거
            
        is_complete = (slots["상의"] and slots["하의"]) or slots["원피스"]
        
        if is_complete:
            if current_ref_score > best_total_score:
                best_total_score = current_ref_score
                matched_items = [v for k, v in slots.items() if v is not None]
                best_recommendation = {
                    "ref_name": ref['set_name'],
                    "items": matched_items
                }

    return best_recommendation

# ==========================================
# 6. 메인 제어부
# ==========================================
if __name__ == "__main__":
    print("\n👔 [2조] 개인 취향 반영 AI 스마트 옷장 (12만 빅데이터 활용)")
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
            print(f"✨ [AI 추천 테마: {result['ref_name']}]")
            for item in result['items']:
                print(f"👉 {item['category']}: {item['color']} {item['sub_category']} (두께:{item['thickness']})")
            show_recommendation_images(result)
        else:
            print(result)