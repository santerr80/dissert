import csv
import shutil
import os

def move_files(csv_file_path):
    # Открываем CSV файл
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)  # Предполагается, что есть заголовки "source" и "destination"
        
        for row in reader:
            source_path = row['source']
            destination_path = row['destination']
            
            try:
                # Проверка существования исходного файла
                if not os.path.exists(source_path):
                    print(f"Файл {source_path} не найден. Пропускаем.")
                    continue
                
                # Создаем целевую директорию, если её нет
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                
                # Перемещаем файл
                shutil.move(source_path, destination_path)
                print(f"Файл {source_path} перемещен в {destination_path}")
                
            except Exception as e:
                print(f"Ошибка при перемещении {source_path}: {str(e)}")

if __name__ == "__main__":
    # Укажите путь к вашему CSV файлу
    csv_path = r"D:\URFU\VKR\Ind_pract\dissert\data\selected\png\destination\images\split\list_files.csv"
    move_files(csv_path)