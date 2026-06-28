import heapq
import streamlit as st
# --- Union-Find for Kruskal ---
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x]) # Path compression
        return self.parent[x]
    
    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry: return False
        if self.rank[rx] < self.rank[ry]: rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]: self.rank[rx] += 1
        return True
    
def kruskal(n, edges):
    """edges: list of (weight, u, v)"""
    edges.sort() # O(E log E)
    uf = UnionFind(n)
    mst = []
    cost = 0
    for w, u, v in edges:
        if uf.union(u, v):
            mst.append((u, v, w))
            cost += w
            if len(mst) == n - 1:
                break
    return mst, cost
    
def prim(n, adj, start=0):
    """adj: adjacency list {u: [(v, w), ...]}"""
    INF = float('inf')
    key = [INF] * n
    parent = [-1] * n
    inMST = [False] * n
    key[start] = 0
    pq = [(0, start)]
    mst = []
    cost = 0
    while pq:
        w, u = heapq.heappop(pq)
        if inMST[u]: continue
        inMST[u] = True
        if parent[u] != -1:
            mst.append((parent[u], u, w))
            cost += w
        for v, wt in adj.get(u, []):
            if not inMST[v] and wt < key[v]:
                key[v] = wt
                parent[v] = u
                heapq.heappush(pq, (wt, v))
    return mst, cost
    
# -------------------- Streamlit UI --------------------

st.title("Minimum Spanning Tree (MST)")
st.subheader("Kruskal's Algorithm and Prim's Algorithm")

if st.button("Run Algorithms"):

    # --- Graph Definition ---
    n = 7
    edges = [
        (7, 0, 1), (5, 0, 3), (8, 1, 2), (9, 1, 3),
        (7, 1, 4), (5, 2, 4), (15, 3, 4), (6, 3, 5),
        (8, 4, 5), (9, 4, 6), (11, 5, 6)
    ]

    adj = {}

    for w, u, v in edges:
        adj.setdefault(u, []).append((v, w))
        adj.setdefault(v, []).append((u, w))

    k_mst, k_cost = kruskal(n, edges[:])
    p_mst, p_cost = prim(n, adj)

    st.subheader("Kruskal's MST")

    for u, v, w in k_mst:
        st.write(f"Edge ({u} - {v})    Weight : {w}")

    st.success(f"Total MST Cost : {k_cost}")

    st.subheader("Prim's MST")

    for u, v, w in p_mst:
        st.write(f"Edge ({u} - {v})    Weight : {w}")

    st.success(f"Total MST Cost : {p_cost}")