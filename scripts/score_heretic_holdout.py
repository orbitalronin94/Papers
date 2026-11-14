#!/usr/bin/env python3
"""Recompute HERETIC-RONIN's 120-item normalized exact-match holdout.

The prompt generator and normalization rules mirror the source implementation
at HERETIC-RONIN commit 1acc15ed5ee14e1a485b84d86562216e7f1be8c9.
This script does not generate model outputs; it audits retained JSON outputs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

PLURALS = [
    ("lápiz", "lápices"), ("pez", "peces"), ("luz", "luces"),
    ("joven", "jóvenes"), ("rubí", "rubíes"), ("régimen", "regímenes"),
    ("carácter", "caracteres"), ("espécimen", "especímenes"),
    ("sofá", "sofás"), ("menú", "menús"), ("bambú", "bambúes"),
    ("crisis", "crisis"), ("lunes", "lunes"), ("tórax", "tórax"),
    ("análisis", "análisis"), ("álbum", "álbumes"),
    ("examen", "exámenes"), ("compás", "compases"),
    ("raíz", "raíces"), ("canción", "canciones"),
]
NAMES = ("Alba", "Bruno", "Celia", "Diego", "Eva", "Fabio", "Gala", "Hugo")
PREFIX = re.compile(r"^(la respuesta es|respuesta:|answer:)")


def holdout_rows() -> list[dict[str, str]]:
    rows = []
    for i in range(20):
        a, b, c = i + 4, (i % 5) + 2, (i % 4) + 1
        rows.append({
            "domain": "mathematics",
            "question": f"Calcula ({a} + {b}) por {c}, menos {i}. Solo el número.",
            "answer": str((a + b) * c - i),
        })
        values = [i + 1, i + 2, i + 3]
        rows.append({
            "domain": "programming",
            "question": f"En Python, ¿qué vale sum({values}) - len({values})? Solo número.",
            "answer": str(sum(values) - len(values)),
        })
        order = [NAMES[(i + j) % len(NAMES)] for j in range(4)]
        rows.append({
            "domain": "logic",
            "question": (
                f"{order[0]} va antes que {order[1]}, {order[1]} antes que "
                f"{order[2]} y {order[2]} antes que {order[3]}. ¿Quién va último?"
            ),
            "answer": order[3],
        })
        volume, density = (i % 5) + 1, i + 2
        rows.append({
            "domain": "natural_science",
            "question": (
                f"Una muestra tiene {volume * density} g y ocupa {volume} cm3. "
                "¿Densidad en g/cm3?"
            ),
            "answer": str(density),
        })
        singular, plural = PLURALS[i]
        rows.append({
            "domain": "language",
            "question": f"Escribe el plural de «{singular}». Solo la palabra.",
            "answer": plural,
        })
        amount = i + 1
        if i < 7:
            question, answer = f"Convierte {amount} kg a gramos. Solo número.", str(amount * 1000)
        elif i < 14:
            question, answer = f"Convierte {amount} litros a mililitros. Solo número.", str(amount * 1000)
        else:
            question, answer = f"Convierte {amount} horas a minutos. Solo número.", str(amount * 60)
        rows.append({"domain": "interdisciplinary", "question": question, "answer": answer})
    return rows


def normalize(value: str) -> str:
    first_line = value.splitlines()[0] if value.splitlines() else value
    first_line = PREFIX.sub("", first_line.strip().casefold()).strip()
    return re.sub(r"\s+", " ", first_line).strip(" \t\r\n.,;:!?¿¡\\\"'()[]{}")


def prompt_hash(rows: list[dict[str, str]]) -> str:
    payload = "".join(
        json.dumps(
            {"domain": row["domain"], "question": row["question"]},
            ensure_ascii=False,
            separators=(",", ":"),
        ) + "\n"
        for row in rows
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def score(path: Path, expected: list[dict[str, str]], expected_count: int) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    details = payload.get("details")
    if not isinstance(details, list):
        raise ValueError(f"{path}: missing list field 'details'")
    if len(details) != expected_count:
        raise ValueError(f"{path}: expected {expected_count} rows, found {len(details)}")

    domain_counts = defaultdict(lambda: {"correct": 0, "total": 0})
    empty = 0
    mismatches = []
    prompt_mismatches = []
    correct_total = 0
    char_lengths = []

    for index, row in enumerate(details):
        for key in ("domain", "question", "answer", "prediction"):
            if key not in row:
                raise ValueError(f"{path}: row {index} lacks {key!r}")
        prediction = str(row["prediction"])
        answer = str(row["answer"])
        correct = normalize(prediction) == normalize(answer)
        correct_total += int(correct)
        domain_counts[str(row["domain"])]["correct"] += int(correct)
        domain_counts[str(row["domain"])]["total"] += 1
        empty += int(not prediction.strip())
        char_lengths.append(len(prediction))

        if "correct" in row and bool(row["correct"]) != correct:
            mismatches.append(index)
        if index >= len(expected) or any(
            row.get(key) != expected[index][key]
            for key in ("domain", "question", "answer")
        ):
            prompt_mismatches.append(index)

    reported = payload.get("correct")
    reported_mismatch = reported is not None and int(reported) != correct_total
    return {
        "file": str(path),
        "items": len(details),
        "recomputed_correct": correct_total,
        "recomputed_accuracy": correct_total / len(details),
        "reported_correct": reported,
        "reported_accuracy": payload.get("accuracy"),
        "reported_total": payload.get("total"),
        "reported_count_matches": not reported_mismatch,
        "per_domain": dict(sorted(domain_counts.items())),
        "empty_predictions": empty,
        "prediction_char_length": {
            "min": min(char_lengths),
            "max": max(char_lengths),
            "mean": sum(char_lengths) / len(char_lengths),
        },
        "stored_row_correctness_mismatches": mismatches,
        "prompt_rows_matching_recovered_generator": len(prompt_mismatches) == 0,
        "prompt_mismatch_indices": prompt_mismatches,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_files", nargs="+", type=Path, help="holdout-before/after JSON files")
    parser.add_argument("--expected-count", type=int, default=120)
    args = parser.parse_args()

    expected = holdout_rows()
    if len(expected) != args.expected_count:
        raise SystemExit(f"generator produced {len(expected)} rows, expected {args.expected_count}")

    report = {
        "scorer": "HERETIC normalized exact-match reproduction",
        "source_workflow_commit": "1acc15ed5ee14e1a485b84d86562216e7f1be8c9",
        "prompt_generator_sha256": prompt_hash(expected),
        "prompt_hash_definition": "SHA-256 of UTF-8 JSONL rows with only domain and question, ensure_ascii=False, compact separators, trailing newline per row",
        "full_reference_set_sha256": hashlib.sha256(
            "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in expected).encode("utf-8")
        ).hexdigest(),
        "results": [score(path, expected, args.expected_count) for path in args.json_files],
    }
    json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
