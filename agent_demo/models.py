from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class TraceNode:
    name: str
    kind: str
    inputs: dict[str, Any]
    outputs: dict[str, Any] = field(default_factory=dict)
    children: list["TraceNode"] = field(default_factory=list)

    def add_child(self, child: "TraceNode") -> None:
        self.children.append(child)


@dataclass
class BugReport:
    title: str
    body: str


@dataclass
class AgentResult:
    final_answer: str
    classification: str
    known_issue: str
    suggested_fix: str
    trace: TraceNode


@dataclass
class EvalCase:
    id: str
    bug_report: BugReport
    expected_classification: str
    expected_contains: list[str]


@dataclass
class EvalResult:
    case_id: str
    passed: bool
    score: float
    notes: list[str]


@dataclass
class EvalSummary:
    total: int
    passed: int
    score: float
    results: list[EvalResult]

