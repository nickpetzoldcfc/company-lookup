import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from app.config import get_settings
from app.schemas import LookupRequest, LookupResponse
from src.company_lookup import CompanyLookup

logger = logging.getLogger("company_lookup_api")

NO_MATCH = {
    "name": None,
    "address": {"street": None, "city": None, "postcode": None},
    "domain": None,
    "company_number": None,
    "credit_score": None,
    "last_default_date": None,
    "match_confidence": "no_match",
    "trade_lines": None,
}


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    logging.basicConfig(level=settings.log_level)

    app.state.company_lookup = CompanyLookup(
        companies_house_filepath=settings.companies_house_path,
        credit_bureau_filepath=settings.credit_bureau_path,
    )
    logger.info(
        "Loaded %d companies", len(app.state.company_lookup.company_name_lookup)
    )
    yield


app = FastAPI(title="Company Lookup API", version="1.4.0", lifespan=lifespan)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/companies/lookup", response_model=LookupResponse)
async def lookup_company(payload: LookupRequest, request: Request) -> LookupResponse:
    logger.info("Lookup request received: %s", payload.model_dump())

    try:
        result = request.app.state.company_lookup.find(payload.model_dump())
    except Exception:
        logger.exception("Lookup failed")
        result = NO_MATCH

    return LookupResponse(**result)
