# /audio_model/train.py

import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# Dummy data (replace with real MFCC or spectrogram features)
X = torch.randn(100, 20)  # 100 samples, 20 features (e.g., MFCC)
y = torch.randint(0, 2, (100,))  # Binary labels (0 or 1)

# Define model
class AudioClassifier(nn.Module):
    def __init__(self):
        super(AudioClassifier, self).__init__()
        self.fc1 = nn.Linear(20, 64)
        self.fc2 = nn.Linear(64, 2)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

model = AudioClassifier()

# Training setup
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
dataset = TensorDataset(X, y)
loader = DataLoader(dataset, batch_size=16, shuffle=True)

# Training loop
for epoch in range(10):
    for batch_X, batch_y in loader:
        optimizer.zero_grad()
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()

# Save model
save_path = './model.pth'
torch.save(model.state_dict(), save_path)

print(f'Model saved to {save_path}')
