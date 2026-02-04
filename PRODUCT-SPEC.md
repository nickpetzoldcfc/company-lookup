# Product Spec: Company Lookup API

We have an existing **Company Lookup** capability that reconciles imperfect, user-submitted company details against authoritative datasets (Companies House and a credit bureau). This logic already exists within the repository and should be reused.

We now want to make this capability available to other internal services via a simple REST API.

From a development perspective, this should be treated as a **new service**. While the core lookup logic already exists via `CompanyLookup.find`, the surrounding application (API layer, structure, configuration, and tooling) is being created from scratch.

---

## Desired behaviour

The API should:

- accept JSON input in the same shape as defined below,
- return JSON output that **strictly follows the data contract**,
- use appropriate HTTP status codes (e.g. success vs invalid input),
- behave deterministically and predictably.

The API is intended for use by production systems. Candidates are expected to demonstrate **sound engineering judgement** when implementing it, including awareness of reliability, security, performance, and long-term maintainability — applied proportionately to the scope of the exercise.

---

## Security and access considerations

The service should be designed with security in mind.

- Infrastructure-level concerns (e.g. IAM, OAuth flows, cloud identity providers) are **out of scope**.
- Application-level mechanisms, such as **simple API key authentication**, request validation, and safe error handling, are **in scope** and may be implemented where appropriate.
- Candidates should feel comfortable calling out risks, assumptions, and next steps, even if not fully implemented.

---

## Data contracts

### Input schema (example)

```json
{
    "name": " robinson ",
    "address": "928 jodie land",
    "postcode": " l7a 5eu ",
    "website": "http://www.hughes.com"
}
```

### Output schema (example)

```json
{
    "address": {
        "city": "Port Colin", // String | NULL
        "postcode": "L7A 5EU", // String | NULL
        "street": "928 Jodie land" // String | NULL
    },
    "company_number": "4958777", // String | NULL
    "credit_score": 887, // Int | NULL
    "domain": "hughes.com", // String | NULL
    "last_default_date": "2020-03-05", // String of ISO Format [YYYY-MM-DD] | NULL
    "match_confidence": "high", // ENUM [no_match | low | medium | high]
    "name": "Robinson PLC", // String "trade_lines": 10 // Int | NULL
}
```

## Using pre-built functionality

The current Company Lookup functionality can be found in `src/company_lookup.py`. The lookup is executed via calling the `find` function on the class itself as follows:

```python
from src.company_lookup import CompanyLookup

companies_house_filepath = "src/data/companies_house.json"
credit_bureau_filepath = "src/data/credit_bureau.csv"

company_lookup = CompanyLookup(
    companies_house_filepath=companies_house_filepath,
    credit_bureau_filepath=credit_bureau_filepath
)

input_data = {  # Same as input contract for API
    "name": " robinson ",
    "address": "928 jodie land",
    "postcode": " l7a 5eu ",
    "website": "http://www.hughes.com"
}

output_data = company_lookup.find(input_data)

print(output_data)
```

```json
// Same as output contract
{
    "address": {
        "city": "Port Colin",
        "postcode": "L7A 5EU",
        "street": "928 Jodie land"
    },
    "company_number": "4958777",
    "credit_score": 887,
    "domain": "hughes.com",
    "last_default_date": "2020-03-05",
    "match_confidence": "high",
    "name": "Robinson PLC",
}
```
