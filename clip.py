import pulp
from collections import defaultdict

visited = set()

def dfs_res(node, comp):
    visited.add(node)
    comp.append(node)
    
    for child in graph[node]:
        if child not in visited:
            dfs_res(child, comp)
    

s1, s2, N, M = input().split()
N = int(N)
M = int(M)

adj_mat = {}
graph = defaultdict(list)

for i in range(M):
  a, b = map(int, input().split())
  
  if a < b:
      adj_mat[(a, b)] = 1
  else:
      adj_mat[(b, a)] = 1

cost = []
possible_edges = {}

for i in range(1, N+1):
  for j in range(i+1, N+1):
    
    var = pulp.LpVariable("x_{0}_{1}".format(i, j), lowBound=0, upBound=1, cat=pulp.LpBinary)
    
    if (i, j) in adj_mat:
      cost.append(1 - var)
    else:
      cost.append(var)
    
    possible_edges[(i, j)] = var


# model
clust_edit_model = pulp.LpProblem("Cluster_Editing_Model", pulp.LpMinimize)

# objective function
clust_edit_model += pulp.lpSum(cost)

# specify constraints
for u in range(1, N+1):
    for v in range(u + 1, N+1):
        for w in range(v + 1, N+1):
          if((u, v) in adj_mat and (v, w) in adj_mat and (u, w) not in adj_mat):
              clust_edit_model += (possible_edges[(u, v)] + possible_edges[(v, w)] - possible_edges[(u, w)] <= 1)
          elif((u, v) in adj_mat and (v, w) not in adj_mat and (u, w) in adj_mat):
              clust_edit_model += (possible_edges[(u, v)] - possible_edges[(v, w)] + possible_edges[(u, w)] <= 1)
          elif((u, v) not in adj_mat and (v, w) in adj_mat and (u, w) in adj_mat):
              clust_edit_model += (-possible_edges[(u, v)] +  possible_edges[(v, w)] + possible_edges[(u, w)] <= 1)


solver = pulp.PULP_CBC_CMD(msg=False)

clust_edit_model.solve(solver)

modif = []

for i in range(1, N+1):
  for j in range(i+1, N+1):
    if (round(possible_edges[(i, j)].value()) == 0 and (i, j) in adj_mat):
        modif.append((i, j))
        adj_mat.pop((i, j))
    elif (round(possible_edges[(i, j)].value()) == 1 and (i, j) not in adj_mat):
        modif.append((i, j))
        adj_mat[(i, j)] = 1

for edge in adj_mat:
    graph[edge[0]].append(edge[1])
    graph[edge[1]].append(edge[0])

timeout = 0

for node in range(1, N+1):
    if node not in visited:
        comp = []
        dfs_res(node, comp)
        
        sum_deg = 0
        for nd in comp:
            sum_deg += len(graph[nd])

        sz = len(comp)
       
        if sum_deg != (sz*(sz-1)):
            timeout = 1
            break

set_tle = 0

if timeout:
   while 1:
       set_tle = 1  
else:
  for modification in modif:
      print(modification[0], modification[1])
