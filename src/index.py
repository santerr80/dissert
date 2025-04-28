import os
from osgeo import gdal

def create_tile_index(tile_directory, output_path):
    # Включаем поддержку PAM для чтения .aux.xml
    gdal.SetConfigOption('GDAL_PAM_ENABLED', 'YES')

    # Собираем список JPEG файлов
    tile_files = [
        os.path.join(tile_directory, f)
        for f in os.listdir(tile_directory)
        if f.lower().endswith('.png')
    ]

    if not tile_files:
        raise ValueError("Нет подходящих тайлов в директории")

    # Проверка: можно ли открыть один файл
    test_file = tile_files[0]
    dataset = gdal.Open(test_file)
    if dataset is None:
        raise RuntimeError(f"Файл {test_file} не распознан как георастровый")

    # Настройки TileIndex
    options = gdal.TileIndexOptions(
        format="GPKG",
        layerName="tiles",
        overwrite=True,
        locationFieldName="location",
        writeAbsolutePath=True,
        recursive=False,
        filenameFilter="*.png",
        minPixelSize=0.01,
        maxPixelSize=10.0,
        metadataOptions=["DESCRIPTION=Tile Index"]
    )

    # Создаем индекс
    result = gdal.TileIndex(output_path, tile_files, options=options)

    if result != 0:
        error_msg = gdal.GetLastErrorMsg()
        raise RuntimeError(f"Ошибка GDAL: {error_msg}")


if __name__ == "__main__":
    tile_dir = r"D:\URFU\VKR\Ind_pract\dissert\data\selected\png\destination\masks"
    output_gpkg = r"D:\URFU\VKR\Ind_pract\dissert\data\selected\png\destination\masks\index.gpkg"

    try:
        create_tile_index(tile_dir, output_gpkg)
        print("Индекс успешно создан.")
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        input("Нажмите Enter для выхода...")