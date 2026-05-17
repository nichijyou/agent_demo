from __future__ import annotations

import argparse
from pathlib import Path

from agent_demo.diagnosis import diagnose
from agent_demo.evaluation import evaluate_dataset, find_case, load_eval_cases
from agent_demo.models import BugReport
from agent_demo.report import write_report
from agent_demo.toy_agent import run_agent
from agent_demo.tracing import render_ascii_tree, save_trace


BASE_DIR = Path(__file__).resolve().parent
TRACE_PATH = BASE_DIR / "traces" / "latest_trace.json"
REPORT_PATH = BASE_DIR / "reports" / "latest_report.md"
EVAL_DATA_PATH = BASE_DIR / "data" / "eval_cases.json"


def main() -> None:
    args = parse_args()
    eval_cases = load_eval_cases(EVAL_DATA_PATH)
    selected_case = find_case(eval_cases, args.case) if args.case else None
    report = selected_case.bug_report if selected_case else default_report()

    agent_result = run_agent(report, fix=args.fix)
    save_trace(agent_result.trace, TRACE_PATH)

    cases_to_eval = [selected_case] if selected_case and not args.eval else eval_cases
    summary = evaluate_dataset(cases_to_eval, fix=args.fix)
    diagnoses = diagnose(summary)
    write_report(REPORT_PATH, agent_result, summary, diagnoses)

    if args.report and not args.eval and not selected_case:
        print("REPORT WRITTEN")
        print(f"REPORT PATH: {REPORT_PATH}")
        return

    if not args.eval and not args.report:
        print_final_answer(agent_result.final_answer)
        print_trace(agent_result.trace)

    print_evaluation(summary)
    print_diagnosis(diagnoses)
    print()
    print(f"TRACE PATH: {TRACE_PATH}")
    print(f"REPORT PATH: {REPORT_PATH}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Deterministic PyCon agent tracing demo.")
    parser.add_argument("--case", help="Run one eval case by id, for example fastapi_422.")
    parser.add_argument("--fix", action="store_true", help="Enable the fixed classifier rule.")
    parser.add_argument("--eval", action="store_true", help="Run the full dataset evaluation.")
    parser.add_argument("--report", action="store_true", help="Generate the Markdown report.")
    return parser.parse_args()


def default_report() -> BugReport:
    return BugReport(
        title="AttributeError when user profile is missing",
        body="The endpoint crashes with 'NoneType' object has no attribute 'email'.",
    )


def print_final_answer(final_answer: str) -> None:
    print("FINAL ANSWER")
    print(final_answer)
    print()


def print_trace(trace: object) -> None:
    print("TRACE TREE")
    print(render_ascii_tree(trace))
    print()


def print_evaluation(summary: object) -> None:
    print("DATASET EVALUATION")
    print(f"cases={summary.total} passed={summary.passed} average_score={summary.score:.2f}")
    for result in summary.results:
        status = "PASS" if result.passed else "FAIL"
        print(f"- {result.case_id}: {status} score={result.score:.2f}")


def print_diagnosis(diagnoses: object) -> None:
    print()
    print("DIAGNOSIS")
    for item in diagnoses:
        print(f"- {item.case_id}: {item.root_cause}")
        for evidence in item.evidence:
            print(f"  evidence: {evidence}")
        for suggestion in item.suggestion:
            print(f"  suggestion: {suggestion}")


if __name__ == "__main__":
    main()
