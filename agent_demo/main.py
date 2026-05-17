from __future__ import annotations

from pathlib import Path

from agent_demo.diagnosis import diagnose
from agent_demo.evaluation import evaluate_dataset, load_eval_cases
from agent_demo.models import BugReport
from agent_demo.report import write_report
from agent_demo.toy_agent import run_agent
from agent_demo.tracing import render_ascii_tree, save_trace


BASE_DIR = Path(__file__).resolve().parent
TRACE_PATH = BASE_DIR / "traces" / "latest_trace.json"
REPORT_PATH = BASE_DIR / "reports" / "latest_report.md"
EVAL_DATA_PATH = BASE_DIR / "data" / "eval_cases.json"


def main() -> None:
    report = BugReport(
        title="AttributeError when user profile is missing",
        body="The endpoint crashes with 'NoneType' object has no attribute 'email'.",
    )

    agent_result = run_agent(report)
    save_trace(agent_result.trace, TRACE_PATH)

    eval_cases = load_eval_cases(EVAL_DATA_PATH)
    summary = evaluate_dataset(eval_cases)
    diagnoses = diagnose(summary)
    write_report(REPORT_PATH, agent_result, summary, diagnoses)

    print("FINAL ANSWER")
    print(agent_result.final_answer)
    print()
    print("TRACE TREE")
    print(render_ascii_tree(agent_result.trace))
    print()
    print("DATASET EVALUATION")
    print(f"cases={summary.total} passed={summary.passed} average_score={summary.score:.2f}")
    print()
    print(f"REPORT PATH: {REPORT_PATH}")


if __name__ == "__main__":
    main()

