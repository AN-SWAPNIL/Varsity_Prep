# Bismillah.

# CSE 207 — Data Structures and Algorithms II: Slide-Complete Viva Recall

This is a reconstruction of the CSE 207 material from the course slides and notes in this workspace. It is meant to restore the concepts, proofs, invariants, traces, and implementation details—not merely supply one-line interview answers. Administrative, repeated title, animation-only, and reference slides are represented in the source matrix rather than repeated as content.

The notation used here is:

- $n=|V|$, $m=|E|$ for a graph unless a section says otherwise.
- $\infty$ is a sentinel larger than every realizable finite answer.
- Directed edge $(u,v)$ has weight $w(u,v)$, capacity $c(u,v)$, or flow $f(u,v)$, according to context.
- “Worst case” is the maximum cost for one input of size $n$; “amortized” is the average cost per operation over a whole sequence, with no probability assumption; “expected” averages over randomness.

## Current source coverage

The reduced source set was re-audited on 24 July 2026. The current DSA-II folder contains **three PDFs / 1,078 pages**:

| Current DSA-II source | Pages | Main material |
|---|---:|---|
| `DSA II.pdf` | 29 | compact syllabus/summary cross-check |
| `Part1merged.pdf` | 630 | graph foundations, MST, shortest paths, APSP, network flow, AVL, red-black, and splay trees |
| `Part2merged.pdf` | 419 | amortized analysis, heaps, hashing, intractability, approximation/exact methods, backtracking, and branch-and-bound |
| **DSA-II total** | **1,078** | **39 low-text/image-heavy pages visually routed** |

Because DSA is the chosen strong subject, the current `461-AE` Algorithm Engineering folder was also mapped into this volume: **seven PDFs / 453 pages**. It reinforces flow, matching, FFT, and NP-completeness and adds stable matching, directed minimum arborescence, and linear-programming ideas. Thus this volume is grounded in **1,531 current algorithm pages**, with overlap between merged/reference material stated rather than double-counted as unique lectures.

String matching remains a syllabus-level topic with little expanded material in the current DSA-II decks; its chapter is retained as an implementable core supplement.

## How to answer an algorithm viva question

Give the answer in this order:

1. **Problem and assumptions** — input, required output, directed/undirected, weighted/unweighted, and restrictions such as “no negative edge.”
2. **Core idea** — one or two sentences.
3. **Invariant** — what remains true after every iteration.
4. **Algorithm or trace** — enough detail that the examiner could implement it.
5. **Correctness** — why the greedy choice, recurrence, or pruning rule cannot lose the answer.
6. **Exact complexity** — name the data structure responsible for it.
7. **Failure mode or alternative** — the usual follow-up question.

For example: “Dijkstra solves single-source shortest paths when every reachable edge has nonnegative weight. It repeatedly settles the unsettled vertex with smallest tentative distance. Once extracted, that distance is final; any alternative path would first cross from a settled to an unsettled vertex and, because the crossing edge is nonnegative, cannot improve it. With an adjacency list and binary heap it is $O((V+E)\log V)$, normally written $O(E\log V)$ for a connected graph. For negative edges I would use Bellman–Ford.”

---

# 1. Analysis, tractability, and lower bounds

## 1.1 What a running-time statement means

An algorithm is normally called **efficient/tractable** when its running time is polynomial in the encoded input length. The distinction is about input length, not the numerical value of an input. An $O(C)$ algorithm is not polynomial when $C$ is written in binary, because its encoding has only $\Theta(\log C)$ bits.

Asymptotic bounds:

- $f(n)=O(g(n))$: there are constants $c,n_0>0$ such that $0\le f(n)\le c g(n)$ for $n\ge n_0$. It is an eventual upper bound.
- $f(n)=\Omega(g(n))$: eventual lower bound.
- $f(n)=\Theta(g(n))$: both.
- $f(n)=o(g(n))$: $f/g\to0$; strictly lower order.
- $f(n)=\omega(g(n))$: $f/g\to\infty$.

Discard constant factors and lower-order terms only after defining the cost model. $O(n)$ arithmetic on unbounded integers is not necessarily $O(n)$ bit time.

Common growth order:

$$
1 < \log n < \sqrt n < n < n\log n < n^2 < n^3 < c^n < n! < n^n
$$

Two practical rules:

- Nested loops do not automatically multiply to the worst visible bounds; count how many times the inner work actually executes.
- A polynomial with a huge exponent can still be unusable, while an exponential algorithm can work for small $n$. “Polynomial” is a structural dividing line, not a stopwatch promise.

## 1.2 Lower bound versus an algorithm’s lower bound

A **problem lower bound** is a bound on every algorithm in a specified computation model. Saying “merge sort is $\Omega(n\log n)$” only describes merge sort. Saying “comparison sorting is $\Omega(n\log n)$” says no comparison-based sorting algorithm can asymptotically beat it in the worst case.

### Decision-tree proof for comparison sorting

For $n$ distinct keys there are $n!$ possible orders. A deterministic comparison algorithm is a binary decision tree:

- one internal node per comparison;
- two outgoing answers;
- at least one leaf per possible input ordering.

A binary tree of height $h$ has at most $2^h$ leaves, so

$$
2^h\ge n!\quad\Rightarrow\quad h\ge\log_2(n!)=\Omega(n\log n).
$$

Stirling’s approximation gives $\log(n!)=n\log n-\Theta(n)$. Therefore merge sort and heap sort are asymptotically optimal **in the comparison model**. Counting/radix sort do not contradict the theorem: they exploit integer structure rather than comparisons alone.

Other useful bounds:

- Finding a maximum needs at least $n-1$ comparisons: every nonmaximum item must lose at least once.
- Finding both minimum and maximum needs at least $\lceil3n/2\rceil-2$ comparisons; compare elements in pairs first.
- Searching an ordered array by comparisons needs $\Omega(\log n)$ worst-case comparisons because there are $n+1$ possible gaps/answers.
- Merely reading an unrestricted array already gives many problems an $\Omega(n)$ bound.

### Reduction as a lower-bound tool

If problem $A$ is already known hard and $A\le_P B$, then an unexpectedly fast algorithm for $B$ would also solve $A$ that fast. The arrow means: **use a solver for $B$ to solve $A$**. Reversing this direction is one of the most common viva mistakes.

---

# 2. Graph foundations

## 2.1 Vocabulary and modeling

A graph is $G=(V,E)$.

- **Undirected:** $\{u,v\}=\{v,u\}$. Degree $\deg(v)$; $\sum_v\deg(v)=2|E|$.
- **Directed:** $(u,v)$ and $(v,u)$ differ. $\sum\text{indeg}=\sum\text{outdeg}=|E|$.
- **Simple graph:** no self-loop and no parallel edge.
- **Walk:** vertices/edges may repeat. **Trail:** no repeated edge. **Path:** no repeated vertex.
- **Cycle:** a closed path, except its first/last vertex coincide.
- **Connected component:** maximal mutually connected set in an undirected graph.
- **Strongly connected component (SCC):** maximal set in which every vertex reaches every other in a digraph.
- **Tree:** connected and acyclic undirected graph. Equivalent facts for $n$ vertices: connected with $n-1$ edges; acyclic with $n-1$ edges; exactly one simple path between each pair.
- **Forest:** disjoint union of trees.
- **DAG:** directed acyclic graph.
- **Bipartite:** vertices split into $L,R$ and every edge crosses the split. An undirected graph is bipartite iff it has no odd cycle.

Model examples:

- routers are vertices and links are edges;
- course prerequisites form a DAG;
- people and friendships form an undirected graph;
- students and courses form a bipartite graph;
- road length is an edge weight, road bandwidth a capacity.

## 2.2 Representations

| Representation | Space | Test $(u,v)$ | Iterate neighbors of $u$ | Best use |
|---|---:|---:|---:|---|
| Adjacency matrix | $\Theta(V^2)$ | $O(1)$ | $O(V)$ | Dense graphs, tiny fixed $V$ |
| Adjacency list | $\Theta(V+E)$ | $O(\deg u)$, or expected $O(1)$ with hash set | $\Theta(\deg u)$ | Sparse graphs and traversal |
| Edge list | $\Theta(E)$ | $O(E)$ | $O(E)$ | Kruskal, input/output, edge scans |

For an undirected adjacency list, store each edge twice, so the total neighbor entries are $2E$. Traversal is still $O(V+E)$.

## 2.3 Breadth-first search

**Purpose.** Reachability and shortest path measured by number of edges in an unweighted graph.

**Invariant.** When a vertex is dequeued, its recorded distance is the minimum number of edges from the source. Vertices are discovered in nondecreasing distance layers.

Why it works: every path to a layer-$k+1$ vertex must come through a layer at least $k$; the FIFO queue processes every layer-$k$ vertex before layer $k+1$.

~~~cpp
vector<int> bfs(const vector<vector<int>>& adj, int s,
                vector<int>& parent) {
    int n = (int)adj.size();
    vector<int> dist(n, -1);
    parent.assign(n, -1);
    queue<int> q;
    dist[s] = 0;                 // Mark at enqueue time, not dequeue time.
    q.push(s);

    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : adj[u]) {
            if (dist[v] == -1) {
                dist[v] = dist[u] + 1;
                parent[v] = u;
                q.push(v);
            }
        }
    }
    return dist;
}
~~~

To reconstruct an $s$-to-$t$ path, follow parent pointers from $t$ back to $s$, then reverse. Distance $-1$ means unreachable.

Complexity:

- adjacency list: $O(V+E)$ time, $O(V)$ auxiliary space;
- adjacency matrix: $O(V^2)$ time.

Common mistakes:

- marking only on dequeue can enqueue one vertex many times;
- ordinary BFS does not minimize weighted distance;
- multi-source BFS is obtained by initially enqueueing all sources at distance 0;
- a directed BFS follows only outgoing edges.

### Bipartite test

BFS/DFS two-colors each component. Give an undiscovered neighbor the opposite color; an edge whose endpoints have the same color proves an odd cycle.

~~~cpp
bool isBipartite(const vector<vector<int>>& adj) {
    int n = adj.size();
    vector<int> color(n, -1);
    for (int s = 0; s < n; ++s) if (color[s] == -1) {
        queue<int> q;
        color[s] = 0; q.push(s);
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (int v : adj[u]) {
                if (color[v] == -1) {
                    color[v] = color[u] ^ 1;
                    q.push(v);
                } else if (color[v] == color[u]) {
                    return false;
                }
            }
        }
    }
    return true;
}
~~~

## 2.4 Depth-first search

DFS follows one unfinished branch as deeply as possible, then backtracks.

~~~cpp
struct DFSInfo {
    vector<int> parent, discover, finish;
    vector<char> color;          // 0 white, 1 gray, 2 black
    int timer = 0;

    void visit(int u, const vector<vector<int>>& adj) {
        color[u] = 1;
        discover[u] = ++timer;
        for (int v : adj[u]) {
            if (color[v] == 0) {
                parent[v] = u;
                visit(v, adj);
            }
        }
        color[u] = 2;
        finish[u] = ++timer;
    }

    void run(const vector<vector<int>>& adj) {
        int n = adj.size();
        parent.assign(n, -1);
        discover.assign(n, 0);
        finish.assign(n, 0);
        color.assign(n, 0);
        for (int u = 0; u < n; ++u)
            if (color[u] == 0) visit(u, adj);
    }
};
~~~

Time is $O(V+E)$ with lists, stack/recursion space $O(V)$.

Important timestamp facts:

- $d[u] < f[u]$.
- Intervals $[d[u],f[u]]$ and $[d[v],f[v]]$ are nested exactly when one is a DFS ancestor of the other; otherwise they are disjoint. This is the **parenthesis theorem**.
- A vertex $v$ is a descendant of $u$ in the DFS forest iff, at discovery of $u$, there is a path from $u$ to $v$ containing only white vertices (**white-path theorem**).

Directed DFS edge classification:

- tree: first discovers $v$;
- back: points to a gray ancestor; a directed graph has a cycle iff DFS finds a back edge;
- forward: points to a proper black descendant but is not a tree edge;
- cross: any other black endpoint.

For an undirected graph, ignore the edge back to the parent; any edge to another already visited vertex proves a cycle.

### Topological sort

A topological order lists every edge $u\to v$ with $u$ before $v$. It exists iff the graph is a DAG.

DFS method: reject on a gray-to-gray back edge; append a vertex when it finishes; reverse the finish list. Correctness: in a DAG, every edge satisfies $f[u]>f[v]$, so decreasing finish time places $u$ before $v$.

Kahn’s method repeatedly removes indegree-zero vertices:

~~~cpp
vector<int> topoSort(const vector<vector<int>>& adj) {
    int n = adj.size();
    vector<int> indeg(n), order;
    for (int u = 0; u < n; ++u)
        for (int v : adj[u]) ++indeg[v];
    queue<int> q;
    for (int v = 0; v < n; ++v) if (indeg[v] == 0) q.push(v);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        order.push_back(u);
        for (int v : adj[u]) if (--indeg[v] == 0) q.push(v);
    }
    if ((int)order.size() != n) return {}; // cycle
    return order;
}
~~~

Both methods are $O(V+E)$. The order need not be unique; it is unique exactly when Kahn’s queue has one choice at every step.

## 2.5 Strongly connected components

Collapsing every SCC into one meta-vertex produces the **condensation graph**, which is always a DAG.

Kosaraju:

1. DFS $G$ and record decreasing finish order.
2. Reverse every edge to obtain $G^T$.
3. DFS $G^T$ in that order; each DFS tree is one SCC.

Why the second pass does not leak: in the condensation DAG, the first pass’s largest finishing SCC behaves as a source for the transpose pass; a DFS from it in $G^T$ cannot reach an unassigned SCC. Repeating peels SCCs one at a time.

~~~cpp
void dfsOrder(int u, const vector<vector<int>>& g,
              vector<char>& seen, vector<int>& order) {
    seen[u] = true;
    for (int v : g[u]) if (!seen[v]) dfsOrder(v, g, seen, order);
    order.push_back(u);
}

void dfsComponent(int u, const vector<vector<int>>& gt, int id,
                  vector<int>& comp) {
    comp[u] = id;
    for (int v : gt[u]) if (comp[v] == -1)
        dfsComponent(v, gt, id, comp);
}

vector<int> kosaraju(const vector<vector<int>>& g) {
    int n = g.size();
    vector<vector<int>> gt(n);
    for (int u = 0; u < n; ++u)
        for (int v : g[u]) gt[v].push_back(u);
    vector<char> seen(n);
    vector<int> order;
    for (int u = 0; u < n; ++u)
        if (!seen[u]) dfsOrder(u, g, seen, order);
    reverse(order.begin(), order.end());
    vector<int> comp(n, -1);
    int id = 0;
    for (int u : order)
        if (comp[u] == -1) dfsComponent(u, gt, id++, comp);
    return comp;
}
~~~

Time $O(V+E)$, space $O(V+E)$. Tarjan’s low-link algorithm also runs in one DFS and $O(V+E)$, but Kosaraju matches the lecture progression more directly.

---

# 3. Disjoint sets and minimum spanning trees

## 3.1 Disjoint-set union (union–find)

DSU maintains a partition under:

- make-set;
- find: representative of an element’s set;
- union: merge two sets.

Use **union by rank/size** and **path compression** together:

~~~cpp
struct DSU {
    vector<int> p, sz;
    explicit DSU(int n) : p(n), sz(n, 1) {
        iota(p.begin(), p.end(), 0);
    }
    int find(int x) {
        return p[x] == x ? x : p[x] = find(p[x]);
    }
    bool unite(int a, int b) {
        a = find(a); b = find(b);
        if (a == b) return false;
        if (sz[a] < sz[b]) swap(a, b);
        p[b] = a;
        sz[a] += sz[b];
        return true;
    }
};
~~~

A sequence of $M$ operations on $n$ elements takes $O(M\alpha(n))$, where inverse Ackermann $\alpha$ is below 5 for any practical input. This is amortized, not a claim that each individual operation is worst-case constant.

## 3.2 MST definitions and facts

For a connected, undirected, weighted graph, a **minimum spanning tree** (MST) is a spanning tree with minimum total edge weight.

- Negative edges are fine.
- If the graph is disconnected, the algorithms produce a minimum spanning forest.
- Distinct edge weights imply a unique MST; equal weights may still happen to have a unique MST.
- An MST minimizes total tree weight, not the path distance between every pair; shortest-path trees and MSTs solve different objectives.

A **cut** $(S,V-S)$ partitions vertices. An edge crosses it if its endpoints are on opposite sides.

**Cut property.** A lightest edge crossing any cut that respects a partial MST forest is safe to add. Exchange proof: take an MST $T$. If it lacks light edge $e$, adding $e$ creates a cycle containing some other crossing edge $f$. Since $w(e)\le w(f)$, replace $f$ by $e$; the result is no heavier and remains a tree.

**Cycle property.** A strictly heaviest edge on a cycle belongs to no MST. If an MST used it, replace it by a lighter edge from the same cycle.

These are the correctness engines behind Kruskal, Prim, and reverse-delete.

## 3.3 Kruskal

Sort edges from light to heavy and add an edge iff it connects two different components.

~~~cpp
struct WEdge { int u, v; long long w; };

pair<long long, vector<WEdge>>
kruskal(int n, vector<WEdge> edges) {
    sort(edges.begin(), edges.end(),
         [](const WEdge& a, const WEdge& b) { return a.w < b.w; });
    DSU dsu(n);
    long long total = 0;
    vector<WEdge> chosen;
    for (const auto& e : edges) {
        if (dsu.unite(e.u, e.v)) { // equivalent to find(u) != find(v)
            chosen.push_back(e);
            total += e.w;
            if ((int)chosen.size() == n - 1) break;
        }
    }
    if ((int)chosen.size() != n - 1)
        throw runtime_error("graph is disconnected");
    return {total, chosen};
}
~~~

The set test must be unequal representatives. One compact slide version accidentally suggests the opposite; that would deliberately create cycles.

Invariant: chosen edges are a forest extendible to some MST. The next accepted edge is lightest across the cut defined by two current components, so the cut property makes it safe.

Complexity:

- sorting: $O(E\log E)=O(E\log V)$ for a simple graph;
- DSU: $O(E\alpha(V))$;
- total: $O(E\log E)$.

With small bounded integer weights, counting/radix sorting can reduce sorting, potentially to $O(E)$.

### Tiny trace

Edges $AB:1, BC:2, AC:3, CD:4, BD:5$:

1. accept $AB$;
2. accept $BC$;
3. reject $AC$ because $A,C$ are already connected;
4. accept $CD$.  
The MST weight is $1+2+4=7$.

## 3.4 Prim

Prim grows one tree. For each outside vertex $v$, its key is the lightest edge connecting it to the current tree.

~~~cpp
pair<long long, vector<int>>
prim(const vector<vector<pair<int,int>>>& adj, int start = 0) {
    int n = adj.size();
    const long long INF = numeric_limits<long long>::max()/4;
    vector<long long> key(n, INF);
    vector<int> parent(n, -1);
    vector<char> used(n);
    using State = pair<long long,int>;
    priority_queue<State, vector<State>, greater<State>> pq;
    key[start] = 0;
    pq.push({0, start});
    long long total = 0;
    int taken = 0;

    while (!pq.empty()) {
        auto [ku, u] = pq.top(); pq.pop();
        if (used[u] || ku != key[u]) continue; // stale lazy-heap entry
        used[u] = true;
        total += ku;
        ++taken;
        for (auto [v, w] : adj[u]) {
            if (!used[v] && w < key[v]) {
                key[v] = w;
                parent[v] = u;
                pq.push({key[v], v});
            }
        }
    }
    if (taken != n) throw runtime_error("graph is disconnected");
    return {total, parent};
}
~~~

