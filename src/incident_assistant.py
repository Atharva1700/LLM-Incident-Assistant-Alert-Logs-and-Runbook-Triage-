#!/usr/bin/env python3
"""LLM-powered incident response assistant."""
from dataclasses import dataclass
from typing import Optional
import json
from anthropic import Anthropic

@dataclass
class Alert:
    service: str
    severity: str
    message: str
    timestamp: str

@dataclass
class Evidence:
    metrics: dict
    logs: list
    runbook: Optional[str]

class IncidentAssistant:
    def __init__(self):
        self.client = Anthropic()
        self.runbooks = self._load_runbooks()
    
    def process_alert(self, alert: Alert) -> dict:
        """Process alert: fetch evidence, propose steps."""
        evidence = self._gather_evidence(alert)
        
        prompt = f"""
Alert received: {alert.message}
Service: {alert.service}
Severity: {alert.severity}

Evidence:
- Metrics: {json.dumps(evidence.metrics, indent=2)}
- Recent logs: {json.dumps(evidence.logs[:5], indent=2)}
- Runbook: {evidence.runbook or "No matching runbook"}

Propose investigation steps. Do NOT take any action.
Cite your evidence for each step.
"""
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return {
            "alert": alert.__dict__,
            "evidence": {
                "metrics": evidence.metrics,
                "logs": evidence.logs,
                "runbook": evidence.runbook
            },
            "proposal": response.content[0].text,
            "requires_approval": True
        }
    
    def _gather_evidence(self, alert: Alert) -> Evidence:
        """Fetch metrics, logs, and matching runbook."""
        # Simulated metrics
        metrics = {
            "cpu_percent": 87.3,
            "memory_mb": 2048,
            "error_rate_pct": 5.2,
            "p99_latency_ms": 1250
        }
        
        # Simulated logs
        logs = [
            f"[{alert.timestamp}] ERROR: Connection timeout to database",
            f"[{alert.timestamp}] WARN: High CPU usage detected",
            "RETRY: Attempting reconnect..."
        ]
        
        # Match runbook
        runbook = self.runbooks.get(alert.service, None)
        
        return Evidence(metrics=metrics, logs=logs, runbook=runbook)
    
    def _load_runbooks(self) -> dict:
        """Load incident runbooks."""
        return {
            "api-service": "1. Check database connectivity\n2. Verify resource limits\n3. Review error logs",
            "cache-service": "1. Check Redis memory\n2. Verify eviction policy\n3. Check network latency",
        }

if __name__ == "__main__":
    assistant = IncidentAssistant()
    alert = Alert(
        service="api-service",
        severity="high",
        message="Error rate spiking above threshold",
        timestamp="2024-01-15T14:30:00Z"
    )
    result = assistant.process_alert(alert)
    print(json.dumps(result, indent=2))
