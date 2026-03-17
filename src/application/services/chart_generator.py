from abc import ABC, abstractmethod
from io import BytesIO
from typing import Optional, TypedDict

from datetime import date

from application.dtos import ChartTheme, ChartType


class ChartData(TypedDict, total=True):
    dates: list[date]
    values: list[int]
    stats: dict
    period_days: int


class ChartGeneratorInterface(ABC):
    @abstractmethod
    async def generate(
        self,
        data: ChartData,
        chart_type: ChartType = "line",
        theme: ChartTheme = "light",
        include_stats: bool = True,
        user_id: Optional[int] = None,
        width: int = 1200,
        height: int = 800,
        dpi: int = 100,
    ) -> BytesIO:
        pass

    @abstractmethod
    async def generate_empty(
        self,
        period_days: int,
        theme: ChartTheme = "light",
        width: int = 800,
        height: int = 400,
        dpi: int = 100,
    ) -> BytesIO:
        pass

    @abstractmethod
    async def shutdown(self) -> None:
        pass
