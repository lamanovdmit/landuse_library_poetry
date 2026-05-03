"""Пользовательские исключения для библиотеки анализа землепользования."""


class LandUseLibraryError(Exception):
    """Базовое исключение библиотеки."""
    pass


class EmptyGeoDataFrameError(LandUseLibraryError):
    """Исключение при передаче пустого GeoDataFrame."""
    pass


class CRSMismatchError(LandUseLibraryError):
    """Исключение при несовпадении систем координат."""
    pass


class InvalidColumnError(LandUseLibraryError):
    """Исключение при отсутствии необходимой колонки в данных."""
    pass


class NoOverlapError(LandUseLibraryError):
    """Исключение при отсутствии пространственного пересечения."""
    pass