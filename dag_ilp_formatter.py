from collections import defaultdict
import sys
import time

def bfs_check(root, adj_list, reach):
    visited = defaultdict(lambda : False)

    q = [root]

    while len(q) > 0:
        u = q.pop(0)

        if u == reach:
            return True

        visited[u] = True

        for v in adj_list[u]:
            if not visited[v]:
                if not (u == root and v == reach):
                    q.append(v)
    
    return False


def remove_shortcuts(adj_list):
    new_adj_list = {}
    for u in adj_list:
        new_adj_list[u] = []
        for v in adj_list[u]:
            if not bfs_check(u, adj_list, v):
                new_adj_list[u].append(v)
    return new_adj_list



def set_levels_aux(v, adj_list, levels):
    
    for u in adj_list[v]:
        levels[u] = max(levels[u], levels[v] + 1)
    
    for u in adj_list[v]:
        set_levels_aux(u, adj_list, levels)



def set_levels(root, adj_list):

    levels = defaultdict(lambda: 0)
    set_levels_aux(root, adj_list, levels)
    # print(levels)
    
    return levels

def get_reachable_vertices(root, adj_list):

    visited = defaultdict(lambda : False)

    q = [root]
    while len(q) > 0:
        u = q.pop(0)

        visited[u] = True
        for v in adj_list[u]:
            if not visited[v]:
                q.append(v)

    return [v for v in visited]


def filter_by_vertices(adj_list, filter):
    new_adj_list = defaultdict(list)

    for u in filter:
        new_adj_list[u] = []
        for v in adj_list[u]:
            if v in filter:
                new_adj_list[u].append(v)
    
    return new_adj_list

def create_subtrees(adj_list):
    subtrees = {}

    for v in adj_list:
        if len(adj_list[v]) > 0:
            subtrees[v] = filter_by_vertices(adj_list, get_reachable_vertices(v, adj_list))
    return subtrees


def create_color_variables(root, colors):
    return [f"t{root}r{color}" for color in colors]

def create_parent_constraints(root, subtree):
    restrictions = []

    # for each subtree...
    # a vertex can be in the path (proot_i) only if either of its parents are
    # this does not apply to the root so...

    parents = defaultdict(list)

    for u in subtree:
        for v in subtree[u]:
            parents[v].append("p" + str(root) + "r" + str(u))
    
    for u in parents:
        restrictions.append(f"p{root}r{u} - {' - '.join(parents[u])} <= 0")

    return restrictions


def create_level_constraints(root, adj_list):
    restrictions = []
    levels = set_levels(root, adj_list)

    vertices_by_level = {level : [i for i in levels if levels[i] == level] for level in set(levels.values())}
    for level in vertices_by_level:
        str_levels = ['p' + str(root) + "r" + str(v) for v in vertices_by_level[level]]
        restrictions.append(f"{' + '.join(str_levels)} - ONE <= 0")

    return restrictions

def create_children_constraints(root, subtree):
    restrictions = []

    for u in subtree:
        if len(subtree[u]) > 0:
            str_children = ['p' + str(root) + "r" + str(v) for v in subtree[u]]
            restrictions.append(f"{' + '.join(str_children)} - ONE <= 0")

    return restrictions



def create_color_constraints(root, adj_list, color_assignments):
    restrictions = []
    colors = list(set(color_assignments.values()))
    for tk in colors:
        tk_vertices = []

        for vi in adj_list:
            if color_assignments[vi] == tk:
                tk_vertices.append("p" + str(root) + "r" + str(vi))
                restrictions.append(f"t{root}r{tk} - p{root}r{vi} >= 0")
        if len(tk_vertices) > 0:
            restrictions.append(f"t{root}r{tk} - {' - '.join(list(map(str, tk_vertices)))} <= 0")
        else:
            restrictions.append(f"t{root}r{tk} <= 0")

    return restrictions


start = time.time()
n, m = map(int, input().split())
color_assignments = {i : c for i, c in zip([k for k in range(n)], list(map(int, input().split())))}
adj_list = defaultdict(list)

parent_list = defaultdict(list)

for _ in range(m):
    u, v = map(int, input().split())
    adj_list[u].append(v)
    if v not in adj_list:
        adj_list[v] = []
    parent_list[v].append(u)

colors = list(set(color_assignments.values()))
# print(colors)

