import segmentation_models_pytorch as smp
import torch
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from PIL import Image
from sklearn.model_selection import train_test_split
import os


# Кастомный датасет
class CustomDataset(Dataset):
    def __init__(self, image_dir, mask_dir, transform=None):
        self.image_dir = image_dir
        self.mask_dir = mask_dir
        self.transform = transform
        self.image_filenames = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]

    def __len__(self):
        return len(self.image_filenames)

    def __getitem__(self, idx):
        img_path = os.path.join(self.image_dir, self.image_filenames[idx])
        mask_path = os.path.join(self.mask_dir, self.image_filenames[idx])
        image = Image.open(img_path).convert("RGB")
        mask = Image.open(mask_path).convert("L")

        if self.transform:
            image = self.transform(image)
            mask = self.transform(mask)

        return image, mask


# создание датасета
image_dir = r"D:\URFU\VKR\Data\selected\jpeg\split"
mask_dir = r"D:\URFU\VKR\Data\selected\jpeg\split\masks"
image, mask = CustomDataset(image_dir, mask_dir, transform=transforms.ToTensor())

# разделение на тренировочную и тестовую выборку
train_images, val_images, train_masks, val_masks = train_test_split(images, masks, test_size=0.2, random_state=42)

model = smp.UnetPlusPlus(encoder_name='resnet34',
                         encoder_depth=5,
                         encoder_weights="imagenet",
                         decoder_channels=(256, 128, 64, 32, 16),
                         decoder_interpolation='nearest',
                         in_channels=3,
                         classes=1,
                         activation='sigmoid',
                         aux_params=None
                         )
model.eval()

