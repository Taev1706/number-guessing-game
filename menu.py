from logic import generate_secret, play_round, get_top_records, MIN_NUMBER, MAX_NUMBER
from data_service import add_record

VERSION = "1.0.2"


def show_banner():
    print()
    print("=" * 42)
    print(f"  Number Guessing Game  v{VERSION}")
    print(f"  Угадайте число от {MIN_NUMBER} до {MAX_NUMBER}")
    print("=" * 42)
    print()


def show_leaderboard():
    records = get_top_records(top_n=10)
    if not records:
        print("\nТаблица рекордов пуста.\n")
        return
    print("\nТОП-10 ЛУЧШИХ РЕЗУЛЬТАТОВ")
    print("-" * 32)
    for i, rec in enumerate(records, start=1):
        print(f"  {i:>2}. {rec['name']:<20} {rec['attempts']} попыток")
    print("-" * 32)
    print()


def main_menu():
    show_banner()
    while True:
        print("1. Новая игра")
        print("2. Таблица рекордов")
        print("3. Выход")
        choice = input("\nВыберите пункт (1/2/3): ").strip()

        if choice == "1":
            name = input("Введите ваше имя: ").strip()
            if not name:
                print("Имя не может быть пустым.\n")
                continue

            secret = generate_secret()
            print(f"\nХорошо, {name}! Я загадал число. Начинайте угадывать...\n")

            attempts = play_round(
                secret=secret,
                get_input=lambda: input("Ваш вариант: "),
                show_output=print,
            )

            add_record(name, attempts)
            print(f"\nРезультат сохранён. Вам понадобилось {attempts} попытки(-ок).\n")

        elif choice == "2":
            show_leaderboard()

        elif choice == "3":
            print("\nДо свидания!\n")
            break

        else:
            print("Некорректный выбор. Введите 1, 2 или 3.\n")


if __name__ == "__main__":
    main_menu()
