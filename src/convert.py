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
        output_filename = f"{base_name}.jpeg"        
        output_path = os.path.join(output_dir, output_filename)

        if os.path.exists(output_path):
            progress_bar.write(f"Файл {output_filename} уже существует. Пропуск.")
            progress_bar.update(1)  # Увеличиваем прогресс при пропуске
            continue

        try:
            # Настройка параметров GDAL
            options = gdal.TranslateOptions(
                format='JPEG',
                resampleAlg=gdal.gdalconst.GRA_Average,
                creationOptions=['QUALITY=50'],
                widthPct=102.4, # устанавливаем разрешение кратное 16
                heightPct=102.4
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