Invariant: vertices already extracted form a tree contained in an MST; every outside key is the cheapest crossing edge currently known. The extracted minimum is globally lightest across the tree/outside cut and is safe.

Complexity:

- adjacency matrix + array minimum: $O(V^2)$, often best for dense graphs;
- adjacency list + binary heap: $O((V+E)\log V)$, written $O(E\log V)$ for connected graphs;
- Fibonacci heap: $O(E+V\log V)$ amortized because decrease-key is $O(1)$ amortized.

**Lazy Prim** stores candidate edges and skips obsolete entries; **eager Prim** stores one best key per outside vertex. The code above is eager logically but uses duplicate heap entries as a practical substitute for decrease-key.

## 3.5 Reverse-delete and clustering

Reverse-delete sorts edges from heavy to light and deletes an edge if the graph remains connected. By the cycle property, any deleted edge is a heaviest edge on some cycle and is unnecessary. A naive connectivity test per edge costs $O(E(V+E))$; specialized dynamic connectivity gives better theoretical bounds. Kruskal is normally simpler.

For **maximum-spacing $k$-clustering**, run Kruskal but stop when exactly $k$ components remain. The next edge that would connect two components has the maximum possible spacing. The exchange argument is the same cut-property reasoning.

## 3.6 MST comparison viva table

| Question | Kruskal | Prim |
|---|---|---|
| Grows | forest of components | one tree |
| Main structure | sorted edge list + DSU | adjacency structure + min-PQ |
| Sparse graph | excellent | excellent |
| Dense matrix graph | sorting all edges less attractive | $O(V^2)$ version excellent |
| Directed graph | not an ordinary MST problem | not an ordinary MST problem |
| Negative weights | allowed | allowed |
| Disconnected input | minimum spanning forest | restart per component for a forest |

---

# 4. Single-source shortest paths

## 4.1 Definitions and relaxation

For a path $p=\langle v_0,\ldots,v_k\rangle$,

$$
w(p)=\sum_{i=1}^{k}w(v_{i-1},v_i).
$$

The shortest-path distance $\delta(s,v)$ is the minimum path weight from $s$ to $v$, or $\infty$ if unreachable. If a reachable negative-weight cycle can lead to $v$, there is no finite minimum: walks can loop around the cycle to decrease weight without bound.

Core facts:

- **Optimal substructure:** every subpath of a shortest path is itself shortest between its endpoints.
- **Triangle inequality:** $\delta(s,v)\le\delta(s,u)+w(u,v)$.
- A shortest simple path has at most $V-1$ edges when no reachable negative cycle is relevant.

Initialize

$$
d[s]=0,\qquad d[v]=\infty\ (v\ne s),\qquad \pi[v]=\text{NIL}.
$$

Relaxation tests whether going through $u$ improves $v$:

~~~cpp
bool relax(int u, int v, long long w,
           vector<long long>& d, vector<int>& parent) {
    const long long INF = numeric_limits<long long>::max()/4;
    if (d[u] == INF || d[v] <= d[u] + w) return false;
    d[v] = d[u] + w;
    parent[v] = u;
    return true;
}
~~~

Relaxation never makes a tentative distance smaller than the true shortest distance if initialization was correct. Once a shortest path’s edges have been relaxed in order, its destination has the correct distance.

## 4.2 Shortest paths in a DAG

Topologically sort the DAG, then relax every outgoing edge in that order. Every predecessor of $v$ is handled before $v$, so when $v$ is reached all possible last edges into it have been considered.

~~~cpp
vector<long long> dagShortestPaths(
    const vector<vector<pair<int,int>>>& adj, int s,
    const vector<int>& topo) {
    const long long INF = numeric_limits<long long>::max()/4;
    vector<long long> d(adj.size(), INF);
    vector<int> parent(adj.size(), -1);
    d[s] = 0;
    for (int u : topo) {
        if (d[u] == INF) continue;
        for (auto [v, w] : adj[u])
            relax(u, v, w, d, parent);
    }
    return d;
}
~~~

Time $O(V+E)$. Negative edges are allowed because a DAG cannot contain a cycle.

## 4.3 Dijkstra

**Assumption:** every edge reachable from $s$ has $w(e)\ge0$. Zero is fine; one negative edge invalidates the greedy proof even if a particular run happens to return the right answer.

Algorithm: keep tentative distances in a min-priority queue. Extract the unsettled vertex of least distance and relax its outgoing edges.

~~~cpp
vector<long long> dijkstra(
    const vector<vector<pair<int,int>>>& adj, int s,
    vector<int>& parent) {
    const long long INF = numeric_limits<long long>::max()/4;
    int n = adj.size();
    vector<long long> d(n, INF);
    parent.assign(n, -1);
    using State = pair<long long,int>;
    priority_queue<State, vector<State>, greater<State>> pq;
    d[s] = 0;
    pq.push({0, s});

    while (!pq.empty()) {
        auto [du, u] = pq.top(); pq.pop();
        if (du != d[u]) continue; // stale entry
        for (auto [v, w] : adj[u]) {
            if (w < 0) throw invalid_argument("Dijkstra needs nonnegative edges");
            if (d[v] > du + w) {
                d[v] = du + w;
                parent[v] = u;
                pq.push({d[v], v});
            }
        }
    }
    return d;
}
~~~

**Settling invariant.** When $u$ is extracted with minimum tentative distance, $d[u]=\delta(s,u)$.

Proof by contradiction: suppose the true shortest path to $u$ first leaves settled set $S$ on edge $(x,y)$. Then $x\in S$, so that edge has already been relaxed and $d[y]\le\delta(s,y)\le\delta(s,u)$, since all remaining edges are nonnegative. The queue chose $u$, so $d[u]\le d[y]$. Together with $d[u]\ge\delta(s,u)$, equality follows.

The slide trace on the standard $s,t,x,y,z$ example settles distances:

$$
d(s)=0,\quad d(y)=5,\quad d(z)=7,\quad d(t)=8,\quad d(x)=9.
$$

Complexity:

- array / adjacency matrix: $O(V^2)$;
- adjacency list + binary heap: $O((V+E)\log V)$;
- Fibonacci heap: $O(E+V\log V)$ amortized.

Do not mark a vertex “final” when first inserted. A later relaxation may improve it; it becomes final only when the current minimum entry is extracted.

## 4.4 Bellman–Ford

Bellman–Ford permits negative edges and detects a **reachable** negative cycle.

~~~cpp
struct BFEdge { int u, v; long long w; };

bool bellmanFord(int n, const vector<BFEdge>& edges, int s,
                 vector<long long>& d, vector<int>& parent) {
    const long long INF = numeric_limits<long long>::max()/4;
    d.assign(n, INF);
    parent.assign(n, -1);
    d[s] = 0; // Do this after initializing all vertices.

    for (int pass = 1; pass <= n - 1; ++pass) {
        bool changed = false;
        for (auto [u, v, w] : edges) {
            if (d[u] != INF && d[v] > d[u] + w) {
                d[v] = d[u] + w;
                parent[v] = u;
                changed = true;
            }
        }
        if (!changed) break;
    }
    for (auto [u, v, w] : edges)
        if (d[u] != INF && d[v] > d[u] + w)
            return false; // reachable negative cycle
    return true;
}
~~~

Invariant after pass $i$: every shortest path using at most $i$ edges has been found. A finite shortest simple path uses at most $V-1$ edges, hence $V-1$ passes suffice. Any further improvement proves a reachable negative cycle.

Time $O(VE)$, space $O(V)$ beyond the edge list. Early termination improves easy instances but not the worst-case bound.

To recover an actual negative cycle, remember a vertex relaxed on the $V$-th pass, follow parent pointers $V$ times to enter the cycle, then follow parents until it repeats.

## 4.5 Which SSSP algorithm?

| Situation | Algorithm | Time |
|---|---|---:|
| Unweighted / equal weights | BFS | $O(V+E)$ |
| DAG, even negative edges | topological relaxation | $O(V+E)$ |
| Nonnegative weights | Dijkstra | $O(E\log V)$ with binary heap |
| Negative edges, no reachable negative cycle | Bellman–Ford | $O(VE)$ |
| Weights only 0 or 1 | 0–1 BFS with deque | $O(V+E)$ |

An MST does not answer SSSP: the globally cheapest tree may omit a direct edge needed for a shortest route from one source.

---

# 5. All-pairs shortest paths

## 5.1 Baselines and min-plus multiplication

Running Bellman–Ford from every source costs $O(V^2E)$. Repeated Dijkstra costs $O(VE\log V)$ with binary heaps but requires nonnegative edges. Johnson preserves that speed while allowing negative edges and no negative cycles.

Let matrix $W$ contain edge weights, with $W[i][i]=0$, $W[i][j]=\infty$ when no edge exists. Define min-plus product:

$$
(A\otimes B)[i,j]=\min_k\{A[i,k]+B[k,j]\}.
$$

If $L^{(r)}[i,j]$ is the shortest $i$-to-$j$ path using at most $r$ edges, then

$$
L^{(r)}=L^{(r-1)}\otimes W.
$$

Sequential extension to $V-1$ edges costs $O(V^4)$. Repeated squaring reaches path lengths $1,2,4,\ldots$ in $O(V^3\log V)$. The compact slide’s two similar matrix routines are easy to confuse: extension by $W$ increments the edge allowance; squaring $L\otimes L$ doubles it.

## 5.2 Floyd–Warshall

Define $D^{(k)}[i,j]$ as the shortest path from $i$ to $j$ whose internal vertices are drawn only from $\{1,\ldots,k\}$. Either the path avoids $k$, or it passes through $k$:

$$
D^{(k)}[i,j]=\min\left(D^{(k-1)}[i,j],
D^{(k-1)}[i,k]+D^{(k-1)}[k,j]\right).
$$

~~~cpp
vector<vector<long long>>
floydWarshall(vector<vector<long long>> d) {
    const long long INF = numeric_limits<long long>::max()/4;
    int n = d.size();
    for (int i = 0; i < n; ++i) d[i][i] = min(d[i][i], 0LL);
    for (int k = 0; k < n; ++k)
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < n; ++j)
                if (d[i][k] != INF && d[k][j] != INF)
                    d[i][j] = min(d[i][j], d[i][k] + d[k][j]);
    return d;
}
~~~

The loop order must have $k$ outermost. A compact slide uses inconsistent indices in the conditional; the correct update is $d[i][j]$ against $d[i][k]+d[k][j]$.

Time $O(V^3)$, space $O(V^2)$. Afterward, any $d[i][i]<0$ signals a negative cycle reachable from and back to $i$.

Path reconstruction: maintain `next[i][j]=j` for an original edge. Whenever route through $k$ improves $(i,j)$, set `next[i][j]=next[i][k]`; repeatedly follow next until $j$.

For transitive closure, replace min by OR and addition by AND:

$$
reach[i][j]\leftarrow reach[i][j]\lor
(reach[i][k]\land reach[k][j]).
$$

## 5.3 Johnson’s algorithm

Johnson handles sparse directed graphs with negative edges but no negative cycle.

1. Add new source $q$ and zero-weight edge $q\to v$ for every original vertex.
2. Run Bellman–Ford from $q$. If it detects a negative cycle, stop.
3. Let potential $h(v)=\delta(q,v)$.
4. Reweight every original edge:

$$
w'(u,v)=w(u,v)+h(u)-h(v).
$$

5. Run Dijkstra from every original source using $w'$.
6. Convert answers back:

$$
\delta(u,v)=\delta'(u,v)-h(u)+h(v).
$$

The signs matter. Several shorthand notes are easy to miscopy; these are the correct two formulas.

Why all reweighted edges are nonnegative:

$$
h(v)\le h(u)+w(u,v)
\Rightarrow w(u,v)+h(u)-h(v)\ge0.
$$

Why shortest paths are preserved: for a path $p=u=v_0,\ldots,v_k=v$, potentials telescope:

$$
w'(p)=w(p)+h(u)-h(v).
$$

Every $u$-to-$v$ path gets the same endpoint-dependent offset, so their ordering is unchanged.

Complexity:

- Bellman–Ford: $O(VE)$;
- $V$ binary-heap Dijkstra runs: $O(VE\log V)$;
- commonly stated as $O(VE+V^2\log V)$ with Fibonacci heaps, or $O(VE\log V)$ with binary heaps on sparse graphs;
- space $O(V+E)$ plus the $O(V^2)$ output if all distances are stored.

## 5.4 Difference constraints

A system

$$
x_j-x_i\le b
$$

becomes edge $i\to j$ of weight $b$. Add a zero-edge source to every variable and run Bellman–Ford. If there is no negative cycle, shortest-path labels form a feasible assignment because

$$
d[j]\le d[i]+b\Rightarrow d[j]-d[i]\le b.
$$

A negative cycle is a certificate that the constraints are inconsistent.

---

# 6. Network flow

## 6.1 Flow, capacity, value, and cut

A flow network $G=(V,E,s,t,c)$ is directed, has source $s$, sink $t$, and nonnegative capacities.

A feasible $s$-$t$ flow satisfies:

1. **Capacity:** $0\le f(u,v)\le c(u,v)$.
2. **Conservation:** for every $v\notin\{s,t\}$,

$$
\sum_{(u,v)\in E}f(u,v)=\sum_{(v,w)\in E}f(v,w).
$$

Flow value is net flow leaving the source:

$$
|f|=\sum_{(s,v)}f(s,v)-\sum_{(v,s)}f(v,s).
$$

An $s$-$t$ cut $(A,B)$ partitions $V$, with $s\in A,t\in B$. Its capacity counts only original forward edges from $A$ to $B$:

$$
c(A,B)=\sum_{u\in A,v\in B}c(u,v).
$$

**Do not confuse network-flow control with transport-layer flow control.** Here flow is a mathematical assignment on graph edges. TCP flow control prevents a sender from overflowing a receiver’s buffer.

## 6.2 Residual network and why naive greedy fails

Sending flow on a path and never revising it can make an early bad choice. The residual network supplies the “undo” mechanism.

For an original edge $u\to v$:

- forward residual capacity is $c_f(u,v)=c(u,v)-f(u,v)$;
- reverse residual capacity is $c_f(v,u)=f(u,v)$.

Traversing a reverse residual edge subtracts previously sent flow on its corresponding original edge. Residual edges with zero capacity are omitted.

An **augmenting path** is an $s$-to-$t$ path in the residual graph. Its bottleneck is the minimum residual capacity on it. Augment every path edge by that bottleneck—adding on forward edges, subtracting on reverse edges.

## 6.3 Ford–Fulkerson and the max-flow/min-cut theorem

Ford–Fulkerson is a method rather than one fixed path-selection algorithm:

~~~text
set every flow to 0
while residual graph has an s-to-t path P:
    delta = minimum residual capacity on P
    augment delta along P
return flow
~~~

### Flow-value lemma and weak duality

For every flow $f$ and cut $(A,B)$,

$$
|f|=f(A,B)-f(B,A)\le c(A,B).
$$

The equality follows by summing flow conservation over vertices of $A$: internal flows cancel, leaving net flow across the cut. Capacity and nonnegativity yield the inequality. Thus **every flow value is at most every cut capacity**.

### Equivalence theorem

For a feasible flow $f$, these are equivalent:

1. there is a cut whose capacity equals $|f|$;
2. $f$ is maximum;
3. the residual graph has no augmenting path.

The nontrivial direction is 3 $\Rightarrow$ 1. Let $A$ be vertices reachable from $s$ in the residual graph and $B=V-A$. Since $t\notin A$:

- every original edge from $A$ to $B$ is saturated, or it would be residual;
- every original edge from $B$ to $A$ carries zero flow, or its reverse would be residual.

Therefore $|f|=c(A,B)$. Weak duality makes both optimal. This proves the **max-flow/min-cut theorem** and gives an $O(E)$ way to recover a minimum cut after max flow: one residual DFS/BFS from $s$.

### Integrality and generic complexity

With integer capacities, every bottleneck and resulting flow remains integer. Ford–Fulkerson then terminates after at most $|f^*|$ augmentations and costs $O(E|f^*|)$. It is **pseudo-polynomial**, because $|f^*|$ can be exponential in the number of bits used to encode capacities. With irrational capacities, adversarial path choices can even fail to terminate or converge to the maximum.

## 6.4 Edmonds–Karp

Edmonds–Karp is Ford–Fulkerson with BFS choosing a residual path with the fewest edges.

~~~cpp
struct FlowEdge {
    int to, rev;
    long long cap; // current residual capacity
};

struct EdmondsKarp {
    int n;
    vector<vector<FlowEdge>> g;
    explicit EdmondsKarp(int n) : n(n), g(n) {}

    void addEdge(int u, int v, long long c) {
        FlowEdge a{v, (int)g[v].size(), c};
        FlowEdge b{u, (int)g[u].size(), 0};
        g[u].push_back(a);
        g[v].push_back(b);
    }

    long long maxFlow(int s, int t) {
        long long answer = 0;
        while (true) {
            vector<int> pv(n, -1), pe(n, -1);
            queue<int> q;
            q.push(s); pv[s] = s;
            while (!q.empty() && pv[t] == -1) {
                int u = q.front(); q.pop();
                for (int i = 0; i < (int)g[u].size(); ++i) {
                    if (g[u][i].cap > 0 && pv[g[u][i].to] == -1) {
                        pv[g[u][i].to] = u;
                        pe[g[u][i].to] = i;
                        q.push(g[u][i].to);
                    }
                }
            }
            if (pv[t] == -1) break;

            long long add = numeric_limits<long long>::max();
            for (int v = t; v != s; v = pv[v])
                add = min(add, g[pv[v]][pe[v]].cap);
            for (int v = t; v != s; v = pv[v]) {
                FlowEdge& e = g[pv[v]][pe[v]];
                e.cap -= add;
                g[v][e.rev].cap += add;
            }
            answer += add;
        }
        return answer;
    }
};
~~~

For parallel edges, call add-edge separately. For an undirected capacity edge, add two independent directed capacity edges; do not mistake a residual reverse edge for an original opposite-capacity edge.

### Why Edmonds–Karp is $O(VE^2)$

1. One BFS plus augmentation costs $O(E)$.
2. Residual shortest-path distances from $s$ never decrease after a BFS augmentation.
3. Every augmentation saturates at least one **critical** directed residual edge $(u,v)$ on a shortest path, so $d(v)=d(u)+1$.
4. Before that same directed edge can become critical again, flow must first be sent through its reverse $(v,u)$. At that later time the level relation for the reverse gives $d_{\text{later}}(u)=d_{\text{later}}(v)+1$.
5. Since levels never decrease,

$$
d_{\text{later}}(u)\ge d_{\text{earlier}}(v)+1
=d_{\text{earlier}}(u)+2.
$$

Thus each directed edge can be critical only $O(V)$ times. There are $O(E)$ residual edge directions, hence $O(VE)$ augmentations. Multiply by $O(E)$ per BFS/augmentation:

$$
O(VE)\cdot O(E)=O(VE^2).
$$

This bound is independent of capacity magnitudes and therefore polynomial in encoded input size.

## 6.5 Capacity scaling

Let $C$ be the largest integer capacity. Start $\Delta$ as the largest power of two at most $C$. During a $\Delta$-phase, use only residual edges of capacity at least $\Delta$; exhaust such paths, then halve $\Delta$.

There are $1+\lfloor\log_2 C\rfloor$ phases. At the start of a phase the remaining possible improvement is at most $2E\Delta$, while each augmentation adds at least $\Delta$, so there are $O(E)$ augmentations per phase. With $O(E)$ path search:

$$
O(E^2\log C).
$$

At $\Delta=1$, integer residual capacities mean the restricted residual graph equals the full positive residual graph, so no path implies maximum flow.

## 6.6 Dinic’s algorithm

Dinic uses a BFS **level graph** and sends a **blocking flow** through edges satisfying

