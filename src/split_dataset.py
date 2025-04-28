import os
import shutil
from sklearn.model_selection import train_test_split
import random

# Пути к каталогам
images_dir = r"D:\URFU\VKR\Ind_pract\dissert\data\work\images"
masks_dir = r"D:\URFU\VKR\Ind_pract\dissert\data\work\masks"
output_dirs = {
    'train': {'images': 'train/images', 'masks': 'train/masks'},
    'test': {'images': 'test/images', 'masks': 'test/masks'},
    'val': {'images': 'val/images', 'masks': 'val/masks'}
}

# Создание выходных каталогов, если они не существуют
for split in output_dirs:
    os.makedirs(output_dirs[split]['images'], exist_ok=True)
    os.makedirs(output_dirs[split]['masks'], exist_ok=True)

# Получение списка имен файлов (предполагается, что имена совпадают в images и masks)
image_files = [f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))]
random.shuffle(image_files)  # Перемешиваем файлы для случайного разделения

# Разделение на train, test, val (70%, 15%, 15%)
train_files, temp_files = train_test_split(image_files, train_size=0.7, random_state=42)
test_files, val_files = train_test_split(temp_files, test_size=0.5, random_state=42)

# Функция для копирования файлов
def copy_files(file_list, split):
    for file_name in file_list:
        # Копирование изображения
        src_image = os.path.join(images_dir, file_name)
        dst_image = os.path.join(output_dirs[split]['images'], file_name)
        shutil.copy2(src_image, dst_image)
        
        # Копирование маски (предполагается, что имя совпадает)
        mask_name = file_name  # Если имена масок отличаются, нужно адаптировать
        src_mask = os.path.join(masks_dir, mask_name)
        dst_mask = os.path.join(output_dirs[split]['masks'], mask_name)
        if os.path.exists(src_mask):
            shutil.copy2(src_mask, dst_mask)
        else:
            print(f"Маска для {file_name} не найдена в {masks_dir}")

# Копирование файлов в соответствующие каталоги
copy_files(train_files, 'train')
copy_files(test_files, 'test')
copy_files(val_files, 'val')

print("Разделение завершено!")