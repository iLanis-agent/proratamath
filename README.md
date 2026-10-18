# Prorata Math

Prorated bill arithmetic by days. A bill is for the whole period; you were there for part of it.

## What it computes

- **The prorate truth** - a bill, the days it covers and the days used: a 1200.00 bill over 30 days with 12 days used is 480.00.
- **The daily truth** - what one day costs: a 90.00 bill over 30 days is 3.00 per day.
- **The split truth** - one bill shared by days present, to the cent: 100.00 over days 10, 10, 10 is 33.34, 33.33, 33.33.

## Boundary

Arithmetic only. Prorata Math divides the amount you type by the days you type, to the cent. It does not say how a bill should be shared, what a lease or utility agreement requires, or what is fair. You and the people involved decide that.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic.
- `oracle.py` - the Python mirror that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (32 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/proratamath/
Repo: https://github.com/iLanis-agent/proratamath
