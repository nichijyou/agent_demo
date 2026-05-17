from __future__ import annotations

from pathlib import Path

from agent_demo.models import AgentResult, EvalSummary


def write_report(
    path: Path,
    agent_result: AgentResult,
    summary: EvalSummary,
    diagnoses: list[str],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Bug Triage Agent Report",
        "",
        "## Single Case",
        "",
        agent_result.final_answer,
        "",
        "## Dataset Evaluation",
        "",
        f"- Cases: {summary.total}",
        f"- Passed: {summary.passed}",
        f"- Average score: {summary.score:.2f}",
        "",
        "## Diagnosis",
        "",
    ]
    lines.extend(f"- {item}" for item in diagnoses)
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")

