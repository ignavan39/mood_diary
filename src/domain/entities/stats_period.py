from enum import Enum


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
