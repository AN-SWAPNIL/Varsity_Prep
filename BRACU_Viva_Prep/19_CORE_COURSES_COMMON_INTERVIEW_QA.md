# Bismillah.

# Core CSE Viva and Interview Question Bank

This volume converts the ten main course books into an oral-exam format. It is
not a replacement for the detailed books. Use it to practise saying an answer
without notes, drawing the mechanism, writing the core code, and surviving the
follow-up question.

The chapter order follows the requested order:

1. DSA
2. Machine Learning
3. Discrete Mathematics
4. OOP
5. Networking
6. Software Engineering
7. Security
8. DBMS
9. Artificial Intelligence
10. Operating Systems

## 0.1 What "detailed enough" means in this pack

For an algorithm, a complete answer contains:

1. problem and input/output contract;
2. central idea and data structure;
3. a small trace or diagram;
4. correctness invariant or proof idea;
5. time and space complexity;
6. assumptions, failure cases, and the nearest alternative;
7. implementable code or pseudocode when appropriate.

This matches MIT 6.006's own algorithm-answer standard: description,
worked example/diagram, correctness argument, and complexity analysis
([MIT 6.006 syllabus](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/pages/syllabus/)).

For a systems or design question, use:

> Definition -> mechanism -> concrete example -> trade-off -> failure/security case.

For a mathematical or ML question, use:

> Define variables and assumptions -> write the equation -> interpret every term ->
> give a numeric or visual example -> state what the equation does not imply.

## 0.2 Local-slide and external-source map

| Course | Local academic sources | Detailed local book | Current external cross-check |
|---|---|---|---|
| DSA | `203-DSA1`, `207-DSA2`, selected `461-AE` | `01_DSA_I_SLIDE_COMPLETE.md`, `02_DSA_II_SLIDE_COMPLETE.md` | MIT 6.006/6.046 |
| ML | `471-ML`, including diffusion notebook | `11_MACHINE_LEARNING_SLIDE_COMPLETE.md` | Stanford CS229, scikit-learn |
| Discrete | `103-DM` | `10_DISCRETE_MATHEMATICS_SLIDE_COMPLETE.md` | MIT 6.042/6.1200 |
| OOP | `107-OOP` C++ and Java | `03_OOP_CPP_JAVA_SLIDE_COMPLETE.md` | Oracle Java language/API documentation |
| Networking | `311-DC`, `321-Networking` | `07_NETWORKING_SLIDE_COMPLETE.md` | IETF RFCs 768, 8200, 9293, 9846 |
| SWE | `307-SWE`, `325-ISD` | `08_SOFTWARE_ENGINEERING_SLIDE_COMPLETE.md` | Agile Manifesto, Scrum Guide |
| Security | `405-Security` | `13_SECURITY_CORE_COMPLETE.md` | NIST, OWASP, IETF TLS |
| DBMS | `215-DBMS` | `05_DBMS_SLIDE_COMPLETE.md` | PostgreSQL documentation, MIT/UC Berkeley DB courses |
| AI | `317-AI` | `09_ARTIFICIAL_INTELLIGENCE_SLIDE_COMPLETE.md` | UC Berkeley CS188 |
| OS | `313-OS` | `06_OPERATING_SYSTEMS_SLIDE_COMPLETE.md` | OSTEP, Duke/UW systems curricula |

