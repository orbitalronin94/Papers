#!/usr/bin/env python3
"""Recompute descriptive metrics from official RONINIA holdout JSON or ZIP artifacts.

This script intentionally does not score answer correctness and does not infer EOS
emission: the current output schema does not record a termination reason.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_payload(path: Path) -> tuple[dict[str, Any], str | None]:
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as archive:
            candidates = [
                name for name in archive.namelist()
                if name.endswith(".json")
                and "manifest" not in Path(name).name.lower()
                and "holdout" in Path(name).name.lower()
            ]
            if len(candidates) != 1:
                raise ValueError(f"{path}: expected one holdout JSON in ZIP, found {candidates}")
            payload = json.loads(archive.read(candidates[0]))
        return payload, sha256_bytes(path.read_bytes())
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload, None


def percentile_nearest_rank(values: list[float], q: float) -> float:
    ordered = sorted(values)
    return ordered[max(0, math.ceil(q * len(ordered)) - 1)]


def summarize(path: Path) -> dict[str, Any]:
    payload, archive_sha = load_payload(path)
    rows = payload.get("results")
    if not isinstance(rows, list) or not rows:
        raise ValueError(f"{path}: missing non-empty results list")
    generation = payload.get("generation") or {}
    token_limit = int(generation.get("max_new_tokens", 0))
    if token_limit <= 0:
        raise ValueError(f"{path}: invalid or missing max_new_tokens")

    answers: list[str] = []
    token_lengths: list[int] = []
    byte_lengths: list[int] = []
    latencies: list[float] = []
    domains: Counter[str] = Counter()
    empty_by_domain: Counter[str] = Counter()
    token_limit_by_domain: Counter[str] = Counter()
    for row in rows:
        answer = row.get("answer")
        token_ids = row.get("generated_token_ids")
        if not isinstance(answer, str) or not isinstance(token_ids, list):
            raise ValueError(f"{path}: malformed result row {row.get('id')}")
        domain = str(row.get("domain", "unknown"))
        answers.append(answer)
        token_lengths.append(len(token_ids))
        byte_lengths.append(len(answer.encode("utf-8")))
        latencies.append(float(row["elapsed_seconds"]))
        domains[domain] += 1
        if not answer.strip():
            empty_by_domain[domain] += 1
        if len(token_ids) == token_limit:
            token_limit_by_domain[domain] += 1

    return {
        "label": payload.get("label"),
        "completed_steps": payload.get("completed_steps"),
        "parameter_count": payload.get("parameter_count"),
        "holdout_count": len(rows),
        "checkpoint_sha256": payload.get("checkpoint_sha256"),
        "tokenizer_sha256": payload.get("tokenizer_sha256"),
        "holdout_sha256": payload.get("holdout_sha256"),
        "seed": payload.get("seed"),
        "generation": generation,
        "archive_sha256": archive_sha,
        "empty_outputs": sum(not answer.strip() for answer in answers),
        "token_limit_hits": sum(length == token_limit for length in token_lengths),
        "distinct_exact_answers": len(set(answers)),
        "distinct_stripped_answers": len({answer.strip() for answer in answers}),
        "mean_generated_tokens": round(statistics.mean(token_lengths), 6),
        "median_generated_tokens": statistics.median(token_lengths),
        "mean_output_bytes": round(statistics.mean(byte_lengths), 6),
        "max_output_bytes": max(byte_lengths),
        "mean_latency_seconds": round(statistics.mean(latencies), 6),
        "p50_latency_seconds": round(statistics.median(latencies), 6),
        "p90_latency_seconds_nearest_rank": round(percentile_nearest_rank(latencies, 0.90), 6),
        "domain_counts": dict(sorted(domains.items())),
        "empty_by_domain": dict(sorted(empty_by_domain.items())),
        "token_limit_hits_by_domain": dict(sorted(token_limit_by_domain.items())),
        "eos_emissions": None,
        "eos_note": "Not recorded in the current JSON schema; do not infer from output length alone.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifacts", nargs="+", type=Path, help="Holdout JSON files or ZIP artifacts")
    parser.add_argument("--require-common-protocol", action="store_true", help="Require same holdout/tokenizer hashes and generation settings")
    args = parser.parse_args()
    summaries = [summarize(path) for path in args.artifacts]
    if args.require_common_protocol:
        keys = ("holdout_sha256", "tokenizer_sha256", "seed", "generation")
        for key in keys:
            values = {json.dumps(item.get(key), sort_keys=True) for item in summaries}
            if len(values) != 1:
                raise SystemExit(f"Protocol mismatch for {key}: {values}")
    print(json.dumps(summaries, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
