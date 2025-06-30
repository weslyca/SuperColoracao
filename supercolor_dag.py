n, arcs = map(int, input().split())
colors = list(map(int, input().split()))

#(u, v, colors, vertices)

def alt_shift(i):
    if i >= 0:
        return 1 << i
    return 0

color_markers = [alt_shift(i) for i in colors]
vertex_markers = [1 << i for i in range(n)]

reachable_sets = {i : {color_markers[i],} for i in range(n)}

connections = {i : [] for i in range(n)}

# paths = {i : set() for i in range(n)}
for _ in range(arcs):
    u, v = map(int, input().split())
    connections[u].append(v)
    # paths[u].add((u, v, color_markers[u] | color_markers[v], vertex_markers[u] | vertex_markers[v]))

start_time = [-1 for _ in range(n)]
end_time = [-1 for _ in range(n)]
time = 0

cycle_detected = False

def run_dfs(vertex):
    global time

    start_time[vertex] = time
    time += 1

    for l in connections[vertex]:
        # print(l)
        if start_time[l] > -1 and end_time[l] == -1:
            cycle_detected = True
        if start_time[l] == -1:
            run_dfs(l)
    
    end_time[vertex] = time
    time += 1

    for l in connections[vertex]:
        reachable_sets[vertex] = (
            reachable_sets[vertex]
            .union(set([(color_markers[vertex] | r_set) for r_set in reachable_sets[l]]))
        )

for vertex in range(len(start_time)):
    if start_time[vertex] == -1:
        run_dfs(vertex)

def get_number_colors(entry):
    c = entry
    number = 0
    while c > 0:
        number += c % 2
        c = c // 2
    return (number, entry)

for v in range(n):
    l = [get_number_colors(entry) for entry in reachable_sets[v]]
    print(v, max(l))



