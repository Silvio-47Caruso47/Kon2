import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Инструмент визуализации зависимостей (Вариант 25)")
    parser.add_argument("--package", required=True, help="Имя анализируемого пакета")
    parser.add_argument("--repo", required=True, help="URL-адрес репозитория или путь к файлу")
    parser.add_argument("--test-mode", action="store_true", help="Режим работы с тестовым репозиторием")
    parser.add_argument("--version", required=True, help="Версия пакета")
    parser.add_argument("--ascii-tree", action="store_true", help="Режим вывода в виде ASCII-дерева")
    parser.add_argument("--depth", type=int, required=True, help="Максимальная глубина анализа")
    args = parser.parse_args()
    if not args.package.strip():
        print("Ошибка: Имя пакета не может быть пустым.")
        sys.exit(1)
    if args.depth < 0:
        print("Ошибка: Максимальная глубина не может быть отрицательной.")
        sys.exit(1)
    if not args.version.strip():
        print("Ошибка: Версия пакета не может быть пустой.")
        sys.exit(1)
    print("--- Настройки приложения ---")
    print(f"package: {args.package}")
    print(f"repo: {args.repo}")
    print(f"test-mode: {args.test_mode}")
    print(f"version: {args.version}")
    print(f"ascii-tree: {args.ascii_tree}")
    print(f"depth: {args.depth}")
    print("----------------------------")
if __name__ == "__main__":
    main()
