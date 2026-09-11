from pathlib import Path

import pandas as pd
from PIL import Image
from torch.utils.data import Dataset

class PsicogeneseDataset(Dataset):
"""
Dataset para carregamento das imagens de produções escritas
e seus respectivos níveis psicogenéticos.
"""

```
LABELS = {
    "PRE_SILABICO": 0,
    "SILABICO": 1,
    "SILABICO_ALFABETICO": 2,
    "ALFABETICO": 3,
}

def __init__(self, csv_file, image_dir, transform=None):
    self.data = pd.read_csv(csv_file)
    self.image_dir = Path(image_dir)
    self.transform = transform

    self.data["label_id"] = self.data["label"].map(self.LABELS)

    if self.data["label_id"].isnull().any():
        labels_invalidas = (
            self.data.loc[
                self.data["label_id"].isnull(), "label"
            ]
            .unique()
            .tolist()
        )

        raise ValueError(
            f"Labels desconhecidas encontradas: {labels_invalidas}"
        )

def __len__(self):
    return len(self.data)

def __getitem__(self, index):
    row = self.data.iloc[index]

    image_path = self.image_dir / row["filename"]

    image = Image.open(image_path).convert("RGB")

    label = int(row["label_id"])

    if self.transform:
        image = self.transform(image)

    return image, label
```
