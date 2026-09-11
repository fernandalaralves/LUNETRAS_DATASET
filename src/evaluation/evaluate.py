import torch
from sklearn.metrics import (
classification_report,
confusion_matrix,
)

LABEL_NAMES = [
"PRE_SILABICO",
"SILABICO",
"SILABICO_ALFABETICO",
"ALFABETICO",
]

@torch.no_grad()
def get_predictions(model, dataloader, device):
model.eval()

```
all_predictions = []
all_labels = []

for images, labels in dataloader:
    images = images.to(device)

    outputs = model(images)

    predictions = outputs.argmax(dim=1)

    all_predictions.extend(
        predictions.cpu().numpy()
    )

    all_labels.extend(
        labels.numpy()
    )

return all_labels, all_predictions
```

def evaluate_predictions(labels, predictions):
report = classification_report(
labels,
predictions,
target_names=LABEL_NAMES,
zero_division=0,
)

```
matrix = confusion_matrix(
    labels,
    predictions,
)

return report, matrix
```
