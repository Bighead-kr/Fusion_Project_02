import torch.nn as nn

class ColorHarmonyNN(nn.Module):
    def __init__(self):
        super(ColorHarmonyNN, self).__init__()
        # 상의 RGB(3) + 하의 RGB(3) = 총 6개의 입력을 받습니다.
        self.net = nn.Sequential(
            nn.Linear(6, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid() # 0(나쁨) ~ 1(좋음) 사이 점수를 뱉습니다.
        )

    def forward(self, x):
        return self.net(x)