import torch.nn as nn
from torchvision.models import resnet18

def create_model(num_classes=4):
"""
Cria o modelo de classificação.

```
O número padrão de classes corresponde às quatro categorias
psicogenéticas inicialmente definidas.
"""

model = resnet18(weights="DEFAULT")

num_features = model.fc.in_features

model.fc = nn.Linear(num_features, num_classes)

return model
```
