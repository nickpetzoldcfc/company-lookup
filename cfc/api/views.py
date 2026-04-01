import hashlib
import json
import logging
import time

from django.core.cache import cache
from ninja import Router

from api.rate_limiter import check_rate_limit
from api.schemas import CompanyLookupRequest, CompanyLookupResponse
from api.services import get_company_lookup

logger = logging.getLogger("api.views")

router = Router()


def _cache_key(data: dict) -> str:
    normalised = json.dumps(
        {k: (v.strip().lower() if isinstance(v, str) else v) for k, v in sorted(data.items()) if v},
        sort_keys=True,
    )
    return f"lookup:{hashlib.sha256(normalised.encode()).hexdigest()}"


@router.post("/lookup", response=CompanyLookupResponse)
def company_lookup(request, payload: CompanyLookupRequest):
    check_rate_limit()

    input_data = {
        "name": payload.name or "",
        "website": payload.website or "",
        "postcode": payload.postcode or "",
        "address": payload.address or "",
    }

    key = _cache_key(input_data)
    cached = cache.get(key)
    if cached is not None:
        logger.info("Cache hit for key=%s", key)
        return cached

    start = time.monotonic()
    logger.info("Lookup started for name=%r", payload.name)

    lookup = get_company_lookup()
    result = lookup.find(input_data)

    duration_ms = (time.monotonic() - start) * 1000
    logger.info("Lookup completed in %.1fms, confidence=%s", duration_ms, result["match_confidence"])

    cache.set(key, result, timeout=300)
    return result
