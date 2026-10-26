import pytest

from pyperflab.benchmarks import BenchmarkCase, sum_builtin, sum_loop
from pyperflab.engine import run_benchmarks


def test_run_benchmarks_returns_statistics():
    case = BenchmarkCase("sum", [1, 2, 3], {"loop": sum_loop, "builtin": sum_builtin})
    results = run_benchmarks([case], repeats=3, warmups=0)
    assert len(results) == 2
    assert all(result.repeats == 3 for result in results)
    assert all(result.median_seconds >= 0 for result in results)
    assert all(result.speedup >= 1 for result in results)


def test_rejects_different_results():
    case = BenchmarkCase("broken", [1, 2], {"correct": sum_builtin, "wrong": lambda values: 999})
    with pytest.raises(ValueError, match="different"):
        run_benchmarks([case], repeats=1, warmups=0)


@pytest.mark.parametrize("repeats,warmups", [(0, 1), (1, -1)])
def test_rejects_invalid_run_counts(repeats, warmups):
    with pytest.raises(ValueError):
        run_benchmarks([], repeats=repeats, warmups=warmups)
