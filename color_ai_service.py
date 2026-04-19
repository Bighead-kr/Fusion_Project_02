import torch
import numpy as np
from aiai.color_model import ColorHarmonyNN

# 1. 색상 사전 (RGB 수치화)
COLOR_MAP = {
    "화이트": [255, 255, 255], "블랙": [0, 0, 0], "그레이": [128, 128, 128],
    "네이비": [0, 0, 128], "베이지": [245, 245, 220], "아이보리": [255, 255, 240],
    "카키": [107, 142, 35], "브라운": [165, 42, 42], "블루": [0, 0, 255],
    "데님": [21, 67, 96], "차콜": [54, 69, 79]
}

def get_rgb(color_name):
    # 이름에 포함된 단어로 매칭 (예: '연청' -> '데님')
    for key, val in COLOR_MAP.items():
        if key in color_name: return val
    return [128, 128, 128]

# 2. 날씨(온도) 기반 색상 가중치 로직
def get_weather_color_bonus(color_name, current_temp):
    bonus = 0.0
    if current_temp >= 25: # 여름
        if any(c in color_name for c in ["화이트", "블루", "스카이블루"]): bonus = 0.2
    elif current_temp < 10: # 겨울
        if any(c in color_name for c in ["블랙", "네이비", "차콜", "브라운"]): bonus = 0.2
    else: # 봄/가을
        if any(c in color_name for c in ["베이지", "아이보리", "카키", "그레이"]): bonus = 0.2
    return bonus

# 3. 통합 점수 계산기 (메인에서 호출할 함수)
def get_final_fashion_score(top_color, bottom_color, current_temp):
    # A. AI 조화도 점수
    model = ColorHarmonyNN()
    try:
        model.load_state_dict(torch.load('color_model.pth', map_location='cpu'))
        model.eval()
        t_rgb = np.array(get_rgb(top_color)) / 255.0
        b_rgb = np.array(get_rgb(bottom_color)) / 255.0
        inp = torch.FloatTensor(np.concatenate([t_rgb, b_rgb])).unsqueeze(0)
        with torch.no_grad():
            harmony_score = model(inp).item()
    except:
        harmony_score = 0.5 
        
    # B. 날씨 보너스
    weather_score = get_weather_color_bonus(top_color, current_temp) + \
                    get_weather_color_bonus(bottom_color, current_temp)
                    
    return harmony_score + weather_score