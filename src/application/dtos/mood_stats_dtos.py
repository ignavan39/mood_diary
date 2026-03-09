from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional


class StatsPeriod(Enum):
    WEEK = 7
    MONTH = 30
    QUARTER = 90
    HALF_YEAR = 180
    YEAR = 365
    ALL = 0

    @property
    def label(self) -> str:
        labels = {
            7: "Неделя",
            30: "Месяц",
            90: "3 месяца",
            180: "Полгода",
            365: "Год",
            0: "Все время",
        }
        return labels.get(self.value, f"{self.value} дней")

    @property
    def callback_data(self) -> str:
        return f"stats_{self.value}"


@dataclass
class MoodStatsDTO:
    total_entries: int = 0
    avg_mood: float = 0.0
    min_mood: int = 0
    max_mood: int = 0
    period_days: int = 7
    last_entry_date: Optional[date] = None
    first_entry_date: Optional[date] = None

    @property
    def mood_emoji(self) -> str:
        if self.avg_mood <= 2:
            return "😢"
        elif self.avg_mood <= 4:
            return "😟"
        elif self.avg_mood <= 6:
            return "😐"
        elif self.avg_mood <= 8:
            return "🙂"
        else:
            return "😄"

    @property
    def mood_text(self) -> str:
        if self.avg_mood <= 2:
            return "Очень плохое"
        elif self.avg_mood <= 4:
            return "Плохое"
        elif self.avg_mood <= 6:
            return "Нейтральное"
        elif self.avg_mood <= 8:
            return "Хорошее"
        else:
            return "Отличное"

    def format_period_text(self) -> str:
        """Форматирует текст периода"""
        if self.period_days == 7:
            return "за неделю"
        elif self.period_days == 30:
            return "за месяц"
        elif self.period_days == 90:
            return "за 3 месяца"
        elif self.period_days == 180:
            return "за полгода"
        elif self.period_days == 365:
            return "за год"
        else:
            return f"за {self.period_days} дней"