# print(adj_list.items())

# k = len(set(colors.values()))

# levels = set_levels(adj_list)
# print(levels)
# vertices_by_level = {level : [i for i in levels if levels[i] == level] for level in set(levels.values())}
# print(vertices_by_level)

# print(adj_list)

new_graph = remove_shortcuts(adj_list)

# print(new_graph)

subtrees = create_subtrees(new_graph)

# for root, subtree in subtrees.items():
#     print(root, subtree)

print("Maximize")

tk_variables = [f"t{root}r{color}" for root in subtrees for color in colors]
print(f"  {' + '.join(tk_variables)}")


print("Subject To")
# print("PARENT CONSTRAINTS")

pc = 0
for root, subtree in subtrees.items():
    restrictions = create_parent_constraints(root, subtree)
    for r in restrictions:
        print(f"  pc{pc}: {r}")
        pc += 1

# lc = 0
# # print("LEVEL CONSTRAINTS")
# for root, subtree in subtrees.items():
#     restrictions = create_level_constraints(root, subtree)
#     for r in restrictions:
#         print(f"  lc{lc}: {r}")
#         lc += 1
kc = 0
# print("LEVEL CONSTRAINTS")
for root, subtree in subtrees.items():
    restrictions = create_children_constraints(root, subtree)
    for r in restrictions:
        print(f"  kc{kc}: {r}")
        kc += 1


cc = 0
# print("COLOR CONSTRAINTS")
for root, subtree in subtrees.items():
    restrictions = create_color_constraints(root, subtree, color_assignments)
    for r in restrictions:
        print(f"  cc{cc}: {r}")
        cc += 1

print("Bounds")

# for tk in tk_variables:
#     print(f"  0 <= {tk} <= 1")

# for root, subtree in subtrees.items():
#     subtree_vertices = get_reachable_vertices(root, subtree)
#     for v in subtree_vertices:
#         print(f"  0 <= p{root}r{v} <= 1")

print(f"  1 <= ONE <= 1")

#Variable type
print("Binary")
variables = [tk for tk in tk_variables]
for root, subtree in subtrees.items():
    subtree_vertices = get_reachable_vertices(root, subtree)
    for v in subtree_vertices:
        # print(f"  0 <= p{root}r{v} <= 1")
        variables.append(f"p{root}r{v}")
print(f"  {' '.join(variables)}")

print("End")

end = time.time()


# print(f"Formatting time: {end - start}")

# # create color matrix

# print("Maximize")
# #====================
# # 
# # 

# print(f"  {' + '.join([f't{color}' for color in range(1, k+1)])}")

# print("Subject To")
# # constraints...

# parent_constraint = 0

# for pi in range(1, n+1):
#     if len(parent_list[pi]) > 0: 
#         p_parents = ['p' + str(parent) for parent in parent_list[pi]]
#         print(f"  pc{parent_constraint}: p{pi} - {' - '.join(p_parents)} <= 0")
#         parent_constraint+=1

# level_constraint = 0
# for level in vertices_by_level:
#     str_levels = ['p' + str(v) for v in vertices_by_level[level]]
#     print(f"  lc{level_constraint}: {' + '.join(str_levels)} -1 <= 0")
#     level_constraint += 1

# color_constraint = 0
# for tk in range(1, k+1):

#     tk_vertices = []
#     for vi in range(1, n+1):
#         if colors[vi] == tk:
#             tk_vertices.append("p" + str(vi))
#             print(f"  cc{color_constraint}: t{tk} - p{vi} >= 0")
#             color_constraint += 1

#     # vertices that have tk as color
#     print(f"  cc{color_constraint}: t{tk} - {' - '.join(list(map(str, tk_vertices)))} <= 0"  )

# print("Bounds")

# for tk in range(1, k+1):
#     print(f'  0 <= t{tk} <= 1')

# print(f'  p{1} = 1')

# for pi in range(2, n+1):
#     print(f'  0 <= p{pi} <= 1')


# # print("Generals")
# # # all path variables
# # # and also color_in_path?

# # variables = [f"p{vertex}" for vertex in range(1, n+1)] + [f"t{color}" for color in range(1, k+1)]

# # print(f"  {' '.join(variables)}")


# print("End")

# # each of the vertices i has an associated variable pi







