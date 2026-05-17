from __future__ import annotations


def classify_bug_tool(title: str, body: str, fix: bool = False) -> str:
    text = f"{title} {body}".lower()
    if "fastapi" in text and "422" in text:
        if fix:
            return "fastapi_validation_error"
        return "dependency_version_error"
    if "none" in text or "null" in text or "attributeerror" in text:
        return "none_handling"
    if "indexerror" in text or "out of range" in text:
        return "bounds_check"
    if "timeout" in text or "slow" in text:
        return "performance"
    return "general_python"


def search_known_issue_tool(classification: str) -> str:
    known_issues = {
        "none_handling": "Common when optional values are used before validation.",
        "bounds_check": "Common when loops assume a list has at least one item.",
        "performance": "Common when repeated work happens inside a tight loop.",
        "dependency_version_error": (
            "Common when a framework or package changed behavior between versions."
        ),
        "fastapi_validation_error": (
            "Common when the request JSON does not match the FastAPI validation schema."
        ),
        "general_python": "No exact known issue found.",
    }
    return known_issues[classification]


def suggest_fix_tool(classification: str, known_issue: str) -> str:
    fixes = {
        "none_handling": "Add an explicit None guard before accessing attributes.",
        "bounds_check": "Check collection length before indexing, or iterate directly.",
        "performance": "Cache repeated computations and measure the hot path.",
        "dependency_version_error": (
            "Pin and compare package versions before changing application code."
        ),
        "fastapi_validation_error": (
            "Align the request body with the validation schema and inspect field errors."
        ),
        "general_python": "Reproduce with a minimal test, then isolate the failing branch.",
    }
    return f"{fixes[classification]} Context: {known_issue}"
