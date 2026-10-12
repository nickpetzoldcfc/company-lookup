from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def client() -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client


def test_health(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_lookup_high_confidence(client: TestClient) -> None:
    response = client.post(
        "/v1/companies/lookup",
        json={
            "name": "FREEMAN",
            "address": "989 Hayes mission",
            "postcode": " b8t  6jr ",
            "website": " WWW.RICHARDS.COM",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["match_confidence"] == "high"
    assert body["company_number"] == "4568157"
    assert body["name"] == "Freeman PLC"


def test_lookup_no_match(client: TestClient) -> None:
    response = client.post(
        "/v1/companies/lookup",
        json={"name": "Definitely Not A Real Company"},
    )

    assert response.status_code == 200
    assert response.json()["match_confidence"] == "no_match"


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"name": ""},
        {"name": None},
        {"name": "x" * 256},
    ],
)
def test_lookup_rejects_invalid_input(client: TestClient, payload: dict) -> None:
    response = client.post("/v1/companies/lookup", json=payload)

    assert response.status_code == 422
