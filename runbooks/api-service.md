# API Service Incident Runbook

## High Error Rate (> 5%)

1. Check database connectivity
2. Review slow query logs
3. Check service resource usage (CPU, memory)
4. If database is slow, check for missing indexes
5. Escalate to on-call DBA if unresolved

## High Latency (p99 > 1000ms)

1. Check request queue depth
2. Profile recent deployments
3. Check downstream service health
4. Review cache hit rates
