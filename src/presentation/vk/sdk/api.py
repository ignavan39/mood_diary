import asyncio
from io import BytesIO
import logging
from typing import Any, Optional

from presentation.vk.sdk.types import VkUser

from vk_api import VkApi

logger = logging.getLogger(__name__)


class VkSdk:
    def __init__(self, vk: VkApi) -> None:
        self._vk = vk

    async def send_message(
        self,
        user_id: int,
        text: str,
        keyboard: Optional[str] = None,
        attachment: Optional[str] = None,
    ) -> bool:
        params = {
            "user_id": user_id,
            "message": text,
            "random_id": 0,
        }
        if keyboard:
            params["keyboard"] = keyboard
        if attachment:
            params["attachment"] = attachment

        try:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(
                None,
                lambda: self._vk.method("messages.send", params),
            )
            logger.debug("Sent to VK %d: %s", user_id, text[:50])
            return True
        except Exception as e:
            logger.error("Failed to send message to %d: %s", user_id, e)
            return False

    async def answer_callback_event(
        self,
        event_id: str,
        user_id: int,
        action: Optional[dict] = None,
    ) -> bool:
        params = {
            "event_id": event_id,
            "user_id": user_id,
            "action": action or {},
        }

        try:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(
                None,
                lambda: self._vk.method("messages.sendMessageEventAnswer", params),
            )
            logger.debug("Callback answered: %s", event_id)
            return True
        except Exception as e:
            logger.error("Failed to answer callback %s: %s", event_id, e)
            return False

    async def call_vk_method(self, method: str, params: dict[str, Any]) -> Any:
        try:
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self._vk.method(method, params),
            )
            logger.debug("VK API call: %s with %s", method, params)
            return result
        except Exception as e:
            logger.error("VK API method %s failed: %s", method, e)
            raise

    async def get_user_by_id(self, user_id: int) -> VkUser | None:
        import asyncio

        def _sync_fetch() -> VkUser | None:
            users = self._vk.method("users.get", {"user_ids": [user_id]})
            if users:
                u = users[0]
                return VkUser(
                    id=u.get("id"),
                    first_name=u.get("first_name"),
                    last_name=u.get("last_name"),
                )

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, _sync_fetch)

    async def upload_photo(self, image_bytes: bytes, peer_id: int) -> str:
        from vk_api.upload import VkUpload

        def _sync_upload() -> str:
            upload = VkUpload(self._vk)
            photos = upload.photo_messages(
                photos=BytesIO(image_bytes),
                peer_id=peer_id,
            )
            p = photos[0]
            return f"photo{p['owner_id']}_{p['id']}"

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, _sync_upload)
