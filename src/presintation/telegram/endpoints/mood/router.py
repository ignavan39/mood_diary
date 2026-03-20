import asyncio
import logging
from math import ceil

from aiogram import Bot, F, Router
from aiogram.enums import ChatAction
from aiogram.exceptions import TelegramNetworkError
from aiogram.filters import Command
from aiogram.types import BufferedInputFile, CallbackQuery, Message
from dependency_injector.providers import Factory
from dependency_injector.wiring import Provide, inject

from application.dtos import GenerateInfographicRequest
from application.use_cases import RecordMoodUseCase
from application.use_cases.generate_mood_infographic import (
    GenerateMoodInfographicUseCase,
    InfographicStats,
)
from application.use_cases.update_mood import UpdateMoodUseCase
from infrastructure.ioc.container.application import AppContainer
from presintation.common import Messages
from presintation.telegram.endpoints.mood.controllers import (
    GetRecordMoodMenuController,
    RecordMoodController,
    UpdateMoodController,
)

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("mood"))
async def get_menu(message: Message) -> None:
    controller = GetRecordMoodMenuController()
    await controller.call(message)


@router.callback_query(F.data.startswith("mood_"))
async def record_mood(
    callback: CallbackQuery,
    use_case_factory: Factory[RecordMoodUseCase] = Provide[
        AppContainer.services.record_mood_use_case
    ],
) -> None:
    use_case: RecordMoodUseCase = use_case_factory.provider()
    return await RecordMoodController(use_case).call(callback)


@router.callback_query(F.data.startswith("update_yes_"))
@inject
async def handle_update_confirmed(
    callback: CallbackQuery,
    use_case_factory: Factory[UpdateMoodUseCase] = Provide[
        AppContainer.services.update_mood_use_case
    ],
) -> None:
    use_case: UpdateMoodUseCase = use_case_factory.provider()
    return await UpdateMoodController(use_case).call(callback)


@router.message(Command("export"))
@inject
async def cmd_export(
    message: Message,
    bot: Bot,
    use_case_factory: Factory[GenerateMoodInfographicUseCase] = Provide[
        AppContainer.services.generate_mood_infographic_use_case
    ],
) -> None:
    if message.from_user is None:
        return
    user_id = message.from_user.id

    args = message.text.split()[1:] if message.text else []
    days = 30
    chart_type = "line"
    theme = "light"

    for arg in args:
        if arg.isdigit():
            days = int(arg)
        elif arg in ("line", "bar", "calendar"):
            chart_type = arg
        elif arg in ("light", "dark"):
            theme = arg

    thinking = await message.answer(Messages.INOGRAPHIC_GENERATING)
    buffer = None
    action_task: asyncio.Task | None = None

    try:
        use_case: GenerateMoodInfographicUseCase = use_case_factory.provider()

        request = GenerateInfographicRequest(
            external_user_id=user_id,
            days=days,
            chart_type=chart_type,
            format="png",
            include_stats=True,
            theme=theme,
        )

        async def keep_uploading() -> None:
            while True:
                try:
                    await bot.send_chat_action(
                        chat_id=message.chat.id,
                        action=ChatAction.UPLOAD_PHOTO,
                    )
                except Exception:
                    pass
                await asyncio.sleep(4)

        action_task = asyncio.create_task(keep_uploading())

        try:
            response = await use_case.execute(request)
        finally:
            action_task.cancel()
            try:
                await action_task
            except asyncio.CancelledError:
                pass

        caption = format_infographic_caption(response.stats, response.is_empty)
        buffer = response.image_data
        image_bytes: bytes = buffer.getvalue()

        photo = BufferedInputFile(image_bytes, filename=response.filename)

        for attempt in range(3):
            try:
                await message.answer_photo(
                    photo=photo,
                    caption=caption,
                    parse_mode="HTML",
                )
                break
            except TelegramNetworkError as e:
                if attempt == 2:
                    logger.error("Failed to send photo after 3 attempts: %s", e)
                    raise
                logger.warning("answer_photo timeout, retry %d/3: %s", attempt + 1, e)
                await asyncio.sleep(2)
                photo = BufferedInputFile(image_bytes, filename=response.filename)

    except Exception as e:
        logger.exception("Export failed: %s", e)
        await message.answer(Messages.ERROR_GENERATE_INFOGRAPHIC)
    finally:
        if action_task is not None and not action_task.done():
            action_task.cancel()
            try:
                await action_task
            except asyncio.CancelledError:
                pass

        await thinking.delete()
        if buffer is not None:
            buffer.close()


def format_infographic_caption(stats: InfographicStats, is_empty: bool = False) -> str:
    if is_empty or stats.total_entries == 0:
        return Messages.format(
            Messages.INFOGRAPHIC_EMPTY_CAPTION,
            period=Messages.get_period_label(stats.period_days),
        )

    avg = ceil(stats.avg_mood)
    emoji = Messages.get_mood_emoji(avg)
    mood_text = Messages.get_mood_text(avg)

    trend_emoji = Messages.TREND_EMOJIS.get(stats.trend, "➡️")
    trend_text = Messages.TREND_TEXTS.get(stats.trend, "Стабильно")

    return Messages.format(
        Messages.INFOGRAPHIC_CAPTION,
        emoji=emoji,
        period=Messages.get_period_label(stats.period_days),
        total=stats.total_entries,
        avg=avg,
        mood_text=mood_text,
        min=stats.min_mood,
        max=stats.max_mood,
        trend_emoji=trend_emoji,
        trend_text=trend_text,
    )
