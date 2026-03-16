import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Histogram

logger = logging.getLogger(__name__)

bot_messages_total = Counter(
    "bot_messages_total",
    "Total messages processed",
    ["platform", "command", "status"]
)

bot_request_duration = Histogram(
    "bot_request_duration_seconds",
    "Request duration in seconds",
    ["platform", "command"]
)


class MetricsHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args) -> None:
        pass
    
    def do_GET(self) -> None:
        if self.path == "/metrics":
            self.send_response(200)
            self.send_header("Content-Type", CONTENT_TYPE_LATEST)
            self.end_headers()
            self.wfile.write(generate_latest())
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