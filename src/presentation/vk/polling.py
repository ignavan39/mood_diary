import logging
import threading
from typing import Callable, Optional

import vk_api
from vk_api.longpoll import VkEventType, VkLongPoll

from presentation.vk.sdk.types import VkMessage, VkUser


logger = logging.getLogger(__name__)


class VkLongPolling:
    POLL_TIMEOUT: int = 25
    RECONNECT_DELAY: int = 2

    def __init__(
        self,
        token: str,
        group_id: int,
        on_message: Callable[[VkMessage], bool],
        api_version: str = "5.199",
    ) -> None:
        self._token = token
        self._group_id = group_id
        self._on_message = on_message
        self._api_version = api_version

        self._vk: Optional[vk_api.VkApi] = None
        self._longpoll: Optional[VkLongPoll] = None
        self._stop_event = threading.Event()
        self._running = False
        self._thread: Optional[threading.Thread] = None

    def _init_session(self) -> None:
        self._vk = vk_api.VkApi(token=self._token)

        try:
            self._vk.method("groups.getById", {"group_id": self._group_id})
            logger.info("VK session validated for group %d", self._group_id)
        except vk_api.exceptions.ApiError as e:
            logger.error("Invalid VK token or group access: %s", e)
            raise

        self._longpoll = VkLongPoll(self._vk, self._group_id)

    def _adapt_message(self, event) -> Optional[VkMessage]:
        if event.type != VkEventType.MESSAGE_NEW:
            return None

        if hasattr(event, 'from_me') and event.from_me:
            return None

        user_id = getattr(event, 'user_id', None)
        peer_id = getattr(event, 'peer_id', getattr(event, 'chat_id', None))
        text = getattr(event, 'text', '') or ''
        timestamp = getattr(event, 't', 0)

        if user_id is None or peer_id is None:
            logger.debug("Skipping event with missing user_id or peer_id: %s", event.raw)
            return None

        payload = None
        if hasattr(event, 'raw') and isinstance(event.raw, dict):
            payload = event.raw.get('object', {}).get('payload')

        return VkMessage(
            from_user=VkUser(
                id=user_id,
                first_name="",
                last_name="",
            ),
            peer_id=peer_id,
            text=text,
            timestamp=timestamp,
            payload=payload,
        )

    def _polling_loop(self) -> None:
        logger.info("Starting Long Polling loop")
        self._running = True

        try:
            self._init_session()

            if self._longpoll is None:
                raise RuntimeError("LongPoll not initialized")

            for event in self._longpoll.listen():
                if self._stop_event.is_set():
                    logger.info("Stop signal received, exiting polling")
                    break
                message = self._adapt_message(event)
                if message is None:
                    continue

                logger.debug(
                    "Received message from %d: %s",
                    message.from_user.id,
                    message.text[:50],
                )

                self._on_message(message)

        except vk_api.exceptions.ApiError as e:
            logger.error("VK API error in polling: %s", e)
        except Exception as e:
            logger.exception("Unexpected error in polling: %s", e)
        finally:
            self._running = False
            logger.info("Long Polling loop finished")

    def start(
        self,
        main_loop,
        on_error: Optional[Callable[[Exception], None]] = None,
    ) -> threading.Thread:
        self._stop_event.clear()

        def _run_with_async():
            try:
                self._polling_loop()
            except Exception as e:
                if on_error:
                    on_error(e)
                raise

        self._thread = threading.Thread(
            target=_run_with_async,
            name=f"vk-polling-{self._group_id}",
            daemon=True,
        )
        self._thread.start()

        logger.info("Long Polling thread started: %s", self._thread.name)
        return self._thread

    def stop(self, timeout: float = 10.0) -> bool:
        logger.info("Stopping Long Polling...")
        self._stop_event.set()

        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=timeout)
            if self._thread.is_alive():
                logger.warning("Polling thread didn't stop within %ds", timeout)
                return False

        self._running = False
        logger.info("Long Polling stopped")
        return True

    @property
    def is_running(self) -> bool:
        return self._running


__all__ = ["VkLongPolling"]
