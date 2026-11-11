import argparse
import sys
import os
import collections


def get_direct_dependencies(filepath):
    dependencies = []
    if not os.path.exists(filepath):
        print(f"Ошибка: Файл '{filepath}' не найден!")
        sys.exit(1)
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line.startswith("Requires-Dist:"):
                    dep_info = line.replace(
                        "Requires-Dist:", ""
                    ).strip()
                    dep_name = dep_info.split()[0]
                    dependencies.append(dep_name)
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        sys.exit(1)
    return dependencies


def load_graph(filepath):
    graph = {}
    if not os.path.exists(filepath):
        print(f"Ошибка: Файл '{filepath}' не найден!")
        sys.exit(1)
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if ':' not in line:
                    print(f"Ошибка формата: {line}")
                    sys.exit(1)
                parts = line.split(':')
                pkg = parts[0].strip().upper()
                deps = parts[1].strip().split()
                graph[pkg] = deps
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)
    return graph


def bfs_traversal(graph, start_pkg, max_depth, filter_sub):
    visited = set()
    queue = collections.deque()
    queue.append((start_pkg, 0))
    visited.add(start_pkg)
    result = []
    while queue:
        current_pkg, current_depth = queue.popleft()
        result.append(current_pkg)
        if current_depth >= max_depth:
            continue
        deps = graph.get(current_pkg, [])
        for dep in deps:
            dep = dep.upper()
            if filter_sub and filter_sub in dep:
                continue
            if dep not in visited:
                visited.add(dep)
                queue.append((dep, current_depth + 1))
                
    return result


def create_parser():
    parser = argparse.ArgumentParser(
        description="Инструмент визуализации зависимостей")
    parser.add_argument(
        "--package", required=True, help="Имя пакета")
    parser.add_argument(
        "--repo", required=True, help="Путь к файлу")
    parser.add_argument(
        "--test-mode", action="store_true", help="Режим тестов")
    parser.add_argument(
        "--version", required=True, help="Версия пакета")
    parser.add_argument(
        "--ascii-tree", action="store_true", help="Вывод деревом")
    parser.add_argument(
        "--depth", type=int, required=True, help="Глубина")
    parser.add_argument(
        "--filter", required=False, default="", help="Фильтр")
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    if not args.package.strip():
        print("Ошибка: Имя пакета не может быть пустым.")
        sys.exit(1)
    if args.depth < 0:
        print("Ошибка: Глубина не может быть отрицательной.")
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
    print(f"filter: {args.filter}")
    print("----------------------------")
    if args.test_mode:
        graph = load_graph(args.repo)
        start_pkg = args.package.upper()
        found_packages = bfs_traversal(
            graph, start_pkg, args.depth, args.filter.upper())
        print(f"\nНайденные пакеты (BFS, глубина {args.depth}):")
        for pkg in found_packages:
            print(f"- {pkg}")
    else:
        print("\n--- Прямые зависимости ---")
        deps = get_direct_dependencies(args.repo)
        if not deps:
            print("Прямых зависимостей не найдено.")
        else:
            for dep in deps:
                print(f"- {dep}")
    print("---------------------------")


if __name__ == "__main__":
    main()
