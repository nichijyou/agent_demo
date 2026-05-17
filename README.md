# Stop Debugging Agents Blind

Tracing and Evaluating LLM Apps with Python.

This repository is a small PyCon demo for a deterministic Python bug triage
agent. It uses no real LLM API, no API key, no LangChain, no LangGraph, no
OpenTelemetry, no web UI, and no database.

Source files are intentionally stored with normal physical line breaks.

## Demo Goal

Show the core workflow for understanding an LLM-style application:

```text
wrap -> trace -> structure -> evaluate -> diagnose -> report
```

The agent receives a Python bug report, makes a mock LLM plan, calls tools,
records a trace tree, evaluates against a tiny dataset, diagnoses failures from
the trace, and writes a Markdown report.

## Why This Demo Exists

Agent failures are often debugged by staring at final answers. That is too late
in the pipeline. The interesting bugs often happen in the trajectory: a bad
classification, a wrong tool input, or a plausible answer produced from the
wrong path.

This demo makes that visible with plain Python data structures.

## Project Structure

```text
agent_demo/
  main.py          # CLI entry point
  models.py        # dataclass models for reports, evals, and trace spans
  tracing.py       # span wrapper, JSON trace export, ASCII tree renderer
  tools.py         # deterministic bug triage tools
  toy_agent.py     # mock LLM plan plus tool workflow
  evaluation.py    # dataset evaluation
  diagnosis.py     # trace-based root cause analysis
  report.py        # Markdown report writer
  data/
    eval_cases.json
  reports/
  traces/
tests/
```

## Run Commands

Run the intentional FastAPI 422 failure:

```bash
python -m agent_demo.main --case fastapi_422
```

Run the full default demo:

```bash
python -m agent_demo.main
```

Run the same case after the classifier fix:

```bash
python -m agent_demo.main --case fastapi_422 --fix
```

Run dataset evaluation:

```bash
python -m agent_demo.main --eval
```

Generate the latest report:

```bash
python -m agent_demo.main --report
```

Run tests:

```bash
pytest
```

## Expected Output

The CLI prints:

- a single-case final answer
- an ASCII trace tree using span names, span kinds, durations, and summaries
- a dataset score
- structured diagnosis
- paths for `agent_demo/traces/latest_trace.json` and
  `agent_demo/reports/latest_report.md`

## Intentional Failure

The `fastapi_422` case says:

```text
FastAPI returns 422 when I send a POST request with JSON.
```

The expected classification is:

```text
fastapi_validation_error
```

By default, the classifier intentionally returns:

```text
dependency_version_error
```

That sends the agent down the wrong tool path. The final answer may sound
reasonable, but the trace shows the mistake.

## Before And After With `--fix`

Before:

```bash
python -m agent_demo.main --case fastapi_422
```

Expected result: the case fails evaluation. The diagnosis points at
`classify_bug_tool` and shows the downstream `search_known_issue_tool` input.

After:

```bash
python -m agent_demo.main --case fastapi_422 --fix
```

Expected result: the case passes because the classifier now recognizes FastAPI
validation/schema errors.

## Thesis-Inspired Ideas

This demo maps to a few practical ideas for LLM app engineering:

- Wrap the workflow before it becomes too complex to observe.
- Trace intermediate decisions, not just final text.
- Structure traces so they can be evaluated and reported.
- Diagnose failures from trajectory evidence.
- Evaluate the path, not only whether the answer sounds good.

## PyCon Adaptation

Everything is deliberately tiny and inspectable:

- standard library application code
- deterministic mock LLM behavior
- dataclasses instead of framework objects
- JSON trace output that can be opened during a talk
- one intentional failure that is easy to explain live

## Five-Minute Live Demo Script

1. Run `python -m agent_demo.main --case fastapi_422` and show the failure.
2. Open `agent_demo/traces/latest_trace.json` and point to span structure.
3. Read the diagnosis: wrong classifier output caused the wrong tool path.
4. Run `python -m agent_demo.main --case fastapi_422 --fix` and show the pass.
5. Run `python -m agent_demo.main` and show the full workflow.
6. Run `python -m agent_demo.main --report` and open the Markdown report.
7. Close with the punchline: debugging agents starts with tracing the path.
