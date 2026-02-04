# Technical Interview Brief: Company Lookup API

This interview is designed to simulate a realistic delivery scenario: taking an existing piece of business functionality and **productionising it as a backend service**.

The aim is not to test algorithmic problem-solving, but to understand how you:

- refine a loosely defined requirement,
- make sensible engineering decisions,
- and deliver a clean, production-minded REST API using modern development practices (including AI-assisted tooling).

We are not looking for trick solutions or completeness. We’re interested in how you **clarify requirements, structure work, and execute** under realistic constraints.

---

## How the interview will run

You should expect to:

- spend time early on **understanding and refining the problem**, including how the API should behave,
- ask clarifying questions and call out ambiguities,
- make reasonable assumptions and document them,
- write a short refinement or implementation ticket locally (e.g. in Markdown),
- and then focus on **executing and delivering a working API**.

There is no fixed split between “planning” and “coding”. You should manage your time in whatever way best supports delivering a clear, well-designed solution.

You’re welcome to ask questions at any point. Equally, if you prefer to work quietly and focus during the build, that’s completely fine.

---

## Implementation expectations

- You’ll be given existing Company Lookup functionality defined in `./src/` and asked to expose it behind an HTTP API.
- Any Python framework is fine (FastAPI, Flask, Django, etc.).
- AI-assisted development tools are encouraged and may be used freely.
- Infrastructure code (Terraform, pipelines, cloud setup) is **not** expected.

This exercise should be treated as the creation of a **new backend service**, rather than a small change to an existing one.

As such, we’re interested in the **foundational decisions** you make when starting a service from scratch, for example:

- project and package structure,
- dependency and package management approach,
- basic static analysis or linting considerations,
- and sensible defaults for a new codebase.

We don’t expect these to be fully implemented or production-hardened within the time available, but we do expect you to apply judgement and be able to explain the choices you make.

---

## Expectations and constraints

- Prioritise **clear API behaviour**, structure, and readability.
- Reasonable request/response validation and error handling are expected.
- Considerations such as logging, observability, and security are encouraged and should be applied with judgement.
- Testing (unit or integration) and static analysis are encouraged where time allows.
- No infrastructure, deployment, or cloud configuration is required.

The goal is **not** to configure every possible tool or system, but to demonstrate how you would **set a new service up for success**.

Please commit and push all changes at the end of the interview.
