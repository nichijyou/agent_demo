from __future__ import annotations

"""Regression tests for the PyCon demo workflow."""

from pathlib import Path

from agent_demo.diagnosis import diagnose
from agent_demo.evaluation import evaluate_dataset, find_case, load_eval_cases
from agent_demo.main import EVAL_DATA_PATH, REPORT_PATH, TRACE_PATH, main


def test_default_fastapi_422_fails() -> None:
    case = find_case(load_eval_cases(EVAL_DATA_PATH), "fastapi_422")
    summary = evaluate_dataset([case])

    assert summary.passed == 0
    assert summary.results[0].passed is False
    assert (
        "expected classification fastapi_validation_error"
        in summary.results[0].notes[0]
    )
    assert diagnose(summary)[0].root_cause.startswith(
        "The classifier selected the wrong bug category"
    )


def test_fastapi_422_fix_passes() -> None:
    case = find_case(load_eval_cases(EVAL_DATA_PATH), "fastapi_422")
    summary = evaluate_dataset([case], fix=True)

    assert summary.passed == 1
    assert summary.results[0].passed is True


def test_trace_json_is_generated(monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["agent_demo.main", "--case", "fastapi_422"])
    main()

    assert Path(TRACE_PATH).exists()
    assert "classify_bug_tool" in Path(TRACE_PATH).read_text(encoding="utf-8")


def test_report_markdown_is_generated(monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["agent_demo.main", "--report"])
    main()

    text = Path(REPORT_PATH).read_text(encoding="utf-8")
    assert "# Bug Triage Agent Report" in text
    assert "## Root cause" in text
    assert "## Trace tree excerpt" in text
