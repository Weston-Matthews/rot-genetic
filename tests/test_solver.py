"""Tests for the rotation cipher genetic solver."""

import pytest
from rot_genetic import solve, decrypt_with_shift


def _caesar(text: str, shift: int) -> str:
    """Encrypt with Caesar shift (for test fixtures)."""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cleaned = "".join(c for c in text.upper() if c in alphabet)
    return "".join(alphabet[(alphabet.index(c) + shift) % 26] for c in cleaned)


SAMPLE = (
    "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG "
    "THIS IS A LONGER SAMPLE OF ENGLISH TEXT USED TO TEST THE GENETIC ALGORITHM "
    "FREQUENCY ANALYSIS SHOULD RECOVER THE CORRECT SHIFT RELIABLY"
)


@pytest.mark.parametrize("true_shift", [0, 1, 7, 13, 25])
def test_solves_known_shift(true_shift: int):
    ciphertext = _caesar(SAMPLE, true_shift)
    found_shift, plaintext, score = solve(ciphertext, generations=80, population_size=50, seed=42)
    assert found_shift == true_shift
    assert "THEQUICKBROWNFOX" in plaintext.replace(" ", "")
    assert score > -5.0  # reasonable fitness for English


def test_short_text_raises():
    with pytest.raises(ValueError):
        solve("ABC")


def test_decrypt_utility():
    cipher = _caesar("HELLO WORLD", 3)
    assert decrypt_with_shift(cipher, 3) == "HELLOWORLD"
