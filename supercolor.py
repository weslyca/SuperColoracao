import time
import pandas as pd

n, arcs = map(int, input().split())
colors = list(map(int, input().split()))

#(u, v, colors, vertices)

color_markers = [1 << i for i in colors]
vertex_markers = [1 << i for i in range(n)]

adj = {u : [] for u in range(n)}
for _ in range(arcs):
    u, v = map(int, input().split())
    # paths[u].add((u, v, color_markers[u] | color_markers[v], vertex_markers[u] | vertex_markers[v]))
    adj[u].append(v)



def get_paths(n, arcs, adj, color_markers, vertex_markers):
    paths = {i : set() for i in range(n)}
    for u in adj:
        for v in adj[u]:
            paths[u].add((u, v, color_markers[u] | color_markers[v], vertex_markers[u] | vertex_markers[v]))


    change = True
    iterations = 0
    while change:
        iterations += 1
        change = False
        all_visited_paths = []
        for u in paths:
            all_visited_paths += paths[u]

        for u1, v1, colors1, vertices1 in all_visited_paths:
            for u2, v2, colors2, vertices2 in paths[v1]:
                if vertices1 & vertices2 == vertex_markers[u2]:
                    if (u1, v2, colors1 | colors2, vertices1 | vertices2) not in paths[u1]:
                        change=True
                    paths[u1].add((u1, v2, colors1 | colors2, vertices1 | vertices2))
    
    return paths

def get_super_values(n, arcs, adj, colors, color_markers, vertex_markers):
    res = {}
    v_colors = {}

    def get_number_colors(entry):
        c = entry[2]
        number = 0
        while c > 0:
            number += c % 2
            c = c // 2
        return number

    def get_path_vertices(entry):
        c = entry[3]
        vertices = []
        curr = 0
        while c > 0:
            if c % 2 != 0:
                vertices.append(curr)
            curr += 1
            c = c // 2
        return vertices

    paths = get_paths(n, arcs, adj, color_markers, vertex_markers)

    for u in paths:
        l = (list(map(get_number_colors, paths[u])))
        # vertices = (list(map(get_path_vertices, paths[u])))
        # if u == 4:
        #     print(list(zip(l, vertices)))
        if len(l) > 0:
            res[u] = max(l)
        else:
            res[u] = 1 if colors[u] in colors else 0

    return res


values = []
for _ in range(30):
    start = time.time()
    res = get_super_values(n, arcs, adj, colors, color_markers, vertex_markers)
    end = time.time()
    print(f"Elapsed time for {n} vertices: {end - start}s")
    values.append(end-start)


for v, super_v in sorted(res.items()):
    print(f"Super-value for {v}: {super_v}, {''}")
    # print(f"{u} : {v}")


print("Statistics")

series = pd.Series(values)

print(series)
print("Mean: ", series.mean())
print("Standard deviation: ", series.std())


# for u in [61, 63, 65, 66, 72, 74, 87, 88, 89, 91, 194, 207, 217, 224]:
#     l = list(zip(list(map(get_number_colors, paths[u])), paths[u]))
#     # print(paths[u])
#     # print(l)
#     if len(l) > 0:
#         res[u] = max(l)
#         print(res[])
#     else:
#         res[u] = 1 if colors[u] in [1, 2] else 0
