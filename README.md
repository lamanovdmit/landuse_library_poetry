# LandUse Library Poetry
Библиотека для анализа структуры землепользования городских территорий.

## Установка
```python
pip install landuse-library-poetry
```

## Использование
```python
from landuse_library_poetry import calculate_landuse_area, landuse_share_by_district, dominant_landuse
```

## Функции
 - calculate_landuse_area() - расчёт площадей участков
 - landuse_share_by_district() - доли категорий по районам
 - dominant_landuse() - доминирующая категория для района

## Пример использования
```python
import geopandas as gpd
from shapely.geometry import Polygon
from landuse_library_poetry import (
    calculate_landuse_area,
    landuse_share_by_district,
    dominant_landuse,
)

# Создание тестовых данных
districts_gdf = gpd.GeoDataFrame({
    'district_id': ['D1'],
    'geometry': [Polygon([(0, 0), (0, 10), (10, 10), (10, 0)])]
}, crs="EPSG:32637")

landuse_gdf = gpd.GeoDataFrame({
    'category': ['Жилая', 'Парк'],
    'geometry': [
        Polygon([(0, 0), (0, 8), (6, 8), (6, 0)]),
        Polygon([(6, 0), (6, 10), (10, 10), (10, 0)])
    ]
}, crs="EPSG:32637")

# Расчёт площадей
landuse_with_area = calculate_landuse_area(landuse_gdf)

# Доли категорий по районам
shares = landuse_share_by_district(districts_gdf, landuse_gdf, 'category')

# Доминирующая категория
dominant = dominant_landuse(districts_gdf, landuse_gdf, 'category')

print(landuse_with_area[['category', 'area']])
print(shares)
print(dominant)
```

## Ссылки
 - PyPI: https://pypi.org/project/landuse-library-poetry/
 - TestPyPI: https://test.pypi.org/project/landuse-library-poetry/
