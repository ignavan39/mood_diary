from typing import Optional

from application.dtos import MoodStatsDTO
from application.use_cases.get_user_profile import UserSettings
from domain.entities import StatsPeriod


class StringBuilder:
    def __init__(self) -> None:
        self._text = ""

    def append(self, text: str) -> "StringBuilder":
        self._text += text
        return self

    def add_line(self, text: str) -> "StringBuilder":
        self._text += "\n" + text
        return self

    def add_doble_line(self, text: str) -> "StringBuilder":
        self._text += "\n\n" + text
        return self

    def get_text(self) -> str:
        return self._text


class Messages:
    WELCOME_STUB_MESSAGE = "нажми /start чтобы начать"
    WELCOME_TEXT = (
        "👋Привет, {full_name}!\n\n"
        "Я помогу тебе отслеживать настроение.\n"
        "Используй /mood чтобы оценить своё состояние."
    )
    WELCOME_TEXT_FOR_REGISTERED_USER = (
        "✅ С возвращением, {full_name}!\n\nИспользуй /mood чтобы отметить настроение"
    )

    INFOGRAPHIC_CAPTION = (
        "{emoji} Твоё настроение за {period}\n\n"
        "📈 Статистика:\n"
        "• Записей: {total}\n"
        "• Среднее: {avg:.1f}/10 ({mood_text})\n"
        "• Мин/Макс: {min}/{max}\n"
        "• Тренд: {trend_text}\n\n"
        "Сгенерировано @mood_diary_bbot"
    )

    INFOGRAPHIC_EMPTY_CAPTION = (
        "📊 Нет данных за {period}\n\n"
        "Используй /mood чтобы начать отслеживать настроение!\n\n"
        "Сгенерировано @mood_diary_bbot"
    )

    CHOOSE_PERIOD = "📊 Выбери период для получения статистики:"

    INOGRAPHIC_GENERATING = "🎨 Генерирую инфографику..."

    TREND_TEXTS = {
        "improving": "Улучшается",
        "declining": "Ухудшается",
        "stable": "Стабильно",
        "unstable": "нестабильно",
        "unstable_improving": "нестабильно, ухудшается",
        "unstable_declining": "нестабильно, но улучшается",
    }

    STUB_MESSAGE = "Чем могу помочь? Нажми /help для справки."

    HELP_TEXT = (
        "📖 Справка по боту\n\n"
        "🎯 Оценить настроение:\n"
        "• Нажми '🎯 Оценить настроение' или /mood\n"
        "• Выбери значение от 0 до 10\n"
        "• Можно обновить запись за сегодня\n\n"
        "📊 Статистика:\n"
        "• Нажми '👤 Профиль' или /profile\n"
        "• Выбери период: неделя, месяц, год\n"
        "• Посмотри среднее настроение и тренды\n\n"
        "• Нажми '📊 Экспортировать инфографику' или /export\n"
        "• Выбери период: неделя, месяц, год\n"
        "• Посмотри среднее настроение и тренды\n\n"
        "🔒 Приватность:\n"
        "• Все данные хранятся локально\n"
        "• Никто не имеет доступа к твоей статистике\n"
        "💡 Советы:\n"
        "• Записывай настроение каждый день\n"
        "• Смотри статистику за месяц для паттернов\n\n"
        "Сделано с заботой о ментальном здоровье 🌱\n"
        "🔗 Исходный код GitHub: https://github.com/ignavan39/mood_diary"
    )

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

    PROFILE_TITLE = "Профиль: {full_name}"
    PROFILE_SETTINGS = "🔧 Настройки"
    PROFILE_SETTINGS_REMINDER = "Напоминание:"
    PROFILE_SETTINGS_REMINDER_ENABLED = "🔔 Включено"
    PROFILE_SETTINGS_REMINDER_DISABLED = "🔕 Выключено"

    PROFILE_STATS_TITLE = "📊 Статистика: {period}"

    PROFILE_STATS_NO_DATA = (
        "❌ Нет записей за этот период.\n\n"
        "Используй /mood чтобы добавить первую запись!"
    )

    PROFILE_STATS_DETAILS = (
        "{emoji} Среднее настроение: {avg}/10 ({mood_text})\n\n"
        "📈 Детали:\n"
        "• Записей: {total}\n"
        "• Минимум: {min}/10\n"
        "• Максимум: {max}/10\n\n"
        "🕐 Период:\n"
        "• Первая запись: {first}\n"
        "• Последняя: {last}"
    )

    @classmethod
    def get_profile_text(
        cls,
        full_name: str,
        user_settings: UserSettings,
    ) -> str:
        return (
            StringBuilder()
            .append(Messages.format(Messages.PROFILE_TITLE, full_name=full_name))
            .add_doble_line(Messages.format(Messages.PROFILE_SETTINGS))
            .add_line(
                Messages.format(
                    Messages.PROFILE_SETTINGS_REMINDER,
                    enabled=user_settings.reminder_enabled,
                )
            )
            .add_line(
                Messages.format(
                    Messages.PROFILE_SETTINGS_REMINDER_ENABLED
                    if user_settings.reminder_enabled
                    else Messages.PROFILE_SETTINGS_REMINDER_DISABLED
                )
            )
            .get_text()
        )

    @classmethod
    def get_profile_text_with_stats(
        cls,
        full_name: str,
        period: StatsPeriod,
        mood_stats: Optional[MoodStatsDTO],
        user_settings: UserSettings,
    ) -> str:

        period_label = Messages.get_period_str_by_day(period.value)
        profile_text = cls.get_profile_text(full_name, user_settings)
        return (
            StringBuilder()
            .append(profile_text)
            .add_doble_line(
                Messages.format(Messages.PROFILE_STATS_TITLE, period=period_label)
            )
            .add_doble_line(
                Messages.format(
                    Messages.PROFILE_STATS_DETAILS,
                    emoji=Messages.get_mood_emoji(int(mood_stats.avg_mood)),
                    avg=mood_stats.avg_mood,
                    mood_text=Messages.get_mood_text(mood_stats.avg_mood),
                    total=mood_stats.total_entries,
                    min=mood_stats.min_mood,
                    max=mood_stats.max_mood,
                    first=mood_stats.first_entry_date or "—",
                    last=mood_stats.last_entry_date or "—",
                )
                if mood_stats is not None
                else Messages.PROFILE_STATS_NO_DATA
            )
            .get_text()
        )

    BTN_MOOD = "🎯 Оценить настроение"
    BTN_STATS = "📊 Моя статистика"
    BTN_EXPORT = "📈 Экспорт"
    BTN_HELP = "📖 Помощь"
    BTN_PROFILE = "👤 Профиль"
    BTN_MAIN_MENU = "🏠 Главное меню"
    BTN_YES = "✅ Да, обновить"
    BTN_NO = "❌ Нет, отмена"
    BTN_CANCEL = "❌ Отмена"
    BTN_EXPORT_INFORGRAPHIC = "📊 Экспортировать инфографику"
    BTN_BACK = "🔙 Назад"

    BTN_COMMAND_MAP: dict[str, str] = {
        BTN_MOOD: "mood",
        BTN_STATS: "stats",
        BTN_EXPORT: "export",
        BTN_HELP: "help",
        BTN_PROFILE: "profile",
        BTN_MAIN_MENU: "start",
    }

    PERIODS_TO_STR_MAP: dict[int, str] = {
        7: "Неделя",
        30: "Месяц",
        90: "3 месяца",
        180: "Полгода",
        365: "Год",
        0: "Все время",
    }

    PERIODS_TO_LABEL_MAP: dict[str, StatsPeriod] = {
        "неделя": StatsPeriod.WEEK,
        "месяц": StatsPeriod.MONTH,
        "3 месяца": StatsPeriod.QUARTER,
        "полгода": StatsPeriod.HALF_YEAR,
        "год": StatsPeriod.YEAR,
        "все время": StatsPeriod.ALL,
    }

    LABEL_TO_PERIOD_MAP: dict[StatsPeriod, str] = {
        StatsPeriod.WEEK: "неделя",
        StatsPeriod.MONTH: "месяц",
        StatsPeriod.QUARTER: "3 месяца",
        StatsPeriod.HALF_YEAR: "полгода",
        StatsPeriod.YEAR: "год",
        StatsPeriod.ALL: "все время",
    }

    MOOD_TEXTS = {
        "very_bad": "Очень плохое",
        "bad": "Плохое",
        "neutral": "Нейтральное",
        "good": "Хорошее",
        "excellent": "Отличное",
        "no_data": "Нет данных",
    }

    REMINDER_DISABLE_TEXT = "🔕 Отключить напоминания"

    REMINDER_ENABLE_TEXT = "⏰ Включить напоминания"
    REMINDER_EDIT_TEXT = "Изменить время напоминания {current}"
    REMINDER_TEXT = "🔔 Напоминание: отметить настроение за сегодня!"

    INVALID_PERIOD = "❌ Неверный период"

    INVALID_DIARY_RATING = (
        "❌ Неверное значение, значение должно быть в диапазоне от 1 до 10"
    )
    ERROR_GENERIC = "⚠️ Ошибка. Попробуйте позже."
    ERROR_GENERATE_INFOGRAPHIC = (
        "❌ Ошибка при генерации инфографики. Попробуйте позже."
    )

    @classmethod
    def get_command_by_btn(cls, text: str) -> str | None:
        return cls.BTN_COMMAND_MAP.get(text.strip())

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
    def get_period_str_by_day(cls, days: int) -> str:
        return cls.PERIODS_TO_STR_MAP.get(days, f"{days} дней")

    @classmethod
    def get_period_label_by_str(cls, identifier: str) -> StatsPeriod | None:
        return cls.PERIODS_TO_LABEL_MAP.get(identifier)

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
    def get_mood_emoji(value: float) -> str:
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
