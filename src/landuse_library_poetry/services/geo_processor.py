"""Сервисный модуль для геопространственных операций."""

import geopandas as gpd
from loguru import logger


def calculate_overlay_area(
    districts_gdf: gpd.GeoDataFrame,
    landuse_gdf: gpd.GeoDataFrame,
    district_id_column: str,
) -> gpd.GeoDataFrame:
    """Вычисляет площади пересечений районов и категорий землепользования."""
    logger.info("Performing spatial overlay...")
    overlay_gdf = gpd.overlay(districts_gdf, landuse_gdf, how="intersection")
    overlay_gdf["overlay_area"] = overlay_gdf.geometry.area
    logger.info(f"Overlay completed: {len(overlay_gdf)} intersections found")
    return overlay_gdf