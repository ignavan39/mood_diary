from domain.entities import StatsPeriod
from presentation.common import Messages
from presentation.vk.sdk.keyboards import ButtonColor, VkKeyboard


def kb_stats_period() -> str:
    return (
        VkKeyboard(inline=False)
        .add_text(
            Messages.LABEL_TO_PERIOD_MAP[StatsPeriod.WEEK], color=ButtonColor.PRIMARY
        )
        .add_text(
            Messages.LABEL_TO_PERIOD_MAP[StatsPeriod.MONTH], color=ButtonColor.PRIMARY
        )
        .row()
        .add_text(
            Messages.LABEL_TO_PERIOD_MAP[StatsPeriod.QUARTER],
            color=ButtonColor.SECONDARY,
        )
        .add_text(
            Messages.LABEL_TO_PERIOD_MAP[StatsPeriod.YEAR], color=ButtonColor.SECONDARY
        )
        .add_text(
            Messages.LABEL_TO_PERIOD_MAP[StatsPeriod.ALL], color=ButtonColor.SECONDARY
        )
        .row()
        .add_text("🔙 Назад", color=ButtonColor.NEGATIVE)
        .to_json()
    )
