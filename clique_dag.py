import time
import pandas as pd

n, arcs = map(int, input().split())
colors = list(map(int, input().split()))
colors = {i : colors[i] for i in range(n)}

#(u, v, colors, vertices)

def alt_shift(i):
    if i >= 0:
        return 1 << i
    return 0

color_markers = [alt_shift(i) for i in colors]
vertex_markers = [1 << i for i in range(n)]

reachable_sets = {i : {color_markers[i],} for i in range(n)}

connections = {}

# paths = {i : set() for i in range(n)}
for _ in range(arcs):
    u, v = map(int, input().split())
    if u not in connections:
        connections[u] = []
    connections[u].append(v)

    if v not in connections:
        connections[v] = []

def graph_closure(connections):
    closure = {v : [] for v in connections}

    #bfs
    for r in connections:
        visited = {v : False for v in connections}
        queue = [r]
        while len(queue) > 0:
            u = queue.pop(0)
            visited[u] = True
            
            for v in connections[u]:
                if not visited[v]:
                    queue.append(v)
                    closure[r].append(v)

    return closure



def check_clique_expansion(v, connections, clique):
    expansion_possible = True
    for w in clique:
        if not (w in connections[v]):
            expansion_possible = False
    return expansion_possible

def expand_clique(v, clique):
    return (v,) + clique


def remove_same_color_arcs(connections, colors):
    new_connections = {u : [] for u in connections}
    for u in connections:
        for v in connections[u]:
            if colors[u] != colors[v]:
                new_connections[u].append(v)
    return new_connections 

def make_topological_order(connections):
    order = []
    visited = {u : False for u in connections}

    def apply_recursion(u):
        visited[u] = True
        for v in connections[u]:
            if not visited[v]:
                apply_recursion(v)
        order.append(u)
    
    for u in connections:
        if not visited[u]:
            apply_recursion(u)
    return order


def compute_super(connections, colors):

    closure = graph_closure(connections=connections)

    preprocessed_graph = remove_same_color_arcs(closure, colors)
    top_order = make_topological_order(preprocessed_graph)

        
    # print("Preprocessed_graph:")
    # for u, adju in preprocessed_graph.items():
    #     print(u, ": ", adju)
    # print()


    # print("topological_order: ", top_order)

    cliques = {v: {(v,)} for v in connections}

    for u in top_order:
        for v in preprocessed_graph[u]:
            for clique in cliques[v]:
                if check_clique_expansion(u, preprocessed_graph, clique):
                    new_clique = expand_clique(u, clique)
                    cliques[u].add(new_clique)

    # print("Cliques:")
    # for u, adju in cliques.items():
    #     print(u, ": ", adju)
    # print()

    super_values = {v : max(cliques[v], key=len)  for v in cliques}
    return super_values

values = []

for _ in range(30):
    start = time.time()
    super_values = compute_super(connections, colors)
    end = time.time()
    print(f"Elapsed time for {n} vertices: {end - start}s")
    values.append(end-start)

# print("Connections:")
# for u, adju in connections.items():
#     print(u, ": ", adju)
# print()


# print("super_values:")
# for u, super_value in super_values.items():
#     print(u, ": ", super_value)
# print()

for v in range(n):
    if v not in super_values:
        super_values[v] = set([colors[v]])
    super = super_values[v]
    print(f"Super-value for {v}: {len(super)}, {super}")

print("Statistics")

series = pd.Series(values)

print(series)
print("Mean: ", series.mean())
print("Standard deviation: ", series.std())