$$
level[v]=level[u]+1.
$$

A blocking flow saturates at least one edge on every $s$-to-$t$ path in the current level graph. Then the next BFS shortest residual path is strictly longer.

~~~cpp
struct Dinic {
    struct Edge { int to, rev; long long cap; };
    int n;
    vector<vector<Edge>> g;
    vector<int> level, it;
    explicit Dinic(int n) : n(n), g(n), level(n), it(n) {}

    void addEdge(int u, int v, long long c) {
        Edge a{v, (int)g[v].size(), c};
        Edge b{u, (int)g[u].size(), 0};
        g[u].push_back(a); g[v].push_back(b);
    }
    bool bfs(int s, int t) {
        fill(level.begin(), level.end(), -1);
        queue<int> q; q.push(s); level[s] = 0;
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (const Edge& e : g[u])
                if (e.cap > 0 && level[e.to] == -1) {
                    level[e.to] = level[u] + 1;
                    q.push(e.to);
                }
        }
        return level[t] != -1;
    }
    long long dfs(int u, int t, long long pushed) {
        if (u == t || pushed == 0) return pushed;
        for (int& i = it[u]; i < (int)g[u].size(); ++i) {
            Edge& e = g[u][i];
            if (e.cap <= 0 || level[e.to] != level[u] + 1) continue;
            long long send = dfs(e.to, t, min(pushed, e.cap));
            if (send) {
                e.cap -= send;
                g[e.to][e.rev].cap += send;
                return send;
            }
        }
        return 0;
    }
    long long maxFlow(int s, int t) {
        long long flow = 0, INF = numeric_limits<long long>::max()/4;
        while (bfs(s, t)) {
            fill(it.begin(), it.end(), 0);
            while (long long pushed = dfs(s, t, INF)) flow += pushed;
        }
        return flow;
    }
};
~~~

The lecture’s advance–retreat presentation constructs the same blocking-flow idea: advance along a level edge, augment at $t$, delete saturated edges, and retreat/delete a vertex that cannot advance.

General bound in the slides: at most $V-1$ phases, $O(EV)$ per phase in the basic analysis, hence $O(EV^2)$. The standard current-edge DFS implementation above has the familiar $O(V^2E)$ general bound. In a simple unit-capacity network, the Even–Tarjan analysis gives $O(E\sqrt V)$, which yields the same bound for bipartite matching networks.

## 6.7 Bipartite matching and Hall’s theorem

For bipartite $G=(L\cup R,E)$:

1. add source $s$, with capacity-1 edge to every $u\in L$;
2. direct every original edge $L\to R$, capacity 1;
3. add every $v\in R\to t$, capacity 1.

An integral flow of value $k$ corresponds exactly to a matching of size $k$: choose the $L\to R$ edges carrying one unit. Capacity 1 prevents either endpoint from being used twice.

**Hall’s marriage theorem.** When $|L|=|R|$, a perfect matching exists iff for every $S\subseteq L$,

$$
|N(S)|\ge|S|.
$$

Necessity: distinct vertices of $S$ need distinct partners. Sufficiency follows from min cut: if no perfect matching exists, a minimum cut below $|L|$ exposes some $S$ with too few neighbors.

Running times:

- repeated ordinary augmenting paths: $O(EV)$;
- unit-network Dinic / Hopcroft–Karp idea: $O(E\sqrt V)$.

## 6.8 Disjoint paths and Menger

Give every original edge unit capacity. An integral flow of value $k$ decomposes into $k$ edge-disjoint $s$-$t$ paths (cycles can be discarded), and $k$ edge-disjoint paths give a value-$k$ flow.

Therefore:

$$
\max\{\text{edge-disjoint }s\text{-}t\text{ paths}\}
=\min\{\text{edges whose deletion separates }s,t\}.
$$

This is the edge version of Menger’s theorem and is directly max-flow/min-cut. For internally vertex-disjoint paths, split each vertex $v\ne s,t$ into $v_{in}\to v_{out}$ of capacity 1.

## 6.9 Circulation, demands, and lower bounds

For circulation with vertex demand $d(v)$, use the slide convention:

$$
\text{inflow}(v)-\text{outflow}(v)=d(v),
$$

so $d(v)>0$ is demand and $d(v)<0$ is supply. A necessary condition is total demand = total supply.

Reduction:

- add super-source $s'\to v$ of capacity $-d(v)$ for each supply vertex;
- add $v\to t'$ of capacity $d(v)$ for each demand vertex;
- a feasible circulation exists iff a max flow saturates every new source/sink edge, i.e. has value equal to total demand.

For an edge lower bound $\ell(u,v)\le f(u,v)\le c(u,v)$, first commit $\ell(u,v)$. Replace its residual capacity by $c-\ell$ and adjust endpoint balances:

- tail $u$ has already sent $\ell$, so its required net balance changes accordingly;
- head $v$ has already received $\ell$.

Then solve the induced demand-circulation instance. Integer data give an integer feasible circulation by max-flow integrality.

## 6.10 Flow applications from the slides

### Survey design

Use circulation with lower/upper bounds to enforce how many questions each customer answers and how many responses each product receives. Feasibility means all survey quotas can be met simultaneously.

### Foreground/background image segmentation

Create one vertex per pixel, source = foreground, sink = background:

- source/pixel and pixel/sink capacities encode the cost of assigning that pixel to the opposite label;
- antiparallel neighbor edges of capacity $p_{ij}$ penalize separating similar adjacent pixels.

An $s$-$t$ minimum cut selects the labeling minimizing unary assignment costs plus boundary disagreement costs.

### Project selection with prerequisites

Each project has profit $p_v$, possibly negative. Add:

- $s\to v$ of capacity $p_v$ for positive-profit projects;
- $v\to t$ of capacity $-p_v$ for negative-profit projects;
- infinite-capacity $v\to w$ if selecting $v$ requires $w$.

The source side of a finite minimum cut is prerequisite-closed. Minimizing lost positive profit plus accepted negative cost is equivalent to maximizing selected total profit.

### Baseball elimination

For candidate team $z$, assume it wins all remaining games. Add:

- source to each remaining game node $x\!-\!y$, capacity = games left between them;
- game node to team nodes $x,y$, infinite capacity;
- team $x$ to sink, capacity $w_z+r_z-w_x$.

Team $z$ is not eliminated iff all source/game edges can be saturated. A minimum cut also yields a subset of teams certifying elimination, not merely a yes/no answer.

### $k$-regular bipartite graphs and matrix rounding

- Every $k$-regular bipartite graph has a perfect matching: send $1/k$ on every middle edge to obtain a value-$n$ fractional flow; integrality guarantees an integral matching.
- Feasible rounding of a real matrix and its row/column sums is modeled as circulation with floor/ceiling lower and upper bounds. The original real matrix is feasible; integrality supplies consistent integer rounding.

## 6.11 Flow viva traps

- A cut’s capacity counts edges $A\to B$, not $B\to A$.
- Flow value is net source outflow, not the sum over all edges.
- A reverse residual edge represents cancellation; it need not exist in the original network.
- “No augmenting path” proves maximum; “no path made of unsaturated original forward edges” does not.
- Generic Ford–Fulkerson is not automatically polynomial; Edmonds–Karp is.
- Max-flow value equals min-cut **capacity**, not necessarily number of cut edges unless all capacities are 1.

---

# 7. Search trees: BST baseline, predecessor, and successor

## 7.1 Binary-search-tree invariant

For every node $x$:

- every key in its left subtree is less than $x.key$;
- every key in its right subtree is greater than $x.key$.

If duplicates are allowed, choose and document one consistent policy, such as store a multiplicity counter or send equal keys right. Rotations preserve in-order key order and therefore preserve this invariant.

Search, insert, minimum, maximum, predecessor, successor, and delete cost $O(h)$, where $h$ is tree height. A balanced tree has $h=\Theta(\log n)$; an ordinary BST can become a length-$n$ chain.

### Example used throughout

~~~text
                 20
              /      \
            10        30
           /  \      /  \
          5   15    25   40
             /  \
            13  17
~~~

Its in-order sequence is

$$
5,10,13,15,17,20,25,30,40.
$$

## 7.2 Predecessor and successor

The **predecessor** of node $x$ is the greatest key strictly smaller than $x.key$. The **successor** is the smallest key strictly greater.

Predecessor:

1. If $x$ has a left subtree, return its maximum: go left once, then all the way right.
2. Otherwise go upward while $x$ is a left child. The first ancestor for which $x$ lies in its right subtree is the predecessor.

Successor is symmetric:

1. If $x$ has a right subtree, return its minimum.
2. Otherwise climb while $x$ is a right child; the first ancestor approached from its left is the successor.

~~~cpp
Node* minimum(Node* x) {
    while (x && x->left) x = x->left;
    return x;
}
Node* maximum(Node* x) {
    while (x && x->right) x = x->right;
    return x;
}
Node* successor(Node* x) {
    if (x->right) return minimum(x->right);
    Node* p = x->parent;
    while (p && x == p->right) { x = p; p = p->parent; }
    return p;
}
Node* predecessor(Node* x) {
    if (x->left) return maximum(x->left);
    Node* p = x->parent;
    while (p && x == p->left) { x = p; p = p->parent; }
    return p;
}
~~~

Examples:

- predecessor/successor of 15 are 13 and 17;
- predecessor/successor of 20 are 17 and 25;
- 5 has no predecessor; 40 has no successor;
- predecessor is not always the parent: predecessor of 20 is deep descendant 17.

## 7.3 BST deletion

Three structural cases:

1. no child: remove the node;
2. one child: splice the child into its place;
3. two children: use successor $y=\min(x.right)$. Move $y$ into $x$’s place; $y$ has no left child, so its old position is easy to splice.

The transplant helper replaces one subtree by another without deciding how the removed subtree’s children should be rearranged.

~~~text
TRANSPLANT(T,u,v)
    if u.parent = NIL: T.root = v
    else if u = u.parent.left: u.parent.left = v
    else: u.parent.right = v
    if v != NIL: v.parent = u.parent

DELETE(T,z)
    if z.left = NIL: TRANSPLANT(T,z,z.right)
    else if z.right = NIL: TRANSPLANT(T,z,z.left)
    else:
        y = MINIMUM(z.right)
        if y.parent != z:
            TRANSPLANT(T,y,y.right)
            y.right = z.right; y.right.parent = y
        TRANSPLANT(T,z,y)
        y.left = z.left; y.left.parent = y
~~~

Balanced BST deletion uses the same order logic, then restores its own balance invariant.

---

# 8. AVL trees

## 8.1 Invariant and height

An AVL tree is a BST in which every node satisfies

$$
BF(x)=height(x.left)-height(x.right)\in\{-1,0,1\}.
$$

Let $N(h)$ be the minimum number of nodes in an AVL tree of height $h$. The sparsest height-$h$ tree has child heights $h-1$ and $h-2$:

$$
N(h)=1+N(h-1)+N(h-2).
$$

This is Fibonacci-like, so $N(h)=\Omega(\varphi^h)$ and

$$
h=O(\log n),\qquad h\lesssim1.44\log_2(n+2).
$$

Therefore search, insert, and delete are $O(\log n)$.

## 8.2 Rotations

A rotation changes only a constant number of pointers and preserves the in-order sequence.

Right rotation at $y$:

~~~text
          y                     x
         / \                   / \
        x   C      --->       A   y
       / \                       / \
      A   B                     B   C
~~~

Left rotation is the mirror image.

Four imbalance shapes:

| Heavy path | Repair |
|---|---|
| LL | one right rotation |
| RR | one left rotation |
| LR | left-rotate left child, then right-rotate node |
| RL | right-rotate right child, then left-rotate node |

The label describes the first two directions from the unbalanced node toward the newly inserted/deletion-affected region.

## 8.3 Implementable AVL

~~~cpp
struct AVLNode {
    int key, h = 1;
    AVLNode *left = nullptr, *right = nullptr;
    explicit AVLNode(int k) : key(k) {}
};

int height(AVLNode* x) { return x ? x->h : 0; }
int balanceFactor(AVLNode* x) {
    return x ? height(x->left) - height(x->right) : 0;
}
void pull(AVLNode* x) {
    x->h = 1 + max(height(x->left), height(x->right));
}

AVLNode* rotateRight(AVLNode* y) {
    AVLNode* x = y->left;
    AVLNode* B = x->right;
    x->right = y;
    y->left = B;
    pull(y);                     // lower node first
    pull(x);
    return x;
}

AVLNode* rotateLeft(AVLNode* x) {
    AVLNode* y = x->right;
    AVLNode* B = y->left;
    y->left = x;
    x->right = B;
    pull(x);
    pull(y);
    return y;
}

AVLNode* rebalance(AVLNode* x) {
    pull(x);
    if (balanceFactor(x) > 1) {
        if (balanceFactor(x->left) < 0)
            x->left = rotateLeft(x->left);   // LR
        return rotateRight(x);               // LL after possible conversion
    }
    if (balanceFactor(x) < -1) {
        if (balanceFactor(x->right) > 0)
            x->right = rotateRight(x->right); // RL
        return rotateLeft(x);                 // RR after possible conversion
    }
    return x;
}

AVLNode* avlInsert(AVLNode* root, int key) {
    if (!root) return new AVLNode(key);
    if (key < root->key) root->left = avlInsert(root->left, key);
    else if (key > root->key) root->right = avlInsert(root->right, key);
    else return root; // duplicate policy: ignore
    return rebalance(root);
}

AVLNode* avlErase(AVLNode* root, int key) {
    if (!root) return nullptr;
    if (key < root->key) root->left = avlErase(root->left, key);
    else if (key > root->key) root->right = avlErase(root->right, key);
    else {
        if (!root->left || !root->right) {
            AVLNode* child = root->left ? root->left : root->right;
            delete root;
            return child;
        }
        AVLNode* s = root->right;
        while (s->left) s = s->left;
        root->key = s->key;
        root->right = avlErase(root->right, s->key);
    }
    return rebalance(root);
}
~~~

Insertion needs at most one local single/double restructuring at the first unbalanced ancestor; above it, subtree height returns to its prior value. Deletion may reduce subtree height after a repair, so imbalance can propagate all the way to the root and require $O(\log n)$ rotations total.

Edge cases:

- recalculate heights bottom-up and lower rotated node first;
- during deletion, child balance 0 is possible and a single rotation is still correct;
- every recursive return must use the possibly new subtree root.

---

# 9. Red–black trees

## 9.1 Five properties

Use one shared black sentinel `NIL` instead of ordinary null pointers:

1. every node is red or black;
2. the root is black;
3. every `NIL` leaf is black;
4. a red node has two black children—no red-red parent/child;
5. every path from a node to a descendant `NIL` has the same number of black nodes.

Define black-height $bh(x)$ as the number of black nodes on any path from, but **not including**, $x$ down to a `NIL`.

## 9.2 Why height is logarithmic

Lemma: the subtree rooted at $x$ contains at least $2^{bh(x)}-1$ internal nodes. Induct on height; each child has black-height at least $bh(x)-1$, so together they contain at least

$$
2(2^{bh(x)-1}-1)+1=2^{bh(x)}-1.
$$

Property 4 ensures at least half the nodes on any root-to-leaf path are black, so $bh(root)\ge h/2$. Hence

$$
n\ge2^{h/2}-1
\Rightarrow h\le2\log_2(n+1).
$$

The tree is less rigidly balanced than AVL but still guarantees $O(\log n)$ operations.

## 9.3 Rotations

Left rotation at $x$ promotes its right child $y$; $y.left$ becomes $x.right$, then $x$ becomes $y.left$. Right rotation is symmetric. Rotations preserve BST order but not colors automatically.

~~~text
LEFT-ROTATE(T,x)
    y = x.right
    x.right = y.left
    if y.left != T.nil: y.left.parent = x
    y.parent = x.parent
    if x.parent = T.nil: T.root = y
    else if x = x.parent.left: x.parent.left = y
    else: x.parent.right = y
    y.left = x
    x.parent = y
~~~

## 9.4 Insertion fix-up

BST-insert $z$, make both children `NIL`, and color $z$ red. Red preserves black-height; the only possible violation is a red parent.

While parent is red, let $g$ be grandparent and $u$ the uncle. Assume parent is $g.left$; mirror left/right for the other side.

1. **Uncle red:** color parent and uncle black, grandparent red, and continue from grandparent. This moves the red-red issue upward without changing black-height.
2. **Uncle black, triangle (LR):** set current to parent and left-rotate parent. It becomes the line case.
3. **Uncle black, line (LL):** color parent black, grandparent red, right-rotate grandparent.

Finally color root black. There are at most two rotations; recoloring can travel $O(\log n)$.

~~~text
RB-INSERT-FIXUP(T,z)
    while z.parent.color = RED
        if z.parent = z.parent.parent.left
            y = z.parent.parent.right                 // uncle
            if y.color = RED                          // case 1
                z.parent.color = BLACK
                y.color = BLACK
                z.parent.parent.color = RED
                z = z.parent.parent
            else
                if z = z.parent.right                 // case 2
                    z = z.parent
                    LEFT-ROTATE(T,z)
                z.parent.color = BLACK                // case 3
                z.parent.parent.color = RED
                RIGHT-ROTATE(T,z.parent.parent)
        else
            same code with left and right exchanged
    T.root.color = BLACK
~~~

Example logic: inserting into the outside grandchild of a black-uncle configuration needs one rotation; inserting into the inside grandchild first rotates the parent, then the grandparent.

## 9.5 Deletion and the “double black”

Perform ordinary BST deletion, but remember the color of the node physically removed. Removing red changes no black-height. Removing black leaves one path with one fewer black; the replacement $x$, possibly `NIL`, conceptually carries an extra black.

Exact structural skeleton:

~~~text
RB-DELETE(T,z)
    y = z
    original = y.color
    if z.left = T.nil
        x = z.right
        RB-TRANSPLANT(T,z,z.right)
    else if z.right = T.nil
        x = z.left
        RB-TRANSPLANT(T,z,z.left)
    else
        y = TREE-MINIMUM(z.right)
        original = y.color
        x = y.right
        if y.parent = z
            x.parent = y             // important even when x is the sentinel
        else
            RB-TRANSPLANT(T,y,y.right)
            y.right = z.right
            y.right.parent = y
        RB-TRANSPLANT(T,z,y)
        y.left = z.left
        y.left.parent = y
        y.color = z.color
    if original = BLACK
        RB-DELETE-FIXUP(T,x)
~~~

Assume $x$ is a left child; mirror for a right child. Let sibling $w=x.parent.right$:

1. **Sibling red:** parent must be black. Recolor sibling black and parent red; left-rotate parent. The new sibling is black, reducing to cases 2–4.
2. **Sibling black, both children black:** color sibling red and move extra black to parent.
3. **Sibling black, near child red, far child black:** color near child black and sibling red; right-rotate sibling. This converts to case 4.
4. **Sibling black, far child red:** give sibling parent’s color, color parent and far child black, left-rotate parent, and finish.

~~~text
RB-DELETE-FIXUP(T,x)
    while x != T.root and x.color = BLACK
        if x = x.parent.left
            w = x.parent.right
            if w.color = RED                             // case 1
                w.color = BLACK
                x.parent.color = RED
                LEFT-ROTATE(T,x.parent)
                w = x.parent.right
            if w.left.color = BLACK and w.right.color = BLACK // case 2
                w.color = RED
                x = x.parent
            else
                if w.right.color = BLACK                 // case 3
                    w.left.color = BLACK
                    w.color = RED
                    RIGHT-ROTATE(T,w)
                    w = x.parent.right
                w.color = x.parent.color                 // case 4
                x.parent.color = BLACK
                w.right.color = BLACK
                LEFT-ROTATE(T,x.parent)
                x = T.root
        else
            same code with left and right exchanged
    x.color = BLACK
