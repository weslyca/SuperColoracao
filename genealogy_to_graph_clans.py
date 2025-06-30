n = int(input())

individuals = set()

connections = {}

color_corresp = {}
id_corresp = {}
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

    if clan not in color_corresp:
        color_corresp[clan] = n_colors
        n_colors += 1

    colors[self_vert] = color_corresp[clan]

if id_corresp["0"] in connections:
    del connections[id_corresp["0"]]
    del id_corresp["0"]

n = n_vert

print(n, (sum([len(connections[l]) for l in connections])))
print(' '.join([str(colors[i]) for i in range(n)]))

for l in connections:
    for k in connections[l]:
        print(l, k)

print()
print("Color correspondences")
for c in color_corresp:
    print (f"{c} : {color_corresp[c]}")

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


