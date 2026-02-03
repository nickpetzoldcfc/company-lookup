# Product Spec

We currently have a **Company Lookup** capability that reconciles imperfect, user-submitted company details against authoritative datasets (Companies House and a credit bureau). This logic already exists from the Codility exercise and can be found within this repo.

We now want to make this capability available to other internal services via a simple HTTP API.

## Desired behaviour

The API should:

- Accept JSON input in the same shape as the original assessment
- Return JSON output that strictly follows the original output contract
- Use appropriate HTTP status codes (e.g. success vs invalid input)
- Behave deterministically and predictably

The API is intended for internal use, but should be designed as if it could later be productionised.

## Expectations and constraints

- Focus on clear API design, structure, and readability.
- Reasonable request/response validation and error handling are expected.
- Testing (unit or integration) and static analysis are encouraged where time allows.
- No infrastructure, deployment, or cloud configuration is required.
- AI-assisted tooling is explicitly allowed and encouraged — we're interested in how you use it to accelerate delivery while retaining control and clarity.

## What we're evaluating

We'll primarily be looking at:

- How you refine and clarify a loosely defined requirement
- How you structure and expose backend functionality via an API
- The clarity, maintainability, and intent of your code
- Your ability to explain and review your own work

We're not expecting a finished or "perfect" solution — the focus is on approach, judgement, and communication, not raw output.