~~~

Deletion uses at most three rotations and $O(\log n)$ recoloring/ancestor steps.

## 9.6 AVL versus red–black

| Property | AVL | Red–black |
|---|---|---|
| Balance | height difference at most 1 | color/black-height constraints |
| Height | tighter, about $1.44\log_2 n$ max | at most $2\log_2(n+1)$ |
| Search | often slightly faster | guaranteed $O(\log n)$ |
| Updates | may rebalance more | few rotations, especially insertion |
| Typical use | lookup-heavy in-memory index | general ordered maps/sets, library trees |

Java `TreeMap`/`TreeSet` and C++ ordered `map`/`set` are normally balanced search trees, commonly red–black implementations. Do not claim that an unordered `HashMap` is a red–black tree as its primary structure; modern implementations may treeify a long collision bucket, but hashing remains the main organization.

---

# 10. Splay trees

## 10.1 Idea and rotation cases

A splay tree is a BST with no stored balance field. After accessing node $x$, repeatedly rotate it to the root:

- **zig:** parent is root; one rotation;
- **zig-zig:** $x$ and parent are both left children or both right children; rotate grandparent, then parent in the same direction;
- **zig-zag:** one is a left child and the other a right child; rotate parent, then grandparent in opposite directions.

The order in zig-zig matters. Merely rotating $x$ upward one single rotation at a time is the naive move-to-root rule and can have $\Omega(n)$ amortized cost. The paired zig-zig/zig-zag operations reshape the whole access path.

~~~text
SPLAY(T,x)
    while x.parent != NIL
        p = x.parent; g = p.parent
        if g = NIL
            rotate x over p                              // zig
        else if (x = p.left) = (p = g.left)
            rotate p over g; rotate x over p             // zig-zig
        else
            rotate x over p; rotate x over g             // zig-zag
~~~

The slide example starts from a long chain and uses zig-zig, zig-zag, and a final zig to bring the accessed item to the root while substantially shortening the path.

## 10.2 Search, insert, split, join, delete

- **Search hit:** ordinary BST search, then splay the found node.
- **Search miss:** a common robust convention splays the last visited node; it keeps the working-set benefit around the missed key.
- **Insert:** BST-insert, then splay the new node.
- **Split by key $k$:** splay $k$, or the last accessed neighbor. Detach so all keys $\le k$ form one tree and all keys $>k$ the other.
- **Join $L,R$:** require every key in $L$ less than every key in $R$. Splay maximum of $L$; its right child is empty, so attach $R$.
- **Top-down delete:** splay $x$ to root, remove it, and join its left and right trees.

~~~text
DELETE(T,x)
    SEARCH-AND-SPLAY(T,x)
    if T.root.key != x: return not-found
    L = T.root.left; R = T.root.right
    detach L and R
    if L = NIL: T.root = R
    else:
        T.root = L
        m = MAXIMUM(L)
        SPLAY(T,m)
        T.root.right = R
~~~

One operation can cost $\Theta(n)$; every operation is $O(\log n)$ **amortized**, so $m$ operations from an empty tree cost $O(m\log n)$.

## 10.3 Potential proof / access lemma

Let $size(x)$ be the number of nodes in $x$’s subtree, rank $r(x)=\log size(x)$, and

$$
\Phi(T)=\sum_{x\in T}r(x).
$$

For one double rotation (zig-zig or zig-zag), the amortized charge is at most

