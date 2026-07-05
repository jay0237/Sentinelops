from prometheus_client import Counter, Histogram
from slowapi import Limiter
from slowapi.util import get_remote_address

REQUEST_COUNT = Counter(
    "sentinelops_api_requests_total",
    "Total API Requests"
)

SAFE_PROMPT_COUNT = Counter(
    "sentinelops_safe_prompts_total",
    "Total safe prompts"
)

BLOCKED_PROMPT_COUNT = Counter(
    "sentinelops_blocked_prompts_total",
    "Total blocked prompts"
)

HIGH_THREAT_COUNT = Counter(
    "sentinelops_high_threat_total",
    "Total high threat prompts"
)

REQUEST_DURATION = Histogram(
    "sentinelops_request_duration_seconds",
    "Duration of API requests in seconds"
)

limiter = Limiter(key_func=get_remote_address)
