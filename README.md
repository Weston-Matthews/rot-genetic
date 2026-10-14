# rot-genetic

A simple genetic algorithm that recovers the shift of a rotation (Caesar) cipher using English letter frequency analysis.

## What it does

- Evolves a small population of candidate shifts (0–25).
- Scores each candidate by how closely the decrypted letter frequencies match English.
- Uses elitism, simple crossover, and mutation.
- Returns the best shift and the decrypted text.

Rotation ciphers have a tiny keyspace, so a genetic algorithm is educational rather than necessary, but the same pattern extends to harder ciphers.

## Install / run

Requires Python 3.10+.

```bash
# From the repo root
pip install -e .
# or with poetry
poetry install
```

## Usage

```python
from rot_genetic import solve

ciphertext = "WKH TXLFN EURZQ IRA MXPSV RYHU WKH ODCB GRJ"
shift, plaintext, score = solve(ciphertext)
print(f"Shift: {shift}")
print(f"Plaintext: {plaintext}")
print(f"Fitness: {score:.2f}")
```

## Tests

```bash
pytest
```

## Project layout

```
rot_genetic/
  __init__.py
  solver.py          # GA + frequency scoring
tests/
  test_solver.py
```
