from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any

import pytest


_REPORT_PATH = Path(__file__).resolve().parents[1] / "test-reports" / "report.html"
_REPORTS: dict[str, dict[str, Any]] = {}


def pytest_runtest_logreport(report: pytest.TestReport) -> None:
    if report.when != "call":
        return

    captured_output = "\n".join(
        f"{section_name}:\n{section_text}"
        for section_name, section_text in report.sections
        if section_text
    )
    _REPORTS[report.nodeid] = {
        "name": report.nodeid,
        "outcome": report.outcome,
        "duration": report.duration,
        "output": captured_output,
        "details": str(report.longrepr) if report.failed else "",
    }


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    _REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for result in _REPORTS.values():
        details = result["details"] or result["output"] or ""
        rows.append(
            "<tr>"
            f"<td>{escape(result['name'])}</td>"
            f"<td class=\"{escape(result['outcome'])}\">{escape(result['outcome'])}</td>"
            f"<td>{result['duration']:.3f}s</td>"
            f"<td><pre>{escape(details)}</pre></td>"
            "</tr>"
        )

    summary = f"{len(_REPORTS)} test case(s), pytest exit status {exitstatus}"
    document = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Pytest Report</title>
<style>
body {{ font-family: sans-serif; margin: 2rem; color: #222; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #ccc; padding: .5rem; text-align: left; vertical-align: top; }}
th {{ background: #eee; }}
.pass {{ color: #176b2c; font-weight: bold; }}
.fail, .error {{ color: #a11; font-weight: bold; }}
pre {{ max-height: 20rem; overflow: auto; white-space: pre-wrap; }}
</style>
</head>
<body>
<h1>Pytest Report</h1>
<p>{escape(summary)}</p>
<table>
<thead><tr><th>Test</th><th>Status</th><th>Duration</th><th>Details</th></tr></thead>
<tbody>{''.join(rows)}</tbody>
</table>
</body>
</html>
"""
    _REPORT_PATH.write_text(document, encoding="utf-8")
