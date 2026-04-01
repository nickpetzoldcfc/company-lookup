import threading
import time

from ninja.errors import HttpError

MAX_REQUESTS = 10
WINDOW_SECONDS = 1.0

_lock = threading.Lock()
_timestamps: list[float] = []


def check_rate_limit():
    now = time.monotonic()
    with _lock:
        cutoff = now - WINDOW_SECONDS
        while _timestamps and _timestamps[0] < cutoff:
            _timestamps.pop(0)
        if len(_timestamps) >= MAX_REQUESTS:
            raise HttpError(429, "Rate limit exceeded. Maximum 10 requests per second.")
        _timestamps.append(now)


def reset_rate_limiter():
    with _lock:
        _timestamps.clear()
