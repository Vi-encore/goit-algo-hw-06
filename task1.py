import networkx as nx
import matplotlib.pyplot as plt

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

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=2000)
labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)


plt.title("Залізничне сполучення між містами")
# plt.show()
plt.savefig("task01.png", format="png")
plt.close()


# Аналіз характеристик графа
print(f"Кількість міст (вершин): {G.number_of_nodes()}")
print(f"Кількість шляхів (ребер): {G.number_of_edges()}")
print(f"Ступінь кожного міста: {dict(G.degree())}")
