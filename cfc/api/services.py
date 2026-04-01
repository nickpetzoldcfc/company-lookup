import os
from functools import lru_cache

from src.company_lookup import CompanyLookup

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "src", "data")


@lru_cache(maxsize=1)
def get_company_lookup() -> CompanyLookup:
    return CompanyLookup(
        companies_house_filepath=os.path.join(DATA_DIR, "companies_house.json"),
        credit_bureau_filepath=os.path.join(DATA_DIR, "credit_bureau.csv"),
    )
