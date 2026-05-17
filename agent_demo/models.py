from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class TraceNode:
    span_id: str
    parent_id: str | None
    name: str
    kind: str
    input: dict[str, Any]
    output: dict[str, Any] = field(default_factory=dict)
    start_time: str = ""
    end_time: str = ""
    duration_ms: float = 0.0
    error: str | None = None
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
    trace: TraceNode


@dataclass
class EvalSummary:
    total: int
    passed: int
    score: float
    results: list[EvalResult]


@dataclass
class Diagnosis:
    case_id: str
    root_cause: str
    evidence: list[str]
    suggestion: list[str]
