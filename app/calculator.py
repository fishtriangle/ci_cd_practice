"""Базовые математические операции и выбор операции по символу."""

from typing import Callable

OPERATIONS: dict[str, tuple[str, Callable[[float, float], float]]] = {
    "+": ("Сложение", lambda a, b: a + b),
    "-": ("Вычитание", lambda a, b: a - b),
    "*": ("Умножение", lambda a, b: a * b),
    "/": ("Деление", lambda a, b: a / b),
}


def calculate(first: float, second: float, operator: str) -> float:
    """Выполнить операцию над двумя числами.

    Args:
        first: первое число (левый операнд).
        second: второе число (правый операнд).
        operator: символ операции из ``OPERATIONS``.

    Raises:
        ValueError: если символ операции неизвестен.
        ZeroDivisionError: если оператор ``/`` и second равен нулю.
    """
    if operator not in OPERATIONS:
        raise ValueError(f"Неизвестная операция: {operator!r}")

    _, func = OPERATIONS[operator]
    return func(first, second)


def format_number(value: float) -> str:
    """Представить число без хвостового ``.0`` (2.0 -> '2')."""
    if value == int(value):
        return str(int(value))
    return f"{value:g}"


def format_result(first: float, second: float, operator: str, result: float) -> str:
    """Собрать строку вида ``2 + 2 = 4``."""
    return f"{format_number(first)} {operator} {format_number(second)} = {format_number(result)}"
