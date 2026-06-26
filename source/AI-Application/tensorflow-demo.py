import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

transform = transforms.Compose([transforms.ToTensor(), transforms.Lambda(lambda x: x.view(-1))])

train_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
test_dataset = datasets.MNIST(root='./data', train=False, download=True, transform=transform)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

model = nn.Sequential(
    nn.Linear(28 * 28, 128),
    nn.ReLU(),
    nn.Linear(128, 10)
)

optimizer = optim.Adam(model.parameters())
loss_fn = nn.CrossEntropyLoss()

for epoch in range(5):
    model.train()
    for images, labels in train_loader:
        optimizer.zero_grad()
        loss_fn(model(images), labels).backward()
        optimizer.step()
    print(f"Epoch {epoch + 1}/5 complete")

model.eval()
correct = 0
with torch.no_grad():
    for images, labels in test_loader:
        correct += (model(images).argmax(dim=1) == labels).sum().item()

print(f"Test accuracy: {correct / len(test_dataset):.4f}")