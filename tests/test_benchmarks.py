import pytest

from pyperflab.benchmarks import (
    build_benchmarks, count_dictionary, count_nested_scan,
    deduplicate_ordered_dict, deduplicate_seen_set, sum_builtin, sum_loop,
)


def test_sum_implementations_match():
    values = [2, 3, 5, 7]
    assert sum_loop(values) == sum_builtin(values) == 17


def test_frequency_implementations_match():
    values = [1, 2, 1, 3, 2, 1]
    assert count_nested_scan(values) == count_dictionary(values)


def test_deduplication_preserves_order():
    values = [3, 1, 3, 2, 1]
    assert deduplicate_seen_set(values) == [3, 1, 2]
    assert deduplicate_ordered_dict(values) == [3, 1, 2]


def test_build_benchmarks_rejects_invalid_size():
    with pytest.raises(ValueError, match="at least 1"):
        build_benchmarks(0)
