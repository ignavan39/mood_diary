from dataclasses import dataclass
from datetime import date
from typing import Literal
from io import BytesIO

from domain.entities.user import Platform


InfographicFormat = Literal["png", "jpg", "webp"]
ChartType = Literal["line", "bar", "calendar"]
ChartTheme = Literal["light", "dark"]
Trend = Literal["improving", "declining", "stable"]


@dataclass
class InfographicStats:
    total_entries: int
    avg_mood: float
    min_mood: int
    max_mood: int
    trend: Trend
    period_days: int
    first_entry_date: date | None = None
    last_entry_date: date | None = None


@dataclass
class GenerateInfographicRequest:
    external_user_id: int
    days: int = 30
    chart_type: ChartType = "line"
    format: InfographicFormat = "png"
    include_stats: bool = True
    theme: ChartTheme = "light"
    platform: Platform = "telegram"


@dataclass
class GenerateInfographicResponse:
    image_data: BytesIO
    filename: str
    stats: InfographicStats
    is_empty: bool = False
