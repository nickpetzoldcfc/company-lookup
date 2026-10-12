# INC-4471: Inconsistent company lookup results

**Raised by:** Customer Onboarding Support
**Priority:** P2
**Service:** company-lookup-api 1.4.0 (production)

## What's happening

Since the 1.4.0 release on Tuesday 29 September, the onboarding team have been reporting that some lookups come back as `no_match` for companies we definitely hold. The odd thing is that it isn't consistent: the same request can work, then fail a minute later, then work again.

Example request they sent us:

```http
POST /v1/companies/lookup
Content-Type: application/json

{
    "name": "Ashworth Group Ltd",
    "address": "Unit 4, Canal Wharf",
    "postcode": "BL1 4QT",
    "website": "https://www.ashworthgroup.co.uk"
}
```

They think they've seen it with "a couple of others" but didn't keep the details.

## Also

Separately, the staging deployment of the next release failed this morning after the nightly credit bureau data refresh. The service won't start. The platform team sent this from the logs:

```text
  File "/service/src/company_lookup.py", line 315, in build_credit_bureau_data_lookups
    record["last_default_date"] = self.normalise_date(
                                  ^^^^^^^^^^^^^^^^^^^^
  File "/service/src/company_lookup.py", line 279, in normalise_date
    raise ValueError(f"Invalid date format: {date_str}")
ValueError: Invalid date format: 13/12/2000

ERROR:    Application startup failed. Exiting.
```

A copy of the refreshed file is at `src/data/staging/credit_bureau.csv`. Staging uses `CREDIT_BUREAU_PATH` to point at it.

Please investigate and fix.
