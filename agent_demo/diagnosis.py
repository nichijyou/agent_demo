from __future__ import annotations

from agent_demo.models import EvalSummary


def diagnose(summary: EvalSummary) -> list[str]:
    if summary.passed == summary.total:
        return ["All eval cases passed. No immediate diagnosis needed."]

    findings = []
    for result in summary.results:
        if not result.passed:
            findings.append(f"{result.case_id}: " + "; ".join(result.notes))
    return findings

