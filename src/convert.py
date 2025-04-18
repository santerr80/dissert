import os
from osgeo import gdal
from tqdm import tqdm   


def convert_ecw(input_dir, output_dir):
    
    gdal.SetConfigOption('GDAL_NUM_THREADS', '10')
    
    file_list = [f for f in os.listdir(input_dir) if f.lower().endswith('.ecw')]
    total_files = len(file_list)

    progress_bar = tqdm(total=total_files, desc="Обработка файлов", unit="файл")

    for filename in file_list:
        input_path = os.path.join(input_dir, filename)
        base_name, ext = os.path.splitext(filename)
        output_filename = f"{base_name}.png"        
        output_path = os.path.join(output_dir, output_filename)

        if os.path.exists(output_path):
            progress_bar.write(f"Файл {output_filename} уже существует. Пропуск.")
            progress_bar.update(1)  # Увеличиваем прогресс при пропуске
            continue

        try:
            # Получаем исходные размеры изображения
            src_ds = gdal.Open(input_path)
            width = src_ds.RasterXSize
            height = src_ds.RasterYSize
            src_ds = None  # Закрываем исходный датасет

            # Рассчитываем целевые размеры, кратные 256
            target_width = ((width - 1) // 256 + 1) * 256
            target_height = ((height - 1) // 256 + 1) * 256

            # Настройка параметров GDAL
            options = gdal.TranslateOptions(
                format='PNG',
                width=target_width,
                height=target_height,
                outputType=gdal.GDT_Byte
            )
            
            # Выполнение преобразования
            ds = gdal.Translate(output_path, input_path, options=options)
            ds = None  # Закрытие датасета
            
            progress_bar.update(1)  # Увеличиваем прогресс после успешной обработки
        except Exception as e:
            progress_bar.write(f"Ошибка при обработке {filename}: {str(e)}")
            progress_bar.update(1)  # Увеличиваем прогресс при ошибке            
            raise Exception(
                "Произошла ошибка при обработке ECW-файла. Проверьте, что GDAL доступен и установлен правильно."    
            )
    progress_bar.close()


input_dir = r"D:\URFU\VKR\Ind_pract\dissert\data\selected"
output_dir = r"D:\URFU\VKR\Ind_pract\dissert\data\selected\png"

convert_ecw(input_dir, output_dir)
