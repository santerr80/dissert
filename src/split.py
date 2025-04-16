import os
from osgeo import gdal
from tqdm import tqdm

input_dir = r"D:\URFU\VKR\Ind_pract\dissert\data\selected\jpeg"
output_dir = r"D:\URFU\VKR\Ind_pract\dissert\data\selected\jpeg\split"
out_size_image = 256


# Функция для обработки TIFF-файлов
def split_image(input_dir, output_dir, out_size_image):

    # Установка конфигурации GDAL
    gdal.SetConfigOption('GDAL_NUM_THREADS', '10')

    # Получаем список всех TIFF-файлов
    file_list = [f for f in os.listdir(input_dir) \
                 if f.lower().endswith('.jpeg')]

    # Подсчет общего числа кусков для всех файлов
    file_info = []
    total_steps = 0

    # Подсчет общего числа кусков для всех файлов
    for filename in file_list:
        input_path = os.path.join(input_dir, filename)
        image_info = gdal.Info(input_path, format="json")
        width = image_info['size'][0]
        height = image_info['size'][1]
        x_count = width // out_size_image
        y_count = height // out_size_image
        count = x_count * y_count
        file_info.append((filename, input_path, x_count, y_count))
        total_steps += count

    # Прогресс-бар
    progress_bar = tqdm(total=total_steps, desc="Обработка файлов", unit="кусок")

    # Обработка каждого TIFF-файла
    for item in file_info:
        filename, input_path, x_count, y_count = item
        base_name, ext = os.path.splitext(filename)
        for i in range(y_count):
            top_y = i * out_size_image
            for j in range(x_count):
                left_x = j * out_size_image
                output_filename = f"{base_name}_{i:03d}_{j:03d}.jpeg"
                output_path = os.path.join(output_dir, output_filename)
                if os.path.exists(output_path):
                    progress_bar.write(f"Файл {output_filename} уже существует.")
                    progress_bar.update(1)
                    continue
                try:
                    options = gdal.TranslateOptions(
                        srcWin=[left_x, top_y, out_size_image, out_size_image],
                        format='JPEG',
                        resampleAlg=gdal.gdalconst.GRA_Average,
                        creationOptions=['QUALITY=50'],
                        strict=True
                    )
                    gdal.Translate(output_path, input_path, options=options)
                    progress_bar.update(1)
                except Exception as e:
                    progress_bar.write(f"Ошибка при обработке {output_filename}: {str(e)}")
                    progress_bar.update(1)

    progress_bar.close()


split_image(input_dir, output_dir, out_size_image)
