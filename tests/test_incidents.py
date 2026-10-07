#!/usr/bin/env python3
"""Test incident assistant on simulated incidents."""
import json
from src.incident_assistant import IncidentAssistant, Alert

def test_high_error_rate():
    """Test handling high error rate alert."""
    assistant = IncidentAssistant()
    alert = Alert(
        service="api-service",
        severity="high",
        message="Error rate 10% above baseline",
        timestamp="2024-01-15T14:30:00Z"
    )
    result = assistant.process_alert(alert)
    
    assert result["alert"]["service"] == "api-service"
    assert result["requires_approval"] == True
    assert "proposal" in result
    assert len(result["evidence"]["logs"]) > 0
    print("✓ High error rate test passed")

def test_cpu_spike():
    """Test handling CPU spike alert."""
    assistant = IncidentAssistant()
    alert = Alert(
        service="cache-service",
        severity="medium",
        message="CPU usage 95%",
        timestamp="2024-01-15T15:00:00Z"
    )
    result = assistant.process_alert(alert)
    
    assert result["evidence"]["metrics"]["cpu_percent"] > 85
    assert "proposal" in result
    print("✓ CPU spike test passed")

if __name__ == "__main__":
    test_high_error_rate()
    test_cpu_spike()
    print("\nAll tests passed!")
