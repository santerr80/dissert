import os
from osgeo import gdal
from tqdm import tqdm
import multiprocessing as mp
from functools import partial

input_dir = r"D:\URFU\VKR\Ind_pract\dissert\data\selected\png\destination\clahe"
output_dir = r"D:\URFU\VKR\Ind_pract\dissert\data\selected\png\destination\clahe\split"
out_size_image = 256

# Функция для обработки одного куска изображения
def process_tile(args, out_size_image, output_dir):
    filename, input_path, i, j = args
    base_name, ext = os.path.splitext(filename)
    top_y = i * out_size_image
    left_x = j * out_size_image
    output_filename = f"{base_name}_{i:03d}_{j:03d}.png"
    output_path = os.path.join(output_dir, output_filename)
    
    if os.path.exists(output_path):
        return (1, f"Файл {output_filename} уже существует.")
    
    try:
        options = gdal.TranslateOptions(
            srcWin=[left_x, top_y, out_size_image, out_size_image],
            format='PNG'
        )
        gdal.Translate(output_path, input_path, options=options)
        return (1, None)
    except Exception as e:
        return (1, f"Ошибка при обработке {output_filename}: {str(e)}")

# Основная функция для параллельной обработки
def split_image(input_dir, output_dir, out_size_image):
    # Установка конфигурации GDAL
    gdal.SetConfigOption('GDAL_NUM_THREADS', 'ALL_CPUS')
    gdal.SetCacheMax(4096)

    # Получаем список всех png-файлов
    file_list = [f for f in os.listdir(input_dir) if f.lower().endswith('.png')]

    # Подсчет общего числа кусков для всех файлов
    file_info = []
    total_steps = 0
    tasks = []

    for filename in file_list:
        input_path = os.path.join(input_dir, filename)
        image_info = gdal.Info(input_path, format='json')
        width = image_info['size'][0]
        height = image_info['size'][1]
        x_count = width // out_size_image
        y_count = height // out_size_image
        count = x_count * y_count
        file_info.append((filename, input_path, x_count, y_count))
        total_steps += count
        
        # Создаем задачи для каждого куска
        for i in range(y_count):
            for j in range(x_count):
                tasks.append((filename, input_path, i, j))

    # Прогресс-бар
    progress_bar = tqdm(total=total_steps, desc="Обработка файлов", unit="кусок")

    # Настройка пула процессов
    num_processes = mp.cpu_count()
    pool = mp.Pool(processes=num_processes)
    
    # Частичная функция для передачи констант
    process_tile_partial = partial(process_tile, out_size_image=out_size_image, output_dir=output_dir)
    
    # Асинхронная обработка задач
    for result, message in pool.imap_unordered(process_tile_partial, tasks):
        progress_bar.update(result)
        if message:
            progress_bar.write(message)
    
    # Закрытие пула и прогресс-бара
    pool.close()
    pool.join()
    progress_bar.close()

if __name__ == '__main__':
    split_image(input_dir, output_dir, out_size_image)