dag_graph = True
gen_type = 'm'
max_colors = 10000

n = int(input())

individuals = set()

connections = {}

color_corresp = {}
id_corresp = {}
vertex_to_id = {}
id_to_sex = {}
n_vert = 0

colors = {}
n_colors = 0

id_corresp["0"] = n+1

for _ in range(n):
    # indivíduo, sexo, pai, mãe, clã, subclã, data de nascimento, e data da morte
    id, sex, father, mother, clan, subclan, dob, dod = input().split()
    # print(n_vert)
    # print(mother, father, id, n_vert)
    if id not in id_corresp:
        id_corresp[id] = n_vert
        n_vert += 1

    if id not in id_to_sex:
        id_to_sex[id] = sex

    if mother not in id_corresp:
        id_corresp[mother] = n_vert
        n_vert += 1

    if father not in id_corresp:
        id_corresp[father] = n_vert
        n_vert += 1

    mother_vert = id_corresp[mother]
    father_vert = id_corresp[father]
    self_vert = id_corresp[id]

    if mother_vert not in connections:
        connections[mother_vert] = []
    connections[mother_vert].append(self_vert)

    if father_vert not in connections:
        connections[father_vert] = []
    connections[father_vert].append(self_vert)

    if self_vert not in connections:
        connections[self_vert] = []

    if self_vert not in vertex_to_id:
        vertex_to_id[self_vert] = id


    # if clan not in color_corresp:
    #     color_corresp[clan] = n_colors
    #     n_colors += 1

    # colors[self_vert] = color_corresp[clan]


# 0 is a stand-in for "unknown"
if id_corresp["0"] in connections:
    del connections[id_corresp["0"]]
    del id_corresp["0"]


# no clans are available so we need to define them
# we take the roots
root_vertices = [x for x in connections]
for x in connections:
    for y in connections[x]:
        if y in root_vertices:
            root_vertices.remove(y)
available_colors = [i for i in range(min(len(root_vertices), max_colors))]


def set_color(v, c, gen_type):
    global connections, colors
    colors[v] = c

    # print(f"Vertex {v} : {connections[v]}, {id_to_sex[vertex_to_id[v]].lower()}")

    if gen_type == 'p' and id_to_sex[vertex_to_id[v]].lower() == 'm':
        for u in connections[v]:
            set_color(u, c, gen_type)
    elif gen_type == 'm' and id_to_sex[vertex_to_id[v]].lower() == 'f':
        for u in connections[v]:
            set_color(u, c, gen_type)

# n = n_vert

i = 0
for v in root_vertices:
    set_color(v, available_colors[i], gen_type)
    i = (i+1)%len(available_colors)

def set_extra_color(v):
    global connections, colors

    # print(f"Setting extra for vertex {v} : {connections[v]}, {id_to_sex[vertex_to_id[v]].lower()}")

    parents = [p for p in connections if v in connections[p]]
    kids = connections[v]

    if len(parents) > 0:
        w = sorted(parents)[0]
    else:
        w = sorted(kids)[0]

    if w not in colors:
        set_extra_color(w)
    set_color(v, colors[w], gen_type)

extra_vertices = [i for i in range(n) if i not in colors]
for v in extra_vertices:
    set_extra_color(v)



print(n, (sum([len(connections[l]) for l in connections])))
print(' '.join([str(colors[i]) for i in range(n)]))

for l in connections:
    for k in connections[l]:
        print(l, k)

print()
print("Set color info...")
print("# of root vertices: ", len(root_vertices))
print("# of available colors: ", len(available_colors))
for color in available_colors:
    print(color, ": ", [v for v in colors if colors[v] == color])
# for c in color_corresp:
#     print (f"{c} : {color_corresp[c]}")

print()

print("Id correspondences")
for c in id_corresp:
    print (f"{c} : {id_corresp[c]}")

print()


start_time = [-1 for _ in range(n)]
end_time = [-1 for _ in range(n)]
time = 0

cycle_detected = False

def run_dfs(vertex):
    global time

    start_time[vertex] = time
    time += 1

    if vertex not in connections:
        connections[vertex] = []

    for l in connections[vertex]:
        if start_time[l] > -1 and end_time[l] == -1:
            cycle_detected = True
        if start_time[l] == -1:
            run_dfs(l)
    
    end_time[vertex] = time
    time += 1


for vertex in range(len(start_time)):
    if start_time[vertex] == -1:
        run_dfs(vertex)

if cycle_detected:
    print("Cycle found")
else:
    print("No cycle found")


