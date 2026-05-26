
from infrastructure import AppContainer
from presentation.vk.notifications.mood_record_reminder import MoodRecordReminder
from presentation.vk.notifications.notify import Notify


def notifications_factory(vk_sdk, container: AppContainer) -> list[Notify]:
    return [
    MoodRecordReminder(
        vk_api=vk_sdk,
        user_repository=container.infrastructure.container.user_repository(),
        scheduler=container.infrastructure.scheduler(),
    ),
]
