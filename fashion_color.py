import torch
import torch.nn as nn
import torch.optim as optim
import json
import numpy as np
from aiai.color_model import ColorHarmonyNN

# 한글 색상명을 숫자로 바꾸는 매퍼 (더 많이 추가해도 좋습니다)
COLOR_MAP = {
    "화이트": [255, 255, 255], "블랙": [0, 0, 0], "그레이": [128, 128, 128],
    "네이비": [0, 0, 128], "베이지": [245, 245, 220], "아이보리": [255, 255, 240],
    "카키": [107, 142, 35], "브라운": [165, 42, 42], "블루": [0, 0, 255],
    "데님": [21, 67, 96]
}

def get_rgb(color_name):
    return COLOR_MAP.get(color_name, [128, 128, 128])

def train():
    print("📚 데이터 로딩 중...")
    with open('reference_fashion.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    X, y = [], []
    for d in data:
        top = next((i for i in d['items'] if i['category'] == '상의'), None)
        bottom = next((i for i in d['items'] if i['category'] == '하의'), None)
        if top and bottom:
            # 상하의 색상을 합쳐서 6개의 숫자로 만듭니다. (정규화 포함)
            X.append(get_rgb(top['color']) + get_rgb(bottom['color']))
            y.append([1.0]) # 전문가의 조합은 무조건 1점(정답)

    X_train = torch.FloatTensor(X) / 255.0
    y_train = torch.FloatTensor(y)

    model = ColorHarmonyNN()
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    criterion = nn.BCELoss()

    print("🚀 학습 시작 (약 1분 소요)...")
    for epoch in range(100):
        optimizer.zero_grad()
        output = model(X_train)
        loss = criterion(output, y_train)
        loss.backward()
        optimizer.step()
        if (epoch + 1) % 20 == 0:
            print(f"Epoch {epoch+1}/100, Loss: {loss.item():.4f}")
    
    # 학습된 지식을 .pth 파일로 저장합니다.
    torch.save(model.state_dict(), 'color_model.pth')
    print("✅ 학습 완료! 'color_model.pth' 파일이 생성되었습니다.")

if __name__ == "__main__":
    train()