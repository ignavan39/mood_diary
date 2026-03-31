import asyncio
import logging
from typing import TYPE_CHECKING, ClassVar

from application.dtos import GenerateInfographicRequest
from application.dtos.infographic_dtos import InfographicStats
from application.use_cases.generate_mood_infographic import (
    GenerateMoodInfographicUseCase,
)
from domain.exceptions import UserNotFoundError
from presentation.common.messages import Messages
from presentation.vk.handlers.base import VkHandler
from presentation.vk.keyboards.main import kb_main
from presentation.vk.sdk.api import VkSdk
from presentation.vk.sdk.types import VkMessage
from presentation.vk.types import Context

if TYPE_CHECKING:
    from infrastructure import AppContainer

logger = logging.getLogger(__name__)

PLATFORM = "vk"


def _format_caption(stats: InfographicStats, is_empty: bool = False) -> str:
    if is_empty or stats.total_entries == 0:
        caption = Messages.format(
            Messages.INFOGRAPHIC_EMPTY_CAPTION,
            period=Messages.get_period_str_by_day(stats.period_days),
        )
    else:
        avg = round(stats.avg_mood, 1)
        caption = Messages.format(
            Messages.INFOGRAPHIC_CAPTION,
            emoji=Messages.get_mood_emoji(avg),
            period=Messages.get_period_str_by_day(stats.period_days),
            total=stats.total_entries,
            avg=avg,
            mood_text=Messages.get_mood_text(avg),
            min=stats.min_mood,
            max=stats.max_mood,
            trend_text=Messages.TREND_TEXTS.get(stats.trend, "Стабильно"),
        )

    return caption


class ExportInfographicHandler(VkHandler):
    COMMANDS: ClassVar[tuple[str, ...]] = (
        Messages.BTN_EXPORT,
        Messages.BTN_EXPORT_INFORGRAPHIC,
        "/export",
        "export",
        "экспорт",
    )

    def __init__(
        self,
        vk_api: "VkSdk",
        container: "AppContainer",
        group_id: int,
    ) -> None:
        super().__init__(vk_api, container, group_id)
        self._use_case: GenerateMoodInfographicUseCase = (
            container.services.generate_mood_infographic_use_case()
        )

    async def handle(self, message: VkMessage, ctx: Context) -> bool:
        if not self._matches_command(message.text.lower()):
            return False

        await self._api.send_message(
            user_id=message.from_user.id,
            text=Messages.INOGRAPHIC_GENERATING,
        )

        typing_task = asyncio.create_task(self._keep_typing(message.from_user.id))
        buffer = None

        try:
            request = GenerateInfographicRequest(
                external_user_id=message.from_user.id,
                days=30,
                chart_type="line",
                format="png",
                include_stats=True,
                theme="light",
                platform=PLATFORM,
            )
            response = await self._use_case.execute(request)

            buffer = response.image_data
            image_bytes = buffer.getvalue()

            attachment = await self._api.upload_photo(image_bytes, message.peer_id)

            caption = _format_caption(response.stats, response.is_empty)

            await self._api.send_message(
                user_id=message.from_user.id,
                text=caption,
                keyboard=kb_main(),
                attachment=attachment,
            )
            return True

        except UserNotFoundError:
            await self._api.send_message(
                user_id=message.from_user.id,
                text=Messages.WELCOME_STUB_MESSAGE,
                keyboard=kb_main(),
            )
            return True

        except Exception as e:
            logger.exception(
                "ExportInfographicHandler error for user %d: %s",
                message.from_user.id,
                e,
            )
            await self._api.send_message(
                user_id=message.from_user.id,
                text=Messages.ERROR_GENERATE_INFOGRAPHIC,
                keyboard=kb_main(),
            )
            return True

        finally:
            typing_task.cancel()
            try:
                await typing_task
            except asyncio.CancelledError:
                pass
            if buffer is not None:
                buffer.close()

    async def _keep_typing(self, user_id: int) -> None:
        while True:
            try:
                await self._api.call_vk_method(
                    "messages.setActivity",
                    {
                        "user_id": user_id,
                        "type": "typing",
                        "group_id": self._group_id,
                    },
                )
            except Exception:
                pass
            await asyncio.sleep(5)
