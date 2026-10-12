# Changelog

## 1.4.0 - Tuesday 29 September 2026

- Run the API with 4 uvicorn workers to handle the onboarding campaign peak (OPS-311).
- Strip "Group" as a company suffix during name normalisation, alongside Inc, LLC, Ltd and PLC (LOOKUP-87, product request).

## 1.3.0 - Monday 14 September 2026

- Request validation: reject empty or oversized fields with a 422.
- Load reference data once at startup via the FastAPI lifespan.

## 1.2.0 - Thursday 3 September 2026

- Initial `/v1/companies/lookup` endpoint wrapping `CompanyLookup.find`.
- `/health` endpoint for the platform readiness probe.
