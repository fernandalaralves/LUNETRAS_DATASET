from torchvision import transforms

def get_train_transforms(image_size=224):
"""
Transformações utilizadas durante o treinamento.

```
Algumas transformações são aleatórias para aumentar a
diversidade das imagens apresentadas ao modelo.
"""

return transforms.Compose([
    transforms.Resize((image_size, image_size)),
    transforms.RandomRotation(5),
    transforms.RandomHorizontalFlip(p=0.0),
    transforms.ToTensor(),
])


def get_validation_transforms(image_size=224):
"""
Transformações utilizadas na validação e no teste.

```
Não utiliza transformações aleatórias.
"""

return transforms.Compose([
    transforms.Resize((image_size, image_size)),
    transforms.ToTensor(),
])

