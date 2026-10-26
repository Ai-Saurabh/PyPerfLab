"""Core benchmark execution and statistics."""

from __future__ import annotations

import platform
import statistics
import sys
import time
from dataclasses import asdict, dataclass
from typing import Any, Callable

from .benchmarks import BenchmarkCase


@dataclass(frozen=True)
class BenchmarkResult:
    benchmark: str
    implementation: str
    repeats: int
    warmups: int
    median_seconds: float
    mean_seconds: float
    min_seconds: float
    max_seconds: float
    stdev_seconds: float
    speedup: float
    python_version: str
    platform: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _measure(function: Callable[[Any], Any], input_data: Any, repeats: int, warmups: int) -> list[float]:
    for _ in range(warmups):
        function(input_data)

    durations: list[float] = []
    for _ in range(repeats):
        start = time.perf_counter()
        function(input_data)
        durations.append(time.perf_counter() - start)
    return durations


def run_benchmarks(
    cases: list[BenchmarkCase],
    repeats: int = 5,
    warmups: int = 1,
) -> list[BenchmarkResult]:
    """Run cases, validate result equivalence, and return timing summaries."""
    if repeats < 1:
        raise ValueError("repeats must be at least 1")
    if warmups < 0:
        raise ValueError("warmups cannot be negative")

    results: list[BenchmarkResult] = []
    for case in cases:
        if not case.implementations:
            raise ValueError(f"benchmark {case.name!r} has no implementations")

        expected = None
        has_expected = False
        raw: list[tuple[str, list[float]]] = []

        for implementation_name, function in case.implementations.items():
            actual = function(case.input_data)
            if not has_expected:
                expected = actual
                has_expected = True
            elif actual != expected:
                raise ValueError(
                    f"Implementation {implementation_name!r} in benchmark "
                    f"{case.name!r} returned a result different from the first implementation"
                )
            durations = _measure(function, case.input_data, repeats, warmups)
            raw.append((implementation_name, durations))

        medians = {name: statistics.median(samples) for name, samples in raw}
        fastest = min(medians.values())
        for name, samples in raw:
            median = statistics.median(samples)
            results.append(
                BenchmarkResult(
                    benchmark=case.name,
                    implementation=name,
                    repeats=repeats,
                    warmups=warmups,
                    median_seconds=median,
                    mean_seconds=statistics.mean(samples),
                    min_seconds=min(samples),
                    max_seconds=max(samples),
                    stdev_seconds=statistics.stdev(samples) if len(samples) > 1 else 0.0,
                    speedup=(median / fastest) if fastest > 0 else 1.0,
                    python_version=sys.version.split()[0],
                    platform=platform.platform(),
                )
            )
    return results
