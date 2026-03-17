from dataclasses import dataclass


@dataclass
class Messages:
    # ─────────────────────────────────────────────────────────────
    # Welcome / Start
    # ─────────────────────────────────────────────────────────────
    WELCOME_TEXT = (
        "👋Привет, {full_name}!\n\n"
        "Я помогу тебе отслеживать настроение.\n"
        "Используй /mood чтобы оценить своё состояние."
    )
    WELCOME_TEXT_FOR_REGISTERED_USER = (
        "✅ С возвращением, {full_name}!\n\nИспользуй /mood чтобы отметить настроение"
    )

    HELP_TEXT = (
        "📖 Справка по боту\n\n"
        "🎯 Оценить настроение:\n"
        "• Нажми '🎯 Оценить настроение' или /mood\n"
        "• Выбери значение от 0 до 10\n"
        "• Можно обновить запись за сегодня\n\n"
        "📊 Статистика:\n"
        "• Нажми '📊 Моя статистика' или /profile\n"
        "• Выбери период: неделя, месяц, год\n"
        "• Посмотри среднее настроение и тренды\n\n"
        "🔒 Приватность:\n"
        "• Все данные хранятся локально\n"
        "• Никто не имеет доступа к твоей статистике\n"
        "💡 Советы:\n"
        "• Записывай настроение каждый день\n"
        "• Смотри статистику за месяц для паттернов\n"
        "🔗 GitHub: https://github.com/ignavan39/mood_diary"
    )

    # ─────────────────────────────────────────────────────────────
    # Mood
    # ─────────────────────────────────────────────────────────────
    MOOD_QUESTION = (
        "Как твоё настроение?\n\n"
        "Выберите значение от 0 до 10:\n"
        "0 = Очень плохо, 10 = Отлично"
    )

    MOOD_SAVED = "{emoji} Настроение сохранено!\n\nОценка: {mood}/10"

    MOOD_UPDATED = (
        "{emoji} Настроение обновлено!\n\nБыло: {old_rating}/10\nСтало: {new_rating}/10"
    )

    MOOD_UPDATE_EQUAL = "{emoji} Настроение не изменилось!\n\nОценка: {rating}/10"

    MOOD_DUPLICATE = (
        "⚠️Запись за {today} уже есть!\n\n"
        "Текущая: {old_rating}/10\n"
        "Новая: {emoji} {mood}/10\n\n"
        "Хотите обновить?"
    )

    # ─────────────────────────────────────────────────────────────
    # Stats
    # ─────────────────────────────────────────────────────────────
    STATS_TITLE = "📊 Статистика: {period}"

    STATS_NO_DATA = (
        "❌ Нет записей за этот период.\n\n"
        "Используй /mood чтобы добавить первую запись!"
    )

    STATS_DETAILS = (
        "📊 Статистика\n\n"
        "{emoji} Среднее настроение: {avg}/10 ({mood_text})\n\n"
        "📈 Детали:\n"
        "• Записей: {total}\n"
        "• Минимум: {min}/10\n"
        "• Максимум: {max}/10\n\n"
        "🕐 Период:\n"
        "• Первая запись: {first}\n"
        "• Последняя: {last}"
    )

    BTN_MOOD = "🎯 Оценить настроение"
    BTN_STATS = "📊 Моя статистика"
    BTN_HELP = "📖 Помощь"
    BTN_PROFILE = "👤 Профиль"
    BTN_MAIN_MENU = "🏠 Главное меню"
    BTN_YES = "✅ Да, обновить"
    BTN_NO = "❌ Нет, отмена"
    BTN_CANCEL = "❌ Отмена"

    PERIOD_LABELS = {
        7: "Неделя",
        30: "Месяц",
        90: "3 месяца",
        180: "Полгода",
        365: "Год",
        0: "Все время",
    }

    MOOD_TEXTS = {
        "very_bad": "Очень плохое",
        "bad": "Плохое",
        "neutral": "Нейтральное",
        "good": "Хорошее",
        "excellent": "Отличное",
        "no_data": "Нет данных",
    }

    INVALID_PERIOD = "❌ Неверный период"

    INVALID_DIARY_RATING = (
        "❌ Неверное значение, значение должно быть в диапазоне от 1 до 10"
    )
    ERROR_GENERIC = "⚠️ Ошибка. Попробуйте позже."

    @classmethod
    def format(cls, text: str, **kwargs) -> str:
        if not text:
            return "[[MISSING_TEXT]]"

        try:
            return text.format(**kwargs)
        except KeyError as e:
            return f"[[FORMAT_ERROR: missing {e}]]"
        except Exception:
            return text

    @classmethod
    def format_by_key(cls, key: str, **kwargs) -> str:
        text = getattr(cls, key, "")
        return cls.format(text, **kwargs)

    @classmethod
    def get_period_label(cls, days: int) -> str:
        return cls.PERIOD_LABELS.get(days, f"{days} дней")

    @classmethod
    def get_mood_text(cls, avg_mood: float) -> str:
        if avg_mood <= 2:
            return cls.MOOD_TEXTS["very_bad"]
        elif avg_mood <= 4:
            return cls.MOOD_TEXTS["bad"]
        elif avg_mood <= 6:
            return cls.MOOD_TEXTS["neutral"]
        elif avg_mood <= 8:
            return cls.MOOD_TEXTS["good"]
        else:
            return cls.MOOD_TEXTS["excellent"]

    @staticmethod
    def get_mood_emoji(value: int) -> str:
        if value <= 2:
            return "😢"
        elif value <= 4:
            return "😟"
        elif value <= 6:
            return "😐"
        elif value <= 8:
            return "🙂"
        else:
            return "😄"
