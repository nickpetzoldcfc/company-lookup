from typing import Optional

from ninja import Schema
from pydantic import model_validator


class CompanyLookupRequest(Schema):
    name: Optional[str] = None
    address: Optional[str] = None
    postcode: Optional[str] = None
    website: Optional[str] = None

    @model_validator(mode="after")
    def at_least_one_field(self):
        if not any([self.name, self.address, self.postcode, self.website]):
            raise ValueError("At least one search field must be provided")
        return self

    @model_validator(mode="after")
    def name_required(self):
        if not self.name or not self.name.strip():
            raise ValueError("'name' is required for company lookup")
        return self


class AddressResponse(Schema):
    city: Optional[str] = None
    postcode: Optional[str] = None
    street: Optional[str] = None


class CompanyLookupResponse(Schema):
    address: AddressResponse
    company_number: Optional[str] = None
    credit_score: Optional[int] = None
    domain: Optional[str] = None
    last_default_date: Optional[str] = None
    match_confidence: str
    name: Optional[str] = None
    trade_lines: Optional[int] = None
