import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    companies_house_path: str
    credit_bureau_path: str
    log_level: str


def get_settings() -> Settings:
    return Settings(
        companies_house_path=os.getenv(
            "COMPANIES_HOUSE_PATH", "src/data/companies_house.json"
        ),
        credit_bureau_path=os.getenv(
            "CREDIT_BUREAU_PATH", "src/data/credit_bureau.csv"
        ),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
    )
