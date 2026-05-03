"""Валидаторы входных данных."""

from typing import Optional
import geopandas as gpd
from loguru import logger
from ..exceptions import CRSMismatchError, EmptyGeoDataFrameError, InvalidColumnError


def validate_gdf_not_empty(gdf: gpd.GeoDataFrame, name: str = "GeoDataFrame") -> None:
    """Проверяет, что GeoDataFrame не пустой."""
    if gdf.empty:
        logger.error(f"{name} is empty")
        raise EmptyGeoDataFrameError(f"{name} не должен быть пустым")


def validate_column_exists(gdf: gpd.GeoDataFrame, column: str) -> None:
    """Проверяет наличие колонки в GeoDataFrame."""
    if column not in gdf.columns:
        logger.error(f"Column '{column}' not found in GeoDataFrame")
        raise InvalidColumnError(f"Колонка '{column}' не найдена в данных")


def validate_crs_match(
    gdf1: gpd.GeoDataFrame,
    gdf2: gpd.GeoDataFrame,
    auto_align: bool = True,
) -> Optional[gpd.GeoDataFrame]:
    """Проверяет совпадение систем координат двух GeoDataFrame."""
    if gdf1.crs != gdf2.crs:
        if auto_align:
            logger.info(f"Aligning CRS: {gdf2.crs} -> {gdf1.crs}")
            return gdf2.to_crs(gdf1.crs)
        else:
            logger.error(f"CRS mismatch: {gdf1.crs} != {gdf2.crs}")
            raise CRSMismatchError(
                f"Системы координат не совпадают: {gdf1.crs} и {gdf2.crs}"
            )
    return gdf2