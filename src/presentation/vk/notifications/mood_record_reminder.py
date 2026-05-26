import logging
import time

from domain.entities import User
from domain.repositories import UserRepository
from infrastructure.scheduler.scheduler import AppScheduler
from presentation.common import Messages
from presentation.vk.notifications.notify import Notify
from presentation.vk.sdk.api import VkSdk

logger = logging.getLogger(__name__)


class MoodRecordReminder(Notify):    
    def __init__(
        self, vk_api: VkSdk, user_repository: UserRepository, scheduler: AppScheduler
    ) -> None:
        self.vk_api = vk_api
        self._user_repository = user_repository
        self._scheduler = scheduler

    async def register(self) -> None:
        self._scheduler.add_cron_job(
            self.notify,
            name="hourly_reminder",
            hour="*",
            minute="0",
        )

    @property
    def get_name(self) -> str:
        return "mood_record_reminder"

    async def notify(self) -> None:
        hour = time.localtime().tm_hour
        processed = 0
        async for user in self._user_repository.iter_users_for_reminder(hour):
            try:
                await self._send_reminder(user)
                processed += 1
            except Exception:
                logger.exception("Failed to send reminder to user %s", user.id)
        logger.info(
            "Reminder job completed: %d users processed for hour=%d", processed, hour
        )

    async def _send_reminder(self, user: User) -> None:
        await self.vk_api.send_message(int(user.external_id), Messages.REMINDER_TEXT)
