from enum import StrEnum

from pydantic import BaseModel, Field


class MatchConfidence(StrEnum):
    NO_MATCH = "no_match"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class LookupRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    address: str | None = Field(default=None, max_length=500)
    postcode: str | None = Field(default=None, max_length=16)
    website: str | None = Field(default=None, max_length=255)


class Address(BaseModel):
    street: str | None
    city: str | None
    postcode: str | None


class LookupResponse(BaseModel):
    address: Address
    company_number: str | None
    credit_score: int | None
    domain: str | None
    last_default_date: str | None
    match_confidence: MatchConfidence
    name: str | None
    trade_lines: int | None
