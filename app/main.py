"""Консольный интерфейс: ввод чисел, выбор операции, вывод результата."""

from app.calculator import OPERATIONS, calculate, format_result


def read_number(prompt: str) -> float:
    """Считать число с повторным запросом при некорректном вводе."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Введите число, например 2 или 2.5.")


def choose_operation() -> str:
    """Показать список операций и вернуть выбранный символ."""
    print("\nДоступные операции:")
    for symbol, (name, _) in OPERATIONS.items():
        print(f"  {symbol} — {name}")

    while True:
        operator = input("Выберите операцию: ").strip()
        if operator in OPERATIONS:
            return operator
        print("Нет такой операции. Выберите один из символов: "
              + ", ".join(OPERATIONS))


def run_once() -> None:
    """Один расчёт: два числа, операция, результат в консоли."""
    first = read_number("Введите первое число: ")

    while True:
        second = read_number("Введите второе число: ")
        operator = choose_operation()
        try:
            result = calculate(first, second, operator)
        except ZeroDivisionError:
            print("На ноль делить нельзя, введите другое второе число.")
            continue
        print(format_result(first, second, operator, result))
        return


def main() -> None:
    """Основной цикл приложения."""
    print("Калькулятор двух чисел")
    while True:
        run_once()
        again = input("Посчитать ещё раз? (y/n): ").strip().lower()
        if again != "y":
            print("До свидания!")
            return


if __name__ == "__main__":
    main()
