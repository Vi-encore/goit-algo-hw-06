import networkx as nx
from collections import deque


def dfs_find_path(graph, start_vertex, end_vertex):
    # Використовуємо стек для зберігання шляхів, а не просто вершин
    # Кожен елемент стеку - це список вершин, що представляють поточний шлях
    stack = [[start_vertex]]
    visited = set()

    while stack:
        # Вилучаємо останній шлях зі стеку
        current_path = stack.pop()
        # Отримуємо останню вершину в поточному шляху
        vertex = current_path[-1]

        # Якщо ми дійшли до кінцевої вершини, повертаємо шлях
        if vertex == end_vertex:
            return current_path

        if vertex not in visited:
            visited.add(vertex)
            # Додаємо сусідні вершини до стеку, формуючи нові шляхи
            # Важливо: додаємо сусідів у зворотному порядку,
            # щоб DFS "глибше" йшов по першому знайденому сусіду
            for neighbor in reversed(graph.get(vertex, [])):
                if neighbor not in visited:
                    new_path = list(current_path)  # Створюємо копію поточного шляху
                    new_path.append(neighbor)
                    stack.append(new_path)
    return None  # Шлях не знайдено


def bfs_find_path(graph, start_vertex, end_vertex):
    # Ініціалізація черги з початковим шляхом
    # Кожен елемент черги - це список вершин, що представляють поточний шлях
    queue = deque([[start_vertex]])
    visited = {start_vertex}  # Множина відвіданих вершин

    while queue:
        # Вилучаємо перший шлях з черги
        current_path = queue.popleft()
        # Отримуємо останню вершину в поточному шляху
        vertex = current_path[-1]

        # Якщо ми дійшли до кінцевої вершини, повертаємо шлях
        if vertex == end_vertex:
            return current_path

        # Додаємо всіх невідвіданих сусідів вершини до кінця черги
        for neighbor in graph.get(vertex, []):
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = list(current_path)  # Створюємо копію поточного шляху
                new_path.append(neighbor)
                queue.append(new_path)
    return None  # Шлях не знайдено


def main():
    G = nx.Graph()
    G.add_nodes_from(["Kyiv", "Kharkiv", "Kherson", "Odesa", "Lviv", "Vinnytsia"])

    G.add_edges_from(
        [
            ("Kyiv", "Kharkiv"),
            ("Kyiv", "Kherson"),
            ("Kyiv", "Odesa"),
            ("Kyiv", "Lviv"),
            ("Kyiv", "Vinnytsia"),
            ("Kharkiv", "Kherson"),
            ("Kharkiv", "Odesa"),
            ("Kharkiv", "Lviv"),
            ("Kherson", "Odesa"),
            ("Kherson", "Lviv"),
            ("Lviv", "Odesa"),
            ("Lviv", "Vinnytsia"),
        ]
    )

    # створюємо список суміжності
    adjacency_list = {node: [] for node in G.nodes()}

    for u, v in G.edges():
        adjacency_list[u].append(v)
        adjacency_list[v].append(u)

    # Сортуємо списки суміжності для детермінованості обходу
    # Це важливо для порівняння, оскільки без цього порядок сусідів може бути випадковим
    # і шляхи, знайдені DFS, можуть відрізнятися при кожному запуску.
    for node in adjacency_list:
        adjacency_list[node].sort()

    print("Список суміжності:")
    for node, neighbors in adjacency_list.items():
        print(f"  {node}: {neighbors}")

    # Задаємо початкову та кінцеву вершини для пошуку шляхів
    start_node = "Kyiv"
    end_node = "Odesa"  # Приклад кінцевої вершини

    print(f"\nПошук шляху з {start_node} до {end_node}:")

    # DFS
    dfs_path = dfs_find_path(adjacency_list, start_node, end_node)
    if dfs_path:
        print(f"Шлях DFS: {' -> '.join(dfs_path)}")
    else:
        print(f"Шлях DFS до {end_node} не знайдено.")

    # BFS
    bfs_path = bfs_find_path(adjacency_list, start_node, end_node)
    if bfs_path:
        print(f"Шлях BFS: {' -> '.join(bfs_path)}")
    else:
        print(f"Шлях BFS до {end_node} не знайдено.")

    print("\n--- Порівняння та пояснення ---")
    if dfs_path and bfs_path:
        if dfs_path == bfs_path:
            print("Обидва алгоритми знайшли однаковий шлях.")
        else:
            print("Алгоритми знайшли різні шляхи.")
            print("\n**Різниця в отриманих шляхах:**")
            print(f"  DFS знайшов шлях: {' -> '.join(dfs_path)}")
            print(f"  BFS знайшов шлях: {' -> '.join(bfs_path)}")

            print("\n**Чому шляхи саме такі?**")
            print("  1. **Алгоритм DFS:**")
            print(
                "     - DFS досліджує якомога далі вздовж кожної гілки перед тим, як повертатися назад."
            )
            print(
                "     - Через це, знайдений DFS шлях часто не є найкоротшим. Його шлях залежить від порядку обходу сусідів (ми відсортували їх для детермінованості) та структури графа."
            )
            print(
                f"     - У даному випадку, при пошуку з {start_node} до {end_node}, DFS рухався по першому доступному сусіду до максимально можливої глибини, перш ніж розглядати інші варіанти. (Наприклад, Kyiv -> Kharkiv -> Odesa, якщо Kharkiv був першим в списку суміжності Kyiv, а Odesa першим в Kharkiv)"
            )

            print("\n  2. **Алгоритм BFS (Breadth-First Search - Пошук у ширину):**")
            print(
                "     - BFS досліджує всі вершини на поточному рівні (відстані від початкової вершини), перш ніж перейти до вершин наступного рівня."
            )
            print(
                f"     - Отже, шлях, знайдений BFS з {start_node} до {end_node}, є найкоротшим можливим за кількістю ребер."
            )
    elif dfs_path is None and bfs_path is None:
        print(f"Шлях з {start_node} до {end_node} не знайдено обома алгоритмами.")
    else:
        print(
            "Один з алгоритмів знайшов шлях, а інший - ні (це не повинно відбуватися в зв'язаному графі, якщо шлях існує)."
        )


if __name__ == "__main__":
    main()
