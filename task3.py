import networkx as nx
from collections import deque


def print_table(distances):
    """
    Форматує та виводить таблицю відстаней.
    """
    print("{:<20} {:<15}".format("Вершина", "Відстань"))
    print("-" * 35)

    for vertex in distances:
        distance = distances[vertex]
        if distance == float("infinity"):
            distance_str = "∞"
        else:
            distance_str = str(f"{distance} км")  # Додаємо "км" для ясності

        print("{:<20} {:<15}".format(vertex, distance_str))


def dijkstra_nx(graph, start_vertex):

    distances = {vertex: float("infinity") for vertex in graph.nodes}
    distances[start_vertex] = 0
    unvisited = list(graph.nodes())

    while unvisited:
        current_vertex = min(unvisited, key=lambda vertex: distances[vertex])

        if distances[current_vertex] == float("infinity"):
            break

        for u, v, data in graph.edges(current_vertex, data=True):
            neighbor = v if u == current_vertex else u
            weight = data.get("weight", 1)
            distance = distances[current_vertex] + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance

        unvisited.remove(current_vertex)
    return distances


def dijkstra_find_path(graph, start_vertex, end_vertex):

    distances = {vertex: float("infinity") for vertex in graph.nodes}
    previous_nodes = {vertex: None for vertex in graph.nodes}  # Для відновлення шляху
    distances[start_vertex] = 0
    unvisited = list(graph.nodes())

    while unvisited:
        current_vertex = min(unvisited, key=lambda vertex: distances[vertex])

        if distances[current_vertex] == float("infinity"):
            break

        if current_vertex == end_vertex:
            path = []
            while current_vertex is not None:
                path.insert(0, current_vertex)
                current_vertex = previous_nodes[current_vertex]
            return path, distances[end_vertex]

        for u, v, data in graph.edges(current_vertex, data=True):
            neighbor = v if u == current_vertex else u
            weight = data.get("weight", 1)  # Вага ребра

            new_distance = distances[current_vertex] + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous_nodes[neighbor] = current_vertex

        unvisited.remove(current_vertex)

    return None, float("infinity")


def main():
    G = nx.Graph()

    nodes = ["Kyiv", "Kharkiv", "Kherson", "Odesa", "Lviv", "Vinnytsia"]
    G.add_nodes_from(nodes)

    # Додаємо ребра з приблизними відстанями (вагами в км)
    # Ці відстані взяті з відкритих джерел, можуть бути округлені.
    edges_with_weights = [
        ("Kyiv", "Kharkiv", 479),
        ("Kyiv", "Kherson", 540),
        ("Kyiv", "Odesa", 475),
        ("Kyiv", "Lviv", 540),
        ("Kyiv", "Vinnytsia", 270),
        ("Kharkiv", "Kherson", 565),
        ("Kharkiv", "Odesa", 570),
        ("Kharkiv", "Lviv", 790),
        ("Kherson", "Odesa", 200),
        ("Kherson", "Lviv", 900),
        ("Odesa", "Lviv", 790),
        ("Lviv", "Vinnytsia", 360),
    ]

    G.add_weighted_edges_from(edges_with_weights)

    print("Граф з вагами (відстанями в км):")
    for u, v, data in G.edges(data=True):
        print(f"  {u} -- {v}: {data['weight']} км")

    print("\n" + "=" * 60)
    print("--- Застосування алгоритму Дейкстри до зваженого графа ---")
    print("Знаходження найкоротших відстаней від кожного міста до інших:")

    for city in G.nodes():
        print(f'\nНайкоротші відстані від "{city}":')
        distances_from_city = dijkstra_nx(G, city)
        print_table(distances_from_city)

    print("\n" + "=" * 60)
    print("--- Приклад знаходження конкретного найкоротшого шляху ---")
    start_path_node = "Kyiv"
    end_path_node = "Kherson"
    path, length = dijkstra_find_path(G, start_path_node, end_path_node)

    if path:
        print(f"\nНайкоротший шлях з {start_path_node} до {end_path_node}:")
        print(f"  Шлях: {' -> '.join(path)}")
        print(f"  Довжина шляху: {length} км")
    else:
        print(f"\nШлях з {start_path_node} до {end_path_node} не знайдено.")

    # Ще один приклад
    start_path_node_2 = "Lviv"
    end_path_node_2 = "Kharkiv"
    path_2, length_2 = dijkstra_find_path(G, start_path_node_2, end_path_node_2)

    if path_2:
        print(f"\nНайкоротший шлях з {start_path_node_2} до {end_path_node_2}:")
        print(f"  Шлях: {' -> '.join(path_2)}")
        print(f"  Довжина шляху: {length_2} км")
    else:
        print(f"\nШлях з {start_path_node_2} до {end_path_node_2} не знайдено.")


if __name__ == "__main__":
    main()
