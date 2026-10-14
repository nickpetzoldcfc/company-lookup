# Technical Interview: Company Lookup API

`company-lookup-api` is a small internal service that matches imperfect company details against Companies House and credit bureau data. It's in production and other teams depend on it. Today you're joining the team that owns it.

## The session (60 minutes)

| Part | Time | What you'll do |
|---|---|---|
| 1 | ~22 min | Investigate and fix a live issue: [INCIDENT.md](INCIDENT.md) |
| 2 | ~10 min | Review a colleague's pull request: [review/PR-218.md](review/PR-218.md) |
| 3 | ~15 min | Design and delivery discussion with us (no laptop needed) |
| 4 | ~10 min | Your experience, and your questions for us |

**Please think out loud.** We're much more interested in how you reason than in how much code you produce. It's fine not to finish; tell us what you'd do next.

**AI coding tools are welcome** in part 1, just as they would be in your day job. Use them however you normally would. We'll ask you to explain the changes you make, so make sure you're comfortable with anything you accept.

Ask us questions at any time. We'll play the roles of product owner, support and colleagues where it helps.

## Getting started

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone <repo-url> company-lookup && cd company-lookup
git checkout -b fix/INC-4471

uv sync                                     # install dependencies
uv run pytest                               # run the tests
uv run ruff check . && uv run ruff format --check .
uv run uvicorn app.main:app --reload        # run the API at http://localhost:8000/docs
```

## Repository layout

```text
app/                   FastAPI service (config, schemas, routes)
src/company_lookup.py  Matching logic (CompanyLookup.find)
src/data/              Reference data (Companies House, credit bureau)
src/tests/             Matching tests and fixtures
tests/                 API tests
ci/pipeline.yml        CI/CD pipeline (tool-agnostic syntax)
Dockerfile             Production image
CHANGELOG.md           Release history
PRODUCT-SPEC.md        Original product spec and data contract
INCIDENT.md            Part 1
review/PR-218.md       Part 2
```
