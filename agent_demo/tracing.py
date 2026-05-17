from __future__ import annotations

import json
from contextlib import contextmanager
from dataclasses import asdict
from pathlib import Path
from typing import Any, Iterator

from agent_demo.models import TraceNode


class Tracer:
    def __init__(self, root_name: str, inputs: dict[str, Any]) -> None:
        self.root = TraceNode(name=root_name, kind="agent", inputs=inputs)
        self._stack = [self.root]

    @contextmanager
    def span(self, name: str, kind: str, inputs: dict[str, Any]) -> Iterator[TraceNode]:
        node = TraceNode(name=name, kind=kind, inputs=inputs)
        self._stack[-1].add_child(node)
        self._stack.append(node)
        try:
            yield node
        finally:
            self._stack.pop()

    def set_output(self, **outputs: Any) -> None:
        self._stack[-1].outputs.update(outputs)


def trace_to_dict(node: TraceNode) -> dict[str, Any]:
    return asdict(node)


def save_trace(node: TraceNode, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(trace_to_dict(node), indent=2), encoding="utf-8")


def render_ascii_tree(node: TraceNode, prefix: str = "") -> str:
    label = f"{node.kind}: {node.name}"
    lines = [prefix + label]
    child_prefix = prefix + "  "
    for child in node.children:
        lines.append(render_ascii_tree(child, child_prefix))
    return "\n".join(lines)

