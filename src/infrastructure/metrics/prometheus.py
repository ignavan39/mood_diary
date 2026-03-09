from prometheus_client import Counter, Histogram, Gauge, start_http_server

messages_total = Counter(
    "bot_messages_total", "Total messages processed", ["command", "status"]
)

users_total = Counter("bot_users_total", "Total registered users")

request_duration = Histogram(
    "bot_request_duration_seconds",
    "Request processing time",
    ["command"],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.5, 5.0, 10.0],
)

active_users = Gauge("bot_active_users", "Active users in last hour")

mood_scores = Gauge("bot_mood_score", "Latest mood scores", ["user_id"])

users_registered_total = Counter(
    "bot_users_registered_total", "Total users registered", ["telegram"]
)


def start_metrics_server(port: int = 8000):
    start_http_server(port)
    print(f"📊 Metrics server started on port {port}")
