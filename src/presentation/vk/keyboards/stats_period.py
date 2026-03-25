from domain.entities import StatsPeriod
from presentation.common import Messages
from presentation.vk.sdk.keyboards import ButtonColor, VkKeyboard


def kb_stats_period() -> str:
    return (
        VkKeyboard(inline=True)
        .add_callback(
            Messages.LABEL_TO_PERIOD_MAP[StatsPeriod.WEEK],
            color=ButtonColor.PRIMARY,
            payload={"period": "7"},
        )
        .add_callback(
            Messages.LABEL_TO_PERIOD_MAP[StatsPeriod.MONTH],
            color=ButtonColor.PRIMARY,
            payload={"period": "30"},
        )
        .row()
        .add_callback(
            Messages.LABEL_TO_PERIOD_MAP[StatsPeriod.QUARTER],
            color=ButtonColor.SECONDARY,
            payload={"period": "90"},
        )
        .add_callback(
            Messages.LABEL_TO_PERIOD_MAP[StatsPeriod.YEAR],
            color=ButtonColor.SECONDARY,
            payload={"period": "365"},
        )
        .row()
        .add_callback(
            Messages.LABEL_TO_PERIOD_MAP[StatsPeriod.ALL],
            color=ButtonColor.SECONDARY,
            payload={"period": "0"},
        )
        .to_json()
    )
