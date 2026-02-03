# Product Spec

We currently have a **Company Lookup** capability that reconciles imperfect, user-submitted company details against authoritative datasets (Companies House and a credit bureau). This logic already exists from the Codility exercise and can be found within this repo.

We now want to make this capability available to other internal services via a simple HTTP API.

## Desired behaviour

The API should:

- Accept JSON input in the same shape as below
- Return JSON output that strictly follows the data contract defined below
- Use appropriate HTTP status codes (e.g. success vs invalid input)
- Behave deterministically and predictably

The API is intended for internal use in production systems so should be designed accordingly.

### Data Contracts

#### Input schema (example)

```json
{
    "name": " robinson ",  // Required
    "address": "928 jodie land",  // Optional
    "postcode": " l7a 5eu ",  // Required
    "website": "http://www.hughes.com"  // Optional
}
```

#### Output schema (example)

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
