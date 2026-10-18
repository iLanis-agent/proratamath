#!/usr/bin/env python3
# Prorata Math oracle - mirrors engine.js.
import json, math, re

def _m(x):
    if not math.isfinite(x) or x <= 0 or x > 1000000:
        raise ValueError("bill must be between 0 and 1000000, over 0")
    return math.floor(x * 100 + 0.5)

def _money(c):
    whole, frac = divmod(c, 100)
    return f"{whole}.{frac:02d}"

def _day(n):
    return f"{n} day" if n == 1 else f"{n} days"

def _days(d):
    if not isinstance(d, int) or d < 1 or d > 366:
        raise ValueError("days in period must be a whole number from 1 to 366")
    return d

def prorate_truth(bill, days, used):
    c = _m(bill)
    d = _days(days)
    if not isinstance(used, int) or used < 0 or used > d:
        raise ValueError("days used must be a whole number from 0 to the days in the period")
    share = (2 * c * used + d) // (2 * d)
    return f"A {_money(c)} bill over {_day(d)}, {_day(used)} used: {_money(share)}."

def daily_truth(bill, days):
    c = _m(bill)
    d = _days(days)
    r = (200 * c + d) // (2 * d)
    whole, f = divmod(r, 10000)
    f = f"{f:04d}"
    while len(f) > 2 and f.endswith("0"):
        f = f[:-1]
    return f"A {_money(c)} bill over {_day(d)} is {whole}.{f} per day."

def split_truth(bill, lst):
    c = _m(bill)
    parts = [p.strip() for p in str(lst).split(",")]
    if len(parts) < 2 or len(parts) > 12:
        raise ValueError("enter 2 to 12 day counts separated by commas")
    ds = []
    for p in parts:
        if not re.fullmatch(r"[0-9]+", p) or int(p) > 366:
            raise ValueError("each day count must be a whole number from 0 to 366")
        ds.append(int(p))
    s = sum(ds)
    if s <= 0:
        raise ValueError("day counts must add up to more than 0")
    base = [c * d // s for d in ds]
    rem = [(c * d) % s for d in ds]
    left = c - sum(base)
    order = sorted(range(len(ds)), key=lambda i: (-rem[i], i))
    for k in range(left):
        base[order[k]] += 1
    return (f"Bill {_money(c)} split over {s} " + ("person-day" if s == 1 else "person-days") +
            f" ({', '.join(str(d) for d in ds)}): " + ", ".join(_money(b) for b in base) + ".")

FNS = {"prorateTruth": prorate_truth, "dailyTruth": daily_truth, "splitTruth": split_truth}

CASES = [
    ("prorateTruth", [1200, 30, 12]), ("prorateTruth", [1200, 30, 0]), ("prorateTruth", [1200, 30, 30]),
    ("prorateTruth", [1000, 31, 10]), ("prorateTruth", [100, 1, 1]), ("prorateTruth", [0.01, 3, 1]),
    ("prorateTruth", [0, 30, 12]), ("prorateTruth", [1200, 0, 0]), ("prorateTruth", [1200, 367, 5]),
    ("prorateTruth", [1200, 30, 31]), ("prorateTruth", [1200, 30, -1]), ("prorateTruth", [1200, 30, 1.5]),
    ("prorateTruth", [1000001, 30, 5]),
    ("dailyTruth", [90, 30]), ("dailyTruth", [100, 30]), ("dailyTruth", [90, 1]), ("dailyTruth", [1200, 365]),
    ("dailyTruth", [90, 0]), ("dailyTruth", [-5, 30]),
    ("splitTruth", [100, "10, 10, 10"]), ("splitTruth", [90, "30,20,10"]), ("splitTruth", [100, "30, 0"]),
    ("splitTruth", [0.01, "1, 1, 1"]), ("splitTruth", [100, "7"]), ("splitTruth", [100, "0, 0"]),
    ("splitTruth", [100, "10, x"]), ("splitTruth", [100, "10, 367"]), ("splitTruth", [100, "1,2,3,4,5,6,7,8,9,10,11,12,13"]),
    ("splitTruth", [100, "1, 1"]), ("splitTruth", [0, "10, 10"]), ("splitTruth", [100, "10, , 10"]),
    ("splitTruth", [100, "010, 5"]),
]

out = []
for fn, args in CASES:
    try:
        exp = FNS[fn](*args)
    except ValueError as e:
        exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")
print(len(out), "cases")
