
# filenames = [
#     "ap_matrilinear",
#     "ap_patrilinear",
#     "arara_matrilinear",
#     "arara_patrilinear",
#     "chacobo_matrilinear",
#     "chacobo_patrilinear",
#     "deni_matrilinear",
#     "deni_patrilinear",
#     "en",
#     "im_matrilinear",
#     "im_patrilinear",
#     "kraho",
#     "xv",
#     "zo"
# ]


filenames = [
    "artificial_2990",
    "artificial_5156",
    "artificial_9750",
    "artificial_23961",
    "artificial_52915",
    "artificial_112921",
    "artificial_253446",
]



def apply_conversion(filename):
    paths_colors = {}
    paths_vertices = {}

    with open("GurobiSols/" + filename + ".sol", 'r') as f:
        lines = f.readlines()
    # objective_value = lines[0].split()
    #t{root}r{color}
    for line in lines[1:-1]:
        if line[0] == 't':
            variable = line.split()[0]
            value = line.split()[1]
            root = int(variable[1:].split("r")[0])
            color = int(variable.split("r")[-1])
            if root not in paths_colors:
                paths_colors[root] = []
            if value == '1':
                paths_colors[root].append(color)
        elif line[0] == 'p':
            variable = line.split()[0]
            value = line.split()[1]
            root = int(variable[1:].split("r")[0])
            vertex = int(variable.split("r")[-1])
            if root not in paths_vertices:
                paths_vertices[root] = []
            if value == '1':
                paths_vertices[root].append(vertex)

    with open("ArtificialGraphs/" + filename + ".txt", 'r') as f:
        lines = f.readlines()
        n, m = lines[0].split()
        vertex_colors = lines[1].split()

    n = int(n)

    lines = "" 
    # for root in sorted(paths_colors.keys()):
    for root in range(n):
        if root not in paths_colors:
            lines += f"Super-value for {root}: 1, [{vertex_colors[root]}], 1, [{root}]\n"
        else:
            colors = paths_colors[root]
            vertices = paths_vertices[root]
            # print(f"{root};{colors};{vertices}")
            # print(f"Super-value for {root}: {len(colors)}, {colors}, {len(vertices)}, {vertices}")

            lines += f"Super-value for {root}: {len(colors)}, {colors}, {len(vertices)}, {vertices}\n"

    with open("ArtificialResults/solver/" + filename + ".txt", 'w') as f:
        f.writelines(lines)

for filename in filenames:
    apply_conversion(filename)