# PyPerfLab

A lightweight, reproducible Python performance lab for comparing implementations, measuring runtime, and exporting benchmark reports.

## Features
- Compare multiple implementations against the same input.
- Warm-up runs and repeated timed measurements.
- Median, mean, minimum, maximum, and standard deviation statistics.
- Verify implementations return equivalent results before timing.
- Export JSON and CSV reports.
- Built-in examples: summing values, counting frequencies, and deduplicating sequences.
- No runtime dependencies outside Python's standard library.
- GitHub Actions CI for Python 3.10, 3.11, and 3.12.

## Requirements
- Python 3.10+
- `pytest` for development tests

## Quick start (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest
```

If activation is blocked, use `.\.venv\Scripts\python.exe -m pip install -e ".[dev]"` and `.\.venv\Scripts\python.exe -m pytest`.

## Run benchmarks

Print results in the terminal:

```bash
python -m pyperflab --size 5000 --repeats 5 --warmups 1
```

Save a JSON report:

```bash
python -m pyperflab --size 20000 --repeats 7 --warmups 2 --format json --output reports/latest.json
```

Save a CSV report:

```bash
python -m pyperflab --size 20000 --repeats 7 --warmups 2 --format csv --output reports/latest.csv
```

The report directory is created automatically.

## Example output

Exact timings vary by machine and system load.

```text
PyPerfLab benchmark results
Benchmark          Implementation  Median (ms)  Speedup
sum_values         loop             0.42          1.20x
sum_values         builtin_sum      0.35          1.00x
count_frequencies  nested_scan      8.20         13.23x
count_frequencies  dictionary       0.62          1.00x
```

Speedup is relative to the fastest median implementation within the same benchmark group. A value of `1.00x` is the fastest median for that group.

## Project structure

```text
PyPerfLab/
├── .github/workflows/tests.yml
├── src/pyperflab/
│   ├── __init__.py
│   ├── __main__.py
│   ├── benchmarks.py
│   ├── cli.py
│   ├── engine.py
│   └── reporting.py
├── tests/
├── pyproject.toml
├── LICENSE
└── README.md
```

## Benchmarking responsibly
- Compare runs on the same computer and under similar system load.
- Increase `--repeats` for more stable estimates.
- Record Python version and platform when sharing results.
- Small workloads may be dominated by interpreter and timer overhead.
- These are local measurements, not universal performance rankings.

## License
MIT. See [LICENSE](LICENSE).
