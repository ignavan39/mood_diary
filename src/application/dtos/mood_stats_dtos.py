from dataclasses import dataclass
from typing import Optional


@dataclass
class MoodStatsDTO:
    total_entries: int = 0
    avg_mood: float = 0.0
    min_mood: int = 0
    max_mood: int = 0
    period_days: int = 7
    last_entry_date: Optional[str] = None
    first_entry_date: Optional[str] = None

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
