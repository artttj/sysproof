import csv
from dataclasses import dataclass, asdict, fields
from pathlib import Path


@dataclass
class Row:
    task: str
    arm: str
    rep: int
    claimed_done: bool
    actually_passed: bool
    traps_caught: bool
    verdict_raw: str


def false_done(claimed_done: bool, actually_passed: bool) -> bool:
    return claimed_done and not actually_passed


_BOOL_FIELDS = {"claimed_done", "actually_passed", "traps_caught"}


def write_rows(rows: list[Row], path: Path) -> None:
    names = [f.name for f in fields(Row)]
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=names)
        w.writeheader()
        for r in rows:
            w.writerow(asdict(r))


def read_rows(path: Path) -> list[Row]:
    out = []
    with open(path, newline="") as fh:
        for d in csv.DictReader(fh):
            for b in _BOOL_FIELDS:
                d[b] = d[b] in ("True", "true", "1")
            d["rep"] = int(d["rep"])
            out.append(Row(**d))
    return out
