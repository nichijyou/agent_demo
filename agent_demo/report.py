from __future__ import annotations

"""Markdown report writer for the PyCon demo."""

from pathlib import Path

from agent_demo.models import AgentResult, Diagnosis, EvalSummary
from agent_demo.tracing import render_ascii_tree


def write_report(
    path: Path,
    agent_result: AgentResult,
    summary: EvalSummary,
    diagnoses: list[Diagnosis],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    failed = [result for result in summary.results if not result.passed]
    lines = [
        "# Bug Triage Agent Report",
        "",
        "## Summary",
        "",
        "A deterministic bug triage agent was traced, evaluated, diagnosed, and reported.",
        "",
        "## Dataset score",
        "",
        f"- Cases: {summary.total}",
        f"- Passed: {summary.passed}",
        f"- Average score: {summary.score:.2f}",
        "",
        "## Failed cases",
        "",
    ]
    if failed:
        for result in failed:
            lines.append(
                f"- {result.case_id}: "
                f"score={result.score:.2f}; "
                f"{'; '.join(result.notes)}"
            )
    else:
        lines.append("- None")

    lines.extend(
        [
            "",
            "## Root cause",
            "",
        ]
    )
    for diagnosis in diagnoses:
        lines.append(f"- {diagnosis.case_id}: {diagnosis.root_cause}")

    lines.extend(["", "## Evidence", ""])
    for diagnosis in diagnoses:
        if diagnosis.evidence:
            lines.append(f"### {diagnosis.case_id}")
            lines.extend(f"- {item}" for item in diagnosis.evidence)
        else:
            lines.append(f"- {diagnosis.case_id}: no failure evidence")

    lines.extend(["", "## Suggestion", ""])
    for diagnosis in diagnoses:
        if diagnosis.suggestion:
            lines.append(f"### {diagnosis.case_id}")
            lines.extend(f"- {item}" for item in diagnosis.suggestion)
        else:
            lines.append(f"- {diagnosis.case_id}: keep current regression set")

    lines.extend(
        [
            "",
            "## Trace tree excerpt",
            "",
            "```text",
            render_ascii_tree(agent_result.trace),
            "```",
            "",
            "## Single case final answer",
            "",
            agent_result.final_answer,
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")
