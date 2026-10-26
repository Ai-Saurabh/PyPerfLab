"""Built-in benchmark workloads and comparable implementations."""

from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class BenchmarkCase:
    """A named benchmark group with a fixed input and implementations."""

    name: str
    input_data: Any
    implementations: dict[str, Callable[[Any], Any]]


def sum_loop(values: list[int]) -> int:
    total = 0
    for value in values:
        total += value
    return total


def sum_builtin(values: list[int]) -> int:
    return sum(values)


def count_nested_scan(values: list[int]) -> dict[int, int]:
    """Simple O(n²) frequency counter included as a comparison baseline."""
    return {value: sum(1 for item in values if item == value) for value in set(values)}


def count_dictionary(values: list[int]) -> dict[int, int]:
    counts: dict[int, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    return counts


def deduplicate_seen_set(values: list[int]) -> list[int]:
    seen: set[int] = set()
    result: list[int] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def deduplicate_ordered_dict(values: list[int]) -> list[int]:
    return list(OrderedDict.fromkeys(values))


def build_benchmarks(size: int = 10_000) -> list[BenchmarkCase]:
    """Create deterministic benchmark inputs for a positive workload size."""
    if size < 1:
        raise ValueError("size must be at least 1")

    values = [(i * 37) % max(1, size // 5) for i in range(size)]
    return [
        BenchmarkCase(
            name="sum_values",
            input_data=list(range(size)),
            implementations={"loop": sum_loop, "builtin_sum": sum_builtin},
        ),
        BenchmarkCase(
            name="count_frequencies",
            input_data=values,
            implementations={
                "nested_scan": count_nested_scan,
                "dictionary": count_dictionary,
            },
        ),
        BenchmarkCase(
            name="deduplicate",
            input_data=values,
            implementations={
                "seen_set": deduplicate_seen_set,
                "ordered_dict": deduplicate_ordered_dict,
            },
        ),
    ]
