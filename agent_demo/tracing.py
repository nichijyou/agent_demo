from __future__ import annotations

"""Tiny trace span helpers used by the demo agent."""

import json
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

from agent_demo.models import TraceNode


class Tracer:
    def __init__(self, root_name: str, input: dict[str, Any]) -> None:
        self._next_id = 1
        self._clock_ms = 0.0
        self.root = TraceNode(
            span_id=self._new_span_id(),
            parent_id=None,
            name=root_name,
            kind="agent",
            input=input,
            start_time=self._now(),
        )
        self._stack = [self.root]

    @contextmanager
    def span(self, name: str, kind: str, input: dict[str, Any]) -> Iterator[TraceNode]:
        parent = self._stack[-1]
        node = TraceNode(
            span_id=self._new_span_id(),
            parent_id=parent.span_id,
            name=name,
            kind=kind,
            input=input,
            start_time=self._now(),
        )
        parent.add_child(node)
        self._stack.append(node)
        try:
            yield node
        except Exception as exc:
            node.error = f"{exc.__class__.__name__}: {exc}"
            raise
        finally:
            node.end_time = self._now()
            node.duration_ms = _duration_ms(node.start_time, node.end_time)
            self._stack.pop()

    def set_output(self, **outputs: Any) -> None:
        self._stack[-1].output.update(outputs)

    def finish(self) -> None:
        self.root.end_time = self._now()
        self.root.duration_ms = _duration_ms(self.root.start_time, self.root.end_time)

    def _new_span_id(self) -> str:
        span_id = f"span-{self._next_id:04d}"
        self._next_id += 1
        return span_id

    def _now(self) -> str:
        value = f"demo+{self._clock_ms:08.3f}ms"
        self._clock_ms += 7.0
        return value


def trace_to_dict(node: TraceNode) -> dict[str, Any]:
    return {
        "span_id": node.span_id,
        "parent_id": node.parent_id,
        "name": node.name,
        "kind": node.kind,
        "type": node.kind,
        "input": node.input,
        "output": node.output,
        "start_time": node.start_time,
        "end_time": node.end_time,
        "duration_ms": node.duration_ms,
        "error": node.error,
        "children": [trace_to_dict(child) for child in node.children],
    }


def save_trace(node: TraceNode, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(trace_to_dict(node), indent=2), encoding="utf-8")


def render_ascii_tree(node: TraceNode, prefix: str = "", is_last: bool = True) -> str:
    connector = ""
    if node.parent_id is not None:
        connector = "└── " if is_last else "├── "

    label = f"{node.name} [{node.kind}] {node.duration_ms:.1f}ms"
    summary = _output_summary(node.output)

    if summary:
        label = f"{label} -> {summary}"
    if node.error:
        label = f"{label} ERROR {node.error}"

    lines = [prefix + connector + label]
    next_prefix = ""
    if node.parent_id is not None:
        next_prefix = prefix + ("    " if is_last else "│   ")

    for index, child in enumerate(node.children):
        lines.append(render_ascii_tree(child, next_prefix, index == len(node.children) - 1))

    return "\n".join(lines)


def find_span(node: TraceNode, name: str) -> TraceNode | None:
    if node.name == name:
        return node
    for child in node.children:
        found = find_span(child, name)
        if found:
            return found
    return None


def _duration_ms(start_time: str, end_time: str) -> float:
    return _parse_demo_time(end_time) - _parse_demo_time(start_time)


def _parse_demo_time(value: str) -> float:
    return float(value.removeprefix("demo+").removesuffix("ms"))


def _output_summary(output: dict[str, Any]) -> str:
    for key in ("classification", "known_issue", "suggested_fix", "final_answer", "plan"):
        if key in output:
            value = output[key]
            if isinstance(value, list):
                value = f"{len(value)} steps"
            text = str(value).replace("\n", " ")
            if len(text) > 72:
                text = text[:69] + "..."
            return f"{key}={text}"
    return ""
