from __future__ import annotations


def classify_bug_tool(title: str, body: str) -> str:
    text = f"{title} {body}".lower()
    if "none" in text or "null" in text or "attributeerror" in text:
        return "none-handling"
    if "indexerror" in text or "out of range" in text:
        return "bounds-check"
    if "timeout" in text or "slow" in text:
        return "performance"
    return "general-python"


def search_known_issue_tool(classification: str) -> str:
    known_issues = {
        "none-handling": "Common when optional values are used before validation.",
        "bounds-check": "Common when loops assume a list has at least one item.",
        "performance": "Common when repeated work happens inside a tight loop.",
        "general-python": "No exact known issue found.",
    }
    return known_issues[classification]


def suggest_fix_tool(classification: str, known_issue: str) -> str:
    fixes = {
        "none-handling": "Add an explicit None guard before accessing attributes.",
        "bounds-check": "Check collection length before indexing, or iterate directly.",
        "performance": "Cache repeated computations and measure the hot path.",
        "general-python": "Reproduce with a minimal test, then isolate the failing branch.",
    }
    return f"{fixes[classification]} Context: {known_issue}"

