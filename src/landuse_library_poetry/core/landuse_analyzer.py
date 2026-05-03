"""Основной модуль анализа землепользования."""

import geopandas as gpd
import pandas as pd
from loguru import logger

from ..exceptions import NoOverlapError
from ..services.geo_processor import calculate_overlay_area
from ..utils.validators import (
    validate_column_exists,
    validate_crs_match,
    validate_gdf_not_empty,
)


def calculate_landuse_area(
    landuse_gdf: gpd.GeoDataFrame, area_column: str = "area"
) -> gpd.GeoDataFrame:
    """Вычисляет площадь каждого участка землепользования."""
    logger.info("Calculating landuse areas...")
    validate_gdf_not_empty(landuse_gdf, "landuse_gdf")
    result_gdf = landuse_gdf.copy()
    result_gdf[area_column] = result_gdf.geometry.area
    logger.info(f"Calculated areas for {len(result_gdf)} features")
    return result_gdf


def landuse_share_by_district(
    districts_gdf: gpd.GeoDataFrame,
    landuse_gdf: gpd.GeoDataFrame,
    category_column: str,
    district_id_column: str = "district_id",
) -> pd.DataFrame:
    """Вычисляет долю каждой категории землепользования в пределах районов."""
    logger.info("Calculating landuse share by district...")

    validate_gdf_not_empty(districts_gdf, "districts_gdf")
    validate_gdf_not_empty(landuse_gdf, "landuse_gdf")
    validate_column_exists(landuse_gdf, category_column)
    validate_column_exists(districts_gdf, district_id_column)

    landuse_gdf_aligned = validate_crs_match(districts_gdf, landuse_gdf)
    overlay_result = calculate_overlay_area(
        districts_gdf, landuse_gdf_aligned, district_id_column
    )

    if overlay_result.empty:
        logger.warning("No overlaps found between districts and landuse")
        raise NoOverlapError(
            "Не найдено пересечений между районами и землепользованием"
        )

    area_by_district_category = (
        overlay_result.groupby([district_id_column, category_column])["overlay_area"]
        .sum()
        .reset_index()
    )

    total_area_by_district = (
        area_by_district_category.groupby(district_id_column)["overlay_area"]
        .sum()
        .reset_index()
    )
    total_area_by_district.columns = [district_id_column, "total_district_area"]

    result = area_by_district_category.merge(
        total_area_by_district, on=district_id_column
    )
    result["share"] = result["overlay_area"] / result["total_district_area"]

    logger.info(
        f"Calculated shares for {len(result)} district-category combinations"
    )
    return result


def dominant_landuse(
    districts_gdf: gpd.GeoDataFrame,
    landuse_gdf: gpd.GeoDataFrame,
    category_column: str,
    district_id_column: str = "district_id",
) -> pd.DataFrame:
    """Определяет доминирующую категорию землепользования для каждого района."""
    logger.info("Determining dominant landuse categories...")

    shares_df = landuse_share_by_district(
        districts_gdf, landuse_gdf, category_column, district_id_column
    )

    idx = shares_df.groupby(district_id_column)["share"].idxmax()
    result = shares_df.loc[idx].copy()
    result = result[[district_id_column, category_column, "share"]]
    result.columns = [district_id_column, "dominant_category", "dominant_share"]

    logger.info(f"Found dominant categories for {len(result)} districts")
    return result