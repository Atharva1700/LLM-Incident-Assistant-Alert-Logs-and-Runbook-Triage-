# LLM Incident Assistant

AI-powered incident response: takes alerts, fetches metrics and logs, matches runbooks, proposes next steps with evidence. Never acts without human approval.

**Stack:** Python, LangGraph, Claude API, Prometheus

**Workflow:**
1. Ingest simulated alert
2. Query Prometheus metrics and logs
3. Match to runbook
4. Propose investigation steps with supporting evidence
5. Await human approval before any action

**Tested:** Validated on set of simulated incidents.
