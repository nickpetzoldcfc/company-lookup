from app import audit


def test_record_and_fetch_lookup() -> None:
    audit.record_lookup("Test Company", "AB1 2CD", "high")

    rows = audit.lookups_for_company("test company")

    assert rows[0]["confidence"] == "high"
