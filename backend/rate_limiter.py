import time
from collections import defaultdict
from fastapi import Request, HTTPException

# Tracks request timestamps per IP address, in memory.
# Resets if the server restarts — fine for a demo project, no persistence needed.
_request_log: dict[str, list[float]] = defaultdict(list)

RATE_LIMIT = 5          # max requests
RATE_WINDOW = 60        # per this many seconds


def get_client_ip(request: Request) -> str:
    # Caddy sits in front of FastAPI, so the real visitor IP is in this header,
    # not in request.client.host (which would just be Caddy's own IP).
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def check_rate_limit(request: Request):
    ip = get_client_ip(request)
    now = time.time()

    # Drop timestamps older than the window, keep only recent ones
    _request_log[ip] = [t for t in _request_log[ip] if now - t < RATE_WINDOW]

    if len(_request_log[ip]) >= RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Max {RATE_LIMIT} requests per {RATE_WINDOW} seconds. Try again shortly."
        )

    _request_log[ip].append(now)
