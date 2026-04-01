# Title

Create an Company Lookup endpoint that fuzzy-matches companies

---

## Business Description

We have an existing **Company Lookup** capability that reconciles imperfect, user-submitted company details against authoritative datasets (Companies House and a credit bureau). This logic already exists within the repository and should be reused.

Users searching may not exact spelling or complete company details, so we need a way to find the company they're looking for with that incomplete info.

---

## Acceptance Criteria

- Allow searching by `name`, `address`, `postcode`, `website` in the following format:
    ```json
    {
        "name": " robinson ",
        "address": "928 jodie land",
        "postcode": " l7a 5eu ",
        "website": "http://www.hughes.com"
    }
- Provide an output in the following format:
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


---

## Technical Details

- Use the `src/company_lookup.py:CompanyLookup.find` function to generate results
- Set up rate limits (10 requests/second)
- Response with a 422 request when the input in invalid
    - Provide details on what was invalid
- Adhere to OWASP API Security recommendations
- Instrument the code with logs at the approriate log level
    - Warnings when we receive an invalid input
    - Info logs to allow us to see how long a process is taking
    - Add timestamps to logs
- Use Django and `django-ninja` to build the API
- Use SQLite as the database
- Implement database caching in Django using the in-memory SQLite database
- The server must return a 500 response instead of crashing if there is an unexpected failure

---

## Task Breakdown

- [ ] **1. Scaffold Django project**
    - Run `django-admin startproject` and create an app (e.g. `api`)
    - Configure `settings.py`: installed apps (`ninja`), SQLite database, logging
    - Wire up `manage.py` as the entrypoint

- [ ] **2. Define request/response schemas**
    - Create django-ninja `Schema` for the input (`name`, `address`, `postcode`, `website` — all optional strings)
    - Create django-ninja `Schema` for the output (matching the acceptance criteria format)
    - Add field-level validation (e.g. reject empty requests where no fields are provided)

- [ ] **3. Build the `/lookup` endpoint**
    - Create a `POST` endpoint using django-ninja's `Router`
    - Accept the input schema, call `CompanyLookup.find()`, return the output schema
    - Return `422` with detail messages when input validation fails

- [ ] **4. Add rate limiting**
    - Implement rate limiting middleware or decorator (10 requests/second)
    - Return `429 Too Many Requests` when the limit is exceeded

- [ ] **5. Implement database caching**
    - Configure Django's cache framework with an in-memory SQLite backend
    - Cache `CompanyLookup.find()` results keyed on normalised input
    - Serve cached responses for repeated lookups

- [ ] **6. Add error handling**
    - Add a global exception handler in middleware so unexpected errors return a `500` JSON response (not a crash/traceback)
    - Return structured error bodies (`{"detail": "..."}`)

- [ ] **7. Instrument with logging**
    - Configure timestamped log formatting in `settings.py`
    - `WARNING` log on invalid input (422 responses)
    - `INFO` logs with timing for each lookup (start → end with duration)

- [ ] **8. OWASP API security hardening**
    - Validate and sanitise all input fields
    - Set security headers (e.g. `Content-Type` enforcement)
    - Ensure verbose error details are not leaked to clients in production

- [ ] **9. Write API-layer tests**
    - Test valid lookups return correct shape and data
    - Test 422 responses for invalid/missing input
    - Test 500 handling for unexpected errors
    - Test rate limiting returns 429

- [ ] **10. Manual smoke test**
    - Start the server (`python manage.py runserver`)
    - `curl` the endpoint with sample data from `src/data/sample_customer_data.json`
    - Verify response matches expected output format
