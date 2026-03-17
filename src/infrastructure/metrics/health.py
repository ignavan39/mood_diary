import logging
import json
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class HealthStatus:
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    STARTING = "starting"
    STOPPING = "stopping"


class HealthChecker:
    def __init__(self):
        self._status = HealthStatus.STARTING
        self._db_connected = False
        self._polling_active = False
        self._started_at = datetime.now()
        self._error_message: Optional[str] = None
        self._last_check: Optional[datetime] = None

    def set_ready(self, db_connected: bool = True, polling_active: bool = True) -> None:
        self._db_connected = db_connected
        self._polling_active = polling_active

        if db_connected and polling_active:
            self._status = HealthStatus.HEALTHY
            self._error_message = None
        else:
            self._status = HealthStatus.UNHEALTHY
            self._error_message = "DB or polling not ready"

        self._last_check = datetime.utcnow()

    def set_unhealthy(self, error: str) -> None:
        self._status = HealthStatus.UNHEALTHY
        self._error_message = error
        self._last_check = datetime.utcnow()

    def set_starting(self) -> None:
        self._status = HealthStatus.STARTING
        self._last_check = datetime.utcnow()

    def set_stopping(self) -> None:
        self._status = HealthStatus.STOPPING
        self._last_check = datetime.utcnow()

    def get_status(self) -> Dict:
        uptime = (datetime.now() - self._started_at).total_seconds()
        return {
            "status": self._status,
            "liveness": self._status != HealthStatus.STARTING,
            "readiness": self._status == HealthStatus.HEALTHY,
            "db_connected": self._db_connected,
            "polling_active": self._polling_active,
            "uptime_seconds": round(uptime, 2),
            "started_at": self._started_at.isoformat(),
            "last_check": self._last_check.isoformat() if self._last_check else None,
            "error": self._error_message,
        }


health_checker = HealthChecker()


class HealthHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == "/health":
            self._handle_health()
        elif self.path == "/health/live":
            self._handle_liveness()
        elif self.path == "/health/ready":
            self._handle_readiness()
        else:
            self.send_response(404)
            self.end_headers()

    def _handle_health(self):
        status = health_checker.get_status()
        code = 200 if status["status"] == HealthStatus.HEALTHY else 503
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(status, indent=2).encode())

    def _handle_liveness(self):
        status = health_checker.get_status()
        code = 200 if status["liveness"] else 503
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status":"alive"}')

    def _handle_readiness(self):
        status = health_checker.get_status()
        code = 200 if status["readiness"] else 503
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status":"ready"}')


def start_health_server(port: int = 8080) -> None:
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    logger.info("🏥 Health server started on port %d", port)
    server.serve_forever()


def start_health_server_thread(port: int = 8080) -> Thread:
    thread = Thread(target=start_health_server, args=(port,), daemon=True)
    thread.start()
    return thread
