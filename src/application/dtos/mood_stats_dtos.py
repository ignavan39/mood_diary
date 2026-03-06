from dataclasses import dataclass


@dataclass
class MoodStatsDTO:
    total: int = 0
    avg_mood: int = 0
    min_mood: int = 0
    max_mood: int = 0
    period_days: int = 7

    @property
    def mood_emoji(self) -> str:
        if self.avg_mood <= 2: return "😢"
        elif self.avg_mood <= 4: return "😟"
        elif self.avg_mood <= 6: return "😐"
        elif self.avg_mood <= 8: return "🙂"
        else: return "😄"
    
    @property
    def mood_text(self) -> str:
        if self.avg_mood <= 2: return "Очень плохое"
        elif self.avg_mood <= 4: return "Плохое"
        elif self.avg_mood <= 6: return "Нейтральное"
        elif self.avg_mood <= 8: return "Хорошее"
        else: return "Отличное"