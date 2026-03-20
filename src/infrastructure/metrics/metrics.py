import functools
import logging
import time
from contextlib import asynccontextmanager
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from typing import Callable

from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)

logger = logging.getLogger(__name__)


bot_messages_total = Counter(
    "bot_messages_total",
    "Total messages processed",
    ["platform", "command", "status"],
)

bot_request_duration = Histogram(
    "bot_request_duration_seconds",
    "Request duration in seconds",
    ["platform", "command"],
    buckets=[0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0],
)

bot_active_users = Gauge(
    "bot_active_users",
    "Number of unique users active in last hour",
    ["platform"],
)

bot_users_registered_total = Counter(
    "bot_users_registered_total",
    "Total registered users",
    ["platform"],
)

bot_export_duration = Histogram(
    "bot_export_duration_seconds",
    "Duration of infographic export generation",
    ["platform"],
    buckets=[0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0],
)

bot_errors_total = Counter(
    "bot_errors_total",
    "Total errors by type",
    ["platform", "command", "error_type"],
)


@asynccontextmanager
async def track_handler(platform: str, command: str):
    start = time.perf_counter()
    status = "success"
    try:
        yield
    except Exception:
        status = "error"
        bot_errors_total.labels(
            platform=platform,
            command=command,
            error_type="unhandled",
        ).inc()
        raise
    finally:
        bot_messages_total.labels(
            platform=platform, command=command, status=status
        ).inc()
        bot_request_duration.labels(platform=platform, command=command).observe(
            time.perf_counter() - start
        )


def track(platform: str, command: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            async with track_handler(platform, command):
                return await func(*args, **kwargs)

        return wrapper

    return decorator


class MetricsHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args) -> None:
        pass

    def do_GET(self) -> None:
        if self.path == "/metrics":
            data = generate_latest()
            self.send_response(200)
            self.send_header("Content-Type", CONTENT_TYPE_LATEST)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_response(404)
            self.end_headers()


def start_metrics_server(port: int = 8000) -> None:
    server = HTTPServer(("0.0.0.0", port), MetricsHandler)
    logger.info("📊 Metrics server started on port %d", port)
    server.serve_forever()


def start_metrics_server_thread(port: int = 8000) -> Thread:
    thread = Thread(target=start_metrics_server, args=(port,), daemon=True)
    thread.start()
    return thread
