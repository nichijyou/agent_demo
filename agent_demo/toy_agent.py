from __future__ import annotations

from agent_demo.models import AgentResult, BugReport
from agent_demo.tools import classify_bug_tool, search_known_issue_tool, suggest_fix_tool
from agent_demo.tracing import Tracer


def mock_llm_plan(report: BugReport) -> list[str]:
    return [
        "classify the bug",
        "search known issues",
        "suggest a fix",
        "write final answer",
    ]


def run_agent(report: BugReport) -> AgentResult:
    tracer = Tracer(
        root_name="bug_triage_agent",
        inputs={"title": report.title, "body": report.body},
    )

    with tracer.span("mock_llm_plan", "llm", {"bug_report": report.title}) as span:
        plan = mock_llm_plan(report)
        span.outputs["plan"] = plan

    with tracer.span("classify_bug_tool", "tool", {"title": report.title}) as span:
        classification = classify_bug_tool(report.title, report.body)
        span.outputs["classification"] = classification

    with tracer.span("search_known_issue_tool", "tool", {"classification": classification}) as span:
        known_issue = search_known_issue_tool(classification)
        span.outputs["known_issue"] = known_issue

    with tracer.span(
        "suggest_fix_tool",
        "tool",
        {"classification": classification, "known_issue": known_issue},
    ) as span:
        suggested_fix = suggest_fix_tool(classification, known_issue)
        span.outputs["suggested_fix"] = suggested_fix

    final_answer = (
        f"Classification: {classification}\n"
        f"Known issue: {known_issue}\n"
        f"Suggested fix: {suggested_fix}"
    )
    tracer.root.outputs["final_answer"] = final_answer

    return AgentResult(
        final_answer=final_answer,
        classification=classification,
        known_issue=known_issue,
        suggested_fix=suggested_fix,
        trace=tracer.root,
    )

