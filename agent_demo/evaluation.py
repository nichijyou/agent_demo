from __future__ import annotations

import json
from pathlib import Path

from agent_demo.models import BugReport, EvalCase, EvalResult, EvalSummary
from agent_demo.toy_agent import run_agent


def load_eval_cases(path: Path) -> list[EvalCase]:
    raw_cases = json.loads(path.read_text(encoding="utf-8"))
    cases = []
    for raw in raw_cases:
        cases.append(
            EvalCase(
                id=raw["id"],
                bug_report=BugReport(**raw["bug_report"]),
                expected_classification=raw["expected_classification"],
                expected_contains=raw["expected_contains"],
            )
        )
    return cases


def find_case(cases: list[EvalCase], case_id: str) -> EvalCase:
    for case in cases:
        if case.id == case_id:
            return case
    raise ValueError(f"Unknown case id: {case_id}")


def evaluate_dataset(cases: list[EvalCase], fix: bool = False) -> EvalSummary:
    results = []
    for case in cases:
        agent_result = run_agent(case.bug_report, fix=fix)
        notes = []
        checks = 0
        passed_checks = 0

        checks += 1
        if agent_result.classification == case.expected_classification:
            passed_checks += 1
        else:
            notes.append(
                f"expected classification {case.expected_classification}, "
                f"got {agent_result.classification}"
            )

        for expected_text in case.expected_contains:
            checks += 1
            if expected_text.lower() in agent_result.final_answer.lower():
                passed_checks += 1
            else:
                notes.append(f"missing expected text: {expected_text}")

        score = passed_checks / checks
        results.append(
            EvalResult(
                case_id=case.id,
                passed=score == 1.0,
                score=score,
                notes=notes or ["all checks passed"],
                trace=agent_result.trace,
            )
        )

    passed = sum(1 for result in results if result.passed)
    score = sum(result.score for result in results) / len(results)
    return EvalSummary(total=len(results), passed=passed, score=score, results=results)
