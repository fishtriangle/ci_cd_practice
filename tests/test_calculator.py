"""Тесты математических операций и форматирования результата."""

import pytest

from app.calculator import OPERATIONS, calculate, format_number, format_result


# --- calculate: корректные вычисления ---

@pytest.mark.parametrize(
    "first, operator, second, expected",
    [
        (2, "+", 2, 4),
        (10, "+", -3, 7),
        (2, "-", 2, 0),
        (3, "-", 5, -2),
        (2, "*", 3, 6),
        (-2, "*", 3, -6),
        (8, "/", 2, 4),
        (7, "/", 2, 3.5),
        (0.1, "+", 0.2, pytest.approx(0.3)),
    ],
)
def test_calculate(first, operator, second, expected):
    assert calculate(first, second, operator) == expected


def test_all_operations_registered():
    assert set(OPERATIONS) == {"+", "-", "*", "/"}


# --- calculate: ошибки ---

def test_calculate_unknown_operator():
    with pytest.raises(ValueError, match="Неизвестная операция"):
        calculate(1, 2, "%")


def test_calculate_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        calculate(1, 0, "/")


# --- format_number ---

@pytest.mark.parametrize(
    "value, expected",
    [
        (2.0, "2"),
        (-2.0, "-2"),
        (0.0, "0"),
        (2.5, "2.5"),
        (0.1 + 0.2, "0.3"),
    ],
)
def test_format_number(value, expected):
    assert format_number(value) == expected


# --- format_result ---

def test_format_result_integer_case():
    assert format_result(2, 2, "+", 4) == "2 + 2 = 4"


def test_format_result_float_case():
    assert format_result(7, 2, "/", 3.5) == "7 / 2 = 3.5"
