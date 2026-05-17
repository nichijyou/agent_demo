from __future__ import annotations

"""Trace-based failure diagnosis for evaluation results."""

from agent_demo.models import Diagnosis, EvalSummary, TraceNode
from agent_demo.tracing import find_span


FASTAPI_ROOT_CAUSE = (
    "The classifier selected the wrong bug category, which sent the agent down "
    "the wrong tool path."
)


def diagnose(summary: EvalSummary) -> list[Diagnosis]:
    if summary.passed == summary.total:
        return [
            Diagnosis(
                case_id="all",
                root_cause=(
                    "All eval cases passed. No immediate diagnosis needed."
                ),
                evidence=[],
                suggestion=[],
            )
        ]

    findings = []
    for result in summary.results:
        if not result.passed:
            findings.append(_diagnose_failure(result.case_id, result.trace, result.notes))
    return findings


def _diagnose_failure(case_id: str, trace: TraceNode, notes: list[str]) -> Diagnosis:
    if case_id == "fastapi_422":
        classify_span = find_span(trace, "classify_bug_tool")
        search_span = find_span(trace, "search_known_issue_tool")
        evidence = []
        if classify_span:
            evidence.append(f"classify_bug_tool input: {classify_span.input}")
            evidence.append(f"classify_bug_tool output: {classify_span.output}")
        if search_span:
            evidence.append(f"search_known_issue_tool input: {search_span.input}")
        return Diagnosis(
            case_id=case_id,
            root_cause=FASTAPI_ROOT_CAUSE,
            evidence=evidence,
            suggestion=[
                "Add a regression test for FastAPI 422.",
                "Improve classifier rule for FastAPI validation errors.",
                "Evaluate trajectory, not only final answer.",
            ],
        )

    return Diagnosis(
        case_id=case_id,
        root_cause=(
            "The agent output did not match the expected evaluation signals."
        ),
        evidence=notes,
        suggestion=["Inspect the trace tree and add a focused regression case."],
    )
