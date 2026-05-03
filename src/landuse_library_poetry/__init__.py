"""
Библиотека для анализа структуры землепользования.

Предоставляет инструменты для:
- Расчёта площадей категорий землепользования
- Анализа распределения категорий по районам
- Определения доминирующих категорий
"""

from .core.landuse_analyzer import (
    calculate_landuse_area,
    dominant_landuse,
    landuse_share_by_district,
)
from .exceptions import (
    CRSMismatchError,
    EmptyGeoDataFrameError,
    InvalidColumnError,
    LandUseLibraryError,
    NoOverlapError,
)

__version__ = "0.1.0"

__all__ = [
    "calculate_landuse_area",
    "landuse_share_by_district",
    "dominant_landuse",
    "LandUseLibraryError",
    "EmptyGeoDataFrameError",
    "CRSMismatchError",
    "InvalidColumnError",
    "NoOverlapError",
]