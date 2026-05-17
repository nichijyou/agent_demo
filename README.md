# Stop Debugging Agents Blind

Tracing and Evaluating LLM Apps with Python.

This is a tiny, deterministic PyCon demo for a Python developer bug triage agent.
It uses no LangChain, no LangGraph, no OpenTelemetry, no API keys, and no real LLM API.

The workflow is:

```text
wrap -> trace -> structure -> evaluate -> diagnose -> report
```

## Run

```bash
python -m agent_demo.main
```

The command prints:

- one single-case final answer
- an ASCII trace tree
- a dataset evaluation summary
- the generated report path

It also writes:

- `agent_demo/traces/latest_trace.json`
- `agent_demo/reports/latest_report.md`

## Files

- `agent_demo/toy_agent.py`: deterministic mock agent workflow
- `agent_demo/tracing.py`: small trace tree wrapper
- `agent_demo/tools.py`: deterministic Python bug triage tools
- `agent_demo/evaluation.py`: dataset evaluation
- `agent_demo/diagnosis.py`: simple diagnosis from eval results
- `agent_demo/report.py`: Markdown report writer

