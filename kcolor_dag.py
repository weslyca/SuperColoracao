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


# print(graph_closure(connections))

def dfs_main(connections, vertex_colors):

    limit = len(set([c for c in vertex_colors.values()]))
    super_value = {}

    for r in connections:
        r_colors = dfs_aux(
            connections, 
            r, 
            vertex_colors,
            set(), 
            limit
        )
        super_value[r] = r_colors
    
    return super_value
    


def dfs_aux(connections, root, vertex_colors, colors, limit):
    curr_colors = colors.union({vertex_colors[root]})

    if limit == 1:
        return curr_colors

    most_colors = curr_colors
    
    for v in connections[root]:
        rec_colors = dfs_aux(
            connections,
            v, 
            vertex_colors, 
            curr_colors, 
            limit-1
        )
        
        if len(rec_colors) > len(most_colors):
            most_colors = rec_colors

    return most_colors


values = []

for _ in range(1):
    start = time.time()
    closure = graph_closure(connections=connections)
    super_values = dfs_main(closure, colors)
    end = time.time()
    print(f"Elapsed time for {n} vertices: {end - start}s")
    values.append(end-start)


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
