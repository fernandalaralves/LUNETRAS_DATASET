import torch
from tqdm import tqdm

def train_one_epoch(model, dataloader, criterion, optimizer, device):
model.train()


total_loss = 0.0
total_correct = 0
total_samples = 0

progress_bar = tqdm(dataloader, desc="Treinamento")

for images, labels in progress_bar:
    images = images.to(device)
    labels = labels.to(device)

    optimizer.zero_grad()

    outputs = model(images)

    loss = criterion(outputs, labels)

    loss.backward()
    optimizer.step()

    total_loss += loss.item() * images.size(0)

    predictions = outputs.argmax(dim=1)

    total_correct += (predictions == labels).sum().item()
    total_samples += labels.size(0)

    progress_bar.set_postfix(
        loss=loss.item()
    )

epoch_loss = total_loss / total_samples
epoch_accuracy = total_correct / total_samples

return epoch_loss, epoch_accuracy
```

@torch.no_grad()
def validate(model, dataloader, criterion, device):
model.eval()

```
total_loss = 0.0
total_correct = 0
total_samples = 0

for images, labels in dataloader:
    images = images.to(device)
    labels = labels.to(device)

    outputs = model(images)

    loss = criterion(outputs, labels)

    total_loss += loss.item() * images.size(0)

    predictions = outputs.argmax(dim=1)

    total_correct += (predictions == labels).sum().item()
    total_samples += labels.size(0)

epoch_loss = total_loss / total_samples
epoch_accuracy = total_correct / total_samples

return epoch_loss, epoch_accuracy