$$
3(r'(x)-r(x)).
$$

For the one possible final zig it is at most

$$
3(r'(x)-r(x))+1.
$$

Summing over the splay telescopes:

$$
\widehat c(\text{splay }x)
\le3(r(root)-r(x))+1
\le3\log n+1.
$$

Walking down the search path is charged together with the rotations; deletion does not increase potential; insertion’s non-splay potential increase is also $O(\log n)$. Starting from the empty tree gives initial potential 0 and nonnegative final potential, so total actual cost is at most total amortized cost.

Why useful: frequently/recently accessed keys move near the root; no parent color/height metadata is needed; split/join are elegant. Why risky: individual latency is unbounded $O(n)$, and the tree changes even on a read.

**Dynamic optimality conjecture:** splay trees are conjectured to be within a constant factor of the best offline BST algorithm for any access sequence. It is an open conjecture, not the same as the proven $O(\log n)$ amortized bound.

---

# 11. Skip lists

## 11.1 Structure and search

A skip list stores a sorted linked list at level 0. Independently promote each key to the next level with probability $p$, usually $1/2$. Higher levels are sparse “express lanes.”

Search starts at the highest head:

1. move right while the next key is less than the target;
2. if moving right would pass it, drop one level;
3. at level 0, test equality.

Example:

~~~text
L3: -inf ---------------- 30 ---------------- +inf
L2: -inf ------ 10 ------ 30 ------ 50 ------ +inf
L1: -inf -- 5 -- 10 -- 20 -- 30 -- 50 ------ +inf
L0: -inf -- 5 -- 10 -- 13 -- 20 -- 30 -- 42 -- 50 -- +inf
~~~

Searching 42: cross 30 at the top, descend, stop before 50, descend to level 0, and move to 42.

## 11.2 Insert/delete implementation

~~~cpp
class SkipList {
    static constexpr int MAX_LEVEL = 32;
    struct Node {
        int key;
        vector<Node*> next;
        Node(int key, int level) : key(key), next(level + 1, nullptr) {}
    };
    Node* head = new Node(numeric_limits<int>::min(), MAX_LEVEL);
    int level = 0;
    mt19937 rng{random_device{}()};
    bernoulli_distribution promote{0.5};

    int randomLevel() {
        int h = 0;
        while (h < MAX_LEVEL && promote(rng)) ++h;
        return h;
    }

public:
    bool contains(int key) const {
        Node* x = head;
        for (int h = level; h >= 0; --h)
            while (x->next[h] && x->next[h]->key < key)
                x = x->next[h];
        x = x->next[0];
        return x && x->key == key;
    }

    void insert(int key) {
        vector<Node*> update(MAX_LEVEL + 1);
        Node* x = head;
        for (int h = level; h >= 0; --h) {
            while (x->next[h] && x->next[h]->key < key)
                x = x->next[h];
            update[h] = x;
        }
        x = x->next[0];
        if (x && x->key == key) return;

        int h = randomLevel();
        if (h > level) {
            for (int i = level + 1; i <= h; ++i) update[i] = head;
            level = h;
        }
        Node* z = new Node(key, h);
        for (int i = 0; i <= h; ++i) {
            z->next[i] = update[i]->next[i];
            update[i]->next[i] = z;
        }
    }

    void erase(int key) {
        vector<Node*> update(MAX_LEVEL + 1);
        Node* x = head;
        for (int h = level; h >= 0; --h) {
            while (x->next[h] && x->next[h]->key < key)
                x = x->next[h];
            update[h] = x;
        }
        x = x->next[0];
        if (!x || x->key != key) return;
        for (int h = 0; h <= level && update[h]->next[h] == x; ++h)
            update[h]->next[h] = x->next[h];
        delete x;
        while (level > 0 && head->next[level] == nullptr) --level;
    }
};
~~~

With $p=1/2$:

- probability a node reaches at least level $k$ is $2^{-k}$;
- expected number of pointers per node is $1/(1-p)=2$;
- maximum level is $O(\log n)$ with high probability;
- search/insert/delete are expected $O(\log n)$, worst case $O(n)$;
- space is expected $O(n)$.

Skip list versus balanced BST: simpler randomized updates and natural concurrent variants, but probabilistic rather than deterministic height guarantees and more forward pointers.

---

# 12. Ordered-structure comparison

| Structure | Search | Insert | Delete | Special point |
|---|---:|---:|---:|---|
| Ordinary BST | $O(h)$ | $O(h)$ | $O(h)$ | may become $h=n$ |
| AVL | $O(\log n)$ worst | $O(\log n)$ | $O(\log n)$ | tight balance |
| Red–black | $O(\log n)$ worst | $O(\log n)$ | $O(\log n)$ | few rotations, library workhorse |
| Splay | $O(\log n)$ amortized, $O(n)$ one op | same | same | locality, no balance metadata |
| Skip list | expected $O(\log n)$, worst $O(n)$ | same | same | randomized levels |
| Hash table | expected $O(1)$ exact lookup | expected $O(1)$ | expected $O(1)$ | no sorted order/range queries |

---

# 13. Amortized analysis

## 13.1 What it is—and is not

Amortized analysis bounds the total actual cost of **every** sequence of operations, then divides that total across the sequence. It is not:

- average-case analysis over an input distribution;
- expected analysis over random choices;
- permission to ignore a rare expensive operation.

An individual dynamic-array append may cost $\Theta(n)$, yet any $n$ appends from empty cost $\Theta(n)$ total, hence $O(1)$ amortized per append.

## 13.2 The three methods

### Aggregate method

Directly bound

$$
\sum_{i=1}^{m}c_i\le T(m).
$$

Then average amortized cost is $T(m)/m$. Different operation types receive the same average charge.

### Accounting method

Assign artificial charge $\widehat c_i$. If $\widehat c_i>c_i$, store the surplus as credit; later expensive operations spend it. Maintain nonnegative credit after every prefix:

$$
\sum_{i=1}^{k}\widehat c_i\ge\sum_{i=1}^{k}c_i
\quad\text{for every }k.
$$

Then total charged cost upper-bounds actual cost.

### Potential method

Potential $\Phi(D_i)$ is stored energy in data-structure state after operation $i$:

$$
\widehat c_i=c_i+\Phi(D_i)-\Phi(D_{i-1}).
$$

Telescoping gives

$$
\sum_{i=1}^{m}\widehat c_i
=\sum_{i=1}^{m}c_i+\Phi(D_m)-\Phi(D_0).
$$

If $\Phi(D_0)=0$ and $\Phi(D_i)\ge0$, total amortized cost upper-bounds actual cost.

Potential belongs to the **state**, not to the operation number. A negative potential can still be used if final potential is always at least initial potential, but nonnegative/zero-initial is the easiest safe design.

## 13.3 Binary counter

Increment a $k$-bit binary counter by flipping trailing 1s to 0 and the first 0 to 1.

Aggregate count: bit 0 flips $n$ times, bit 1 at most $n/2$, bit 2 at most $n/4$, so

$$
n+n/2+n/4+\cdots<2n.
$$

Thus $n$ increments cost $O(n)$, at most 2 amortized bit flips per increment.

Potential proof: $\Phi=$ number of 1 bits. If an increment clears $t$ trailing ones and sets one zero:

$$
c=t+1,\qquad\Delta\Phi=1-t,\qquad
\widehat c=(t+1)+(1-t)=2.
$$

The expensive carry chain spends potential saved in those 1 bits.

## 13.4 Stack with multipop

Operations:

- PUSH costs 1;
- POP costs 1 when nonempty;
- MULTIPOP($k$) pops $\min(k,|S|)$ elements.

No element can be popped more than once after being pushed. Across $m$ operations, total pushes and pops are $O(m)$.

Accounting: charge PUSH 2—one pays now and one credit remains on the item to pay for its eventual pop. POP/MULTIPOP charge 0.

Potential: $\Phi(S)=|S|$. PUSH has amortized $1+1=2$; popping $t$ items has $t-t=0$.

## 13.5 Dynamic array/table

### Doubling

When an array of capacity $m$ is full, allocate capacity $2m$, copy $m$ items, then insert. During $n$ appends, copying costs

$$
1+2+4+\cdots < 2n.
$$

Together with $n$ writes, total is $O(n)$. A convenient potential in the at-least-half-full region is

$$
\Phi=2\,num-size.
$$

Ordinary insertion builds potential; expansion consumes it.

### Deletion and avoiding thrashing

If we double when full and halve immediately when half-full, alternating one insertion and one deletion around the threshold can resize every operation. Use hysteresis:

- grow when load reaches 1;
- shrink only when load reaches $1/4$, reducing capacity by half.

The post-shrink table is half full, leaving a large gap before the next resize. A standard nonnegative potential is

$$
\Phi(T)=
\begin{cases}
2\,num-size, & num\ge size/2,\\
size/2-num, & num<size/2.
\end{cases}
$$

It proves $O(1)$ amortized insert and delete, while each resize remains $\Theta(n)$ actual.

## 13.6 Initialize a large array in $O(1)$

The slides include the classic trick for an array whose memory initially contains arbitrary bits. Maintain:

- data array $A[1..n]$;
- dense list $B[1..k]$ of indices that have been assigned;
- reverse location $C[1..n]$.

Index $i$ is initialized exactly when

$$
1\le C[i]\le k\quad\text{and}\quad B[C[i]]=i.
$$

To first write $i$: increment $k$, set $B[k]=i,C[i]=k$, then set $A[i]$. Read returns a default value when the membership test fails. Initialization sets only $k=0$, so it is $O(1)$; read/write are worst-case $O(1)$; space $O(n)$.

The two-part check is vital because arbitrary old contents of $C[i]$ might accidentally lie within $1..k$.

## 13.7 A nonstandard binary-heap amortization in the summary slide

The summary labels binary-heap extract-min/delete as $O(1)$ **amortized**, although their ordinary worst-case time is $O(\log n)$. This can be a valid redistribution for a chosen operation mix:

$$
\Phi(n)=a\log(n!)
$$

for a constant $a$ large enough to cover a sift path. Removing one item decreases potential by $a\log n$, paying for extract/delete; inserting increases it by $a\log(n+1)$, so insertion remains $O(\log n)$ amortized. Decrease-key does not change size, so it remains $O(\log n)$.

This does **not** make extract-min physically constant time, nor is it the conventional binary-heap table. Conventional worst-case bounds remain insert/extract/decrease/delete $O(\log n)$, find-min $O(1)$. State which accounting scheme is being used.

---

# 14. Priority queues and binary heaps

## 14.1 Interface and invariant

A min-priority queue supports make, insert, find-min, extract-min, decrease-key, delete, and sometimes meld. A binary min-heap is a complete binary tree satisfying

$$
key(parent(i))\le key(i).
$$

Zero-based array indices:

$$
parent(i)=\lfloor(i-1)/2\rfloor,\quad
left(i)=2i+1,\quad right(i)=2i+2.
$$

Completeness gives height $\lfloor\log_2 n\rfloor$.

## 14.2 Sift operations and implementation

~~~cpp
class BinaryMinHeap {
    vector<int> a;

    void siftUp(int i) {
        while (i > 0) {
            int p = (i - 1) / 2;
            if (a[p] <= a[i]) break;
            swap(a[p], a[i]);
            i = p;
        }
    }

    void siftDown(int i) {
        int n = a.size();
        while (true) {
            int best = i;
            int l = 2*i + 1, r = 2*i + 2;
            if (l < n && a[l] < a[best]) best = l;
            if (r < n && a[r] < a[best]) best = r;
            if (best == i) break;
            swap(a[i], a[best]);
            i = best;
        }
    }

public:
    BinaryMinHeap() = default;
    explicit BinaryMinHeap(vector<int> values) : a(move(values)) {
        for (int i = (int)a.size()/2 - 1; i >= 0; --i) siftDown(i);
    }

    bool empty() const { return a.empty(); }
    int minimum() const {
        if (a.empty()) throw underflow_error("empty heap");
        return a[0];
    }
    void push(int x) {
        a.push_back(x);
        siftUp((int)a.size() - 1);
    }
    int extractMin() {
        if (a.empty()) throw underflow_error("empty heap");
        int ans = a[0];
        a[0] = a.back();
        a.pop_back();
        if (!a.empty()) siftDown(0);
        return ans;
    }
};
~~~

If external decrease-key/delete by handle is required, maintain each item’s current array position and update that mapping on every swap. Searching the heap for an arbitrary key is $O(n)$; heap order is weaker than BST order.

## 14.3 Why BUILD-HEAP is $O(n)$, not $O(n\log n)$

Calling sift-down at each internal node looks like $n$ calls of at most $\log n$, but most nodes are near the leaves and move only a little.

At most $n/2^{h+1}$ nodes have height $h$. Therefore

$$
T(n)\le
\sum_{h=0}^{\lfloor\log n\rfloor}
\frac{n}{2^{h+1}}O(h)
=O(n)\sum_{h\ge0}\frac{h}{2^{h+1}}
=O(n).
$$

The infinite sum equals 1. Equivalently, charge one unit for every level a node could descend:

$$
\#\{height\ge1\}+\#\{height\ge2\}+\cdots
\le n/2+n/4+\cdots<n.
$$

Thus:

- inserting $n$ items one by one: $O(n\log n)$;
- bottom-up heapify from the last internal node to root: $O(n)$.

## 14.4 Exact binary-heap bounds

| Operation | Worst-case |
|---|---:|
| make empty / is-empty | $O(1)$ |
| find-min | $O(1)$ |
| insert | $O(\log n)$ |
| extract-min | $O(\log n)$ |
| decrease-key | $O(\log n)$ |
| delete known position | $O(\log n)$ |
| build-heap from array | $O(n)$ |
| meld two ordinary binary heaps | $O(n+m)$ by rebuild |

Heapsort builds a max heap in $O(n)$, then performs $n$ root removals in $O(n\log n)$. It is in-place and worst-case $O(n\log n)$, but normally not stable.

## 14.5 $d$-ary heaps

Each node has up to $d$ children:

$$
parent(i)=\left\lfloor\frac{i-1}{d}\right\rfloor,\qquad
children(i)=di+1,\ldots,di+d.
$$

Height is $\Theta(\log_d n)$:

- insert/decrease-key: $O(\log_d n)$;
- extract/delete: inspect up to $d$ children at each level, $O(d\log_d n)$;
- find-min: $O(1)$.

For a **min** heap, sift-down chooses the **smallest** child. One slide says largest child; that is the max-heap rule and must be reversed.

Large $d$ makes the tree shallower and decrease-key faster but makes each downward step scan more children. This can suit Dijkstra when decrease-key operations greatly outnumber extracts.

---

# 15. Binomial heaps

## 15.1 Binomial trees

$B_0$ is one node. $B_k$ is formed by linking roots of two $B_{k-1}$ trees, making one root the other’s leftmost child.

Properties proved by induction:

- nodes: $2^k$;
- height and root degree: $k$;
- nodes at depth $i$: $\binom{k}{i}$;
- removing the root leaves $B_{k-1},B_{k-2},\ldots,B_0$.

A binomial heap is a root list of heap-ordered binomial trees with at most one tree of each degree. If heap size is

$$
n=(b_r\cdots b_1b_0)_2,
$$

then it contains $B_k$ exactly when $b_k=1$. This is why melding resembles binary addition.

## 15.2 Link and union

To link two degree-$k$ min-heap trees, compare roots and make the larger root a child of the smaller; result is $B_{k+1}$.

Union first merges root lists by nondecreasing degree, then scans them. Equal degrees are “carried” by linking, with one important three-tree case: if three consecutive roots have the same degree, postpone the first pair because the latter two will link into the next degree.

~~~text
BINOMIAL-LINK(y,z)              // key[z] <= key[y]
    y.parent = z
    y.sibling = z.child
    z.child = y
    z.degree++

UNION(H1,H2)
    H.rootList = MERGE-BY-DEGREE(H1.rootList,H2.rootList)
    if empty: return H
    prev = NIL; x = first; next = x.sibling
    while next != NIL
        if x.degree != next.degree
           or (next.sibling != NIL and next.sibling.degree = x.degree)
            prev = x; x = next
        else if x.key <= next.key
            x.sibling = next.sibling
            BINOMIAL-LINK(next,x)
        else
            if prev = NIL: H.head = next
            else: prev.sibling = next
            BINOMIAL-LINK(x,next)
            x = next
        next = x.sibling
    return H
~~~

At most $1+\lfloor\log_2 n\rfloor$ roots exist, so worst-case meld is $O(\log n)$.

## 15.3 Operations

- **Find-min:** scan roots, $O(\log n)$, or maintain a min-root pointer for $O(1)$.
- **Insert:** create a one-node $B_0$ heap and union, $O(\log n)$ worst case.
- **Extract-min:** find/delete minimum root; reverse its child list so degrees increase; union it with remaining heap. $O(\log n)$.
- **Decrease-key:** lower key and swap key/payload upward while smaller than parent. $O(\log n)$. If clients hold node identity rather than key/payload identity, relink nodes instead of swapping only keys.
- **Delete:** decrease to $-\infty$, then extract-min. $O(\log n)$.

With potential $\Phi(H)=$ number of trees:

- insertion has $O(1)$ amortized cost because each carry/link reduces tree count;
- a lazy root-list concatenation meld can be $O(1)$ amortized, delaying consolidation;
- extract-min later pays for consolidation and stays $O(\log n)$.

Be explicit whether the heap eagerly maintains one tree per degree or uses lazy consolidation; this determines whether meld is worst-case $O(\log n)$ or amortized $O(1)$.

---

# 16. Fibonacci heaps

## 16.1 Why they improve graph algorithms

A Fibonacci heap delays structural work:

- roots form a circular doubly linked list;
- trees obey min-heap order but are not binomial trees at all times;
- insert and meld only splice lists;
- consolidation by equal degree occurs during extract-min;
- decrease-key cuts a violating node to the root list and may cascade.

This makes insert, find-min, meld, and decrease-key $O(1)$ amortized, which changes Dijkstra/Prim from binary-heap $O(E\log V)$ to

$$
O(E+V\log V).
$$

In practice, pointer overhead and constants often make binary heaps faster; Fibonacci heaps are especially important theoretically.

## 16.2 Marking and cascading cuts

Every nonroot node has a mark bit:

- an unmarked node that loses its first child becomes marked;
- a marked node that loses another child is cut from its parent and moved to the root list;
- repeat upward;
- roots are unmarked.

Thus a nonroot may lose at most one child without itself being cut. This restriction implies a degree-$k$ node has at least $F_{k+2}$ descendants, so maximum degree is $O(\log n)$.

Core pseudocode:

~~~text
INSERT(H,x)
    x.degree = 0; x.parent = NIL; x.mark = false
    add x to H.rootList
    if H.min = NIL or x.key < H.min.key: H.min = x
    H.n++

MELD(H1,H2)
    concatenate circular root lists
    min = smaller of the two minima

DECREASE-KEY(H,x,k)
    require k <= x.key
    x.key = k
    y = x.parent
    if y != NIL and x.key < y.key
        CUT(H,x,y)
        CASCADING-CUT(H,y)
    if x.key < H.min.key: H.min = x

CUT(H,x,y)
    remove x from y.child list; y.degree--
    add x to root list
    x.parent = NIL; x.mark = false

CASCADING-CUT(H,y)
    z = y.parent
    if z != NIL
        if y.mark = false: y.mark = true
        else:
            CUT(H,y,z)
            CASCADING-CUT(H,z)
~~~

Extract-min:

1. remove minimum root $z$;
2. move all children of $z$ to root list and clear their parents;
3. consolidate roots of equal degree using an auxiliary array indexed by degree;
4. rebuild the root list and min pointer.

~~~text
CONSOLIDATE(H)
    A[0 .. O(log H.n)] = NIL
    for each current root x
        d = x.degree
        while A[d] != NIL
            y = A[d]
            if y.key < x.key: swap(x,y)
            make y a child of x
            A[d] = NIL; d++
        A[d] = x
    rebuild root list from non-NIL A entries and recompute H.min
~~~

Delete is decrease-key to $-\infty$ followed by extract-min.

## 16.3 Potential analysis and bounds

Use the standard potential

$$
\Phi(H)=t(H)+2m(H),
$$

where $t$ is number of root trees and $m$ number of marked nodes. Multiplying the tree term by another positive constant, as in some lecture notation, changes only constants.

- insert adds one root: actual $O(1)$, potential $+1$;
- meld concatenates lists: actual $O(1)$, essentially additive potential;
- decrease-key may perform many cascading cuts, but each cut adds a root while clearing a mark; released marked potential pays for all but constant work;
- extract-min may start with many roots, but consolidation removes roots and the potential decrease pays for linking; only $O(\log n)$ roots remain because maximum degree is $O(\log n)$.

| Operation | Fibonacci heap amortized | Binomial heap typical | Binary heap worst |
|---|---:|---:|---:|
| make / find-min | $O(1)$ | $O(1)$ with min pointer | $O(1)$ |
| insert | $O(1)$ | $O(1)$ amortized, $O(\log n)$ worst | $O(\log n)$ |
| meld | $O(1)$ | $O(\log n)$, or lazy $O(1)$ amortized | $O(n+m)$ |
| decrease-key | $O(1)$ amortized | $O(\log n)$ | $O(\log n)$ |
| extract-min | $O(\log n)$ amortized | $O(\log n)$ | $O(\log n)$ |
| delete | $O(\log n)$ amortized | $O(\log n)$ | $O(\log n)$ |

---

# 17. Hashing

## 17.1 The two-stage idea

A hash table maps a large key universe into array indices:

$$
\text{key}\xrightarrow{\text{hash code}}\text{machine integer}
\xrightarrow{\text{compression}}\{0,\ldots,M-1\}.
$$

The ideal practical hash is fast, deterministic for the lifetime of the table, uses the whole key, and spreads actual keys close to uniformly. It is impossible to avoid collisions when the key universe is larger than the table, so a collision-resolution policy is part of the data structure.

Load factor:

$$
\alpha=\frac{N}{M},
$$

where $N$ is stored keys and $M$ table slots/buckets.

## 17.2 Equality and hash-code contract

For Java-style keys:

$$
x.equals(y)\Rightarrow x.hashCode()=y.hashCode().
$$

The converse is false: equal hash codes do not imply equal objects. Returning a constant hash is legal but destroys performance.

Rules for user-defined keys:

- include every field used by equality;
- use the same fields in equality and hashing;
- do not mutate a key in a way that changes its hash while it is in the table;
- recursively hash reference/array fields;
- handle null consistently.

A common combination is

$$
h\leftarrow31h+\text{fieldHash}.
$$

For string $s_0s_1\ldots s_{L-1}$, Horner’s rule computes

$$
h=s_0\,31^{L-1}+s_1\,31^{L-2}+\cdots+s_{L-1}
$$

with $L$ multiply-add operations:

~~~cpp
uint32_t stringHash(const string& s) {
    uint32_t h = 0;
    for (unsigned char c : s) h = 31u * h + c;
    return h; // unsigned overflow is defined modulo 2^32
}
~~~

Immutable strings can cache the result. A cached value of zero needs a separate “computed” bit if zero itself is a valid hash.

Java modular compression should not use plain absolute value: `abs(INT_MIN)` is still negative. A traditional nonnegative form is

~~~java
(key.hashCode() & 0x7fffffff) % M
~~~

Modern code can use a floor-mod operation. For powers of two, libraries often mix high bits into low bits before masking.

## 17.3 Uniform hashing and unavoidable collisions

The **uniform hashing assumption** says each key is independently/equally likely to land in each bucket. It is an analysis model, not automatically guaranteed by choosing a prime.

Balls-and-bins intuition:

- birthday paradox: collisions appear after only $\Theta(\sqrt M)$ random keys;
- coupon collector: filling every bucket takes about $M\ln M$ keys;
- after $M$ random keys, maximum bucket load is about $\Theta(\log M/\log\log M)$.

A family of **universal hash functions** chooses a function randomly so that for distinct $x,y$,

$$
\Pr[h(x)=h(y)]\le1/M.
$$

Randomizing the chosen function also prevents an adversary from knowing one permanent collision pattern.

## 17.4 Separate chaining

Each array cell points to a collection of all keys hashing there.

~~~cpp
template<class K, class V, class Hash = std::hash<K>>
class ChainedHash {
    vector<list<pair<K,V>>> bucket;
    size_t count = 0;
    Hash hasher;

    size_t index(const K& key) const {
        return hasher(key) % bucket.size();
    }

    void rehashTo(size_t m) {
        vector<list<pair<K,V>>> old = move(bucket);
        bucket.assign(m, {});
        count = 0;
        for (auto& chain : old)
            for (auto& [k,v] : chain) put(k, v);
    }

public:
    explicit ChainedHash(size_t m = 8) : bucket(m) {}

    V* get(const K& key) {
        for (auto& [k,v] : bucket[index(key)])
            if (k == key) return &v;
        return nullptr;
    }

    void put(const K& key, const V& value) {
        auto& chain = bucket[index(key)];
        for (auto& [k,v] : chain)
            if (k == key) { v = value; return; }
        chain.push_front({key, value});
        ++count;
        if ((double)count / bucket.size() >= 8.0)
            rehashTo(2 * bucket.size());
    }

    bool erase(const K& key) {
        auto& chain = bucket[index(key)];
        for (auto it = chain.begin(); it != chain.end(); ++it)
            if (it->first == key) {
                chain.erase(it); --count; return true;
            }
        return false;
    }
};
~~~

Under simple uniform hashing:

- expected chain length is $\alpha=N/M$;
- unsuccessful search is $\Theta(1+\alpha)$;
- successful search is also $\Theta(1+\alpha)$, roughly half a chain after the bucket access;
- worst case is $\Theta(N)$ when all keys collide.

The lecture resizing policy keeps average chain length in a constant band—for example double around $\alpha\ge8$, halve around $\alpha\le2$. Rehash every key because the final index depends on new $M$.

## 17.5 Open addressing

All keys live in the table array. A probe function

$$
h(k,i),\qquad i=0,\ldots,M-1
$$

generates candidate slots. Necessarily $\alpha<1$.

Search follows exactly the same probe sequence as insertion:

- stop with success on equal key;
- stop with failure at a never-used EMPTY cell;
- continue past a DELETED tombstone.

### Linear probing

$$
h(k,i)=(h(k)+i)\bmod M.
$$

Excellent cache locality, but contiguous runs create **primary clustering**: longer clusters attract even more insertions.

Under the usual uniform-hashing approximation, average probes are:

$$
\text{successful}\approx
\frac12\left(1+\frac1{1-\alpha}\right),
$$

$$
\text{unsuccessful/insert}\approx
\frac12\left(1+\frac1{(1-\alpha)^2}\right).
$$

At $\alpha=1/2$, these are about $1.5$ and $2.5$. A compact summary source can be read as swapping these; the squared denominator belongs to unsuccessful search/insert.

### Quadratic probing

$$
h(k,i)=(h_1(k)+c_1i+c_2i^2)\bmod M.
$$

It removes primary clustering but keys with the same initial hash still share a probe sequence (**secondary clustering**). Constants/table size must be chosen so enough slots are visited; a common guarantee uses prime $M$ and keeps $\alpha\le1/2$.

### Double hashing

$$
h(k,i)=(h_1(k)+i\,h_2(k))\bmod M.
$$

Require $h_2(k)\ne0$ and $\gcd(h_2(k),M)=1$, so the sequence can visit every slot. For prime $M$, a common choice is

$$
h_2(k)=1+(k\bmod(M-1)).
$$

Different keys usually get different step sizes, greatly reducing clustering.

### Random probing

Use a key-determined pseudorandom permutation/offset sequence. Search must reproduce the same sequence; genuine fresh randomness on each search would make stored keys impossible to locate.

## 17.6 Linear-probing implementation and deletion

~~~cpp
template<class K, class V, class Hash = std::hash<K>>
class LinearHash {
    enum State : unsigned char { EMPTY, OCCUPIED, DELETED };
    struct Slot { K key{}; V value{}; State state = EMPTY; };
    vector<Slot> a;
    size_t used = 0;      // occupied
    size_t filled = 0;    // occupied + tombstones
    Hash hash;

    size_t locate(const K& key) const {
        size_t m = a.size(), i = hash(key) % m;
        while (a[i].state != EMPTY) {
            if (a[i].state == OCCUPIED && a[i].key == key) return i;
            i = (i + 1) % m;
        }
        return m;
    }

    void rebuild(size_t m) {
        vector<Slot> old = move(a);
        a.assign(m, {});
        used = filled = 0;
        for (auto& s : old) if (s.state == OCCUPIED)
            put(move(s.key), move(s.value));
    }

public:
    explicit LinearHash(size_t m = 8) : a(m) {}

    V* get(const K& key) {
        size_t i = locate(key);
        return i == a.size() ? nullptr : &a[i].value;
    }

    void put(K key, V value) {
        if ((filled + 1.0) / a.size() > 0.5) rebuild(2 * a.size());
        size_t m = a.size(), i = hash(key) % m, firstDeleted = m;
        while (a[i].state != EMPTY) {
            if (a[i].state == OCCUPIED && a[i].key == key) {
                a[i].value = move(value); return;
            }
            if (a[i].state == DELETED && firstDeleted == m) firstDeleted = i;
            i = (i + 1) % m;
        }
        if (firstDeleted != m) i = firstDeleted;
        else ++filled;
        a[i] = {move(key), move(value), OCCUPIED};
        ++used;
    }

    bool erase(const K& key) {
        size_t i = locate(key);
        if (i == a.size()) return false;
        a[i].state = DELETED;
        --used;
        if (a.size() > 8 && used * 8 < a.size()) rebuild(a.size()/2);
        else if (filled > 2*used + 8) rebuild(a.size()); // clear tombstones
        return true;
    }
};
~~~

Why simply clearing a deleted slot fails: a later key displaced past that slot would become unreachable because search stops at the first never-used empty slot. Alternatives:

- leave tombstones and periodically rebuild;
- for linear probing, remove and reinsert the following cluster until an empty slot.

Keep a low load, often at most $1/2$. The slides’ grow-at-$1/2$, shrink-near-$1/8$ thresholds supply hysteresis.

## 17.7 Variants

- **Two-choice chaining:** hash to two buckets and insert in the shorter; maximum chain length drops dramatically, to about $O(\log\log N)$ under the model.
- **Cuckoo hashing:** each key has two candidate positions. Insertion may evict a resident to its alternative; lookup checks constant positions. A cycle triggers rehash. Expected constant operations, worst-case rebuild.
- **Perfect hashing:** for a fixed static set, two-level randomized hashing can give worst-case $O(1)$ lookup with linear expected space.
- **Robin Hood hashing:** when inserting, a key with larger probe distance steals a slot from one with smaller distance; it reduces variance.
- **Bloom filter:** not a symbol table, but a compact probabilistic membership filter. It has false positives but no false negatives if items are only inserted.

## 17.8 Security and cryptographic hashes

Known deterministic functions can enable **algorithmic complexity attacks**. Java’s base-31 string scheme has families such as “Aa” and “BB” with equal hash codes; concatenating such blocks yields exponentially many colliding strings. If an attacker controls keys, a nominal $O(1)$ web-server table can degrade to $O(N)$ per operation.

Mitigations include secret per-process seeding/universal hashing, collision-bucket treeification, and resource limits.

A cryptographic hash aims for preimage/collision resistance and is intentionally more expensive than an ordinary table hash. MD5 and SHA-1 are obsolete for collision security. Passwords should not be stored as a fast unsalted hash at all; use a salted, slow password KDF such as Argon2, scrypt, bcrypt, or PBKDF2.

## 17.9 Hash table versus balanced tree

| Need | Prefer |
|---|---|
| exact lookup, no adversarial concern | hash table, expected $O(1)$ |
| guaranteed worst-case | AVL/RB tree, $O(\log n)$ |
| sorted iteration, predecessor/successor, ranges | balanced BST |
| excellent array cache locality | open addressing |
| graceful high load/easy deletion | chaining |
| attacker-controlled keys | randomized hash or worst-case tree fallback |

Hashing is good for equality lookup, not ordering. A prime table size can help some compression patterns but cannot rescue a poor hash that ignores important key structure.

---

# 18. String matching algorithms

The syllabus slide explicitly includes string matching even though the collected lecture deck has little expanded material. This section supplies the implementable core expected from that heading.

Let text $T$ have length $n$, pattern $P$ length $m$. An occurrence at shift $s$ means

$$
T[s\ldots s+m-1]=P[0\ldots m-1].
$$

## 18.1 Naive matching

Try every shift and compare left to right.

~~~cpp
vector<int> naiveMatch(const string& text, const string& pat) {
    vector<int> at;
    if (pat.empty()) { // convention: empty pattern occurs at every boundary
        for (int i = 0; i <= (int)text.size(); ++i) at.push_back(i);
        return at;
    }
    for (int s = 0; s + (int)pat.size() <= (int)text.size(); ++s) {
        int j = 0;
        while (j < (int)pat.size() && text[s+j] == pat[j]) ++j;
        if (j == (int)pat.size()) at.push_back(s);
    }
    return at;
}
~~~

Worst-case $O((n-m+1)m)=O(nm)$, e.g. repeated characters; auxiliary space $O(1)$ beyond answers. It is perfectly reasonable for tiny patterns/texts and requires no preprocessing.

## 18.2 Rabin–Karp

Compare numeric fingerprints of the pattern and every length-$m$ text window. With base $b$, modulus $q$,

$$
H(c_0\ldots c_{m-1})
=\sum_{j=0}^{m-1}c_jb^{m-1-j}\pmod q.
$$

After removing leading character $x$ and appending $y$:

$$
H'\equiv b(H-xb^{m-1})+y\pmod q.
$$

~~~cpp
vector<int> rabinKarp(const string& t, const string& p) {
    vector<int> ans;
    int n = t.size(), m = p.size();
    if (m == 0) {
        for (int i = 0; i <= n; ++i) ans.push_back(i);
        return ans;
    }
    if (m > n) return ans;

    const long long base = 256, mod = 1'000'000'007;
    long long high = 1;
    for (int i = 1; i < m; ++i) high = high * base % mod;
    long long hp = 0, ht = 0;
    for (int i = 0; i < m; ++i) {
        hp = (hp * base + (unsigned char)p[i]) % mod;
        ht = (ht * base + (unsigned char)t[i]) % mod;
    }
    for (int s = 0; s + m <= n; ++s) {
        if (ht == hp && t.compare(s, m, p) == 0) ans.push_back(s);
        if (s + m < n) {
            ht = (ht - (unsigned char)t[s] * high) % mod;
            if (ht < 0) ht += mod;
            ht = (ht * base + (unsigned char)t[s+m]) % mod;
        }
    }
    return ans;
}
~~~

Preprocessing $O(m)$, rolling $O(n)$. Verification makes it always correct but worst-case $O(nm)$ if many collisions occur. With a random large modulus/base or two independent hashes, expected time is $O(n+m)$. A hash match without character verification is Monte Carlo and can return a false match.

Rabin–Karp is especially useful for many equal-length patterns: hash the patterns into a set and roll once over the text.

## 18.3 Prefix function and KMP

A **border** of a string is a proper prefix that is also a suffix. For pattern $P$, prefix function

$$
\pi[i]=\text{length of the longest proper prefix of }P[0..i]
\text{ that is also its suffix}.
$$

For `ababaca`, the prefix array is

~~~text
P:  a b a b a c a
pi: 0 0 1 2 3 0 1
~~~

When mismatch happens after $j$ matched characters, those characters need not be checked again. The next candidate border length is $\pi[j-1]$.

~~~cpp
vector<int> prefixFunction(const string& p) {
    vector<int> pi(p.size());
    for (int i = 1; i < (int)p.size(); ++i) {
        int j = pi[i-1];
        while (j > 0 && p[i] != p[j]) j = pi[j-1];
        if (p[i] == p[j]) ++j;
        pi[i] = j;
    }
    return pi;
}

vector<int> kmp(const string& text, const string& pat) {
    vector<int> ans;
    if (pat.empty()) {
        for (int i = 0; i <= (int)text.size(); ++i) ans.push_back(i);
        return ans;
    }
    vector<int> pi = prefixFunction(pat);
    int j = 0; // matched prefix length
    for (int i = 0; i < (int)text.size(); ++i) {
        while (j > 0 && text[i] != pat[j]) j = pi[j-1];
        if (text[i] == pat[j]) ++j;
        if (j == (int)pat.size()) {
            ans.push_back(i - (int)pat.size() + 1);
            j = pi[j-1]; // allows overlapping matches
        }
    }
    return ans;
}
~~~

Invariant after processing text position $i$: $j$ is the length of the longest prefix of $P$ equal to a suffix of $T[0..i]$.

Why linear: $j$ increases at most once per processed character, and every iteration of a failure loop strictly decreases $j$. Across the whole run, total increases/decreases are $O(n+m)$. Preprocessing $O(m)$, search $O(n)$, space $O(m)$.

Common bugs:

- falling back to $\pi[j]$ instead of $\pi[j-1]$;
- resetting $j=0$ after a match and missing overlaps;
- indexing the pattern when it is empty;
- confusing a proper prefix with the whole string.

## 18.4 Finite-automaton matcher

State $q\in\{0,\ldots,m\}$ is the number of pattern characters currently matched. Transition

$$
\delta(q,a)=
\text{length of longest prefix of }P
\text{ that is a suffix of }P[0..q-1]a.
$$

Precompute a table for all states and alphabet symbols, then scan text with one transition per character. Search is $O(n)$; a direct preprocessing is $O(m^3|\Sigma|)$, but prefix-function reuse reduces it to $O(m|\Sigma|)$. It is attractive when the same pattern is searched in many texts and the alphabet is small.

KMP can be viewed as storing only failure transitions rather than the full automaton table.

## 18.5 Z algorithm

For string $S$, $Z[i]$ is the length of the longest substring starting at $i$ equal to a prefix of $S$. Maintain a rightmost matched interval $[L,R]$; reuse a previously computed Z value inside it, then extend only beyond $R$.

~~~cpp
vector<int> zFunction(const string& s) {
    int n = s.size();
    vector<int> z(n);
    for (int i = 1, l = 0, r = 0; i < n; ++i) {
        if (i <= r) z[i] = min(r - i + 1, z[i-l]);
        while (i + z[i] < n && s[z[i]] == s[i+z[i]]) ++z[i];
        if (i + z[i] - 1 > r) l = i, r = i + z[i] - 1;
    }
    return z;
}
~~~

Build $S=P+\# +T$ with separator not in either string. Positions in the text part where $Z[i]=m$ are occurrences. Time/space $O(n+m)$.

## 18.6 Choosing a matcher

| Need | Good choice |
|---|---|
| tiny one-off input | naive |
| guaranteed linear single pattern | KMP or Z |
| many equal-length patterns / plagiarism windows | Rabin–Karp |
| same pattern, many texts, small alphabet | automaton |
| many arbitrary patterns | trie + Aho–Corasick |
| excellent practical substring search | Boyer–Moore family / library search |

KMP’s guarantee is deterministic; Rabin–Karp’s linear claim is expected unless collision verification behavior is separately bounded.

---

# 19. FFT and polynomial multiplication

The syllabus explicitly names FFT and applications. The following is the complete recall path from polynomial coefficients to implementable convolution.

## 19.1 Why ordinary multiplication is quadratic

For

$$
A(x)=\sum_{i=0}^{n-1}a_i x^i,\qquad
B(x)=\sum_{j=0}^{m-1}b_j x^j,
$$

their product coefficient is a convolution:

$$
c_k=\sum_{i+j=k}a_i b_j.
$$

The nested-loop method takes $O(nm)$. In point-value representation, however, multiplication is pointwise. FFT converts coefficients to values and back quickly:

1. evaluate both polynomials at enough points;
2. multiply corresponding values;
3. interpolate.

## 19.2 DFT and roots of unity

For length $N$, let

$$
\omega_N=e^{2\pi i/N}.
$$

The discrete Fourier transform is

$$
y_k=\sum_{j=0}^{N-1}a_j\omega_N^{jk},
\qquad k=0,\ldots,N-1.
$$

This is polynomial evaluation at the $N$-th roots of unity. Direct computation is $O(N^2)$.

Root properties:

- $\omega_N^N=1$;
- roots are distinct;
- $\omega_N^{k+N/2}=-\omega_N^k$ for even $N$;
- squaring even-index roots gives $N/2$-th roots.

## 19.3 Cooley–Tukey divide and conquer

Split coefficients into even and odd indices:

$$
A(x)=A_e(x^2)+xA_o(x^2).
$$

Compute length-$N/2$ DFTs $E_k,O_k$. Then

$$
y_k=E_k+\omega_N^k O_k,
$$

$$
y_{k+N/2}=E_k-\omega_N^k O_k.
$$

The recurrence is

$$
T(N)=2T(N/2)+\Theta(N)=\Theta(N\log N).
$$

The inverse DFT uses $\omega_N^{-1}$ and divides every result by $N$:

$$
a_j=\frac1N\sum_{k=0}^{N-1}y_k\omega_N^{-jk}.
$$

## 19.4 Iterative FFT implementation

~~~cpp
using cd = complex<double>;
const double PI = acos(-1.0);

void fft(vector<cd>& a, bool invert) {
    int n = a.size();

    // Bit-reversal permutation.
    for (int i = 1, j = 0; i < n; ++i) {
        int bit = n >> 1;
        for (; j & bit; bit >>= 1) j ^= bit;
        j ^= bit;
        if (i < j) swap(a[i], a[j]);
    }

    for (int len = 2; len <= n; len <<= 1) {
        double angle = 2 * PI / len * (invert ? -1 : 1);
        cd wlen(cos(angle), sin(angle));
        for (int start = 0; start < n; start += len) {
            cd w(1);
            for (int j = 0; j < len/2; ++j) {
                cd u = a[start+j];
                cd v = a[start+j+len/2] * w;
                a[start+j] = u + v;
                a[start+j+len/2] = u - v;
                w *= wlen;
            }
        }
    }
    if (invert)
        for (cd& x : a) x /= n;
}

vector<long long> convolution(const vector<long long>& a,
                              const vector<long long>& b) {
    if (a.empty() || b.empty()) return {};
    int need = (int)a.size() + (int)b.size() - 1;
    int n = 1;
    while (n < need) n <<= 1;
    vector<cd> fa(a.begin(), a.end()), fb(b.begin(), b.end());
    fa.resize(n); fb.resize(n);
    fft(fa, false); fft(fb, false);
    for (int i = 0; i < n; ++i) fa[i] *= fb[i];
    fft(fa, true);
    vector<long long> c(need);
    for (int i = 0; i < need; ++i) c[i] = llround(fa[i].real());
    return c;
}
~~~

The sign convention may be swapped as long as forward and inverse are consistent. Bit reversal places data in the order needed for iterative butterfly stages.

Complexity:

- two forward FFTs + one inverse: $O(N\log N)$;
- pointwise multiplication: $O(N)$;
- space: $O(N)$;
- choose power-of-two $N\ge n+m-1$, or circular wraparound corrupts linear convolution.

## 19.5 Numerical and exactness issues

Floating-point roundoff grows with length and coefficient magnitude. Use:

- `llround`, not truncation;
- coefficient splitting for large integers;
- long double where appropriate;
- an **NTT** (number-theoretic transform) for exact modular convolution.

An NTT replaces complex roots by a primitive $N$-th root modulo prime $p$, requiring $N\mid p-1$. Inverse uses modular inverse of $N$. Multiple NTT primes plus CRT recover larger exact integer coefficients.

## 19.6 Applications

- fast polynomial and big-integer multiplication;
- signal/audio filtering and convolution;
- image filtering in the frequency domain;
- correlation and pattern matching;
- solving linear recurrences and generating-function computations.

The convolution theorem is the central answer:

$$
\operatorname{DFT}(a*b)
=\operatorname{DFT}(a)\odot\operatorname{DFT}(b).
$$

---

# 20. Reductions, P, NP, NP-hardness, and NP-completeness

## 20.1 Decision, search, and optimization

Examples for vertex cover:

- **Decision:** is there a cover of size at most $k$?
- **Search:** find such a cover.
- **Optimization:** find a minimum-size cover.

NP is formally a class of **decision problems**. An optimization problem is not literally “in NP” under that definition; its decision version may be NP-complete, while the optimization problem is called NP-hard.

The variants often polynomially simulate one another:

- optimization $\Rightarrow$ decision: compare optimum with $k$;
- decision $\Rightarrow$ optimum value: binary-search $k$;
- decision $\Rightarrow$ witness: use self-reduction. For SAT, tentatively set a variable false and ask if the remainder is satisfiable; keep it if yes, otherwise set true. For vertex cover, test inclusion/exclusion of vertices while modifying the instance.

This equivalence depends on polynomially bounded encodings and a self-reducible structure; state the particular construction rather than saying every imaginable search problem is automatically identical.

## 20.2 Complexity classes

**P:** decision problems solvable by a deterministic algorithm in polynomial time.

**NP:** decision problems whose YES instances have a polynomial-length certificate verifiable in polynomial time. Equivalently, solvable by a nondeterministic polynomial-time machine. NP means nondeterministic polynomial time, not “non-polynomial.”

Certifier definition: problem $X$ is in NP if there is polynomial-time $C(s,t)$ and polynomial $p$ such that

$$
s\in X\iff \exists t,\ |t|\le p(|s|),\ C(s,t)=\text{YES}.
$$

Examples:

- SAT certificate: truth assignment; evaluate all clauses.
- Hamiltonian-cycle certificate: ordered vertex list; check every vertex exactly once and every consecutive/wrap edge exists.
- Vertex-cover certificate: subset $S$; check $|S|\le k$ and every edge touches $S$.

Known containments:

$$
P\subseteq NP\subseteq EXP.
$$

Whether $P=NP$ is open.

**co-NP:** complements of NP problems; NO instances of an NP problem have short certificates. It is unknown whether $NP=coNP$. $P\subseteq NP\cap coNP$. Primality is in P; classical integer factor decision problems have NP/co-NP evidence and are not known NP-complete. Shor’s quantum algorithm solves factoring in quantum polynomial time, which does not imply a classical P algorithm.

## 20.3 Polynomial many-one reductions

$$
X\le_P Y
$$

means there is a polynomial-time mapping $f$ satisfying

$$
x\in X\iff f(x)\in Y.
$$

Interpretation: given a solver for $Y$, transform and solve $X$. Therefore:

- if $X\le_PY$ and $Y\in P$, then $X\in P$;
- if $X$ is NP-hard and $X\le_PY$, then $Y$ is NP-hard;
- if $Y\le_PX$, hardness of $X$ tells nothing about $Y$.

A reduction must prove both directions of the iff and must have polynomial construction size/time.

**NP-hard:** every problem in NP reduces to it. It need not be a decision problem, need not be in NP, and can even be undecidable.

**NP-complete:** both NP-hard and in NP.

Cook–Levin proves SAT NP-complete. Once one NP-complete problem is known, a normal proof that new problem $Y$ is NP-complete is:

1. show $Y\in NP$ by giving certificate/verifier;
2. choose a known NP-complete $X$;
3. construct $X\le_PY$;
4. prove YES iff YES and polynomial size/time.

If any NP-complete problem is in P, then $P=NP$. If $P\ne NP$, none is in P.

## 20.4 SAT and 3-SAT

A literal is variable $x$ or negation $\neg x$. A clause is an OR of literals; CNF is an AND of clauses. SAT asks whether a CNF formula is satisfiable. 3-SAT restricts each clause to three literals and remains NP-complete.

Do not confuse:

- 2-SAT is in P, solvable through SCC implications;
- 3-SAT is NP-complete;
- checking a proposed assignment is polynomial even though finding one is not known polynomial.

## 20.5 Independent set, vertex cover, and set cover

**Independent set:** no selected pair shares an edge.  
**Vertex cover:** every edge has at least one selected endpoint.

For any $S\subseteq V$:

$$
S\text{ independent}\iff V-S\text{ is a vertex cover}.
$$

Thus

$$
(G,k)_{\text{IS}}\mapsto(G,|V|-k)_{\text{VC}},
$$

and the reverse transformation is identical. The proof checks any edge: it cannot have both endpoints in an independent set exactly when at least one endpoint lies in the complement.

### Vertex cover $\le_P$ set cover

Given $G=(V,E)$:

- universe $U=E$;
- for each vertex $v$, set $S_v=\{e\in E:e\text{ incident to }v\}$;
- retain $k$.

Choosing at most $k$ vertices covering every edge is exactly choosing at most $k$ corresponding sets whose union is $U$.

### 3-SAT $\le_P$ independent set

For formula with $k$ clauses:

1. make one triangle of three literal vertices per clause;
2. connect vertices in different triangles when their literals contradict, $x$ versus $\neg x$;
3. ask for independent set of size $k$.

If the formula is satisfiable, choose one true literal from each clause. No two chosen literals contradict, so they form an independent set. Conversely, an independent set of size $k$ must choose exactly one vertex per clause triangle and cannot choose contradictory literals; assign those selected literals true and extend consistently. Every clause is satisfied.

This proves IS NP-hard; its easily checked vertex subset puts it in NP, so it is NP-complete. The IS–VC and VC–set-cover reductions then transfer hardness in the correct direction.

## 20.6 Hamiltonian cycle and TSP

A Hamiltonian cycle visits every vertex exactly once and returns to the start. It differs from an Euler cycle, which uses every **edge** exactly once and is polynomially testable.

### Directed Hamiltonian cycle $\le_P$ undirected Hamiltonian cycle

Replace each directed vertex $v$ by a forced path

$$
v_{in}-v_{mid}-v_{out}.
$$

For every directed edge $u\to v$, add undirected edge $u_{out}-v_{in}$. Degree constraints force a Hamiltonian cycle to traverse every gadget as a block; inter-gadget choices then encode directed edges. A directed Hamiltonian cycle maps directly to an undirected one, and contracting each forced gadget recovers a directed cycle (up to traversing the whole undirected cycle in the opposite orientation).

The slides also show 3-SAT reducing to directed Hamiltonian cycle via variable tracks and clause detours: the route’s direction through each variable gadget chooses true/false, and every clause node can be visited iff at least one chosen literal track offers its detour.

### Hamiltonian cycle $\le_P$ decision-TSP

Given unweighted $G=(V,E)$, build complete graph on $V$:

$$
w(u,v)=
\begin{cases}
1,&\{u,v\}\in E,\\
2,&\text{otherwise}.
\end{cases}
$$

Ask whether a tour of cost at most $|V|$ exists. A Hamiltonian cycle in $G$ uses $|V|$ weight-1 edges. Conversely, any tour of cost at most $|V|$ has exactly $|V|$ edges, all weight 1, so it is a Hamiltonian cycle in $G$.

Precise terminology:

- **Decision TSP** (“is there a tour of cost $\le B$?”) is NP-complete.
- **Optimization TSP** (“find the minimum tour”) is NP-hard; calling an optimization problem NP-complete is informal/imprecise.

## 20.7 3-coloring and register allocation

Three-coloring asks whether adjacent vertices can receive different colors from three choices.

In the 3-SAT reduction:

- make special triangle TRUE, FALSE, BASE, forcing three distinct reference colors;
- for each variable, connect $x_i$ and $\neg x_i$ to each other and to BASE, so one is TRUE and the other FALSE;
- attach a constant-size clause gadget whose three literal inputs can extend to a valid coloring iff at least one input is TRUE.

Therefore a satisfying assignment extends to a coloring, and a coloring defines an assignment satisfying every clause. Construction size is linear in variables plus clauses.

**Register allocation:** create an interference graph:

- vertex = live program variable;
- edge = two variables simultaneously live, so they cannot share a register;
- color = register.

Allocation with $k$ registers is graph $k$-coloring. For fixed $k\ge3$, the general decision problem is NP-complete. Real compilers use simplification, spilling, coalescing, and heuristics rather than solving every instance optimally.

## 20.8 3-dimensional matching

Given disjoint sets $X,Y,Z$, each size $n$, and allowed triples $T\subseteq X\times Y\times Z$, ask whether $n$ triples can be chosen with no coordinate repeated. A proposed set of triples is easy to verify, but finding a perfect 3D matching is NP-complete. This is a sharp contrast with ordinary bipartite matching, which max flow solves in polynomial time.

The 3-SAT gadget family creates variable-choice triples and clause/cleanup triples so selecting disjoint triples corresponds to one consistent truth choice per variable and one satisfied literal per clause. The important reduction invariant is “every element used exactly once,” which prevents choosing both truth settings.

## 20.9 3-SAT $\le_P$ subset sum

The classic no-carry decimal construction is worth remembering:

1. Make one digit column per variable and one per clause.
2. For variable $x_i$, make numbers $v_i$ and $v'_i$. Both have digit 1 in variable column $i$. In clause column $j$, $v_i$ has 1 if $x_i$ occurs in clause $j$, and $v'_i$ has 1 if $\neg x_i$ occurs.
3. For each clause column add two slack numbers having digit 1 and digit 2 only in that column.
4. Target has digit 1 in each variable column and 4 in each clause column.

The target’s variable digits force exactly one of $v_i,v'_i$, encoding a truth assignment. A clause gets 1–3 from chosen true-literal numbers; slack 1 and/or 2 can raise it to 4 exactly when it received at least 1. No digit sum reaches 10, so no carries interfere.

Thus the target sum is achievable iff every clause has a true literal.

### Subset sum $\le_P$ knapsack

Given positive numbers $a_i$ and target $K$, make item $i$ with

$$
w_i=v_i=a_i,
$$

capacity $W=K$, target value $V=K$. Weight at most $K$ and value at least $K$ force equality, hence exactly a subset sum of $K$.

## 20.10 Pseudo-polynomial is not polynomial

Subset sum/knapsack DP $O(nW)$ is polynomial in numerical capacity $W$, but the binary encoding of $W$ has only $\Theta(\log W)$ bits. Hence this is pseudo-polynomial and does not contradict NP-completeness.

Strong NP-hardness roughly means hardness persists even when numeric values are polynomially bounded; such problems are less likely to admit pseudo-polynomial algorithms.

## 20.11 Fast viva reduction checklist

When shown a proposed reduction $A\to B$, ask:

1. Which problem is already hard? It must be on the left.
2. Can the instance be built in polynomial time and size?
3. Did we prove both YES $\Rightarrow$ YES and YES $\Leftarrow$ YES?
4. Are thresholds transformed correctly, such as $k\mapsto n-k$?
5. Are we proving hardness only, or also membership in NP?
6. Is it a decision version? If not, say NP-hard rather than NP-complete.

---

# 21. Coping with hardness: special cases, DP, approximation, and exact exponential algorithms

NP-hard does not mean “never solvable.” The slides emphasize:

- exploit a special graph class or small parameter;
- use dynamic programming/pseudo-polynomial time;
- use an approximation algorithm with proof;
- use a heuristic with no formal guarantee;
- use backtracking/branch-and-bound;
- use a faster exact exponential algorithm.

## 21.1 Maximum independent set in a forest

Unweighted greedy:

1. choose any leaf $v$ with neighbor $u$;
2. include $v$;
3. delete $u,v$;
4. after all edges disappear, include remaining isolated vertices.

Exchange proof: some optimum contains either $v$ or $u$. If it contains $u$, replace $u$ by leaf $v$; no other chosen vertex is adjacent to $v$. Therefore an optimum containing $v$ exists, making the greedy choice safe. With degree bookkeeping, time $O(V)$.

This fails on general graphs because a low-degree-looking local choice may destroy a better global combination.

## 21.2 Weighted independent set on a tree

Root tree arbitrarily. For each node $u$:

$$
IN[u]=w_u+\sum_{v\in children(u)}OUT[v],
$$

$$
OUT[u]=\sum_{v\in children(u)}\max(IN[v],OUT[v]).
$$

Compute postorder; answer $\max(IN[root],OUT[root])$. To reconstruct, if parent was chosen, exclude child; otherwise choose the better child state.

~~~cpp
pair<long long,long long>
treeIS(int u, int p, const vector<vector<int>>& g,
       const vector<long long>& w) {
    long long in = w[u], out = 0;
    for (int v : g[u]) if (v != p) {
        auto [cin, cout] = treeIS(v, u, g, w);
        in += cout;
        out += max(cin, cout);
    }
    return {in, out};
}
~~~

Time $O(V)$, recursion space $O(V)$. The separator is a single parent edge; this is why the two states suffice.

## 21.3 Planarity and tractable restrictions

A planar graph can be drawn without crossing edges. Planarity testing is linear time. Many hard graph problems become polynomial on trees or restricted-width graphs, but not every planar restriction is easy:

- every planar graph is 4-colorable;
- deciding planar 3-colorability remains NP-complete;
- planar-map coloring and planar-graph coloring translate through region adjacency/duality constructions.

“Special case” must be proved; “planar looks simpler” is not enough.

## 21.4 Chaitin’s simplification algorithm

For $k$-coloring/register allocation:

~~~text
while graph nonempty:
    choose a vertex v with current degree < k
    push v
    delete v and incident edges
while stack nonempty:
    pop v
    assign a color unused by its already colored neighbors
~~~

When $v$ is restored it has fewer than $k$ colored neighbors, so a color exists. It always succeeds for $(k-1)$-degenerate graphs, including graphs whose maximum degree is at most $k-1$. On a general interference graph, getting stuck does not prove non-$k$-colorability; compilers choose a spill candidate and continue heuristically.

## 21.5 Approximation versus heuristic

For minimization, an $r$-approximation satisfies

$$
ALG(I)\le r\,OPT(I).
$$

For maximization, common conventions are $ALG\ge OPT/r$ or a $(1-\varepsilon)$ guarantee. A heuristic seeks a good answer quickly but has no proved worst-case quality. Both can be useful; only the approximation algorithm carries a theorem.

## 21.6 Vertex-cover 2-approximation

Repeatedly take any uncovered edge $(u,v)$, add both endpoints, and delete every incident edge.

~~~cpp
vector<int> vertexCover2Approx(
    int n, const vector<pair<int,int>>& edges) {
    vector<char> removed(edges.size()), chosen(n);
    vector<vector<int>> incident(n);
    for (int i = 0; i < (int)edges.size(); ++i) {
        incident[edges[i].first].push_back(i);
        incident[edges[i].second].push_back(i);
    }
    for (int i = 0; i < (int)edges.size(); ++i) if (!removed[i]) {
        auto [u,v] = edges[i];
        chosen[u] = chosen[v] = true;
        for (int e : incident[u]) removed[e] = true;
        for (int e : incident[v]) removed[e] = true;
    }
    vector<int> ans;
    for (int v = 0; v < n; ++v) if (chosen[v]) ans.push_back(v);
    return ans;
}
~~~

The chosen arbitrary edges form a matching $M$: after selecting one, all edges touching its endpoints disappear. Every vertex cover, including optimum $S^*$, needs at least one distinct endpoint for each matching edge, so $|S^*|\ge|M|$. Algorithm returns $2|M|$, hence

$$
|S|\le2|S^*|.
$$

Time $O(V+E)$. It is not generally optimal.

## 21.7 Knapsack dynamic programs

Items have weight $w_i$, value $v_i$, capacity $W$.

### DP by weight

$$
OPT(i,w)=
\begin{cases}
OPT(i-1,w),&w_i>w,\\
\max(OPT(i-1,w),OPT(i-1,w-w_i)+v_i),&w_i\le w.
\end{cases}
$$

Time $O(nW)$, table space $O(nW)$, or $O(W)$ with weights iterated downward:

~~~cpp
long long knapsack(const vector<int>& wt,
                   const vector<int>& val, int W) {
    vector<long long> dp(W+1);
    for (int i = 0; i < (int)wt.size(); ++i)
        for (int w = W; w >= wt[i]; --w)
            dp[w] = max(dp[w], dp[w-wt[i]] + val[i]);
    return *max_element(dp.begin(), dp.end());
}
~~~

Descending $w$ is what prevents using one 0–1 item repeatedly.

### DP by value

Let $DP[i][v]$ be minimum weight needed to achieve value at least $v$:

$$
DP(i,v)=\min(DP(i-1,v),DP(i-1,\max(0,v-v_i))+w_i).
$$

The largest $v$ with $DP(n,v)\le W$ is optimal. Time $O(n\sum v_i)$.

## 21.8 Knapsack FPTAS

First remove every item with `w_i>W`, because it cannot occur in a feasible solution; handle the empty/zero-value case separately. For positive values and accuracy $\varepsilon>0$, let $V_{\max}=\max\{v_i:w_i\le W\}$ and

$$
K=\frac{\varepsilon V_{\max}}{n},\qquad
v'_i=\left\lfloor\frac{v_i}{K}\right\rfloor.
$$

Run value-based DP on scaled $v'_i$. Rounding loses less than $K$ per chosen item, at most $nK=\varepsilon V_{\max}\le\varepsilon OPT$, because the best remaining single item is feasible and therefore $V_{\max}\le OPT$. Thus the result has value at least $(1-\varepsilon)OPT$. Equivalent ratio notation may call this a $1+\varepsilon$-style scheme after parameter conversion.

Since $\sum v'_i=O(n^2/\varepsilon)$, time is $O(n^3/\varepsilon)$. This is an FPTAS: polynomial in input size and $1/\varepsilon$.

## 21.9 Metric TSP 2-approximation

Assume symmetric distances, nonnegative, and triangle inequality.

1. compute an MST $T$;
2. double every tree edge, making all degrees even;
3. find an Euler tour;
4. shortcut repeated vertices to obtain a Hamiltonian tour.

Proof:

$$
w(T)\le OPT
$$

because deleting one edge from an optimal tour gives a spanning tree. The doubled Euler walk costs $2w(T)\le2OPT$. Triangle inequality ensures shortcutting cannot increase cost. Therefore returned tour costs at most $2OPT$.

Without triangle inequality, shortcutting may be arbitrarily expensive and general TSP has no such guarantee.

## 21.10 Held–Karp exact TSP

Fix city 0. Let

$$
dp[S][v]=\text{minimum cost of a path from 0 to }v
\text{ visiting exactly subset }S,
$$

where $0,v\in S$.

$$
dp[\{0\}][0]=0,
$$

$$
dp[S][v]=\min_{u\in S-\{v\}}
\{dp[S-\{v\}][u]+w(u,v)\}.
$$

Answer:

$$
\min_{v\ne0}dp[All][v]+w(v,0).
$$

~~~cpp
long long heldKarp(const vector<vector<long long>>& w) {
    int n = w.size(), full = 1 << n;
    const long long INF = numeric_limits<long long>::max()/4;
    vector<vector<long long>> dp(full, vector<long long>(n, INF));
    dp[1][0] = 0;
    for (int mask = 1; mask < full; ++mask) {
        if (!(mask & 1)) continue;
        for (int u = 0; u < n; ++u) if (mask & (1 << u)) {
            if (dp[mask][u] == INF) continue;
            for (int v = 1; v < n; ++v) if (!(mask & (1 << v))) {
                int next = mask | (1 << v);
                dp[next][v] = min(dp[next][v], dp[mask][u] + w[u][v]);
            }
        }
    }
    long long ans = INF;
    for (int v = 1; v < n; ++v)
        ans = min(ans, dp[full-1][v] + w[v][0]);
    return n == 1 ? 0 : ans;
}
~~~

Time $O(n^2 2^n)$, space $O(n2^n)$. This is exponentially faster than enumerating $(n-1)!$ tours but still explodes. Euclidean TSP additionally has a PTAS; strong solvers combine cuts, branch-and-bound, and engineering.

---

# 22. Backtracking and branch-and-bound **[Backtracking-BB-207, 18 pages; BranchBound-TSP-207, 20 image-heavy pages]**

These two decks develop **smart exhaustive search**. The worst-case search space remains exponential, but a partial solution is abandoned as soon as a logically safe test proves that none of its descendants can matter.

## 22.1 State-space tree, promising nodes, and pruning

A **state-space tree** represents decisions rather than input graph edges:

- the root is the empty/initial partial solution;
- each edge makes one choice;
- a node stores the choices made so far and any incremental information needed to extend them;
- a leaf is a complete candidate, not necessarily a feasible or optimal one;
- a **promising** node may still lead to a required solution;
- a **non-promising** node cannot lead to a feasible solution, or in optimization cannot beat the best feasible solution already known;
- **pruning** means not generating that node's descendants.

The central proof obligation is one sentence: **why can no pruned descendant be an answer that we need?** A test that merely says a branch “looks bad” may be useful for ordering, but it is not automatically safe for pruning.

| Feature | Backtracking | Branch-and-bound |
|---|---|---|
| Primary use in the slides | feasibility, enumeration, constraint problems | optimization |
| Typical node order | depth-first recursion | FIFO, LIFO, or most-promising/best-first |
| Pruning reason | violates a constraint or cannot reach a solution | infeasible, or optimistic bound cannot beat incumbent |
| Main memory | current path, usually `O(depth)` | live-node set; best-first can be exponential |
| Examples | n-Queens, subset sum | 0-1 knapsack, minimum TSP |

This is a typical-use distinction, not a law of nature: DFS backtracking can optimize by maintaining an incumbent, and branch-and-bound can use DFS. “Backtracking” is also not just another word for recursion. It means **choose, explore, undo**, with systematic pruning; it can be implemented iteratively with an explicit stack.

## 22.2 Generic backtracking template and correctness

~~~text
BACKTRACK(state):
    if state is a complete feasible solution:
        report/update it
        return whether the search may stop

    if no completion of state can be a required solution:
        return false                         // prune

    for each legal next choice, in a chosen order:
        apply choice to state
        if BACKTRACK(state) and only one solution is needed:
            return true
        undo choice from state

    return false
~~~

Useful incremental state avoids recomputing every constraint from scratch. Child order can dramatically change when the first solution is found, but it does not change completeness if every unpruned child is eventually explored.

**Correctness skeleton.** Every full candidate corresponds to one root-to-leaf decision sequence. At a node, the algorithm either explores each possible next decision or prunes the whole subtree using a necessary condition. If the pruning condition is sound, no valid required leaf is removed. Induction on remaining depth therefore shows that every required solution is eventually reported; returning at the first solution is sound when only one is requested.

If branching factor is at most `b` and depth is `d`, the crude worst case is

$$
1+b+b^2+\cdots+b^d=O(b^d).
$$

Pruning improves the number of nodes actually visited, not the general worst-case class.

## 22.3 n-Queens backtracking

Place one queen in each row of an `n x n` board. Once row `r` is being processed, the row constraint is already satisfied; only three constant-time conflicts need tracking:

- column `c`;
- downward diagonal `r-c`, shifted by `n-1` to make an array index;
- upward diagonal `r+c`.

For `n=4`, the two column sequences are `[1,3,0,2]` and `[2,0,3,1]`. The first means queens at `(0,1),(1,3),(2,0),(3,2)`.

~~~cpp
class NQueens {
    int n;
    vector<int> colAtRow;
    vector<char> usedCol, usedDown, usedUp;

    bool place(int r) {
        if (r == n) return true;

        for (int c = 0; c < n; ++c) {
            int down = r - c + n - 1;
            int up = r + c;
            if (usedCol[c] || usedDown[down] || usedUp[up]) continue;

            colAtRow[r] = c;                         // choose
            usedCol[c] = usedDown[down] = usedUp[up] = true;

            if (place(r + 1)) return true;           // explore

            usedCol[c] = usedDown[down] = usedUp[up] = false;
            colAtRow[r] = -1;                        // undo
        }
        return false;
    }

public:
    explicit NQueens(int size)
        : n(size), colAtRow(n, -1), usedCol(n),
          usedDown(2*n - 1), usedUp(2*n - 1) {}

    optional<vector<int>> oneSolution() {
        if (!place(0)) return nullopt;
        return colAtRow;
    }
};
~~~

To enumerate all solutions, record a copy at `r==n`, return to the caller, and do not stop after the first recursive success. With unique columns, at most

$$
n(n-1)\cdots1=n!
$$

placements reach the deepest levels; constant-time conflict checks make the common worst-case statement `O(n!)`, with `O(n)` recursion/state apart from stored answers. This is an upper bound, not a claim that every instance visits every permutation.

**Viva trace:** at row 0 try column 0. When later rows have no safe column, undo the last queen, try its next column, and continue. A crossed-out child in the deck is a partial board whose next queen already attacks an earlier queen.

## 22.4 Subset-sum backtracking and when its pruning is valid

Given positive integers `a[0..n-1]` and target `T`, level `i` decides **include or exclude** `a[i]`. The full binary tree has `2^n` leaves, but the slide gives two safe prunes:

1. if `sum > T`, adding more positive numbers cannot bring it down;
2. if `sum + suffix[i] < T`, even taking every remaining number cannot reach `T`.

Here `suffix[i]=a[i]+...+a[n-1]`.

~~~cpp
bool subsetSumOne(const vector<int>& a, int target,
                  vector<int>& chosen) {
    int n = a.size();
    vector<long long> suffix(n + 1, 0);
    for (int i = n - 1; i >= 0; --i)
        suffix[i] = suffix[i + 1] + a[i];

    function<bool(int,long long)> dfs = [&](int i, long long sum) {
        if (sum == target) return true;
        if (i == n) return false;
        if (sum > target) return false;
        if (sum + suffix[i] < target) return false;

        chosen.push_back(a[i]);                       // include
        if (dfs(i + 1, sum + a[i])) return true;
        chosen.pop_back();                            // undo

        if (dfs(i + 1, sum)) return true;             // exclude
        return false;
    };

    chosen.clear();
    return dfs(0, 0);
}
~~~

Trace the deck's `a={3,5,6,7}`, `T=15`:

- include `3,5,6` gives 14; including 7 overshoots;
- excluding 7 leaves 14 with no remaining value, so the “too small” test prunes;
- undo 6, then include 7: `3+5+7=15`.

Worst case remains `Theta(2^n)` and stack space `O(n)`. The two inequalities above rely on **nonnegative/positive** remaining values. With negative numbers, `sum>T` may later fall and a simple suffix sum is not a valid maximum-reachable bound; use different lower/upper reachable-sum bounds or a different algorithm. Sorting large positive values first may find a solution or overshoot sooner, but suffix values must be recomputed after sorting.

## 22.5 Branch-and-bound: incumbent, optimistic bound, and live nodes

For optimization, maintain:

- an **incumbent**: the best complete feasible solution found so far;
- a set of **live nodes** not yet expanded;
- at each live node, an optimistic bound on the best descendant it could possibly produce.

The bound direction is the most common viva trap:

| Problem | Safe optimistic bound for node `u` | Incumbent | Prune `u` when |
|---|---|---|---|
| minimize | `LB(u) <=` every feasible descendant value | best known upper bound `U` | `LB(u) >= U` |
| maximize | `UB(u) >=` every feasible descendant value | best known lower bound `L` | `UB(u) <= L` |

Equality can be pruned when only one optimum is needed. Do not prune equality if every distinct optimal solution must be enumerated.

~~~text
incumbent = +infinity for minimization, -infinity for maximization
LIVE = {root}

while LIVE is not empty:
    u = select and remove a live node
    if u is infeasible or u's bound cannot improve incumbent:
        continue
    if u is a complete feasible solution:
        update incumbent and remembered solution
        continue
    for each child v of u:
        compute incremental state and a valid optimistic bound
        if v remains feasible and its bound can improve incumbent:
            insert v into LIVE

return incumbent and its solution
~~~

**Why pruning is exact for minimization:** if `LB(u)>=U`, every feasible descendant `x` satisfies `cost(x)>=LB(u)>=U`; therefore none improves the incumbent. Maximization is the symmetric proof.

## 22.6 FIFO, LIFO, and best-bound selection

Branch-and-bound does not prescribe one traversal:

- **FIFO branch-and-bound** uses a queue and explores by level, like BFS.
- **LIFO branch-and-bound** uses a stack/recursion, like DFS; it uses little memory and may find a complete incumbent quickly.
- **best-bound / least-cost branch-and-bound** uses a priority queue: smallest lower bound first for minimization, largest upper bound first for maximization.

The image-heavy TSP deck orders the live-node list first by bounding value and, on a tie, places the deeper node first because it is closer to a complete tour. This is a tie-breaking heuristic, not part of the optimality proof.

A feasible solution found early is valuable because it tightens the incumbent and triggers more pruning. A greedy solution is therefore often used as the initial incumbent even though greediness alone does not prove optimality.

The “stop at first solution” variant in the slide needs a condition: it is sound when the priority queue is ordered by a valid bound and the first complete node removed has an exact objective equal to its key, or more generally when no remaining live bound can beat it. It is not sound merely because an arbitrary heuristic called one node “most promising.”

## 22.7 0-1 knapsack branch-and-bound

For item `i`, weight `w_i>0`, value `v_i>=0`, and capacity `W`, branch on taking or skipping the next item. A node stores `(level, currentWeight, currentValue, upperBound)`.

Sort by nonincreasing ratio `v_i/w_i`. The slide's quick upper bound is

$$
UB=value+(W-weight)\times\text{ratio of the next item}.
$$

Because every later ratio is no larger, pretending that all remaining capacity can earn the next ratio is optimistic and safe. For the slide table

| item | weight | value | ratio |
|---:|---:|---:|---:|
| 1 | 4 | 40 | 10 |
| 2 | 7 | 42 | 6 |
| 3 | 5 | 25 | 5 |
| 4 | 3 | 12 | 4 |

with `W=10`, this gives root `UB=100`, after taking item 1 `UB=40+6*6=76`, and after rejecting item 1 `UB=10*6=60`. The optimum is items 1 and 3: weight 9, value 65.

A tighter standard bound solves the remaining **fractional** knapsack relaxation: take whole remaining items by ratio and, if necessary, a fraction of the next item. Allowing fractions can only improve a maximization result, so it is an upper bound on the 0-1 descendants.

~~~cpp
struct KItem {
    int weight, value;
    double ratio;
};

struct KNode {
    int level;          // items 0..level have been decided
    int weight, value;
    double upper;
};

double fractionalUpper(const KNode& u,
                       const vector<KItem>& item, int W) {
    if (u.weight > W) return -numeric_limits<double>::infinity();

    int totalWeight = u.weight;
    double result = u.value;
    int j = u.level + 1;

    while (j < (int)item.size() &&
           totalWeight + item[j].weight <= W) {
        totalWeight += item[j].weight;
        result += item[j].value;
        ++j;
    }
    if (j < (int)item.size())
        result += (W - totalWeight) * item[j].ratio;
    return result;
}

int knapsackBranchAndBound(vector<pair<int,int>> weightValue, int W) {
    vector<KItem> item;
    for (auto [w,v] : weightValue)
        if (w > 0 && v >= 0)
            item.push_back({w, v, (double)v / w});

    sort(item.begin(), item.end(), [](const KItem& a, const KItem& b) {
        return a.ratio > b.ratio;
    });

    struct LowerUpperFirst {
        bool operator()(const KNode& a, const KNode& b) const {
            return a.upper < b.upper;                 // maximum upper first
        }
    };
    priority_queue<KNode, vector<KNode>, LowerUpperFirst> live;

    KNode root{-1, 0, 0, 0};
    root.upper = fractionalUpper(root, item, W);
    live.push(root);
    int best = 0;

    while (!live.empty()) {
        KNode u = live.top(); live.pop();
        if (u.upper <= best) continue;

        int i = u.level + 1;
        if (i == (int)item.size()) continue;

        KNode take{i,
                   u.weight + item[i].weight,
                   u.value + item[i].value,
                   0};
        if (take.weight <= W) {
            best = max(best, take.value);              // new incumbent
            take.upper = fractionalUpper(take, item, W);
            if (take.upper > best) live.push(take);
        }

        KNode skip{i, u.weight, u.value, 0};
        skip.upper = fractionalUpper(skip, item, W);
        if (skip.upper > best) live.push(skip);
    }
    return best;
}
~~~

Store parent links plus the take/skip decision if the chosen item set must be reconstructed. Sorting costs `O(n log n)`. In the worst case there are `Theta(2^n)` nodes; the shown bound scan costs `O(n)` per node, so a simple worst-case implementation is `O(n2^n)` time with exponential live memory. Good bounds usually cut far more nodes, but do not remove that worst case.

## 22.8 TSP state space, incumbents, and lower bounds

Fix starting city `A` (or 0) to remove rotational duplicates. A node is a partial path

$$
A\to v_1\to\cdots\to v_k.
$$

Its children append one unvisited city. At depth `k`, roughly `n-k` choices remain; complete leaves represent tours after adding the return edge to `A`. Brute force therefore examines `(n-1)!` orders, or half that in a symmetric graph if reversed tours are also identified.

### Initial feasible tour

Nearest-neighbor greedily chooses the cheapest edge to an unvisited city and finally returns to the start. It supplies an **upper bound/incumbent** for minimum TSP, not a proof. In the first image-deck matrix it gives

`A-E-C-G-F-D-B-H-A`, cost 28.

The search later proves that every remaining live node has lower bound at least 28, certifying optimality. In the deck's second matrix, the initial candidate costs 32; branch-and-bound finds `A-C-E-D-B-F-A` of cost 31, tightens the incumbent to 31, and removes every node with lower bound at least 31.

### Directed minimum-outgoing relaxation

Suppose a partial path `P` ends at `last`, has fixed-edge cost `g(P)`, and unvisited set `U`. Every completion must still choose one outgoing edge from `last` and from every vertex in `U`. Therefore

$$
LB(P)=g(P)+
\sum_{u\in\{last\}\cup U}\min_{v\ne u} c(u,v)
$$

is a safe lower bound. The independently chosen minimum edges may revisit vertices or form subtours, so this relaxed object may not be a tour—but that only makes the number *smaller* and hence safely optimistic. Forbidden destinations can be removed to tighten the bound as long as every edge allowed by a real completion remains available.

At the root of the first deck example, the row minima are `4,2,5,5,1,2,3,3`, summing to 25. Thus `25 <= OPT <= 28`. Appending a city replaces the relaxed outgoing choice of the previous last city by an actual paid edge and recomputes the remaining relaxation. A node with `LB>=28` cannot improve the incumbent and is crossed out.

### Symmetric two-incidence relaxation

In an undirected tour every vertex has degree two. If `m_1(v),m_2(v)` are its two cheapest incident edges, then at the root

$$
LB=\frac12\sum_v\bigl(m_1(v)+m_2(v)\bigr).
$$

Any tour supplies two incident edges at each vertex, no cheaper than those two; division by two corrects the fact that each undirected tour edge is counted at both endpoints. For a partial tour, fixed edges consume degree slots: add their actual cost and relax only the remaining incident requirements. The slide describes the same principle as choosing necessary incoming/outgoing incidences for remaining vertices, with only an entry to the start and an exit from the current last vertex still required. Do not blindly add the full root formula to `g(P)`, which would double-count fixed edges.

A stronger lower bound usually prunes more but costs more to compute. Correctness needs optimism, not tightness.

## 22.9 Best-first TSP branch-and-bound code

The following exact implementation uses the directed minimum-outgoing relaxation. It assumes a complete nonnegative cost matrix; a very large `INF` may represent a missing edge. It starts without a greedy incumbent for compactness—seeding `best` and `bestTour` with nearest neighbor improves pruning without changing correctness.

~~~cpp
struct TNode {
    vector<int> path;
    vector<char> used;
    long long cost, lower;
};

pair<long long, vector<int>>
tspBranchAndBound(const vector<vector<long long>>& w) {
    const long long INF = numeric_limits<long long>::max() / 4;
    int n = w.size();
    if (n == 0) return {0, {}};
    if (n == 1) return {0, {0, 0}};

    auto lowerBound = [&](const vector<int>& path,
                          const vector<char>& used,
                          long long cost) {
        int last = path.back();
        if ((int)path.size() == n) {
            if (w[last][0] >= INF) return INF;
            return cost + w[last][0];
        }

        long long lb = cost;
        for (int u = 0; u < n; ++u) {
            if (u != last && used[u]) continue;        // outgoing already fixed
            long long cheapest = INF;
            for (int v = 0; v < n; ++v)
                if (v != u) cheapest = min(cheapest, w[u][v]);
            if (cheapest >= INF || lb > INF - cheapest) return INF;
            lb += cheapest;
        }
        return lb;
    };

    struct SmallerLowerFirst {
        bool operator()(const TNode& a, const TNode& b) const {
            if (a.lower != b.lower) return a.lower > b.lower;
            return a.path.size() < b.path.size();      // deeper breaks a tie
        }
    };
    priority_queue<TNode, vector<TNode>, SmallerLowerFirst> live;

    TNode root{{0}, vector<char>(n, false), 0, 0};
    root.used[0] = true;
    root.lower = lowerBound(root.path, root.used, root.cost);
    live.push(root);

    long long best = INF;
    vector<int> bestTour;

    while (!live.empty()) {
        TNode u = live.top();
        live.pop();
        if (u.lower >= best) continue;

        int last = u.path.back();
        if ((int)u.path.size() == n) {
            if (w[last][0] < INF && u.cost <= INF - w[last][0]) {
                long long exact = u.cost + w[last][0];
                if (exact < best) {
                    best = exact;
                    bestTour = u.path;
                    bestTour.push_back(0);
                }
            }
            continue;
        }

        for (int v = 1; v < n; ++v) if (!u.used[v]) {
            if (w[last][v] >= INF || u.cost > INF - w[last][v]) continue;
            TNode child = u;
            child.path.push_back(v);
            child.used[v] = true;
            child.cost += w[last][v];
            if (child.cost >= best) continue;          // nonnegative weights
            child.lower = lowerBound(child.path, child.used, child.cost);
            if (child.lower < best) live.push(std::move(child));
        }
    }
    return {best, bestTour};
}
~~~

The bound computation shown is `O(n^2)` per generated node in the most literal accounting (`O(n)` remaining tails, each scanning `O(n)` destinations). Precomputed global row minima reduce this relaxed version toward `O(n)` per node, while tighter allowed-edge bounds need more updates. Worst-case search still generates `Theta((n-1)!)` partial permutations and can store exponentially many live nodes.

## 22.10 Exactness, performance, and viva traps

**Exactness invariant:** the incumbent is always a real feasible solution; every live node represents unexamined candidates; every removed node is either expanded, infeasible, or proved unable to improve the incumbent. When no live node can improve, the incumbent is optimal.

| Problem | Unpruned candidate space | Typical safe prune/bound |
|---|---:|---|
| n-Queens | at most `n!` column permutations | used column/diagonals |
| subset sum | `2^n` subsets | overshoot and insufficient remainder, for positive values |
| 0-1 knapsack | `2^n` take/skip leaves | fractional-knapsack upper bound |
| fixed-start TSP | `(n-1)!` city orders | outgoing/degree-based lower bound |

High-yield traps:

1. **Lower versus upper:** minimum problems prune with a lower bound against a feasible upper incumbent; maximum problems do the reverse.
2. **Bound versus estimate:** a value used only to order nodes may be arbitrary; a value used to prune must satisfy a proved inequality for every descendant.
3. **Incumbent versus bound:** an incumbent comes from a complete feasible solution. A relaxed fractional knapsack or malformed TSP edge set is not an incumbent.
4. **Greedy tour:** it supplies a candidate and faster pruning, not optimality by itself.
5. **Backtracking undo:** restore every changed flag, sum, path entry, or count before trying the sibling.
6. **Invalid subset pruning:** `sum>T` is unsafe when negative remaining numbers exist.
7. **First-solution termination:** sound for feasibility; for optimization, stop only when the live bounds certify that nothing can improve it.
8. **Worst case:** spectacular pruning on one trace does not make an NP-hard problem polynomial.

---

# 23. Algorithm Engineering additions from the current source folder

The current Algorithm Engineering folder repeats flow, FFT, reductions, and NP-completeness, but it also adds four useful viva topics that were not explicit enough in the old volume.

## 23.1 Stable matching and Gale–Shapley

### Problem and blocking pair

There are two sets of equal size, traditionally proposers $M$ and receivers $W$. Each participant has a strict preference ordering over the opposite set. A matching is **stable** if it has no **blocking pair** $(m,w)$ such that:

1. $m$ prefers $w$ to the partner assigned to $m$; and
2. $w$ prefers $m$ to the partner assigned to $w$.

A stable matching need not maximize total preference score, minimize dissatisfaction, or be the only stable matching. Stability means that no unmatched pair would jointly abandon their assigned partners.

### Proposer-oriented deferred acceptance

1. Initially every proposer is free.
2. A free proposer proposes to the highest-ranked receiver not yet proposed to.
3. A free receiver tentatively accepts.
4. An engaged receiver keeps the more-preferred of the current partner and the new proposer; the rejected proposer becomes free.
5. Continue until no proposer is free.

“Tentative” is essential: a receiver may later replace the current partner with a more-preferred proposer.

```cpp
// prefM[m] lists receivers from most to least preferred.
// rankW[w][m] is smaller when receiver w prefers proposer m more.
vector<int> galeShapley(const vector<vector<int>>& prefM,
                       const vector<vector<int>>& rankW) {
    int n = (int)prefM.size();
    vector<int> nextChoice(n, 0);
    vector<int> partnerM(n, -1), partnerW(n, -1);
    queue<int> freeM;
    for (int m = 0; m < n; ++m) freeM.push(m);

    while (!freeM.empty()) {
        int m = freeM.front();
        freeM.pop();

        int w = prefM[m][nextChoice[m]++];
        if (partnerW[w] == -1) {
            partnerW[w] = m;
            partnerM[m] = w;
        } else {
            int old = partnerW[w];
            if (rankW[w][m] < rankW[w][old]) {
                partnerW[w] = m;
                partnerM[m] = w;
                partnerM[old] = -1;
                freeM.push(old);
            } else {
                freeM.push(m);
            }
        }
    }
    return partnerM;
}
```

### Why it terminates and why it is stable

- A proposer never proposes to the same receiver twice.
- There are only $n^2$ possible proposals, so the algorithm terminates in $O(n^2)$ time after the receiver-rank table is built.
- A receiver’s tentative partner can only improve according to that receiver’s preference.

Suppose the final matching has a blocking pair $(m,w)$. Proposer $m$ must have proposed to $w$ before reaching the final, less-preferred partner. Receiver $w$ rejected $m$ immediately or later. At that moment $w$ held someone preferred to $m$, and the held partner only improved afterward. Therefore $w$ cannot prefer $m$ to the final partner—a contradiction.

With complete strict preferences, proposer-oriented Gale–Shapley returns the **proposer-optimal** stable matching and the receiver-pessimal stable matching among all stable matchings. Switching who proposes changes this bias.

### Viva traps

- Stable does not mean globally maximum-weight.
- One side’s optimality is only among **stable** matchings.
- Ties and incomplete preference lists require variants and can change existence/optimality properties.

## 23.2 Augmenting-path bipartite matching without building a flow network

The flow reduction is conceptually clean. The course source also shows the direct Kuhn/DFS view.

A matching is maximum iff there is no augmenting path relative to it. An augmenting path alternates:

```text
unmatched edge, matched edge, unmatched edge, ...
```

and begins/ends at unmatched vertices. Flipping matched/unmatched status along the path increases matching size by one.

```cpp
vector<vector<int>> adj;   // left vertex -> right vertices
vector<int> matchRight;    // matched left vertex, or -1
vector<char> seenLeft;

bool augment(int u) {
    if (seenLeft[u]) return false;
    seenLeft[u] = true;

    for (int v : adj[u]) {
        if (matchRight[v] == -1 || augment(matchRight[v])) {
            matchRight[v] = u;
            return true;
        }
    }
    return false;
}

int maximumMatching(int nLeft, int nRight) {
    matchRight.assign(nRight, -1);
    int answer = 0;
    for (int u = 0; u < nLeft; ++u) {
        seenLeft.assign(nLeft, false); // fresh search per attempt
        answer += augment(u);
    }
    return answer;
}
```

One DFS attempt is $O(E)$; trying all left vertices gives $O(VE)$ in a simple bound. Hopcroft–Karp finds a maximal set of shortest augmenting paths per phase and improves this to $O(E\sqrt V)$.

**Do not confuse these:**

- maximal matching: no edge can be added directly;
- maximum matching: largest possible cardinality;
- stable matching: no blocking pair under preferences.

## 23.3 Minimum-cost directed arborescence

An $r$-arborescence is a directed spanning tree rooted at $r$:

- root $r$ has indegree zero;
- every other vertex has indegree one;
- every vertex is reachable from $r$.

It is not an ordinary undirected MST. Prim/Kruskal and the undirected cut property do not directly solve it.

### Chu–Liu/Edmonds contraction idea

For every vertex $v\ne r$, choose a minimum-weight incoming edge.

- If some nonroot vertex has no incoming edge, no rooted spanning arborescence exists.
- If the chosen edges contain no directed cycle, they are the optimum arborescence.
- If they contain a directed cycle $C$, every feasible arborescence must break that cycle by entering one cycle vertex from outside. Contract $C$ into one supervertex and solve the smaller problem.

For an edge $(u,v)$ entering the contracted cycle, use adjusted cost

$$
w'(u,v)=w(u,v)-\operatorname{in}[v],
$$

where $\operatorname{in}[v]$ is the selected minimum incoming-edge cost for $v$. The subtraction avoids paying the already-accounted selected incoming edge twice.

After recursively solving the contracted graph:

1. expand the cycle;
2. keep all selected cycle edges except the one entering the vertex chosen by the recursive external edge;
3. restore original edge identities.

A straightforward implementation is $O(VE)$; more sophisticated implementations improve the bound.

### Correctness intuition

Subtracting each chosen incoming minimum gives a lower-bound normalization: any arborescence pays at least that much for every nonroot vertex. A directed cycle is the only obstruction to simultaneously taking all normalized zero-cost incoming choices. Contracting represents the one decision that matters—where the final arborescence enters and breaks the cycle.

## 23.4 Linear programming as an algorithmic language

A common maximization form is

$$
\max c^\top x
\quad\text{subject to}\quad
Ax\le b,\qquad x\ge0.
$$

The corresponding dual form is

$$
\min b^\top y
\quad\text{subject to}\quad
A^\top y\ge c,\qquad y\ge0.
$$

Terms:

- **feasible:** satisfies all constraints;
- **infeasible:** no point satisfies all constraints;
- **unbounded:** objective can improve without limit;
- **optimal:** feasible and no feasible point has a better objective.

### Duality

For every primal-feasible $x$ and dual-feasible $y$,

$$
c^\top x\le b^\top y.
$$

This is **weak duality** and gives an immediate certificate: a primal solution and dual solution with equal values are both optimal. Under the ordinary feasibility/boundedness conditions of linear programming, strong duality says the optimal values are equal.

Complementary slackness explains which constraints are tight:

$$
y_i(b_i-a_i^\top x)=0,
\qquad
x_j((A^\top y)_j-c_j)=0.
$$

Positive dual weight requires its primal constraint to be tight; a positive primal variable requires its dual constraint to be tight.

### LP relaxation and integrality

An integer program requires selected variables to be integers. Dropping integrality gives an LP relaxation:

- minimization relaxation gives a lower bound;
- maximization relaxation gives an upper bound.

That bound can guide branch-and-bound. Rounding is not automatically feasible or approximately good; it needs a problem-specific proof.

Some combinatorial LPs, including standard max-flow formulations, have integral optima when capacities are integral because of their structural constraint matrices. General LPs do not promise integral solutions.

### Algorithm distinction

- **Simplex:** moves between vertices of the feasible polytope; often excellent in practice but has exponential worst-case examples.
- **Ellipsoid:** polynomial-time theoretical algorithm using a separation-oracle view; historically important, usually not the default practical solver.
- **Interior-point:** follows the interior of the feasible region and has polynomial-time variants with strong practical performance.

The key viva lesson is not to say “linear programming means simplex” or “LP is exponential.” Linear programming is polynomial-time solvable, while particular algorithms have different theoretical and practical behavior.

## 23.5 Current Algorithm Engineering source ledger

| Source | Pages | Retained viva value |
|---|---:|---|
| `Algorithm.pdf` | 35 image-heavy pages | stable marriage and algorithm traces |
| `Algorithm2.pdf` | 75 | reductions/complexity and algorithm-design reinforcement |
| `Complexity-Sowdha.pdf` | 23 image-heavy pages | complexity-class/reduction cross-check |
| `FFT-Sowdha.pdf` | 9 image-heavy pages | FFT derivation/trace cross-check |
| `LP-Sowdha.pdf` | 22 image-heavy pages | primal/dual and LP-algorithm recall |
| `Merged_slides_AE.pdf` | 280 | stable matching, NP-completeness, flow, matching, arborescence, FFT, and LP |
| `Mincost-Arborescence.pdf` | 9 image-heavy pages | directed minimum-arborescence contraction |
| **Total** | **453** | integrated here rather than creating another viva volume |

---

# 24. Final DSA-II self-test

- [ ] State graph representations and trace BFS/DFS with exact `O(V+E)` assumptions.
- [ ] Prove cut/cycle properties and trace Kruskal/Prim with DSU or heap costs.
- [ ] Distinguish Dijkstra, Bellman–Ford, DAG shortest paths, Floyd–Warshall, and Johnson by assumptions and complexity.
- [ ] Construct a residual graph, augment flow, and derive Edmonds–Karp `O(VE^2)`.
- [ ] Trace APSP predecessor reconstruction and identify a negative cycle.
- [ ] Perform AVL and red–black rotations; state every invariant before repair cases.
- [ ] Explain splay amortized—not worst-case per operation—and skip-list expected bounds.
- [ ] Use aggregate, accounting, and potential methods on a concrete sequence.
- [ ] Prove bottom-up `BUILD-HEAP` is `Theta(n)` by summing node heights.
- [ ] Compare binary, d-ary, binomial, and Fibonacci heaps by operation/workload.
- [ ] Implement chaining/open addressing and explain load factor, deletion, and unavoidable collisions.
- [ ] Trace naive, Rabin–Karp, KMP, automaton, and Z matching.
- [ ] Explain DFT/FFT representation, roots of unity, bit reversal, and convolution complexity.
- [ ] Give a complete polynomial-reduction proof direction and distinguish P, NP, NP-hard, and NP-complete.
- [ ] Trace backtracking versus branch-and-bound and justify every pruning bound.
- [ ] Distinguish exact exponential, pseudo-polynomial, approximation, PTAS/FPTAS, and heuristic algorithms.
- [ ] Explain stable matching, blocking pairs, Gale–Shapley optimality, and $O(n^2)$.
- [ ] Distinguish stable, maximal, and maximum matching; trace one augmenting-path repair.
- [ ] Explain why a directed minimum arborescence needs cycle contraction rather than Prim/Kruskal.
- [ ] State primal/dual LP, weak duality, complementary slackness, and relaxation bounds.
- [ ] Account for the three current DSA-II PDFs and the seven Algorithm Engineering sources using the ledgers above.
