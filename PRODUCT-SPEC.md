# Product Spec: Company Lookup API

The **Company Lookup** capability reconciles imperfect, user-submitted company details against authoritative datasets (Companies House and a credit bureau). It is exposed to other internal services as a REST API (`company-lookup-api`, see `app/`).

This is the original product spec the service was built from. It describes the business behaviour and data contract the API is expected to honour.

---

## Desired behaviour

The HTTP Endpoint should:

- accept JSON input in the same shape as defined below,
- return JSON output that **strictly follows the data contract**,
- use appropriate HTTP status codes (e.g. success vs invalid input),
- behave deterministically and predictably.

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
    "name": "Robinson PLC", // String
    "trade_lines": 10 // Int | NULL
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
