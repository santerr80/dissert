import cv2
import numpy as np
import os
import glob

def enhance_image(input_path, output_path):
    # Загрузка изображения
    img = cv2.imread(input_path)
    
    # Преобразование в HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    
    # CLAHE для канала V
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    v_clahe = clahe.apply(v)
    
    # CLAHE для канала H 
    clahe_h = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    h_clahe = clahe_h.apply(h)
    
    # # CLAHE для канала S
    clahe_s = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    s_clahe = clahe_s.apply(s)
    
    # Гамма-коррекция (например, γ=1.2)
    # gamma = 1.2
    # v_gamma = np.power(v_clahe / 255.0, gamma) * 255
    # v_gamma = v_gamma.astype(np.uint8)
    
    # Сборка обратно
    hsv_corrected = cv2.merge([h_clahe, s_clahe, v_clahe])
    img_result = cv2.cvtColor(hsv_corrected, cv2.COLOR_HSV2BGR) 
    
    # Сохранение
    cv2.imwrite(output_path, img_result)

# Пути к директориям
input_dir = r'D:\URFU\VKR\Ind_pract\dissert\data\selected\png\destination'
output_dir = r'D:\URFU\VKR\Ind_pract\dissert\data\selected\png\destination\clahe'
    

# Создаем выходную директорию, если её нет
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
# 
# Обрабатываем все .png файлы в input_dir
for filename in glob.glob(os.path.join(input_dir, '*.png')):
    input_path = filename
    output_filename = os.path.basename(filename)
    output_path = os.path.join(output_dir, output_filename)
    
    enhance_image(input_path, output_path)
    print(f"Обработан файл: {output_filename}")

print("Вся обработка завершена!")