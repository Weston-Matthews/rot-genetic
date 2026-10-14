"""Simple genetic algorithm to solve rotation (Caesar) ciphers."""

from __future__ import annotations

import random
import string
from collections import Counter
from typing import List, Tuple

# Approximate English letter frequencies (A-Z), normalized
ENGLISH_FREQS = [
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
    0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
    0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
    0.00978, 0.02360, 0.00150, 0.01974, 0.00074,
]

ALPHABET = string.ascii_uppercase
ALPHABET_SIZE = 26


def _clean(text: str) -> str:
    """Keep only A-Z letters and uppercase them."""
    return "".join(c for c in text.upper() if c in ALPHABET)


def _rotate(text: str, shift: int) -> str:
    """Rotate cleaned text by shift positions (positive = decrypt Caesar)."""
    return "".join(
        ALPHABET[(ALPHABET.index(c) - shift) % ALPHABET_SIZE] for c in text
    )


def _letter_frequencies(text: str) -> List[float]:
    """Return normalized letter frequencies for A-Z."""
    if not text:
        return [0.0] * ALPHABET_SIZE
    counts = Counter(text)
    total = len(text)
    return [counts.get(ch, 0) / total for ch in ALPHABET]


def fitness(ciphertext: str, shift: int) -> float:
    """
    Score a candidate shift.
    Higher is better. Uses negative chi-squared distance to English frequencies.
    """
    cleaned = _clean(ciphertext)
    if not cleaned:
        return float("-inf")
    decrypted = _rotate(cleaned, shift)
    observed = _letter_frequencies(decrypted)
    # Chi-squared; lower distance = better, so negate
    chi2 = sum(
        (obs - exp) ** 2 / exp
        for obs, exp in zip(observed, ENGLISH_FREQS)
        if exp > 0
    )
    return -chi2


def _random_shift() -> int:
    return random.randint(0, ALPHABET_SIZE - 1)


def _crossover(a: int, b: int) -> int:
    """Simple crossover for integer shifts: pick one parent or average."""
    if random.random() < 0.5:
        return a
    return b


def _mutate(shift: int, mutation_rate: float = 0.2) -> int:
    if random.random() < mutation_rate:
        return (shift + random.randint(-3, 3)) % ALPHABET_SIZE
    return shift


def solve(
    ciphertext: str,
    population_size: int = 40,
    generations: int = 60,
    elite_count: int = 6,
    mutation_rate: float = 0.3,
    seed: int | None = None,
) -> Tuple[int, str, float]:
    """
    Run a simple genetic algorithm to recover the Caesar shift.

    Returns:
        (best_shift, decrypted_text, best_fitness)
    """
    if seed is not None:
        random.seed(seed)

    cleaned = _clean(ciphertext)
    if len(cleaned) < 10:
        raise ValueError("Ciphertext too short for reliable frequency analysis.")

    # Initial population
    population: List[int] = [_random_shift() for _ in range(population_size)]

    best_shift = 0
    best_score = float("-inf")
    best_plain = ""

    for gen in range(generations):
        # Evaluate
        scored = [(fitness(ciphertext, s), s) for s in population]
        scored.sort(reverse=True)  # highest fitness first

        # Track global best
        if scored[0][0] > best_score:
            best_score = scored[0][0]
            best_shift = scored[0][1]
            best_plain = _rotate(cleaned, best_shift)

        # Elitism: keep top individuals
        next_pop: List[int] = [s for _, s in scored[:elite_count]]

        # Fill rest with offspring + occasional fresh randoms
        while len(next_pop) < population_size:
            if random.random() < 0.1:
                next_pop.append(_random_shift())
                continue
            # Tournament-ish: pick from top half
            parent_a = random.choice(scored[: max(2, population_size // 2)])[1]
            parent_b = random.choice(scored[: max(2, population_size // 2)])[1]
            child = _crossover(parent_a, parent_b)
            child = _mutate(child, mutation_rate)
            next_pop.append(child)

        population = next_pop

    # Final best
    final_plain = _rotate(cleaned, best_shift)
    return best_shift, final_plain, best_score


def decrypt_with_shift(ciphertext: str, shift: int) -> str:
    """Utility: decrypt using a known shift (for testing)."""
    return _rotate(_clean(ciphertext), shift)
