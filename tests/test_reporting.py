import csv
import json

from pyperflab.benchmarks import BenchmarkCase, sum_builtin, sum_loop
from pyperflab.engine import run_benchmarks
from pyperflab.reporting import format_console, write_csv, write_json


def sample_results():
    case = BenchmarkCase("sum", [1, 2, 3], {"loop": sum_loop, "builtin": sum_builtin})
    return run_benchmarks([case], repeats=2, warmups=0)


def test_json_report_round_trip(tmp_path):
    output = tmp_path / "nested" / "report.json"
    write_json(sample_results(), output)
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert len(payload) == 2
    assert payload[0]["benchmark"] == "sum"


def test_csv_report_writes_header_and_rows(tmp_path):
    output = tmp_path / "report.csv"
    write_csv(sample_results(), output)
    with output.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 2
    assert "median_seconds" in rows[0]


def test_console_report_is_readable():
    output = format_console(sample_results())
    assert "PyPerfLab benchmark results" in output
    assert "Median (ms)" in output
