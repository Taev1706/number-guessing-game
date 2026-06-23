import random
from data_service import get_all_records

MIN_NUMBER = 1
MAX_NUMBER = 100


def generate_secret(low: int = MIN_NUMBER, high: int = MAX_NUMBER) -> int:
    if low >= high:
        raise ValueError("Нижняя граница должна быть меньше верхней.")
    return random.randint(low, high)


def check_guess(guess: int, secret: int) -> str:
    if not isinstance(guess, int) or not isinstance(secret, int):
        raise TypeError("Оба аргумента должны быть целыми числами.")
    if guess < secret:
        return "too_low"
    if guess > secret:
        return "too_high"
    return "correct"


def parse_guess(raw: str, low: int = MIN_NUMBER, high: int = MAX_NUMBER) -> int:
    raw = raw.strip()
    if not raw:
        raise ValueError("Ввод не может быть пустым.")
    try:
        value = int(raw)
    except ValueError:
        raise ValueError(f"'{raw}' — не целое число.")
    if value < low or value > high:
        raise ValueError(f"Число должно быть от {low} до {high}.")
    return value


def get_top_records(top_n: int = 10) -> list:
    records = get_all_records()
    parsed = [{"name": r["name"], "attempts": int(r["attempts"])} for r in records]
    return sorted(parsed, key=lambda r: r["attempts"])[:top_n]


def play_round(
    secret: int,
    get_input,
    show_output,
    low: int = MIN_NUMBER,
    high: int = MAX_NUMBER,
) -> int:
    attempts = 0
    while True:
        raw = get_input()
        try:
            guess = parse_guess(raw, low, high)
        except ValueError as e:
            show_output(f"Ошибка: {e}")
            continue

        attempts += 1
        result = check_guess(guess, secret)

        if result == "correct":
            show_output(f"Верно! Вы угадали за {attempts} попытки(-ок).")
            return attempts
        elif result == "too_low":
            show_output("Слишком мало. Попробуйте больше.")
        else:
            show_output("Слишком много. Попробуйте меньше.")