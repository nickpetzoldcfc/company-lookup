import json
import pathlib

import pytest
from company_lookup import CompanyLookup

HIGH_CONFIDENCE_DATA_FILE = (
    pathlib.Path(__file__).parent / "test_data" / "high_confidence_test_data.json"
)
MEDIUM_CONFIDENCE_DATA_FILE = (
    pathlib.Path(__file__).parent / "test_data" / "medium_confidence_test_data.json"
)
LOW_CONFIDENCE_DATA_FILE = (
    pathlib.Path(__file__).parent / "test_data" / "low_confidence_test_data.json"
)
NO_MATCH_DATA_FILE = (
    pathlib.Path(__file__).parent / "test_data" / "no_match_test_data.json"
)

DATA_DIR = pathlib.Path(__file__).parent / "data"


@pytest.fixture(scope="session")
def company_lookup():
    return CompanyLookup(
        companies_house_filepath=DATA_DIR / "companies_house.json",
        credit_bureau_filepath=DATA_DIR / "credit_bureau.csv",
    )


def load_high_confidence_cases():
    """Return an iterable of pytest.param for @parametrize."""

    with open(HIGH_CONFIDENCE_DATA_FILE) as f:
        high_confidence_data = json.load(f)

    for i, record in enumerate(high_confidence_data):
        yield pytest.param(
            record["input"], record["expected_output"], id=f"high_confidence_case_{i}"
        )


def load_medium_confidence_cases():
    """Return an iterable of pytest.param for @parametrize."""

    with open(MEDIUM_CONFIDENCE_DATA_FILE) as f:
        medium_confidence_data = json.load(f)

    for i, record in enumerate(medium_confidence_data):
        yield pytest.param(
            record["input"], record["expected_output"], id=f"medium_confidence_case_{i}"
        )


def load_low_confidence_cases():
    """Return an iterable of pytest.param for @parametrize."""

    with open(LOW_CONFIDENCE_DATA_FILE) as f:
        low_confidence_data = json.load(f)

    for i, record in enumerate(low_confidence_data):
        yield pytest.param(
            record["input"], record["expected_output"], id=f"low_confidence_case_{i}"
        )


def load_no_match_cases():
    """Return an iterable of pytest.param for @parametrize."""

    with open(NO_MATCH_DATA_FILE) as f:
        no_match_data = json.load(f)

    for i, record in enumerate(no_match_data):
        yield pytest.param(
            record["input"], record["expected_output"], id=f"no_match_case_{i}"
        )


@pytest.mark.parametrize("input, expected_output", list(load_high_confidence_cases()))
def test_high_confidence_matches(company_lookup, input, expected_output):
    assert company_lookup.find(input) == expected_output


@pytest.mark.parametrize("input, expected_output", list(load_medium_confidence_cases()))
def test_medium_confidence_matches(company_lookup, input, expected_output):
    assert company_lookup.find(input) == expected_output


@pytest.mark.parametrize("input, expected_output", list(load_low_confidence_cases()))
def test_low_confidence_matches(company_lookup, input, expected_output):
    assert company_lookup.find(input) == expected_output


@pytest.mark.parametrize("input, expected_output", list(load_no_match_cases()))
def test_no_match_cases(company_lookup, input, expected_output):
    assert company_lookup.find(input) == expected_output
