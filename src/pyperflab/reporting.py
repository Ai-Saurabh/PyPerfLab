"""Console, JSON, and CSV report writers."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable

from .engine import BenchmarkResult


def to_json(results: Iterable[BenchmarkResult]) -> str:
    return json.dumps([result.to_dict() for result in results], indent=2)


def write_json(results: Iterable[BenchmarkResult], path: str | Path) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(to_json(results) + "\n", encoding="utf-8")


def write_csv(results: Iterable[BenchmarkResult], path: str | Path) -> None:
    rows = [result.to_dict() for result in results]
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        destination.write_text("", encoding="utf-8")
        return
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def format_console(results: Iterable[BenchmarkResult]) -> str:
    rows = list(results)
    if not rows:
        return "No benchmark results."
    headings = ("Benchmark", "Implementation", "Median (ms)", "Speedup")
    data = [
        (row.benchmark, row.implementation, f"{row.median_seconds * 1000:.3f}", f"{row.speedup:.2f}x")
        for row in rows
    ]
    widths = [max(len(headings[i]), *(len(row[i]) for row in data)) for i in range(len(headings))]
    line = "  ".join(headings[i].ljust(widths[i]) for i in range(len(headings)))
    separator = "  ".join("-" * width for width in widths)
    body = ["  ".join(value.ljust(widths[i]) for i, value in enumerate(row)) for row in data]
    return "\n".join(["PyPerfLab benchmark results", line, separator, *body])
