"""Command-line interface for PyPerfLab."""

from __future__ import annotations

import argparse
from pathlib import Path

from .benchmarks import build_benchmarks
from .engine import run_benchmarks
from .reporting import format_console, write_csv, write_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pyperflab",
        description="Compare Python implementations with repeated local benchmarks.",
    )
    parser.add_argument("--size", type=int, default=10_000, help="workload size (default: 10000)")
    parser.add_argument("--repeats", type=int, default=5, help="timed runs per implementation")
    parser.add_argument("--warmups", type=int, default=1, help="warm-up runs per implementation")
    parser.add_argument("--format", choices=("console", "json", "csv"), default="console", help="report format")
    parser.add_argument("--output", type=Path, help="optional report path for JSON or CSV")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.size < 1:
        parser.error("--size must be at least 1")
    if args.repeats < 1:
        parser.error("--repeats must be at least 1")
    if args.warmups < 0:
        parser.error("--warmups cannot be negative")
    if args.output and args.format == "console":
        parser.error("--output requires --format json or --format csv")
    if args.format in {"json", "csv"} and not args.output:
        parser.error("--output is required when --format is json or csv")

    results = run_benchmarks(build_benchmarks(args.size), repeats=args.repeats, warmups=args.warmups)
    if args.format == "console":
        print(format_console(results))
    elif args.format == "json":
        write_json(results, args.output)
        print(f"Wrote JSON report to {args.output}")
    else:
        write_csv(results, args.output)
        print(f"Wrote CSV report to {args.output}")
    return 0