The question selection was amplified beyond BRACU using broad university
comprehensive/qualifying-exam topic maps, including
[UCLA's CS written qualifying syllabus](https://web.cs.ucla.edu/classes/written.qualifying.exam/WQEsyllabus.html),
[Duke's operating-systems qualifying syllabus](https://cs.duke.edu/graduate/exam-syllabus-510),
and [Brooklyn College's CS comprehensive-exam map](https://www.brooklyn.edu/cis/graduate/computer-science-graduate-comprehensive-exams/).
These sources establish recurring domains; they are not claimed to provide a
statistical ranking of every interview question.

---

# 1. Data Structures and Algorithms

**Deep source:** `01_DSA_I_SLIDE_COMPLETE.md` and
`02_DSA_II_SLIDE_COMPLETE.md`.

## Q1. What is the difference between an algorithm, a program, an ADT, and a data structure?

An **algorithm** is a finite, unambiguous procedure that maps valid inputs to
the required outputs. A **program** is an implementation of one or more
algorithms in a language and execution environment.

An **abstract data type (ADT)** specifies observable values and operations:
for example, a stack supports `push`, `pop`, `top`, and `empty`. A **data
structure** is a concrete representation and implementation of that contract:
an array stack and linked stack implement the same ADT with different memory
and performance trade-offs.

Good follow-up: the interface says *what*; the representation and algorithms
say *how*.

## Q2. Explain Big-O, Big-Omega, and Big-Theta precisely.

For eventually nonnegative functions:

$$
f(n)\in O(g(n))
\iff
\exists c>0,n_0\ \forall n\ge n_0:\ f(n)\le c g(n).
$$

`O` is an asymptotic upper bound, `Omega` a lower bound, and `Theta` both:

$$
f(n)\in\Theta(g(n))
\iff
f(n)\in O(g(n))\cap\Omega(g(n)).
$$

Do not say that Big-O automatically means worst case. Worst/average/best case
describes *which inputs or probability model*; `O`, `Omega`, and `Theta`
describe asymptotic bounds on the resulting function.

## Q3. Recursion or iteration: which is better?

Neither is universally better.

- Recursion is natural when the problem is recursively structured: trees,
  divide-and-conquer, DFS, backtracking, and inductive definitions.
- Iteration usually avoids function-call overhead and call-stack overflow.
- A recursive program uses an implicit stack; an iterative simulation often
  uses an explicit stack carrying exactly the pending state.
- Tail recursion saves stack only when the language/runtime guarantees
  tail-call elimination. Java and standard C++ do not guarantee it.

For `sum(1..n)`, iteration uses constant auxiliary space:

```cpp
long long sumTo(int n) {
    long long sum = 0;
    for (int i = 1; i <= n; ++i) sum += i;
    return sum;
}
```

The direct recursion uses `Theta(n)` call-stack space:

```cpp
long long sumTo(int n) {
    if (n <= 0) return 0;
    return n + sumTo(n - 1);
}
```

Both take `Theta(n)` time; the formula `n(n+1)/2` takes `Theta(1)` arithmetic
operations under the word-RAM assumption, with overflow still a concern.

## Q4. How do you solve a recurrence?

First derive it from the code; do not apply a theorem blindly.

- Substitution/induction works broadly.
- A recursion tree exposes per-level work.
- Master theorem applies to recurrences of the form
  `T(n)=aT(n/b)+f(n)` under its conditions.
- Characteristic roots solve common linear recurrences such as Fibonacci.

Example:

$$
T(n)=2T(n/2)+\Theta(n).
$$

There are `log_2 n` levels and each level performs `Theta(n)` nonrecursive
work, so `T(n)=Theta(n log n)`.

## Q5. Array versus linked list?

| Property | Dynamic array | Linked list |
|---|---|---|
| Index access | `O(1)` | `O(n)` |
| Search | `O(n)` unsorted | `O(n)` |
| Insert/delete at known node | shifting may be `O(n)` | `O(1)` after locating node |
| Append | amortized `O(1)` | `O(1)` with tail |
| Memory locality | strong | weak |
| Overhead | spare capacity | pointer(s) per node |

The usual interview trap is saying "linked-list insertion is `O(1)`" without
stating that the insertion position/node is already known.

## Q6. Stack, queue, deque, and priority queue?

- Stack: LIFO; recursion, undo, parsing, DFS.
- Queue: FIFO; BFS, scheduling, buffering.
- Deque: insert/delete at both ends; sliding windows, 0-1 BFS.
- Priority queue: removes the minimum/maximum key rather than the oldest;
  Dijkstra, Prim, scheduling, event simulation.

A binary heap implements priority-queue insertion and extraction in
`O(log n)`, peek in `O(1)`, and bottom-up build in `Theta(n)`.

## Q7. Why is bottom-up BUILD-HEAP `O(n)`?

Calling `siftDown` is not `O(log n)` for every node. Most nodes are near
leaves and can move only a small distance. At most about `n/2^(h+1)` nodes
have height `h`, therefore

$$
T(n)
\le
\sum_{h\ge0}\frac{n}{2^{h+1}}O(h)
=
O(n)\sum_{h\ge0}\frac{h}{2^{h+1}}
=O(n).
$$

Repeatedly inserting `n` keys is `O(n log n)`; Floyd's bottom-up construction
is `Theta(n)`.

```cpp
void siftDown(vector<int>& a, int i, int n) {
    while (true) {
        int largest = i;
        int l = 2 * i + 1, r = 2 * i + 2;
        if (l < n && a[l] > a[largest]) largest = l;
        if (r < n && a[r] > a[largest]) largest = r;
        if (largest == i) return;
        swap(a[i], a[largest]);
        i = largest;
    }
}

void buildHeap(vector<int>& a) {
    for (int i = static_cast<int>(a.size()) / 2 - 1; i >= 0; --i)
        siftDown(a, i, static_cast<int>(a.size()));
}
```

## Q8. Explain BST predecessor and successor with an example.

For a node `x`, the **successor** is the smallest key strictly greater than
`x`; the **predecessor** is the largest key strictly smaller than `x`.

```text
          20
        /    \
      10      30
     /  \    /  \
    5   15  25  40
       /  \
      12  17
```

- Successor of `15` is `17`: minimum in its right subtree.
- Predecessor of `15` is `12`: maximum in its left subtree.
- Successor of `17` is `20`: climb until the first ancestor for which the
  current node lies in the ancestor's left subtree.
- Predecessor of `25` is `20`: symmetric upward rule.

Search, insert, delete, predecessor, and successor cost `O(h)`, where `h` is
tree height. A plain BST can have `h=n`; a balanced BST keeps `h=O(log n)`.

## Q9. What does a tree rotation do?

A rotation changes a constant number of local pointers while preserving
inorder key order.

```text
Right rotation at y                 Left rotation at x

        y                                   x
       / \                                 / \
      x   C       ->                      A   y
     / \                                     / \
    A   B                                   B   C
```

It is `O(1)`. AVL and red-black trees use rotations to repair balance, not to
perform ordinary search.

## Q10. State the red-black tree properties and height result.

Using black sentinel `NIL` leaves:

1. every node is red or black;
2. root is black;
3. every `NIL` leaf is black;
4. a red node has black children;
5. every path from a node to a descendant `NIL` has equal black height.

No path can have two consecutive red nodes. The longest root-leaf path is at
most twice the shortest. A subtree of black height `bh` contains at least
`2^bh-1` internal nodes, yielding:

$$
h\le 2\log_2(n+1).
$$

Thus search, insert, and delete are `O(log n)`. AVL trees are more strictly
balanced and often faster for lookup-heavy workloads; red-black trees usually
need fewer rebalancing changes under updates.

## Q11. Compare common sorting algorithms.

| Algorithm | Best | Average | Worst | Stable? | Extra space |
|---|---:|---:|---:|---|---:|
| Insertion | `O(n)` | `O(n^2)` | `O(n^2)` | yes | `O(1)` |
| Selection | `O(n^2)` | `O(n^2)` | `O(n^2)` | usually no | `O(1)` |
| Merge | `O(n log n)` | `O(n log n)` | `O(n log n)` | yes | `O(n)` arrays |
| Quick | `O(n log n)` | `O(n log n)` | `O(n^2)` | usually no | expected `O(log n)` stack |
| Heap | `O(n log n)` | `O(n log n)` | `O(n log n)` | no | `O(1)` |
| Counting | `O(n+k)` | `O(n+k)` | `O(n+k)` | can be | `O(n+k)` |

Choose using data size, key range, stability, memory, existing order, and
worst-case requirement. Comparison sorting has an `Omega(n log n)` worst-case
decision-tree lower bound; counting/radix sorting escape it by using more
structure than comparisons.

## Q12. How would you search for an element in a list?

Ask what is known and what operations repeat.

- One lookup in an unsorted list: linear scan, `O(n)`.
- Sorted random-access array: binary search, `O(log n)`.
- Many exact-membership queries: hash set, expected `O(1)`.
- Ordered predecessor/range queries: balanced BST, `O(log n)`.
- Static sorted data with compact memory: sorted array plus binary search.

```cpp
int binarySearch(const vector<int>& a, int target) {
    int lo = 0, hi = static_cast<int>(a.size()); // [lo, hi)
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] < target) lo = mid + 1;
        else hi = mid;
    }
    return (lo < static_cast<int>(a.size()) && a[lo] == target) ? lo : -1;
}
```

Invariant: every possible target position remains inside `[lo,hi)`.

## Q13. BFS versus DFS?

BFS uses a queue and explores by nondecreasing edge count. It finds shortest
paths in an unweighted graph. DFS uses recursion/an explicit stack and is
central to cycle detection, topological ordering, SCCs, and structural
classification. With adjacency lists both take `Theta(V+E)`.

```cpp
vector<int> bfs(const vector<vector<int>>& g, int s) {
    vector<int> dist(g.size(), -1);
    queue<int> q;
    dist[s] = 0;
    q.push(s);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : g[u]) {
            if (dist[v] == -1) {
                dist[v] = dist[u] + 1;
                q.push(v);
            }
        }
    }
    return dist;
}
```

## Q14. Dijkstra versus Bellman-Ford versus Floyd-Warshall?

| Algorithm | Problem | Weight condition | Main time |
|---|---|---|---:|
| BFS | SSSP | equal/unit weights | `O(V+E)` |
| DAG relaxation | SSSP | any weights, DAG | `O(V+E)` |
| Dijkstra | SSSP | nonnegative edges | `O((V+E)log V)` binary heap |
| Bellman-Ford | SSSP | negative edges allowed | `O(VE)` |
| Floyd-Warshall | APSP | no relevant negative cycle | `O(V^3)` |
| Johnson | APSP sparse | negative edges, no negative cycle | Bellman-Ford + repeated Dijkstra |

The path-weight equation is:

$$
w(p)=\sum_{i=1}^{k} w(v_{i-1},v_i).
$$

Dijkstra's settled-node proof fails with negative edges because a later
negative edge may improve a node already finalized.

## Q15. Prim versus Kruskal?

Both use the MST cut property.

- Kruskal sorts edges, takes the next safe edge joining different DSU
  components, and grows a forest.
- Prim starts from a vertex and repeatedly adds the cheapest edge crossing
  from the current tree to an outside vertex.

Kruskal with sorting is `O(E log E)`; Prim with adjacency lists and a binary
heap is `O(E log V)`. Both allow negative weights. A disconnected graph
produces a minimum spanning forest, not one spanning tree.

## Q16. Greedy versus dynamic programming?

A greedy algorithm commits to one locally attractive choice and never
revisits it. It needs a proof such as an exchange argument, stays-ahead
argument, or matroid structure. Dynamic programming stores solutions to
overlapping subproblems when optimal substructure holds.

Fractional knapsack is greedy by value/weight ratio because fractions permit
an exchange. The same rule fails for 0/1 knapsack, which needs DP or another
exact/approximate method.

## Q17. What is a DP state, transition, base case, and evaluation order?

For 0/1 knapsack:

$$
DP[i][c]
=
\max\bigl(DP[i-1][c],\ v_i+DP[i-1][c-w_i]\bigr)
$$

when `w_i<=c`; otherwise copy `DP[i-1][c]`.

- State: best value using the first `i` items and capacity `c`.
- Choice: skip or take item `i`.
- Base: no items or zero capacity gives zero.
- Order: increasing `i`; for 1D optimization, iterate capacity downward so
  one item is not reused.
- Complexity: `O(nW)` time and `O(W)` space, pseudo-polynomial in numeric
  capacity `W`, not polynomial in its bit length.

## Q18. What is hashing, and why are collisions unavoidable?

A hash table maps a large key universe into a finite array. If more distinct
keys are mapped than slots, the pigeonhole principle guarantees a collision.
Collisions are handled by separate chaining or open addressing.

Expected `O(1)` assumes controlled load factor and sufficiently good hash
distribution. Worst case is `O(n)`. Equal objects must hash equally; unequal
objects may still collide.

## Q19. Explain max flow, residual capacity, and a cut.

A flow satisfies capacity constraints and conservation at nonterminal
vertices. For edge `(u,v)`:

$$
0\le f(u,v)\le c(u,v).
$$

The residual graph contains remaining forward capacity
`c(u,v)-f(u,v)` and reverse capacity `f(u,v)`. Reverse edges let a later
augmenting path cancel an earlier choice. An `s-t` cut partitions vertices
into `S` and `T`; its capacity is the total capacity from `S` to `T`.
Max-flow/min-cut says the maximum flow value equals the minimum cut capacity.

```text
s --3--> a --2--> t
 \       |
  \2     |1
   v     v
    b --3--> t
```

Do not greedily consume paths without residual reverse edges; that can trap a
suboptimal routing.

## Q20. Why is Edmonds-Karp `O(VE^2)`?

Edmonds-Karp is Ford-Fulkerson where every augmenting path is found by BFS in
the residual graph.

1. One BFS costs `O(E)`.
2. Shortest residual distance from `s` to every vertex never decreases.
3. When an edge becomes saturated as a critical edge on a shortest
   augmenting path, it cannot become critical again until its endpoints'
   distance relationship has increased.
4. Each directed edge is critical only `O(V)` times.
5. Across `E` edges there are `O(VE)` augmentations.

Therefore:

$$
O(E)\text{ per BFS}\times O(VE)\text{ augmentations}
=O(VE^2).
$$

The proof is independent of numeric capacity magnitude, unlike generic
integer-capacity Ford-Fulkerson's `O(E|f^*|)` augmentation bound.

## Q21. Backtracking versus branch-and-bound?

Both search a state-space tree.

- Backtracking prunes when a partial solution cannot become feasible.
- Branch-and-bound solves optimization problems and prunes when an optimistic
  bound cannot beat the incumbent solution.

Worst-case time remains exponential. Correct pruning requires a valid
feasibility condition or optimistic bound; an invalid bound can prune the
optimal solution.

## Q22. What are P, NP, NP-hard, and NP-complete?

- `P`: decision problems solvable in polynomial time.
- `NP`: yes-instances have polynomial-size certificates verifiable in
  polynomial time.
- NP-hard: every problem in NP reduces to it in polynomial time; it need not
  itself be a decision problem or lie in NP.
- NP-complete: both in NP and NP-hard.

To prove a new problem `B` NP-hard, reduce a known NP-hard problem `A` **to**
`B`: `A <=p B`. Reversing that arrow proves the wrong claim.

## DSA board drill checklist

- Trace recursion and state its stack space.
- Implement binary search with a clear interval invariant.
- Build a heap bottom-up and prove `Theta(n)`.
- Draw BST predecessor/successor and an RBT rotation.
- Trace BFS/DFS and state `O(V+E)`.
- Relax one Dijkstra/Bellman-Ford edge.
- Run one Kruskal/Prim step and name the cut.
- Draw a residual graph and one Edmonds-Karp augmentation.
- Define a DP state before writing its recurrence.
- State one greedy exchange proof and one counterexample.

---

# 2. Machine Learning

**Deep source:** `11_MACHINE_LEARNING_SLIDE_COMPLETE.md`.

## Q1. What is machine learning?

Machine learning constructs a model whose performance on a task improves from
data/experience rather than encoding every decision rule manually.

- Supervised learning uses labeled targets.
- Unsupervised learning discovers structure without labels.
- Reinforcement learning learns a policy through interaction and reward.

A complete answer names the task, data, model/hypothesis class, loss or reward,
optimization process, and evaluation protocol.

## Q2. What exactly are bias and variance?

They are statistical components of expected prediction error, not synonyms
for underfitting and overfitting.

Assume:

$$
y=f(x)+\epsilon,\qquad
\mathbb E[\epsilon\mid x]=0,\qquad
\operatorname{Var}(\epsilon\mid x)=\sigma^2.
$$

Train on a random dataset `D`, producing predictor `hat f_D`. At fixed `x`:

$$
\mathbb E_{D,\epsilon}\!\left[(y-\hat f_D(x))^2\right]
=
\sigma^2
+
\left(\mathbb E_D[\hat f_D(x)]-f(x)\right)^2
+
\mathbb E_D\!\left[
\left(\hat f_D(x)-\mathbb E_D[\hat f_D(x)]\right)^2
\right].
$$

Therefore:

$$
\text{expected test MSE}
=
\text{irreducible noise}
+
\text{Bias}^2
+
\text{Variance}.
$$

- Bias: systematic difference between the mean learned prediction and the
  target function.
- Variance: how much learned predictions change across training samples.
- Noise: uncertainty no model can remove from the given information.

This formulation is cross-checked by
[Stanford CS229 error analysis](https://cs229.stanford.edu/notes2021fall/error-analysis.pdf)
and the [scikit-learn bias-variance example](https://scikit-learn.org/stable/auto_examples/ensemble/plot_bias_variance.html).

## Q3. How are bias/variance related to underfitting/overfitting?

They are related diagnostic patterns:

| Pattern | Training error | Validation/test error | Typical component |
|---|---:|---:|---|
| Underfit | high | high, often close | high bias |
| Good fit | low enough | low and close | balanced |
| Overfit | very low | much higher | high variance |

But the words are not definitions of each other. Bias and variance are
expectations over possible training datasets; under/overfitting are observed
learning/generalization behaviors.

To reduce high bias: richer features/model, weaker regularization, longer or
better optimization. To reduce high variance: more representative data,
regularization, simpler model, bagging, augmentation, or early stopping.
Google's current ML course also distinguishes fitting behavior from expected
error components
([Google ML overfitting](https://developers.google.com/machine-learning/crash-course/overfitting/overfitting)).

## Q4. Why train/validation/test split?

- Training set fits parameters.
- Validation set chooses hyperparameters, thresholds, and models.
- Test set is used once for a final unbiased estimate.

Repeatedly selecting based on test performance makes the test set part of the
training process. Preprocessing must be fitted on training data only. In
cross-validation, scaling/imputation/feature selection must run inside each
training fold.

## Q5. Parameter versus hyperparameter?

Parameters are learned by training: regression coefficients, tree splits,
neural weights. Hyperparameters configure learning/model capacity: learning
rate, regularization strength, depth, `k`, architecture, batch size.
Hyperparameters are selected with validation data or nested CV, not the final
test set.

## Q6. Loss, empirical risk, and generalization?

Loss `L(y,hat y)` measures one prediction. Empirical risk averages training
loss:

$$
\hat R(\theta)=\frac1n\sum_{i=1}^{n}L(y_i,f_\theta(x_i)).
$$

Expected/population risk averages over the true data distribution. Training
minimizes empirical risk; ML succeeds only if that produces low population
risk. Regularization, validation, suitable inductive bias, and representative
data help close the generalization gap.

## Q7. Linear regression and its assumptions?

Linear regression models:

$$
\hat y=w^\top x+b.
$$

Ordinary least squares minimizes:

$$
J(w,b)=\frac1n\sum_i(y_i-\hat y_i)^2.
$$

For coefficient inference, common assumptions include correct linear
specification, independent errors, zero conditional mean, homoscedasticity,
and no perfect multicollinearity; normality is mainly needed for exact small
sample inference, not to compute OLS.

## Q8. Logistic regression: why is it classification?

It models log-odds as linear:

$$
\log\frac{p(y=1\mid x)}{1-p(y=1\mid x)}=w^\top x+b,
\qquad
p=\sigma(z)=\frac1{1+e^{-z}}.
$$

Binary cross-entropy is the negative Bernoulli log-likelihood:

$$
L=-[y\log p+(1-y)\log(1-p)].
$$

The probability threshold is a decision choice and should reflect class
priors and false-positive/false-negative costs, not automatically stay at
`0.5`.

## Q9. Gradient descent, SGD, and mini-batch?

$$
\theta_{t+1}=\theta_t-\eta\nabla_\theta J(\theta_t).
$$

- Batch gradient uses all examples: stable but expensive per step.
- SGD uses one example: noisy, frequent updates.
- Mini-batch uses a subset: vectorization plus useful stochasticity.

Too large a learning rate can diverge/oscillate; too small can be extremely
slow. Adaptive optimizers do not remove the need to choose a schedule and
validate generalization.

## Q10. L1, L2, Ridge, Lasso, and Elastic Net?

$$
\text{Ridge: }J+\lambda\|w\|_2^2,
\qquad
\text{Lasso: }J+\lambda\|w\|_1.
$$

L2 smoothly shrinks correlated coefficients; L1 has a cornered geometry that
can drive coefficients exactly to zero. Elastic Net combines both:

$$
J+\lambda_1\|w\|_1+\lambda_2\|w\|_2^2.
$$

Regularization strength is a hyperparameter. Standardize features when scale
would otherwise change the penalty unfairly.

## Q11. Precision, recall, specificity, and F1?

$$
\text{Precision}=\frac{TP}{TP+FP},
\qquad
\text{Recall}=\frac{TP}{TP+FN},
$$

$$
\text{Specificity}=\frac{TN}{TN+FP},
\qquad
F_1=\frac{2PR}{P+R}.
$$

Accuracy can be misleading on imbalanced data. Use recall when missed
positives are costly, precision when false alarms are costly, PR-AUC for
rare-positive ranking, ROC-AUC for class-separation ranking, and calibration
when probabilities themselves drive decisions.

## Q12. How do you handle imbalanced classes?

Use stratified splitting; appropriate metrics; class weighting or focal loss;
careful under/oversampling inside training folds; data collection/augmentation;
threshold tuning on validation data; and probability calibration. Never
balance the test set into an unrealistic prevalence and then present that as
deployment performance.

## Q13. Decision tree, random forest, and boosting?

- A decision tree recursively chooses feature splits that reduce impurity.
- Random forest trains decorrelated trees on bootstrap samples and random
  feature subsets, then averages/votes; it mainly reduces variance.
- Boosting adds weak learners sequentially to correct residuals/gradients; it
  can reduce bias but may chase noise.

XGBoost is a regularized, optimized gradient-boosted-tree system. Mentioning
its name is not a substitute for explaining additive boosting, shrinkage,
tree complexity control, and gradient/Hessian-based fitting.

## Q14. Entropy and information gain?

For class proportions `p_k`:

$$
H(S)=-\sum_k p_k\log_2 p_k.
$$

A split's information gain is parent entropy minus the weighted child
entropy. A pure node has entropy zero. Greedy splitting does not guarantee a
globally smallest or best-generalizing tree; depth/min-samples/pruning control
capacity.

## Q15. KNN versus k-means?

KNN is supervised: find nearby labeled examples and vote/average. Prediction
cost is high unless indexed; scaling and distance choice matter.

K-means is unsupervised: alternate assignment to nearest centroid and centroid
recomputation to decrease within-cluster squared Euclidean distance. It is
initialization-sensitive and prefers roughly spherical, similarly scaled
clusters.

## Q16. SVM and the kernel trick?

For separable data, SVM maximizes geometric margin. The soft-margin objective
trades margin against hinge-loss violations using `C`. Kernel methods replace
explicit feature vectors with inner products `K(x,z)`, enabling nonlinear
boundaries. Kernel validity requires a positive-semidefinite Gram matrix under
the standard formulation.

## Q17. PCA: what does it optimize?

After centering, PCA finds orthonormal directions of maximum projected
variance, equivalently minimum squared reconstruction error for a fixed
linear subspace dimension. Compute it with covariance eigendecomposition or
SVD. Standardize first when feature units/scales should not dominate.
PCA is unsupervised and may discard low-variance but label-predictive
directions.

## Q18. What is backpropagation?

Backpropagation is reverse-mode automatic differentiation on a computation
graph. It repeatedly applies the chain rule from loss to earlier
intermediates, reusing local derivatives so all parameter gradients are
computed efficiently.

For `z=Wx+b`, `a=phi(z)`:

$$
\frac{\partial L}{\partial W}
=
\frac{\partial L}{\partial z}x^\top.
$$

Backprop computes gradients; an optimizer such as SGD/Adam uses them to update
parameters.

## Q19. Why nonlinearity in a neural network?

The composition of linear maps is still a linear map. Nonlinear activations
allow curved decision boundaries and hierarchical representations. ReLU is
simple and avoids positive-side saturation; sigmoid/tanh are useful in
specific gates/outputs but can saturate, producing small gradients.

## Q20. Batch normalization versus layer normalization?

- Batch norm normalizes a feature/channel using batch statistics; behavior
  differs between training and inference and small/non-IID batches can be
  difficult.
- Layer norm normalizes features within each example/token and is independent
  of batch size; it is standard in Transformers.

Neither is merely "scaling inputs." Both introduce learned affine parameters
and affect optimization dynamics.

## Q21. CNN versus Vision Transformer?

CNN:

- local receptive fields and shared convolution weights;
- strong locality/translation inductive bias;
- efficient on grids and often data-efficient.

Vision Transformer:

- splits an image into patches, embeds them as tokens, adds positional
  information, and applies self-attention;
- supports global token interaction early;
- often benefits strongly from pretraining/large data.

Patch count `N` makes ordinary attention roughly `O(N^2 d)` in time and
`O(N^2)` in attention memory.

## Q22. What is self-attention?

$$
\operatorname{Attention}(Q,K,V)
=
\operatorname{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right)V.
$$

Queries decide what each token seeks, keys expose what tokens contain, and
values carry the mixed content. Scaling prevents dot products from growing
with dimension and saturating softmax. Multi-head attention learns multiple
projection subspaces.

## Q23. Transformer versus Mamba?

A Transformer explicitly mixes token pairs through attention and supports
highly parallel training, but ordinary full attention is quadratic in
sequence length. Mamba is a selective state-space architecture with a
recurrent state update whose parameters depend on the input, aiming for
linear-time sequence processing and compact inference state.

Do not claim one universally replaces the other. Compare task quality,
hardware kernels, training stability, context use, and latency/memory.

## Q24. Data leakage?

Leakage occurs when training features, preprocessing, or model selection uses
information unavailable at real prediction time or belonging to validation/
test targets. Examples: scaling before split, future records in time-series
features, duplicates across folds, target-derived encodings without
out-of-fold construction.

The remedy is to reproduce the true deployment chronology and package every
learned preprocessing step inside the training pipeline.

## Q25. What would you do when a model performs badly?

1. Verify labels, split, leakage, metric, and a simple baseline.
2. Compare training and validation errors to diagnose optimization, bias, or
   variance patterns.
3. Slice errors by class/subgroup/time/source.
4. Inspect confusion matrix, residuals, calibration, and corrupted examples.
5. Change one hypothesis at a time; log experiments and run ablations.
6. Re-check performance under expected distribution shift and deployment
   constraints.

## ML board drill checklist

- Derive and interpret bias squared + variance + noise.
- Draw training/validation curves for underfit and overfit.
- Derive logistic cross-entropy and one gradient step.
- Compute precision/recall/F1 from a confusion matrix.
- Calculate one decision-tree entropy split.
- Trace one k-means iteration.
- Draw convolution output shape and parameter count.
- Write the attention equation and label `Q`, `K`, `V`.
- Compare CNN, ViT, Transformer, and Mamba without hype.
- Explain leakage in one realistic pipeline.

---

# 3. Discrete Mathematics

**Deep source:** `10_DISCRETE_MATHEMATICS_SLIDE_COMPLETE.md`.

## Q1. Proposition, predicate, tautology, contradiction, satisfiable?

A proposition is a declarative statement with a truth value. A predicate
contains variables and becomes a proposition after assignment or
quantification. A tautology is true under every valuation; a contradiction
under none; a satisfiable formula under at least one.

Implication `p -> q` is false only when `p` is true and `q` is false.

## Q2. Converse, inverse, and contrapositive?

For `p -> q`:

- converse: `q -> p`;
- inverse: `not p -> not q`;
- contrapositive: `not q -> not p`.

Only the contrapositive is logically equivalent to the original implication.
A biconditional `p <-> q` requires both directions.

## Q3. Negate quantified statements.

$$
\neg(\forall x\,P(x))\equiv\exists x\,\neg P(x),
\qquad
\neg(\exists x\,P(x))\equiv\forall x\,\neg P(x).
$$

Example: the negation of "every student passed some exam" is not "no student
passed any exam." Formally:

$$
\neg\forall s\,\exists e\,Passed(s,e)
\equiv
\exists s\,\forall e\,\neg Passed(s,e).
$$

Order matters: `forall x exists y` generally differs from
`exists y forall x`.

## Q4. Common proof methods and when to use them?

- Direct: assume hypotheses and derive conclusion.
- Contrapositive: prove `not q -> not p`.
- Contradiction: assume the negation of the desired claim and derive an
  impossibility.
- Cases: partition possibilities exhaustively.
- Induction: base plus inductive step for recursively indexed statements.
- Construction: explicitly build the required object.
- Counterexample: one valid example disproves a universal claim.

A proof is not a list of examples; examples motivate or falsify, but do not
prove a universal statement.

## Q5. Weak versus strong induction?

Weak induction assumes `P(k)` to prove `P(k+1)`. Strong induction assumes
`P(0),...,P(k)`. They are logically equivalent, but strong induction matches
problems whose next case depends on several smaller cases.

Every induction proof must clearly state:

1. proposition `P(n)`;
2. base case(s);
3. induction hypothesis;
4. step proving the next case;
5. conclusion and valid starting range.

## Q6. Set, subset, power set, Cartesian product, and partition?

- `A subseteq B`: every member of `A` lies in `B`.
- `P(A)`: set of all subsets; if `|A|=n`, then `|P(A)|=2^n`.
- `A x B`: ordered pairs `(a,b)`.
- A partition is a collection of nonempty, pairwise disjoint blocks whose
  union is the whole set.

An equivalence relation's equivalence classes form a partition, and every
partition induces an equivalence relation.

## Q7. Function: injective, surjective, bijective?

- Injective: `f(a)=f(b)` implies `a=b`.
- Surjective: every codomain element has at least one preimage.
- Bijective: both; only then is an inverse function from codomain to domain
  defined everywhere and uniquely.

For finite sets of equal size, injection, surjection, and bijection imply one
another; not so for arbitrary unequal/infinite settings.

## Q8. Equivalence relation versus partial order?

| Relation | Required properties |
|---|---|
| Equivalence | reflexive, symmetric, transitive |
| Partial order | reflexive, antisymmetric, transitive |

Antisymmetric does not mean "not symmetric." It says:

$$
aRb\land bRa\Rightarrow a=b.
$$

`<=` is a partial order; congruence modulo `n` is an equivalence relation.

## Q9. State and prove the pigeonhole principle.

If `N` objects are mapped into `m` boxes, some box contains at least:

$$
\left\lceil\frac{N}{m}\right\rceil
$$

objects.

Proof by contradiction: if every box contained at most
`ceil(N/m)-1`, the total capacity would be less than `N`, contradicting that
all objects were placed.

The ordinary form says `m+1` objects in `m` boxes force a shared box.
[MIT 6.042's counting rules](https://live.ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/a784497ca2bfa98ecb310214329c9b7e_MIT6_042JF10_rec15_sol.pdf)
use the same function-mapping formulation.

## Q10. Give a solid real-world/computing use of pigeonhole.

**Hash collision:** a hash function maps a much larger key universe into `m`
table positions/hash values. If more than `m` distinct keys are inserted, at
least two keys share a mapped value. The theorem proves that collisions are
unavoidable; collision resolution is therefore part of hash-table design.

Always identify:

- objects: inserted distinct keys;
- boxes: possible hash values/slots;
- mapping: `key -> h(key)`;
- counting inequality: more keys than possible values.

Other valid examples:

- among 367 people, two share a birthday even allowing 29 February;
- among any 38 integers, two have the same remainder modulo 37, so their
  difference is divisible by 37;
- a lossless fixed-length compressor cannot make every possible input shorter,
  because there are fewer shorter output strings than inputs.

## Q11. Sum rule, product rule, permutation, combination?

- Disjoint alternatives add.
- Sequential independent counts multiply.

$$
P(n,r)=\frac{n!}{(n-r)!},
\qquad
\binom nr=\frac{n!}{r!(n-r)!}.
$$

Permutation counts ordered selections; combination ignores order. For
repeated identical objects with multiplicities `n_1,...,n_k`, arrangements:

$$
\frac{n!}{n_1!\cdots n_k!}.
$$

## Q12. Inclusion-exclusion?

$$
|A\cup B|=|A|+|B|-|A\cap B|.
$$

For three sets, add singleton sizes, subtract pairwise intersections, add the
triple intersection. It corrects repeated counting. "At least one" is often
easier by complement:

$$
\#(\text{at least one})=\#(\text{all})-\#(\text{none}).
$$

## Q13. Ordinary generating function?

For sequence `a_0,a_1,...`, its OGF is:

$$
A(x)=\sum_{n\ge0}a_nx^n.
$$

The coefficient of `x^n` stores `a_n`. Multiplying generating functions
convolves sequences, which models distributing a total among choices.
Generating functions transform recurrences/counting constraints into
algebraic equations and coefficient extraction.

## Q14. Graph, path, cycle, connected component, and tree?

A graph `G=(V,E)` has vertices and edges. A path has no repeated vertices
under the common simple-path convention; a cycle returns to its start without
repeating other vertices. A connected component is a maximal connected
subgraph.

For a finite undirected graph, any two imply the third:

1. connected;
2. acyclic;
3. has `|V|-1` edges.

That is the central tree characterization.

## Q15. Handshaking lemma?

$$
\sum_{v\in V}\deg(v)=2|E|.
$$

Each undirected edge contributes one to the degree of each endpoint.
Therefore the number of odd-degree vertices is even.

## Q16. Euler versus Hamilton?

- Euler trail/circuit uses every **edge** exactly once.
- Hamiltonian path/cycle visits every **vertex** exactly once.

For an undirected graph after ignoring isolated vertices:

- Euler circuit: connected and every degree even.
- Open Euler trail: connected and exactly two vertices odd.

Hamiltonian existence has no comparably simple general degree criterion and
is NP-complete as a decision problem.

## Q17. Bipartite graph and coloring?

A graph is bipartite iff it has no odd cycle. BFS/DFS two-coloring tests this
in `O(V+E)`.

```text
Left set       Right set
  u1 ----------- v1
   | \            |
   |  \           |
  u2 ----------- v2
```

A proper coloring gives adjacent vertices different colors. `chi(G)` is the
minimum number. Greedy coloring uses at most `Delta(G)+1`, but its result
depends on vertex order and need not be optimal.

## Q18. How do recurrences connect discrete math to DSA?

They describe a sequence or recursive computation using earlier values.

- Hanoi: `T(n)=2T(n-1)+1=2^n-1`.
- Merge sort: `T(n)=2T(n/2)+Theta(n)=Theta(n log n)`.
- Bit strings avoiding `11`: `a_n=a_(n-1)+a_(n-2)`.

State base cases. Without them, a recurrence does not uniquely define a
sequence.

## Discrete board drill checklist

- Build a truth table and negate nested quantifiers.
- Prove one parity/divisibility statement directly and by contrapositive.
- Give a complete induction proof.
- Identify objects, boxes, and mapping in pigeonhole.
- Solve a counting problem by complement/inclusion-exclusion.
- Classify a relation and compute equivalence classes.
- Prove the handshaking lemma and tree edge count.
- Distinguish Euler, Hamilton, bipartite, and general coloring problems.

---

# 4. Object-Oriented Programming

**Deep source:** `03_OOP_CPP_JAVA_SLIDE_COMPLETE.md`.

## Q1. Class, object, state, behavior, and identity?

A class defines a type's representation and operations. An object is a runtime
instance with:

- state: current field values;
- behavior: methods it can perform;
- identity: distinction from other instances even when states are equal.

Two separate `Student` objects can be logically equal while remaining
different identities.

## Q2. Explain the four OOP pillars without slogans.

- **Encapsulation:** keep representation and invariants behind a controlled
  interface.
- **Abstraction:** expose essential operations and suppress irrelevant
  implementation detail.
- **Inheritance:** derive a subtype that reuses/extends behavior under a valid
  "is-a" relationship.
- **Polymorphism:** one interface/reference type can invoke behavior of
  multiple concrete runtime types.

Encapsulation is not merely making fields private; methods must preserve the
class invariant and avoid leaking mutable internals.

## Q3. Polymorphism in short?

Polymorphism means one interface, many implementations. A base reference can
refer to different subtype objects, and an overridden instance method is
selected from the runtime object type.

```java
interface Shape {
    double area();
}

final class Circle implements Shape {
    private final double r;
    Circle(double r) { this.r = r; }
    public double area() { return Math.PI * r * r; }
}

final class Rectangle implements Shape {
    private final double w, h;
    Rectangle(double w, double h) { this.w = w; this.h = h; }
    public double area() { return w * h; }
}

Shape s = new Circle(2);
System.out.println(s.area()); // Circle implementation
```

Oracle calls this virtual method invocation
([Oracle polymorphism tutorial](https://docs.oracle.com/javase/tutorial/java/IandI/polymorphism.html)).

## Q4. Overloading versus overriding?

| Overloading | Overriding |
|---|---|
| same name, different parameter list | subtype supplies same compatible instance-method signature |
| resolved from compile-time argument types | selected by runtime object type |
| return type alone cannot overload | covariant reference return allowed |
| inheritance not required | inheritance/interface implementation required |

Static methods are hidden, not dynamically overridden. Fields are also
resolved by reference/declared type.

## Q5. Early binding versus late binding?

**Early/static binding** resolves the target using compile-time information:
overloads, static methods, private methods, and fields.

**Late/dynamic binding** selects an overridden virtual/instance method using
the runtime object type.

```java
class A {
    void f(Object x) { System.out.println("A.Object"); }
    void g() { System.out.println("A.g"); }
}
class B extends A {
    void f(String x) { System.out.println("B.String"); } // overload, not override
    @Override void g() { System.out.println("B.g"); }
}

A x = new B();
x.f("hi"); // A.Object: overload selected using declared type A
x.g();     // B.g: override selected using runtime type B
```

## Q6. Encapsulation versus abstraction?

Encapsulation controls access and protects representation. Abstraction
chooses the essential conceptual interface. A stack's `push/pop` is the
abstraction; hiding whether it uses an array or linked nodes is encapsulation.

## Q7. Inheritance versus composition?

Inheritance should model substitutability: every subtype object must honor the
base type's behavioral contract. Composition models "has-a" and delegates to
owned collaborators, giving more runtime flexibility and less coupling.

Prefer composition when the relationship is reuse rather than genuine
substitutability. "A car has an engine" is composition; "a circle is a shape"
can be inheritance/interface implementation.

## Q8. Abstract class versus interface in Java?

An abstract class can have instance state, constructors, protected helpers,
and partial implementation. A class can extend only one class.

An interface expresses a contract and supports multiple interface
inheritance. Modern interfaces may have default/static/private methods but no
ordinary per-instance fields. Choose an abstract class for a shared stateful
base; an interface for a capability across otherwise unrelated types.

## Q9. C++ virtual function, pure virtual function, and virtual destructor?

`virtual` enables dynamic dispatch through a base pointer/reference. A pure
virtual declaration such as `virtual double area() const = 0;` makes the class
abstract.

If an object may be deleted through a base pointer, the base destructor must
be virtual:

```cpp
struct Shape {
    virtual double area() const = 0;
    virtual ~Shape() = default;
};
```

Without it, deleting a derived object through `Shape*` has undefined behavior
and may skip derived cleanup.

## Q10. Constructor/destructor order?

In C++ construction: virtual bases, ordinary bases, data members in
declaration order, then the constructor body. Destruction reverses the
completed construction order.

Java initializes superclass state before subclass state and runs superclass
constructor before the subclass body. Calling overridable methods from a
constructor is dangerous because the subtype may observe partially initialized
state.

## Q11. Shallow copy, deep copy, and the Rule of Five?

A shallow copy duplicates pointer/reference values, so objects share nested
resources. A deep copy duplicates logically owned mutable resources.

In C++, a resource-owning class may need destructor, copy constructor, copy
assignment, move constructor, and move assignment: the Rule of Five. Prefer
RAII members such as `vector`, `string`, and smart pointers so the Rule of Zero
applies.

## Q12. Equality in Java: `==`, `equals`, and `hashCode`?

- For primitives, `==` compares values.
- For references, `==` compares identity.
- `equals` defines logical equality.

`equals` should be reflexive, symmetric, transitive, consistent, and false
for `null`. If `a.equals(b)`, then `a.hashCode()==b.hashCode()` must hold.
The converse need not hold. Mutating fields used by equality/hash while an
object is a `HashMap` key can make it unfindable.

This contract is specified in
[Java `Object`](https://docs.oracle.com/en/java/javase/15/docs/api/java.base/java/lang/Object.html).

```java
@Override
public boolean equals(Object o) {
    if (this == o) return true;
    if (!(o instanceof Student other)) return false;
    return id == other.id && Objects.equals(name, other.name);
}

@Override
public int hashCode() {
    return Objects.hash(id, name);
}
```

## Q13. Exceptions: checked, unchecked, `throw`, `throws`, and `finally`?

- Checked exceptions must be caught or declared.
- Unchecked exceptions derive from `RuntimeException`; they often signal
  violated preconditions/programming errors.
- `throw` creates/raises one exception.
- `throws` declares possible propagation in a method signature.
- `finally` normally runs during stack unwinding; use try-with-resources for
  deterministic resource closing.

Do not catch `Exception` merely to ignore it. Either recover meaningfully,
translate with context while preserving the cause, or allow it to propagate.

## Q14. Generics and PECS?

Generics provide reusable, compile-time type-safe containers and algorithms.
Java generics are invariant: `List<Integer>` is not a subtype of
`List<Number>`.

PECS:

- producer extends: read `T` values from `List<? extends T>`;
- consumer super: write `T` values into `List<? super T>`.

```java
static <T> void copy(List<? super T> dst, List<? extends T> src) {
    for (T x : src) dst.add(x);
}
```

## Q15. Core Java collections and when to choose them?

| Need | Interface/implementation | Typical performance |
|---|---|---|
| indexed sequence | `ArrayList` | get `O(1)`, end append amortized `O(1)` |
| frequent deque ends | `ArrayDeque` | ends amortized `O(1)` |
| unique unordered | `HashSet` | expected `O(1)` |
| unique sorted | `TreeSet` | `O(log n)` |
| key-value unordered | `HashMap` | expected `O(1)` |
| key-value sorted/range | `TreeMap` | `O(log n)` |
| next min/max | `PriorityQueue` | peek `O(1)`, add/remove `O(log n)` |

Program to the interface where possible. `LinkedList` is rarely the best
default because poor locality and traversal cost often dominate.

## Q16. Sort examples in Java?

```java
List<Student> students = new ArrayList<>(input);

students.sort(Comparator
    .comparingDouble(Student::cgpa).reversed()
    .thenComparing(Student::name)
    .thenComparingInt(Student::id));
```

Natural ordering uses `Comparable<T>`; alternative/client-specific orderings
use `Comparator<T>`. A comparator must be transitive and should be consistent
with equality when a sorted set/map is expected to share equality semantics.

## Q17. Diamond problem?

In C++ multiple inheritance can create two copies of a common base:

```text
      Person
      /    \
 Student  Employee
      \    /
    TeachingAssistant
```

Virtual inheritance can share one `Person` base. Java avoids multiple class
inheritance but permits multiple interfaces; conflicting default methods must
be resolved explicitly.

## Q18. How would you teach functions using sum `1..n`?

Start with a loop learners already understand, then identify repeated
responsibility:

```cpp
long long sumTo(int n) {
    long long total = 0;
    for (int i = 1; i <= n; ++i) total += i;
    return total;
}
```

Motivation:

- name a reusable idea;
- parameter `n` makes it general;
- return value separates calculation from printing;
- caller code becomes readable;
- the function can be tested independently;
- later replace implementation with `n(n+1)/2` without changing callers.

State precondition (`n>=0`), return type/overflow, and a few tests:
`sumTo(0)=0`, `sumTo(1)=1`, `sumTo(5)=15`.

## OOP board drill checklist

- Draw class/object/reference relationships.
- Show overload resolution versus override dispatch.
- Implement a polymorphic `Shape` example.
- Explain virtual destructor and RAII.
- Implement value equality plus hash.
- Choose a collection and justify complexity/order/duplicates.
- Write a generic PECS example and a comparator chain.

---

# 5. Networking

**Deep source:** `07_NETWORKING_SLIDE_COMPLETE.md`.

## Q1. OSI versus TCP/IP?

OSI is a seven-layer reference model: physical, data link, network, transport,
session, presentation, application. The Internet stack is commonly grouped as
link, Internet/network, transport, and application.

Encapsulation:

```text
Application data
  -> TCP segment / UDP datagram
  -> IP packet
  -> link frame
  -> bits/signals
```

Layers are conceptual boundaries, not proof that every protocol maps neatly
to exactly one OSI box.

## Q2. Full forms and differences: TCP versus UDP?

TCP is **Transmission Control Protocol**. UDP is **User Datagram Protocol**.

| TCP | UDP |
|---|---|
| connection-oriented | connectionless |
| reliable ordered byte stream | message/datagram boundaries preserved |
| retransmission and duplicate handling | no built-in delivery/order guarantee |
| receiver flow control | no built-in flow control |
| congestion control | no built-in congestion control |
| larger state/header/handshake | 8-byte header, no connection handshake |

UDP is not automatically "faster." It has lower protocol setup/state, but an
application needing reliability/congestion behavior must implement or adopt
it. DNS, real-time media, DHCP, and QUIC use UDP. RFC 768 describes UDP as a
minimal datagram service without delivery/duplicate guarantees
([RFC 768](https://www.rfc-editor.org/info/rfc768/)).

## Q3. What do SYN and ACK mean?

`SYN` synchronizes initial TCP sequence numbers. `ACK` means the
acknowledgment field is valid; its value is the next sequence number expected.
A SYN consumes one sequence number.

`SYN-ACK` is one TCP segment with both flags set: "I acknowledge your initial
sequence number, and here is mine."

## Q4. Explain the TCP three-way handshake.

```text
Client                                  Server
CLOSED                                  LISTEN
SYN, seq=x                   -------->
                              <-------- SYN+ACK, seq=y, ack=x+1
ACK, seq=x+1, ack=y+1         -------->
ESTABLISHED                              ESTABLISHED
```

It synchronizes both directions' sequence spaces and reduces confusion from
old duplicate connection attempts. It is not a TLS handshake and does not
encrypt data. The current TCP standard is
[RFC 9293](https://www.rfc-editor.org/rfc/rfc9293.html).

## Q5. Flow control versus congestion control?

**Flow control** protects the receiving endpoint from a sender that is too
fast. TCP receiver advertises `rwnd`.

**Congestion control** protects the network path from too much offered load.
The sender maintains `cwnd` based on acknowledgments, loss, delay, or ECN.

Approximately:

$$
\text{send window}=\min(rwnd,cwnd).
$$

Do not answer "both reduce speed." Say whom each protects, which state/window
implements it, and what signal changes it.

## Q6. Slow start, congestion avoidance, fast retransmit, fast recovery?

- Slow start grows `cwnd` rapidly, roughly doubling per RTT while ACKs arrive.
- Congestion avoidance grows more cautiously, roughly additive per RTT in
  classic Reno-style description.
- Three duplicate ACKs suggest a missing segment while later data arrived;
  fast retransmit resends without waiting for timeout.
- Fast recovery reduces sending rate without always returning to the smallest
  window.
- Timeout is a stronger congestion signal and triggers a larger reduction.

Exact behavior varies by TCP congestion-control algorithm; state assumptions.

## Q7. What reliability does TCP add?

Sequence numbers, acknowledgments, checksum error detection, retransmission
timer, duplicate suppression, ordered delivery, receive buffering, sliding
windows, and connection state. TCP provides a byte stream, not application
message boundaries: the application must frame its own records.

## Q8. DHCP and DORA?

DHCP dynamically supplies an IP address lease and options such as subnet
mask/prefix, default gateway, DNS server, and lease time.

```text
Client                         DHCP server
Discover (broadcast)   ---->
                     <----    Offer
Request               ---->
                     <----    Acknowledge
```

This is DORA: Discover, Offer, Request, Acknowledge. DHCPv4 commonly uses UDP
client port 68 and server port 67. A relay forwards requests across subnets.
The protocol is defined in [RFC 2131](https://www.rfc-editor.org/info/rfc2131/).

## Q9. IPv4 versus IPv6?

| IPv4 | IPv6 |
|---|---|
| 32-bit address | 128-bit address |
| variable base header with checksum | fixed 40-byte base header, no header checksum |
| routers may fragment | source handles fragmentation via extension header |
| broadcast exists | multicast/anycast; no broadcast |
| ARP | Neighbor Discovery over ICMPv6 |
| widespread NAT | restores abundant addressing; NAT not required by scarcity |

IPv6 includes extension headers, SLAAC, and link-local addresses. It does not
automatically encrypt all traffic. See
[RFC 8200](https://www.rfc-editor.org/info/rfc8200/).

## Q10. What is subnetting/CIDR?

Prefix `/p` uses `p` network bits. IPv4 `/24` leaves 8 host bits:
`2^8=256` total addresses, traditionally 254 ordinary host addresses after
network/broadcast exclusions.

Example: split `192.168.10.0/24` into four equal subnets. Borrow 2 bits:
`/26`, block size 64:

```text
192.168.10.0/26
192.168.10.64/26
192.168.10.128/26
192.168.10.192/26
```

Longest-prefix matching selects the most specific matching route.

## Q11. ARP and why it is local?

ARP resolves an IPv4 next-hop address to a MAC address on the local link.
For a remote destination, the host ARPs for the default gateway's MAC, not
the remote server's MAC. Routers replace link-layer headers hop by hop while
IP addresses normally remain end-to-end (absent NAT).

ARP has no authentication, enabling local ARP poisoning. Switch protections
and end-to-end TLS reduce risk.

## Q12. DNS resolution?

The stub resolver asks a recursive resolver. On a cache miss the resolver may
query root, TLD, and authoritative servers, then cache records according to
TTL.

Common records:

- `A`: IPv4 address;
- `AAAA`: IPv6 address;
- `CNAME`: alias;
- `MX`: mail exchanger;
- `NS`: authoritative name server;
- `TXT`: text/policy data.

DNS commonly uses UDP, but TCP is used for some large responses, transfers,
or retry. Modern encrypted transports include DoT and DoH; DNSSEC authenticates
DNS data, not query confidentiality.

## Q13. NAT: what does it do and what does it not do?

NAPT/PAT maps internal `(address,port)` pairs to a public `(address,port)`.
It conserves IPv4 addresses and permits return demultiplexing.

NAT is not encryption or identity authentication. It complicates inbound
connections and breaks pure end-to-end addressing; applications may use port
forwarding or traversal techniques.

## Q14. Hub, switch, router, and gateway?

- Hub repeats physical signals to every port.
- Switch learns source MAC locations and forwards frames within a link/VLAN.
- Router forwards IP packets between networks using a routing table.
- Gateway is a broader term for a device/service translating or connecting
  unlike networks/protocols; "default gateway" is normally the local router.

## Q15. Distance-vector versus link-state routing?

Distance vector exchanges destination cost estimates with neighbors and uses
Bellman-Ford-style updates:

$$
D_x(y)=\min_{v\in N(x)}\{c(x,v)+D_v(y)\}.
$$

It can suffer count-to-infinity; split horizon/poison reverse help.

Link state floods topology/cost information, then each router runs Dijkstra
locally. It requires flooding/database consistency but converges with a fuller
topology view.

## Q16. Error detection: parity, checksum, CRC?

- Parity detects odd numbers of bit flips under simple parity.
- Internet checksum adds fixed-width words with one's-complement arithmetic;
  inexpensive but weaker.
- CRC treats bits as a polynomial over `GF(2)` and sends a remainder after
  division by generator polynomial; strong for burst errors.

Detection is not correction. Hamming codes add enough parity structure to
locate/correct limited errors.

## Q17. Stop-and-wait, Go-Back-N, Selective Repeat?

- Stop-and-wait permits one outstanding frame: simple, low utilization on
  large bandwidth-delay paths.
- GBN permits a sender window, cumulative ACKs, and retransmits from a missing
  frame onward.
- SR buffers out-of-order frames and retransmits individual losses; it needs
  more receiver state and careful sequence-space sizing.

For SR, sequence-number space should be at least twice the window to avoid
confusing old and new frames.

## Q18. FDM versus TDM?

FDM gives users separate frequency bands at the same time, with guard bands.
TDM gives users the full channel in different time slots, with
synchronization/guard-time concerns.

Neither is universally better. FDM suits continuous spectral allocation;
TDM suits digital time sharing. Statistical TDM improves utilization for
bursty users but adds headers/buffering.

## Q19. What is TLS?

TLS creates a secure channel over a reliable ordered transport. The handshake:

1. negotiates version/algorithms;
2. establishes shared traffic keys, normally with ephemeral Diffie-Hellman;
3. authenticates the server certificate/signature;
4. binds the transcript with `Finished`;
5. protects records using authenticated encryption.

TLS provides confidentiality, integrity, and peer authentication under the
certificate/identity model. It does not authorize application actions, clean
malware, or secure a compromised endpoint. The current TLS 1.3 specification
is [RFC 9846](https://www.rfc-editor.org/info/rfc9846/), which obsoletes RFC
8446.

## Q20. Socket, port, and client/server lifecycle?

A socket is an OS communication endpoint. A TCP connection is identified by
protocol plus source/destination IP and port.

TCP server:

```text
socket -> bind -> listen -> accept -> recv/send -> close
```

TCP client:

```text
socket -> connect -> send/recv -> close
```

`send`/`recv` can transfer fewer bytes than requested; robust code loops.
Network byte order is big-endian. A server should validate lengths before
allocation and define application framing.

## Networking board drill checklist

- Draw encapsulation and one router hop.
- Draw TCP handshake with exact sequence/ACK numbers.
- Contrast `rwnd` and `cwnd`.
- Trace DORA and DNS resolution.
- Subnet a `/24` and perform longest-prefix match.
- Draw ARP for a remote destination via a gateway.
- Compare distance vector and link state.
- Trace GBN/SR after a loss.
- Explain TLS after TCP and list what it cannot protect.

---

# 6. Software Engineering

**Deep source:** `08_SOFTWARE_ENGINEERING_SLIDE_COMPLETE.md`.

## Q1. Software engineering versus programming?

Programming implements executable behavior. Software engineering includes
requirements, architecture/design, implementation, verification, deployment,
operations, maintenance, security, teamwork, estimation, and risk over the
system lifecycle.

The distinction is scale and lifecycle responsibility, not that one writes
code and the other does not.

## Q2. SDLC phases?

Typical activities:

```text
feasibility/planning -> requirements -> design -> implementation
-> testing -> deployment -> operation/maintenance -> retirement
```

Real processes include feedback loops. A sequential diagram does not mean
requirements never change or testing begins only after all code is complete.

## Q3. Waterfall versus Agile?

Waterfall emphasizes planned phase gates, baselines, and predictable
deliverables; it can fit stable/regulatory work with expensive changes.
Agile uses short increments, frequent feedback, reprioritization, and
continuous technical quality.

Agile values working software and change response, but does not say "no
documentation" or "no plan"
([Agile Manifesto](https://agilemanifesto.org/)).

## Q4. Scrum roles, artifacts, and events?

The current Scrum Guide calls them accountabilities:

- Product Owner maximizes product value and orders Product Backlog.
- Scrum Master supports Scrum effectiveness and removes organizational
  impediments.
- Developers create a usable Increment.

Artifacts: Product Backlog, Sprint Backlog, Increment, each with its
commitment (Product Goal, Sprint Goal, Definition of Done). Events include
Sprint, Planning, Daily Scrum, Review, and Retrospective. Scrum is defined by
the [official Scrum Guide](https://scrumguides.org/download.html).

## Q5. Kanban versus Scrum?

Scrum uses timeboxed Sprints, defined accountabilities/events, and a Sprint
Goal. Kanban visualizes workflow, limits work in progress, measures flow, and
pulls new work when capacity is available. Teams can combine Scrum with
Kanban flow practices.

Core Kanban metrics: lead time, cycle time, throughput, work in progress, and
work-item age.

## Q6. Functional versus nonfunctional requirements?

Functional requirements specify services/behaviors: "system shall allow a
student to register." Nonfunctional requirements specify qualities and
constraints: latency, availability, security, accessibility, compliance,
capacity.

Make NFRs measurable. "Fast" is weak; "95th-percentile response time below
300 ms for 1,000 concurrent users under workload X" is testable.

## Q7. Requirement elicitation and validation?

Elicitation techniques: interviews, workshops, observation, questionnaires,
document/interface analysis, prototypes, and use cases/user stories.

Validate requirements for correctness, completeness, consistency,
feasibility, priority, traceability, testability, and stakeholder agreement.
Prototypes reveal misunderstandings but are not automatically production
architecture.

## Q8. Use case, user story, and acceptance criteria?

A use case describes actor-goal interaction with preconditions, main flow,
alternatives, and postconditions. A user story is a lightweight value
statement:

> As a role, I want capability, so that benefit.

Acceptance criteria make completion testable. Neither format removes the need
for domain rules, NFRs, or interface contracts.

## Q9. Verification versus validation?

- Verification: are we building the product correctly against specification?
- Validation: are we building the right product for stakeholder need?

Reviews/static analysis/unit tests support verification; user acceptance,
field evaluation, and stakeholder feedback support validation. Activities can
overlap.

## Q10. Cohesion and coupling?

High cohesion keeps closely related responsibilities within a module. Low
coupling reduces knowledge/dependency between modules. Aim for both.

Common coupling channels include shared global state, concrete construction,
temporal call ordering, unstable data formats, and broad interfaces.

## Q11. SOLID with one concrete example each?

- SRP: `Invoice` should not also print, persist, and email itself.
- OCP: add a new `PaymentStrategy` implementation without editing a giant
  type switch.
- LSP: subtype preserves preconditions/postconditions/invariants; a square
  with independent width/height setters violates a rectangle contract.
- ISP: clients depend on small role interfaces, not unused operations.
- DIP: high-level policy depends on abstraction; inject repository/gateway
  rather than constructing a concrete DB client inside business logic.

## Q12. Design pattern versus algorithm?

A design pattern is a named, reusable collaboration structure with context,
forces, and consequences. An algorithm is a procedure computing a result.

Examples:

- Strategy selects interchangeable behavior.
- Observer publishes changes to subscribers.
- Factory Method delegates object creation.
- Adapter converts one interface to another.
- Decorator adds behavior by wrapping.

Do not force patterns into small code. A pattern earns its cost when it
isolates real variation or collaboration complexity.

## Q13. Common design-pattern comparison questions?

- Adapter changes an interface; Decorator preserves an interface while adding
  behavior; Facade offers a simplified front to a subsystem.
- Strategy changes an algorithm; State changes behavior as internal state
  changes.
- Observer is one-to-many notification; Mediator centralizes many-to-many
  collaboration.
- Chain of Responsibility passes a request through potential handlers;
  Command packages an operation as an object.
- Proxy controls access to another object; Decorator adds responsibility.

## Q14. Unit, integration, system, acceptance, and regression testing?

- Unit: small isolated behavior.
- Integration: component boundaries, protocols, database/external services.
- System: complete deployed behavior against system requirements.
- Acceptance: stakeholder/business suitability.
- Regression: re-run tests after change to catch broken existing behavior.

The test pyramid is guidance: many fast unit tests, fewer integration tests,
and a focused end-to-end layer. Risk can justify a different mix.

## Q15. Black-box versus white-box testing?

Black-box derives tests from behavior/specification: equivalence partitions,
boundary values, decision tables, state transitions. White-box uses code
structure: statement/branch/path/data-flow coverage.

100% statement or branch coverage does not prove correctness. Assertions,
test data quality, oracles, mutation testing, and requirement coverage matter.

## Q16. Stubs, mocks, fakes, and drivers?

- Stub returns canned values.
- Mock verifies expected interactions.
- Fake is a simplified working implementation, e.g. in-memory repository.
- Driver calls a lower-level component when the normal caller is unavailable.

Over-mocking implementation details makes refactoring painful; test observable
contracts and use integration tests for important boundaries.

## Q17. CI, continuous delivery, and continuous deployment?

- CI: frequently merge small changes; automated build/tests/security checks.
- Continuous delivery: every successful change is releasable, but release is
  a business/manual decision.
- Continuous deployment: qualifying changes automatically reach production.

Good pipelines include reproducible builds, artifact immutability, secrets
management, environment promotion, rollback/roll-forward, observability, and
approval controls proportional to risk.

## Q18. Cyclomatic complexity?

For a connected control-flow graph:

$$
M=E-N+2.
$$

It equals the number of linearly independent paths and is often decision
points plus one. It guides testing/refactoring but is not a complete quality
metric; readable domain complexity can be legitimate.

## Q19. COCOMO and function points?

COCOMO estimates effort from size and cost drivers:

$$
PM=A(\text{Size})^E\prod_i EM_i.
$$

Function points estimate user-visible functionality using inputs, outputs,
inquiries, internal files, and external interfaces with adjustment factors.
Both are estimation models, not exact promises. Calibrate with local history
and express uncertainty/range.

## Q20. Technical debt and changing requirements?

Technical debt is future cost/risk created by a design/implementation choice.
Track its principal, interest, affected risks, and payoff plan.

For changing requirements: maintain traceability; assess architecture, tests,
security, data migration, schedule, and stakeholder impact; prioritize;
version contracts; use modular design and automated regression checks.

## Q21. KPI versus metric?

A metric is any measurement. A KPI is a small strategic measure tied to an
important objective. Useful engineering metrics include lead time, deployment
frequency, change-failure rate, recovery time, escaped defects, reliability,
and customer outcomes. Avoid optimizing vanity counts such as lines of code.

## SWE board drill checklist

- Draw an SDLC feedback loop and a Scrum/Kanban board.
- Write one measurable functional requirement and NFR.
- Draw use-case, class, sequence, activity/state, component, and deployment
  diagrams for the appropriate question.
- Refactor one SOLID violation.
- Compare adjacent design patterns with code.
- Design tests using boundaries, branches, and failure paths.
- Explain a CI/CD pipeline, rollback, and production feedback.

---

# 7. Computer Security

**Deep source:** `13_SECURITY_CORE_COMPLETE.md`.

## Q1. CIA triad?

- **Confidentiality:** prevent unauthorized disclosure.
- **Integrity:** prevent or detect unauthorized/incorrect modification.
- **Availability:** keep information/services accessible to authorized users
  when needed.

Security is a set of properties relative to assets, actors, and threats. A
system may preserve confidentiality while failing availability. NIST uses the
same three-pillar model
([NIST CIA explanation](https://www.nccoe.nist.gov/publication/1800-26/VolA/1800-26A.html)).

## Q2. How do you ensure confidentiality?

Start with a threat model and data classification, then combine:

1. data minimization and retention limits;
2. authentication and least-privilege authorization;
3. encryption in transit and at rest;
4. key separation, access control, rotation, and recovery;
5. endpoint hardening, patching, segmentation, and secrets protection;
6. secure backups and controlled sharing;
7. logs/alerts for access and exfiltration;
8. staff/process controls and incident response.

Encryption is central but not sufficient. An authorized compromised process
can read plaintext after decryption.

## Q3. How do you ensure confidentiality of files on your system?

Give a layered answer:

- restrictive owner/group/ACL permissions and separate accounts;
- full-disk encryption for lost/offline devices;
- file/application-level authenticated encryption for selected sensitive
  data;
- KMS/HSM/OS keystore, with keys separate from ciphertext;
- TLS/SFTP/VPN for transfer;
- encrypted, access-controlled backups with restore tests;
- screen lock, secure boot, patching, malware defense, and physical control;
- audit file access and revoke access when roles change;
- securely erase keys/data according to storage technology and policy.

Full-disk encryption does not protect files after an attacker logs into the
running unlocked machine.

## Q4. Should database entries be encrypted?

Encrypt by sensitivity and threat model, not blindly.

| Layer | Primarily protects against | Limitation |
|---|---|---|
| disk/full-volume encryption | stolen/offline media | running DB reads plaintext |
| DB/TDE | data files/backups outside DB engine | privileged DB compromise may read |
| application/field encryption | selected columns from DB-only compromise | search/indexing/rotation complexity |
| TLS | network interception | not data at rest/endpoints |

Randomized authenticated encryption hides equality patterns but prevents
ordinary equality/range indexes. Deterministic encryption enables equality
lookup but leaks repetitions/frequency. Tokenize data that need not be
recoverable locally. OWASP recommends selecting the encryption layer from the
threat model and separating keys from data
([OWASP cryptographic storage](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)).

## Q5. Encryption, hashing, encoding, MAC, and signature?

| Primitive | Secret? | Reversible? | Main property |
|---|---|---|---|
| Encoding | no | yes | representation/compatibility |
| Encryption | key | with key | confidentiality; AEAD also integrity |
| Hash | no | no practical inverse | digest/integrity building block |
| MAC/HMAC | shared secret | no | integrity + shared-key authentication |
| Digital signature | private signing key | verification only | integrity + public verifiability/authenticity |

Hashing alone does not hide data. Encryption without authentication can permit
undetected tampering; prefer AEAD such as AES-GCM or ChaCha20-Poly1305.

## Q6. Symmetric versus asymmetric cryptography?

Symmetric algorithms use one shared secret and are efficient for bulk data.
Asymmetric algorithms use a public/private key pair for signatures,
authentication, or establishing secrets, but are slower and require public
key authenticity.

Hybrid systems use asymmetric authentication/key agreement to derive
symmetric traffic keys, as TLS does.

## Q7. Why should passwords be hashed rather than encrypted?

The server should verify a password, not recover it. Store:

$$
stored=KDF(password,salt,\text{cost parameters})
$$

using a password KDF such as Argon2id, scrypt, bcrypt, or appropriately
configured PBKDF2. A unique random salt defeats precomputed tables and makes
equal passwords hash differently. A pepper can add a separately stored
secret. Tune memory/time cost and support rehash-on-login.

Plain SHA-256 is fast and therefore helps attackers guess quickly.

## Q8. Authentication versus authorization versus accounting?

- Authentication: who are you?
- Authorization: what may you do to this object/action?
- Accounting/auditing: what happened, by whom, and when?

Authentication success never implies access to every resource. Check
authorization server-side for each protected object/action.

## Q9. RBAC versus ABAC?

RBAC grants permissions to roles assigned to users: simple and auditable but
can cause role explosion. ABAC evaluates attributes of subject, resource,
action, and environment: flexible contextual policy but harder to reason
about.

Both should enforce default deny, least privilege, separation of duties, and
complete mediation.

## Q10. What does TLS provide, and how?

TLS 1.3 provides a secure channel with server authentication, optional client
authentication, confidentiality, and integrity. Ephemeral key exchange can
provide forward secrecy. The certificate binds a public key to an identity;
`CertificateVerify` proves private-key possession and binds the transcript;
`Finished` authenticates the negotiated transcript using derived key
material.

TLS does not secure data before encryption/after decryption, authorize users,
or fix vulnerable application logic. Current standard:
[RFC 9846](https://www.rfc-editor.org/info/rfc9846/).

## Q11. Threat, vulnerability, exploit, and risk?

- Threat: potential harmful actor/event.
- Vulnerability: weakness that can be abused.
- Exploit: method/code that exercises a vulnerability.
- Risk: expected harm, often reasoned as likelihood/exposure times impact.

A vulnerability without plausible exposure may have lower immediate risk but
still deserves lifecycle handling. Risk rankings are decision aids, not exact
physics.

## Q12. Least privilege, defense in depth, fail secure?

- Least privilege grants only required rights for required time.
- Defense in depth uses independent layers so one failure is not total
  compromise.
- Fail secure/closed means errors default to denying the sensitive action,
  with designed safe degradation rather than accidental total outage.

These are architecture principles, not products.

## Q13. SQL injection and prevention?

Injection occurs when untrusted data changes query syntax/structure.

Bad:

```java
String sql = "SELECT * FROM users WHERE name='" + input + "'";
```

Good:

```java
PreparedStatement ps =
    conn.prepareStatement("SELECT id, name FROM users WHERE name = ?");
ps.setString(1, input);
```

Use parameterized queries for values, allow-list validation for identifiers
that cannot be parameters, least-privilege DB accounts, safe error handling,
and security tests. Escaping alone is fragile.

## Q14. XSS versus CSRF?

XSS injects script/content that executes under a trusted origin. Prevent with
context-specific output encoding, safe DOM APIs, sanitization for allowed
HTML, and CSP as defense in depth.

CSRF causes an authenticated browser to send an unwanted state-changing
request. Prevent with unpredictable CSRF tokens, `SameSite` cookies,
Origin/Referer validation, and reauthentication for high-risk actions.

XSS can often bypass CSRF protections because it runs in the trusted origin,
so both must be prevented.

## Q15. IDOR/BOLA?

Broken object-level authorization occurs when an attacker changes an object
identifier and the server fails to verify access. Unpredictable IDs are not
the main fix. Every request must authorize the authenticated subject for the
requested object and action.

## Q16. Firewall, WAF, IDS, and IPS?

- Network firewall filters flows/packets using network/transport state.
- WAF inspects HTTP/application patterns.
- IDS detects and alerts.
- IPS is inline and can block.

Signatures detect known patterns; anomaly systems can detect deviation but
produce false positives. None replaces endpoint patching, secure coding, or
authorization.

## Q17. Stateful versus stateless packet filtering?

Stateless filtering evaluates each packet independently against header rules.
It is simple/fast but lacks connection context. Stateful filtering tracks
flow state and permits packets consistent with established connections,
requiring memory and protection against state exhaustion.

Application gateways/proxies can understand higher-level protocol semantics
but add latency/complexity and become trusted endpoints.

## Q18. Digital signature versus MAC: which provides nonrepudiation?

A MAC proves that *someone holding the shared key* generated it; every verifier
could forge the same MAC. A signature is generated only with the private key
and publicly verified, so it supports stronger third-party attribution.

Practical nonrepudiation still depends on key custody, identity proofing,
timestamping, legal/process context, and compromise handling.

## Q19. IND-CPA and why encryption needs randomness?

IND-CPA informally says an efficient attacker choosing two equal-length
messages cannot distinguish which one was encrypted, even with chosen-
plaintext access, except negligible advantage. Deterministic encryption
reveals repeated plaintexts and generally fails this notion. Random nonces/IVs
or randomized schemes prevent equal messages from always producing equal
ciphertexts. Nonce uniqueness requirements are algorithm-specific and
critical.

## Q20. Perfect secrecy and one-time pad?

OTP uses a uniformly random key independent of the message, as long as the
message, used once:

$$
C=M\oplus K,\qquad M=C\oplus K.
$$

For every ciphertext and candidate plaintext of the same length, exactly one
key maps between them, so ciphertext reveals no information about the
plaintext. Reusing a key leaks:

$$
C_1\oplus C_2=M_1\oplus M_2.
$$

OTP is impractical because keys must be truly random, message-length,
distributed securely, and never reused.

## Q21. File/database key management?

Use envelope encryption:

```text
KMS/HSM protects KEK
        |
        v
KEK encrypts DEK
        |
        v
DEK encrypts data with AEAD
```

Store key identifiers/versions with ciphertext; separate duties and systems;
rotate, revoke, audit, back up/recover keys; protect keys in memory; never
hard-code or commit them. Losing a key can permanently lose data; leaking it
can defeat all ciphertext protection.

## Security board drill checklist

- Answer CIA with one failure example for each property.
- Design file confidentiality against theft and against live compromise.
- Decide which DB columns/layers to encrypt and state leakage/trade-offs.
- Draw TLS handshake at certificate/key/Finished level.
- Compare hash, MAC, signature, encryption, and password KDF.
- Fix SQL injection, XSS, CSRF, and IDOR.
- Explain OTP assumptions, nonce uniqueness, and key separation.
- Threat-model one application using assets, actors, entry points, and
  mitigations.

---

# 8. Database Management Systems

**Deep source:** `05_DBMS_SLIDE_COMPLETE.md`.

## Q1. Why DBMS instead of plain files?

A DBMS centralizes structured schema/querying, constraints, concurrent
transactions, indexing/optimization, access control, backup/recovery, and data
independence. Plain files may be appropriate for simple append-only or
single-process data, but applications otherwise reimplement these hard
properties inconsistently.

## Q2. Schema, instance, and three-schema architecture?

Schema is the relatively stable structure; instance is current data.

- External level: user/application views.
- Conceptual level: logical global schema.
- Internal level: physical storage/access paths.

Logical data independence shields external views from conceptual changes;
physical data independence shields logical schema from storage changes.

## Q3. Superkey, candidate, primary, composite, foreign key?

- Superkey uniquely identifies a tuple.
- Candidate key is a minimal superkey.
- Primary key is the selected candidate key.
- Composite key has multiple attributes.
- Foreign key references a candidate/primary key in another or the same
  relation and enforces referential integrity.

`UNIQUE` and `PRIMARY KEY` both enforce uniqueness in typical SQL systems, but
primary key also implies `NOT NULL` and identifies the table's chosen key.

## Q4. `NULL` and three-valued logic?

`NULL` means missing/unknown/not applicable, depending on schema semantics; it
is not zero or empty string. Comparisons such as `x = NULL` produce `UNKNOWN`,
so use `IS NULL`.

`WHERE` keeps only rows for which the predicate is `TRUE`; both `FALSE` and
`UNKNOWN` are filtered. `NOT IN` can surprise when its set contains `NULL`;
`NOT EXISTS` is often safer for anti-joins.

## Q5. INNER and outer joins?

```sql
SELECT s.id, s.name, d.name AS department
FROM student AS s
LEFT JOIN department AS d
  ON d.id = s.department_id;
```

- INNER returns matched pairs only.
- LEFT retains every left row and null-extends unmatched right columns.
- RIGHT is symmetric.
- FULL retains unmatched rows from both.
- CROSS forms a Cartesian product.

Place a condition in `ON` versus `WHERE` carefully for outer joins; a
right-side `WHERE` filter can remove null-extended rows and effectively turn a
left join into an inner one.

## Q6. `WHERE` versus `HAVING`?

`WHERE` filters input rows before grouping. `HAVING` filters groups after
aggregation.

```sql
SELECT department_id, AVG(cgpa) AS avg_cgpa
FROM student
WHERE active = TRUE
GROUP BY department_id
HAVING AVG(cgpa) >= 3.5;
```

## Q7. Correlated subquery versus join?

A correlated subquery references the outer row and is conceptually evaluated
per outer row, though an optimizer may decorrelate it.

```sql
SELECT e.*
FROM employee AS e
WHERE salary > (
    SELECT AVG(x.salary)
    FROM employee AS x
    WHERE x.department_id = e.department_id
);
```

Joins are not automatically faster; compare logical clarity and actual
execution plans.

## Q8. ER model: cardinality and participation?

Entities have identity and attributes; relationships associate entities.
Cardinality constrains maximum participation (`1:1`, `1:N`, `M:N`);
participation constrains minimum (`total/mandatory` versus partial/optional).

Map `M:N` to an associative relation containing both foreign keys plus
relationship attributes. A weak entity needs an identifying owner
relationship and partial key.

## Q9. Functional dependency?

`X -> Y` means any two legal tuples agreeing on `X` must agree on `Y`. It is a
semantic schema constraint, not an accidental pattern in one sample.

Attribute closure `X+` repeatedly adds attributes determined by FDs. Use it
to test superkeys and implication.

## Q10. Normalization and anomalies?

Normalization decomposes a schema to reduce redundant facts and insertion,
update, deletion anomalies while seeking lossless join and useful dependency
preservation.

Example:

```text
ENROLL(StudentId, StudentName, CourseId, CourseTitle, Instructor)
key = (StudentId, CourseId)
StudentId -> StudentName
CourseId  -> CourseTitle, Instructor
```

Student and course details repeat. Decompose:

```text
STUDENT(StudentId, StudentName)
COURSE(CourseId, CourseTitle, Instructor)
ENROLL(StudentId, CourseId)
```

## Q11. 1NF, 2NF, 3NF, BCNF?

- 1NF: relation attributes contain atomic values under the model.
- 2NF: 1NF and no non-prime attribute partially depends on a proper subset of
  a candidate key.
- 3NF: for every nontrivial `X -> A`, `X` is a superkey or `A` is prime.
- BCNF: for every nontrivial `X -> Y`, `X` is a superkey.

BCNF is stricter. A BCNF decomposition is lossless under the standard
algorithm but may lose dependency preservation; 3NF synthesis can preserve a
minimal cover and be lossless with a key relation.

## Q12. Lossless join and dependency preservation?

A decomposition is lossless if joining valid decomposed relations produces
exactly the original relation, with no spurious tuples. For binary
decomposition `R -> R1,R2`, it is lossless under FDs if:

$$
(R_1\cap R_2)\to R_1
\quad\text{or}\quad
(R_1\cap R_2)\to R_2.
$$

Dependency preservation means original FDs can be enforced by constraints on
individual decomposed relations without joining them.

## Q13. ACID?

- Atomicity: all effects commit or none remain.
- Consistency: a transaction preserves declared invariants when started from
  a valid state; DB constraints plus correct application logic matter.
- Isolation: concurrent effects behave according to an isolation model,
  ideally equivalent to an allowed serial execution under serializability.
- Durability: committed effects survive acknowledged failures within the
  system's guarantees.

## Q14. Schedule and conflict serializability?

Two operations conflict when from different transactions, access the same
item, and at least one writes. Build a precedence graph with edge `Ti -> Tj`
when a conflicting operation of `Ti` occurs first. The schedule is conflict
serializable iff the graph is acyclic; a topological order gives an equivalent
serial order.

```text
T1: W(X) --------> T2: R(X)
T2: W(Y) --------> T1: R(Y)
```

Edges both ways form a cycle, so this schedule is not conflict serializable.

## Q15. Two-phase locking and strict 2PL?

2PL has:

1. growing phase: acquire, do not release;
2. shrinking phase: release, acquire no new lock.

It guarantees conflict serializability. Strict 2PL holds exclusive locks
until commit/abort, preventing dirty reads/writes and cascading aborts. 2PL
can deadlock.

## Q16. Database deadlock?

Transactions wait in a cycle for locks. Detect a cycle in the wait-for graph,
then choose a victim to roll back and retry. Prevention approaches include
global lock ordering, timestamp policies, conservative acquisition, and
timeouts. Keep transactions short and indexes selective to reduce lock scope,
but do not claim this eliminates all deadlocks.

## Q17. Isolation anomalies and levels?

Anomalies include dirty read, nonrepeatable read, phantom, lost update, and
write skew. SQL level names do not fully specify every DB implementation;
know the engine's actual guarantees.

Snapshot isolation avoids many read/write conflicts by reading a snapshot but
can allow write skew. Serializable execution prevents anomalies representable
as no serial order, sometimes by blocking or abort/retry.

## Q18. What is MVCC?

MVCC stores/identifies multiple row versions so readers can observe a
consistent snapshot while writers create new versions. It reduces read-write
blocking but needs visibility rules, cleanup/vacuum, and conflict handling.
It is an implementation strategy, not by itself a guarantee of serializable
isolation. PostgreSQL's documentation describes snapshots and nonblocking
reader/writer behavior
([PostgreSQL MVCC](https://www.postgresql.org/docs/17/mvcc-intro.html)).

## Q19. Index and search key?

An index is an auxiliary access structure mapping search-key values to record
locations. A search key need not be unique or a candidate key. Indexes speed
selected reads/order/group/join patterns but consume space and add maintenance
on writes.

Composite index order matters. An index on `(a,b)` naturally supports leading
`a` conditions and then `b`; it does not automatically act like an index on
`b` alone.

## Q20. B+ tree versus B-tree versus hash index?

B+ tree stores data pointers/records at leaves, keeps internal separator keys,
links leaves, and has high fan-out. It supports equality, ranges, sorted scans,
and `O(log_f N)` page traversals.

A B-tree may store data in internal nodes too. A hash index is strong for
equality but has no natural ordered/range traversal. Dynamic hashing manages
growth differently from balanced ordered trees.

## Q21. Clustered versus nonclustered index?

A clustered organization determines or closely follows data's physical order,
making ranges efficient but allowing only one primary physical ordering.
Nonclustered/secondary indexes are separate structures pointing to rows or
primary keys; many can exist but may require random lookups.

Exact terminology differs by DBMS, so describe the physical consequence.

## Q22. Query processing and join algorithms?

Pipeline:

```text
SQL -> parse/analyze -> logical plan -> rewrite/optimize
-> physical plan -> operators -> tuples/results
```

Join choices:

- nested loop: general; excellent with small outer and indexed inner;
- block nested loop: reduces repeated I/O;
- sort-merge: good for sortable/order-compatible inputs and ranges/equality;
- hash join: excellent expected performance for equality joins, not ranges.

## Q23. What does an optimizer do?

It enumerates/reasons about equivalent plans and estimates cardinality,
selectivity, I/O, CPU, memory, and sometimes parallel/network cost. It chooses
access paths, join algorithms, and join order. Bad statistics/correlation
estimates can choose a poor plan.

`EXPLAIN` shows estimates; `EXPLAIN ANALYZE` executes and adds actual
measurements, so use it cautiously on modifying/expensive queries. PostgreSQL
documents plans as trees of scan/join/aggregate nodes
([PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)).

## Q24. Write-ahead logging and recovery?

WAL rule: a change's log record must become durable before the corresponding
dirty data page is written. At commit, required commit/log records become
durable before acknowledging success.

Recovery analyzes state, redoes effects that must appear, and undoes incomplete
transactions depending on the recovery design. Checkpoints limit restart
work; they do not mean every dirty page is necessarily written immediately.

## Q25. View, materialized view, procedure, function, trigger?

- View: stored query, normally computed when read.
- Materialized view: stored result requiring refresh/maintenance.
- Procedure/function: server-side named logic with DB-specific transaction
  semantics.
- Trigger: automatic reaction to data/schema events.

Triggers can enforce cross-cutting rules/audit but hide control flow and can
cause recursion/order surprises. Prefer declarative constraints for rules they
can express.

## Q26. SQL injection: DBMS answer?

Use prepared parameterized statements; never concatenate untrusted values
into SQL. Restrict account privileges, separate read/write/admin roles,
validate dynamic identifiers against an allow-list, protect credentials,
patch the DB, encrypt transport, and audit sensitive operations. Database
encryption does not prevent an injected authorized query from returning
plaintext.

## DBMS board drill checklist

- Design an ER model with cardinality/participation and map it to relations.
- Find attribute closure, candidate key, and minimal cover.
- Normalize a schema and test lossless/dependency preservation.
- Write joins, grouping/HAVING, `EXISTS`, and highest-per-group SQL.
- Draw a B+ tree split and compare index choices.
- Build a precedence/wait-for graph.
- Explain 2PL, MVCC, isolation, and retry.
- Draw query-plan operators and WAL order.

---

# 9. Artificial Intelligence

**Deep source:** `09_ARTIFICIAL_INTELLIGENCE_SLIDE_COMPLETE.md`.

## Q1. AI versus ML?

AI is the broader study/design of agents that perceive, reason, search, plan,
decide, act, and learn. ML is a family of methods that learn models/behavior
from data. A rule-based planner is AI without ML; a classifier is ML used
inside or outside an agent.

## Q2. What is a rational agent?

A rational agent chooses the action expected to maximize its performance
measure given percept history, prior knowledge, available actions, and
computational limits. Rational does not mean omniscient or always successful:
uncertainty and limited information can make a rational action fail.

PEAS describes a task environment: Performance measure, Environment,
Actuators, Sensors.

## Q3. State-space search problem?

Specify:

- state space;
- initial state;
- actions/successor function;
- transition model;
- goal test;
- step/path cost.

A state is an equivalence class containing all information needed for future
decisions. A search-tree node additionally stores search metadata such as
parent, action, depth, and path cost.

## Q4. BFS, DFS, UCS, greedy, A*?

| Search | Frontier order | Complete? | Optimal? |
|---|---|---|---|
| BFS | shallowest depth | finite branching | equal step costs |
| DFS | deepest | not in infinite-depth/cycles | no |
| UCS | lowest `g` | positive/lower-bounded costs | yes under assumptions |
| Greedy | lowest `h` | depends on space handling | no generally |
| A* | lowest `g+h` | under standard conditions | with heuristic/graph assumptions |

Tree search can regenerate states; graph search records explored/best costs.
For UCS/A*, a Boolean visited flag can be insufficient: store best `g` and
reopen if required.

## Q5. Admissible versus consistent heuristic?

Admissible:

$$
0\le h(n)\le h^*(n)
$$

so it never overestimates optimal remaining cost.

Consistent:

$$
h(n)\le c(n,n')+h(n')
$$

for every edge. This makes `f=g+h` nondecreasing along paths. Consistency
implies admissibility when goal heuristic is zero and reachability assumptions
hold. Graph A* with permanent closing relies cleanly on consistency; an
admissible inconsistent heuristic may require reopening.

## Q6. Is A* optimal?

Not unconditionally. A* tree search is optimal with admissible heuristic and
standard positive/lower-bounded cost conditions. Graph-search variants need
correct duplicate handling; consistency permits finalizing a popped state.

Proof idea: before a suboptimal goal of cost greater than `C*` can be popped,
some frontier node on an optimal path has:

$$
f(n)=g(n)+h(n)\le C^*.
$$

The suboptimal goal has `f=g>C*`, contradiction with minimum-`f` selection.

## Q7. What happens if `h(n)=0` in A*?

Then:

$$
f(n)=g(n).
$$

A* becomes uniform-cost search, equivalent to Dijkstra's ordering in the usual
nonnegative graph setting. It remains optimal under those assumptions but
loses heuristic direction. Say "may expand more nodes" rather than claiming
it is always inefficient.

## Q8. Local search, hill climbing, simulated annealing?

Hill climbing keeps one current state and moves to a better neighbor; it can
get stuck at local maxima, plateaus, and ridges. Random restarts help.

Simulated annealing sometimes accepts worse moves:

$$
P(\text{accept worse move})=\exp(-\Delta/T)
$$

for cost increase `Delta>0`. High temperature explores; cooling becomes
selective. Theoretical convergence needs extremely slow schedules; practical
schedules are heuristic.

## Q9. Genetic algorithm?

Maintain a population of encoded candidates; evaluate fitness; select parents;
recombine/crossover; mutate; replace; repeat. It is useful for irregular
search spaces but gives no automatic optimality guarantee. Representation,
fitness design, diversity, constraint handling, and stopping criteria dominate
performance.

## Q10. Minimax?

For deterministic, zero-sum, perfect-information games:

$$
V(s)=
\begin{cases}
Utility(s), & s\text{ terminal},\\
\max_{a}V(Result(s,a)), & s\text{ is MAX},\\
\min_{a}V(Result(s,a)), & s\text{ is MIN}.
\end{cases}
$$

It assumes the opponent chooses the worst outcome for MAX. With branching
factor `b` and depth `m`, time is `O(b^m)` and DFS implementation uses
`O(bm)` memory.

## Q11. Can a human beat an agent if minimax is generated to infinite depth?

Clarify the premise.

- In a finite deterministic zero-sum perfect-information game, complete
  minimax gives an optimal strategy. A human cannot force an outcome better
  than the game's minimax value against it, but may draw or attain the same
  value.
- A literally infinite-depth tree cannot be completely generated in finite
  time. Infinite games need mathematical conditions, terminal/repeated-state
  handling, or a convergent value definition.
- Practical agents use depth cutoffs, evaluation functions, iterative
  deepening, transposition tables, and alpha-beta pruning. Cutoff evaluation
  removes the guarantee of perfect play.

See [Berkeley CS188 minimax](https://inst.eecs.berkeley.edu/~cs188/textbook/games/minimax.html).

## Q12. Alpha-beta pruning?

`alpha` is MAX's best guaranteed value so far; `beta` is MIN's best guaranteed
value. When `alpha>=beta`, remaining children cannot influence the ancestor's
choice and are pruned.

Alpha-beta returns the same minimax value. With ideal ordering it can reduce
effective time to about `O(b^(m/2))`; worst case remains `O(b^m)`.

```text
             MAX
          /       \
       MIN         MIN
     / | \       / | \
    3 12  8     2  X  X

Left MIN = 3, so alpha=3.
Right MIN sees 2, so beta=2 <= alpha; prune X, X.
```

## Q13. Minimax versus expectimax?

Minimax models an adversary choosing the worst child. Expectimax models chance
or a stochastic policy:

$$
V(s)=\sum_{s'}P(s'\mid s,a)V(s')
$$

at chance nodes. Use minimax for optimal opposition, expectimax when
transition/opponent behavior has a known probabilistic model.

## Q14. CSP?

A constraint satisfaction problem has variables, domains, and constraints.
Backtracking assigns variables incrementally.

Heuristics:

- MRV: choose the variable with fewest legal values;
- degree: break ties using most constraints on unassigned variables;
- LCV: try the value eliminating fewest neighbor options;
- forward checking: remove values inconsistent with the latest assignment;
- AC-3: repeatedly enforce arc consistency.

## Q15. Arc consistency and AC-3?

Arc `Xi -> Xj` is consistent if every value in `Di` has some supporting value
in `Dj`. AC-3 keeps a queue of arcs; revising a domain may re-enqueue arcs from
other neighbors. Arc consistency can detect failure and prune, but does not
guarantee a complete global solution.

## Q16. Bayesian network?

A Bayesian network is a DAG whose nodes are random variables and edges encode
direct dependency under the model. The joint factors:

$$
P(X_1,\ldots,X_n)=\prod_iP(X_i\mid Parents(X_i)).
$$

It compactly represents conditional independence. Exact inference by
enumeration/variable elimination can be exponential in graph width; sampling
approximates.

## Q17. HMM?

An HMM has hidden Markov states, observations emitted conditionally from
states, an initial distribution, transition model, and emission model.

```text
X1 ----> X2 ----> X3       hidden states
|        |        |
v        v        v
E1       E2       E3       observations
```

- filtering: current state given observations so far;
- prediction: future state;
- smoothing: past state given later evidence;
- Viterbi: most probable hidden-state sequence.

## Q18. MDP and Bellman optimality?

An MDP contains states `S`, actions `A`, transition probabilities, rewards,
and discount `gamma`. A policy maps states to actions.

$$
V^*(s)=
\max_a\sum_{s'}P(s'\mid s,a)
\left[R(s,a,s')+\gamma V^*(s')\right].
$$

The Bellman equation is an optimality condition. Value iteration repeatedly
applies the backup; policy iteration alternates policy evaluation and
improvement.

## Q19. Q-learning?

$$
Q(s,a)\leftarrow Q(s,a)+\alpha
\left[r+\gamma\max_{a'}Q(s',a')-Q(s,a)\right].
$$

It is off-policy: target uses greedy next action even when behavior explores.
Convergence in the tabular setting needs adequate exploration, suitable
learning rates, stationary MDP assumptions, and bounded rewards. Function
approximation changes the guarantee.

## AI board drill checklist

- Formulate one real problem as state-space search.
- Trace BFS/UCS/A* and show duplicate handling.
- Test a heuristic for admissibility and consistency.
- Prove A* and explain `h=0`.
- Draw minimax and alpha-beta cutoffs.
- Formulate map coloring as CSP and run MRV/AC-3.
- Factor a Bayesian-network joint and draw an HMM.
- Write Bellman/value-iteration/Q-learning equations and explain each term.

---

# 10. Operating Systems

**Deep source:** `06_OPERATING_SYSTEMS_SLIDE_COMPLETE.md`.

## Q1. What does an OS do?

It provides abstractions and manages/protects resources:

- process/thread execution and CPU scheduling;
- virtual memory and protection;
- files/storage and I/O devices;
- IPC/network interfaces;
- authentication/access control;
- controlled sharing, accounting, and failure handling.

Two useful views: resource manager and extended/virtual machine.

## Q2. Kernel mode versus user mode and system call?

User mode cannot execute privileged instructions or directly access protected
kernel memory/devices. Kernel mode can. A system call is a controlled entry
that validates arguments, changes privilege through a trap mechanism, performs
the service, and returns.

A library call is not necessarily a system call; `strlen` is user-space,
while `read` typically enters the kernel.

## Q3. Program, process, and thread?

- Program: passive executable/code/data.
- Process: executing program with virtual address space, resources, and
  protection identity.
- Thread: schedulable execution flow with registers/stack, sharing its
  process's address space and resources.

Threads communicate cheaply through shared memory but one bad thread can
corrupt the process. Processes isolate faults better but IPC/context changes
can cost more.

## Q4. Process states and PCB?

```text
             dispatch
READY --------------------> RUNNING
  ^                           |   \
  |                           |    \ exit
  | preempt                   |     v
  +---------------------------+  TERMINATED
                              |
                              | wait/I/O
                              v
                           BLOCKED
                              |
                              | event complete
                              +--------> READY
```

PCB stores state, program counter/registers, scheduling data, memory mappings,
open resources, accounting, credentials, and links. Exact fields vary.

## Q5. Context switch?

Save the outgoing execution context and restore the incoming one. It enables
multiplexing but performs no user work and may disturb caches, TLB, branch
predictor, and locality. A mode switch can occur without switching process;
not every system call causes a process context switch.

## Q6. Scheduling criteria?

CPU utilization, throughput, turnaround time, waiting time, response time,
fairness, deadlines, and predictability. These objectives conflict: improving
interactive response may reduce batch throughput.

$$
\text{Turnaround}=Completion-Arrival,
$$

$$
\text{Waiting}=Turnaround-CPU\ burst,
\qquad
\text{Response}=First\ run-Arrival.
$$

## Q7. FCFS, SJF/SRTF, priority, Round Robin?

- FCFS: arrival order, simple, convoy effect.
- SJF: shortest next CPU burst, minimizes average waiting when bursts are
  known; prediction required.
- SRTF: preemptive SJF.
- Priority: highest priority first; low-priority starvation, mitigated by
  aging.
- RR: each ready process gets time quantum; responsive, but tiny quantum
  increases switching and huge quantum approaches FCFS.

Always calculate with arrival times and separate waiting from response.

## Q8. Multilevel feedback queue (MLFQ)?

Multiple priority queues use different quanta. New jobs start high. Jobs that
consume full allotments move down; jobs yielding quickly tend to remain high,
approximating interactive/short-job preference without knowing future burst.
Periodic global boosts prevent starvation and defeat some history errors.

Gaming prevention accounts for total allotment at a level, not merely each
individual burst before voluntary yield.

## Q9. Race condition and critical-section requirements?

A race occurs when outcome depends on unsafe timing of accesses to shared
mutable state. `count++` is read-modify-write and can lose updates.

Critical-section solution aims for mutual exclusion, progress, and bounded
waiting under its model. Disabling interrupts is not a general user-space
multicore solution.

## Q10. Mutex, semaphore, monitor, and condition variable?

- Mutex has ownership and protects a critical section.
- Counting semaphore represents permits/resources; binary semaphore can
  signal but does not necessarily have mutex ownership semantics.
- Monitor combines shared state, methods, implicit mutual exclusion, and
  condition variables.
- Condition variable lets a thread sleep until a predicate may have changed;
  always recheck in a loop because wakeups do not guarantee the predicate.

```c
lock(m);
while (!condition)
    wait(cv, m);   // atomically release m and sleep; reacquire on return
use_resource();
unlock(m);
```

## Q11. Peterson's algorithm?

For two threads under a sequentially consistent shared-memory model:

```c
flag[i] = true;
turn = j;
while (flag[j] && turn == j) { }
/* critical section */
flag[i] = false;
```

It demonstrates mutual exclusion, progress, and bounded waiting conceptually.
Modern compilers/CPUs reorder ordinary memory operations, so real code needs
language atomics/memory ordering; use proper mutexes rather than hand-coding
Peterson.

## Q12. Four necessary deadlock conditions?

1. mutual exclusion;
2. hold and wait;
3. no preemption;
4. circular wait.

All are necessary for classical resource deadlock. Prevention breaks one;
avoidance stays in safe states; detection allows then detects; recovery aborts,
rolls back, or preempts where possible.

## Q13. Safe, unsafe, and deadlocked state?

A safe state has some order in which all processes can complete assuming
declared maximum needs. Unsafe means no guaranteed safe sequence; it is not
necessarily already deadlocked. Deadlocked means a set cannot progress due to
cyclic waits/resources.

Banker's algorithm tentatively grants a request only if:

$$
Need=Max-Allocation
$$

and the resulting state still has a safe completion sequence.

## Q14. Paging versus segmentation?

Paging divides virtual memory into fixed-size pages and physical memory into
frames, avoiding external fragmentation but allowing internal fragmentation.
Segmentation uses variable-size logical regions (code, stack, module) with
base/limit, matching program structure but suffering external fragmentation.

Modern systems commonly use paging, sometimes with segmentation concepts at
the protection/layout level.

## Q15. Address translation and TLB?

For page size `2^p`, low `p` virtual-address bits are page offset; remaining
bits form VPN. Page table maps VPN to physical frame number; offset is
unchanged.

```text
Virtual address = [ VPN | offset ]
                       |
                    TLB hit?
                    /      \
                  yes      no -> page-table walk
                   |                |
                   +------ PFN -----+
Physical address = [ PFN | offset ]
```

A TLB miss means translation is not cached; a page fault means the mapping is
not presently valid/resident or violates access. They are not synonyms.

## Q16. Multilevel page table bit walk?

Example: 32-bit virtual address, 4 KiB pages gives 12-bit offset and 20-bit
VPN. If a two-level scheme uses 10 bits per level:

```text
VA = [ directory 10 | table 10 | offset 12 ]
```

Directory index finds a page-table page; table index finds the PTE; PTE gives
frame and permission/present bits. Multilevel tables allocate lower levels
only for used regions, saving memory for sparse address spaces at the cost of
additional walk accesses (mostly hidden by TLB hits).

## Q17. Page fault handling?

1. hardware traps with fault address/cause;
2. OS validates address and access permission;
3. invalid access terminates/signals process;
4. if valid but absent, choose/free a frame, possibly evict dirty victim;
5. read page from backing store or create zero page;
6. update PTE/TLB state;
7. restart faulting instruction.

Minor/major terminology depends on whether disk I/O is needed.

## Q18. FIFO, optimal, LRU, Clock?

- FIFO evicts oldest loaded page; can show Belady's anomaly.
- Optimal evicts page used farthest in future; benchmark, not implementable.
- LRU evicts least recently used; exact implementation can be expensive.
- Clock/second chance approximates recency with reference bits.

Always trace a reference string with a fixed frame count and count faults.
Do not infer that more frames always reduce FIFO faults.

## Q19. Thrashing and working set?

Thrashing occurs when active working sets exceed available frames, producing
constant page faults and low useful CPU utilization. Working-set/locality
models keep pages used in a recent window; page-fault-frequency control and
admission/load reduction can respond. Adding CPU scheduling pressure alone
can worsen thrashing.

## Q20. Internal versus external fragmentation?

Internal fragmentation wastes space inside allocated fixed-size units.
External fragmentation leaves free memory split into holes so enough total
space exists but not a sufficiently large contiguous region. Paging removes
external fragmentation for physical allocation, not all internal waste or
virtual-layout concerns.

## Q21. File, inode, directory, and file descriptor?

An inode-like structure stores metadata and pointers to file data, not the
filename. A directory maps names to inode/object identifiers. A process file
descriptor indexes its open-file table entry, which carries current offset/
flags and references system file/vnode state.

Hard links are multiple directory names for one inode; symbolic links store a
path. Unlink removes a name; storage is reclaimed when link/reference rules
permit.

## Q22. Journaling and WAL idea in a file system?

Before applying related metadata/data updates in place, record enough intent/
changes in a durable log. After crash, replay committed log transactions and
discard incomplete ones under the journal protocol. Journaling improves
crash consistency but is not a backup and cannot prevent all application-level
corruption.

## Q23. Disk scheduling?

- FCFS: arrival order, fair/simple.
- SSTF: nearest request, good immediate seek, can starve distant tracks.
- SCAN: elevator sweeps both directions.
- C-SCAN: services one direction and wraps for more uniform wait.
- LOOK/C-LOOK: reverse/wrap at last pending request rather than physical end.

On SSDs mechanical seek scheduling matters far less; queueing, parallelism,
wear, controller behavior, and latency remain.

## Q24. `fork`, `exec`, and `wait`?

`fork` creates a child process, commonly using copy-on-write mappings; returns
0 in child and child PID in parent. `exec` replaces the current process image;
it does not create a new process. `wait` collects child termination status.

A terminated but unreaped child is a zombie. An orphan is a live child whose
parent exited and is reparented/adopted according to OS rules.

## Q25. IPC methods?

- Pipes/FIFOs: byte streams, simple producer-consumer.
- Message queues: kernel-managed messages.
- Shared memory: fastest data sharing but explicit synchronization.
- Sockets: local/network endpoints.
- Signals/events: asynchronous notification, small payload.
- RPC: request/response abstraction over communication, with partial-failure
  semantics unlike local calls.

Choose using address-space boundary, data volume, latency, topology,
persistence, security, and failure model.

## Q26. Why have a cache?

Caches exploit temporal and spatial locality to bridge latency/bandwidth gaps.

$$
AMAT=HitTime+MissRate\times MissPenalty.
$$

Caches introduce consistency/coherence, replacement, write-policy, security
side channels, and warm-up issues. A cache improves average behavior only when
the workload has exploitable locality and overhead is controlled.

The OSTEP text organizes OS fundamentals around virtualization, concurrency,
and persistence
([Operating Systems: Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/)).

## OS board drill checklist

- Draw process states and calculate scheduling metrics.
- Trace RR/MLFQ with arrivals and quanta.
- Show a lost update and fix with mutex/condition variable/semaphore.
- Draw resource allocation/wait-for graph and find a deadlock.
- Run Banker's safe-sequence test.
- Split a virtual address and walk a multilevel page table.
- Trace page replacement and distinguish TLB miss/page fault.
- Draw inode/directory/open-file relationships.
- Explain `fork -> exec -> wait` and one IPC choice.

---

# 11. Cross-Course Rapid Follow-Ups

These are the follow-ups interviewers use to check whether an answer was
memorized.

## 11.1 For every algorithm

1. What invariant is true before and after each iteration?
2. Why does it terminate?
3. Why is the returned result correct?
4. What is the tight complexity and input-size parameter?
5. What changes for sparse/dense, sorted/unsorted, negative/nonnegative input?
6. What is the smallest counterexample to a tempting wrong approach?
7. Can you write implementable code without hiding the central step?

## 11.2 For every data/system design

1. Which threat/failure/workload model are you assuming?
2. What state is stored and who owns it?
3. What happens concurrently?
4. What happens after partial failure/retry?
5. What is the security boundary?
6. What do you monitor, and how do you recover?
7. Which trade-off would make you choose the alternative?

## 11.3 For every equation

1. Define every symbol and its units/domain.
2. State assumptions before using it.
3. Derive or justify the important step.
4. Calculate a tiny numeric example.
5. Interpret the result in words.
6. State the failure case or what the equation does not prove.

## 11.4 Final high-probability mixed questions

1. Why is BUILD-HEAP linear?
2. Show BST predecessor/successor and an RBT rotation.
3. Prove Edmonds-Karp `O(VE^2)`.
4. Bias/variance equation: why are they not under/overfitting?
5. State pigeonhole and give a concrete hash/remainder application.
6. Explain equality, exceptions, generics, collections, and sorting.
7. TCP versus UDP; what do SYN/ACK mean?
8. Flow control versus congestion control.
9. DHCP DORA; IPv4 versus IPv6.
10. What does TLS provide and not provide?
11. File confidentiality and selective database encryption.
12. Normalize a schema and test serializability.
13. Explain MVCC, B+ tree, and WAL.
14. A* optimality assumptions and `h=0`.
15. Infinite-depth minimax question.
16. MLFQ scheduling and starvation prevention.
17. TLB miss versus page fault.
18. Deadlock conditions, safe state, and Banker's algorithm.
19. Early versus late binding and polymorphism.
20. Verification versus validation; Agile/Kanban/Scrum.

## 11.5 Honest final audit statement

The ten detailed course books are now the concept/slide recall layer; this file
is the oral question-and-answer layer. No finite document can literally contain
every question an interviewer may invent. The preparation target is stronger:
cover every major source topic, teach the mechanism, and prepare the invariant,
equation, trace, code, complexity, trade-off, and failure case that generate
most follow-ups.

