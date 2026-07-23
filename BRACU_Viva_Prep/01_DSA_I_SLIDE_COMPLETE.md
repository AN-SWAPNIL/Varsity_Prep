# Bismillah.

# Data Structures and Algorithms I -- Slide-Complete Viva Recall Book

> **Purpose.** This is a recall book, not a list of one-line interview answers. Read a definition, redraw the picture or trace, then explain the invariant and complexity aloud. Code is written in clear C++17-style pseudocode; the ideas are language-independent.
>
> **Current source boundary (re-audited 24 July 2026).** The reduced `203-DSA1` folder now contains four sources totaling **523 pages**: `Algorithms.pdf` (219), `Dsa bayezid sir.pdf` (22 image-only handwritten pages), `DSA Merged Part1.pdf` (254), and `DSA_note_by_Promi.pdf` (28). The current main sources still support the complete elementary-data-structure, graph-traversal, divide-and-conquer, greedy, and dynamic-programming spine of this volume. Old references to removed individual PowerPoint decks and auxiliary PDFs have been deleted. AVL/red-black repair, MST, shortest paths, flow, hashing, and complexity classes remain in DSA II.

## How to use this book in the final days

For each major algorithm, be able to say five things without looking:

1. **Contract:** input, output, and assumptions.
2. **Representation/state:** what is stored and what each variable means.
3. **Invariant or recurrence:** why the method is correct.
4. **Trace:** one small example on the board.
5. **Cost:** derive it; do not merely recite a Big-O symbol.

The labels used below are:

- **Board answer:** a compact explanation suitable for a viva.
- **Invariant/proof:** the statement that remains true and proves correctness.
- **Trap:** a tempting but false or incomplete answer.
- **Source correction:** a point where the locally stored slide/note is ambiguous or wrong.

## Contents

1. Algorithms, ADTs, correctness, and analysis
2. Recursion, iteration, and recurrence solving
3. List ADT, arrays, linked lists, and free lists
4. Stacks and their applications
5. Queues, circular queues, deques, and priority queues
6. Binary trees and traversals
7. Binary search trees
8. Binary heaps, priority queues, build-heap, and heapsort
9. Graph language and representations
10. BFS, DFS, bipartite testing, cycles, and topological ordering
11. Searching and sorting
12. Divide and conquer
13. Greedy algorithms
14. Dynamic programming
15. Board-ready comparisons, traps, and drills
16. Source coverage matrix and correction ledger

---

# 1. Algorithms, ADTs, correctness, and analysis

## 1.1 Problem, algorithm, program, data structure, and ADT

- A **problem** specifies a required input-output relationship, for example: given an array and a key, return an index containing the key or report absence.
- An **algorithm** is a finite, unambiguous, effective sequence of steps that solves every valid instance of a problem.
- A **program** is an implementation of one or more algorithms in a programming language, together with representation choices, input handling, and system details.
- A **data structure** is a way to organize data and its relationships so selected operations can be performed efficiently.
- An **abstract data type (ADT)** specifies observable values and operations, not their storage. A stack ADT promises `push`, `pop`, and `top`; it may be implemented by an array or a linked list.

**Logical versus physical form.** A list is logically an ordered sequence. Physically it may occupy consecutive array cells or scattered linked nodes. Clients should depend on the logical contract, not representation details.

**Board answer -- why study DSA?** The same data can be represented in several ways, and no representation is best for every workload. Arrays provide constant-time indexing but costly middle insertion; linked lists give constant-time insertion once the predecessor is known but no constant-time random access. DSA is the study of choosing and proving the right trade-off.

### Choosing a structure

Ask:

1. What operations dominate: access, search, insert, delete, minimum, FIFO, graph-neighbor iteration?
2. What must be guaranteed: order, uniqueness, stability, worst-case latency?
3. Is the input static or dynamic? How large can it grow?
4. What memory overhead and locality are acceptable?
5. Is average/expected performance enough, or is a worst-case bound required?

An ADT hides **how**; an algorithm chooses **steps**; a data structure supplies an efficient **representation**.

## 1.2 Correctness

An algorithm is correct when it terminates and returns the specified output for every valid input.

- **Partial correctness:** if it terminates, its result is correct.
- **Termination:** a well-founded measure decreases and cannot decrease forever.
- **Total correctness:** partial correctness plus termination.

### Loop-invariant proof template

For a loop, state a property (P) and prove:

1. **Initialization:** (P) holds before the first iteration.
2. **Maintenance:** if (P) holds before an iteration, the body makes it hold before the next.
3. **Termination:** when the loop ends, (P) plus the exit condition implies the desired result.

Example for insertion sort: before iteration `i`, `a[0..i-1]` is a sorted permutation of its original elements. Inserting `a[i]` preserves that property. At `i=n`, the whole array is sorted.

### Recursive proof template

Prove a base case, assume recursive calls correctly solve smaller instances, then show the combine step solves the current instance. Also identify a size measure that strictly decreases.

## 1.3 Why asymptotic analysis instead of seconds?

Experimental timing depends on processor, compiler, language, cache, system load, implementation skill, and chosen test data. It is useful after implementation but cannot cleanly compare algorithms on all input sizes. Asymptotic analysis counts a **basic operation** as a function of input size and studies growth as input becomes large.

Let (T(n)) be the number of elementary steps for input size (n). Constants and lower-order terms matter in engineering, but growth rate predicts scaling.

### Cases and styles of analysis

- **Worst case:** maximum cost over all inputs of size (n); gives a guarantee.
- **Best case:** minimum cost; often not representative.
- **Average case:** expectation under an explicitly stated input distribution.
- **Expected/probabilistic:** expectation over random choices made by the algorithm and/or a stated input model.
- **Amortized:** average cost per operation over every possible sequence, without assuming a probability distribution.

**Trap:** amortized does not mean average-case. Dynamic-array append is amortized $O(1)$ even for an adversarial operation sequence, while a single resize still costs $\Theta(n)$.

## 1.4 Formal asymptotic notation

For eventually nonnegative functions:

- $f(n) \in O(g(n))$ if there exist $c>0,n_0$ such that $0\le f(n)\le c g(n)$ for all $n\ge n_0$. This is an asymptotic upper bound.
- $f(n) \in \Omega(g(n))$ if there exist $c>0,n_0$ such that $0\le c g(n)\le f(n)$ for all $n\ge n_0$. This is a lower bound.
- $f(n) \in \Theta(g(n))$ iff it is in both $O(g(n))$ and $\Omega(g(n))$; a tight bound.

Example: $3n^2+5n+7\in\Theta(n^2)$. For $n\ge1$, it is at least $3n^2$, and for sufficiently large $n$, it is at most $15n^2$.

**Language trap:** "the complexity is at least $O(n)$" mixes directions. Say "upper-bounded by $O(n)$" or "lower-bounded by $\Omega(n)$." Big-O itself is not "the exact worst case"; it is a set of upper bounds.

### Common growth order

$$
1 < \log n < \sqrt n < n < n\log n < n^2 < n^3 < 2^n < n!
$$

Changing the logarithm base only multiplies by a constant: $\log_a n=\log_b n/\log_b a$, so all fixed bases are $\Theta(\log n)$.

### Counting patterns

```cpp
// Theta(n): exactly n iterations
for (int i = 0; i < n; ++i) work();

// Theta(n^2): sum_{i=0}^{n-1} i = n(n-1)/2
for (int i = 0; i < n; ++i)
    for (int j = 0; j < i; ++j) work();

// Theta(log n): i takes 1,2,4,...
for (int i = 1; i < n; i *= 2) work();

// Theta(n log n): n choices of i, log n choices of j
for (int i = 0; i < n; ++i)
    for (int j = 1; j < n; j *= 2) work();
```

Nested loops are **not automatically** $O(n^2)$; count the actual ranges. Consecutive blocks add, nested independent blocks multiply, and dependent ranges often form a sum.

### Input parameters matter

Graph time is naturally expressed using both (|V|) and (|E|). Matrix multiplication may use dimensions (m,n,p). Do not silently compress independent parameters into one (n).

## 1.5 Tractability and examples from the analysis notes

Polynomial-time problems are normally called **tractable** in this course context; exponential and factorial algorithms quickly become impractical. This is a growth-rate convention, not a claim that every high-degree polynomial is practical.

- Finding the maximum of (n) values needs (n-1) comparisons: $\Theta(n)$.
- Binary search repeatedly halves the candidate range: $\Theta(\log n)$.
- Merging two sorted arrays of total length (n) is $\Theta(n)$.
- Brute-force closest pair checks $\binom{n}{2}$ pairs: $\Theta(n^2)$.
- Enumerating every subset takes $\Theta(2^n)$ subsets before the work inside each subset.

### Time-space trade-off

Extra memory can avoid repeated work: memoized Fibonacci stores answers to obtain $O(n)$ time; a lookup table can accelerate queries; a hash table spends capacity for expected constant-time lookup. Conversely, recomputation may reduce storage.

---

# 2. Recursion, iteration, and recurrences

## 2.1 Recursion mental model

A recursive function calls itself on a smaller instance. Every call creates an **activation record** containing parameters, local variables, return address, and bookkeeping. These frames form the runtime call stack.

A valid recursive solution needs:

1. one or more base cases;
2. progress toward a base case;
3. a correct combination of subproblem answers.

```cpp
long long sumTo(long long n) {
    if (n <= 0) return 0;       // base case
    return n + sumTo(n - 1);    // smaller instance
}
```

Trace for `sumTo(4)`:

```text
sumTo(4)
= 4 + sumTo(3)
= 4 + 3 + sumTo(2)
= 4 + 3 + 2 + sumTo(1)
= 4 + 3 + 2 + 1 + sumTo(0)
= 10
```

Recurrence: (T(n)=T(n-1)+\Theta(1)=\Theta(n)). Stack depth and auxiliary space are $\Theta(n)$.

### Iterative version

```cpp
long long sumToIter(long long n) {
    long long ans = 0;
    for (long long x = 1; x <= n; ++x) ans += x;
    return ans;
}
```

It has $\Theta(n)$ time and $\Theta(1)$ auxiliary space. The formula (n(n+1)/2) is $\Theta(1)$ under a fixed-width arithmetic model, though arbitrary-precision bit complexity is different.

## 2.2 Recursion versus iteration

Neither is universally "better."

| Criterion | Recursion | Iteration |
|---|---|---|
| Natural fit | Trees, DFS, divide-and-conquer, backtracking | Sequential repetition, simple state machines |
| Extra state | Implicit call stack | Explicit variables/structure |
| Space | Usually proportional to depth | Often $O(1)$, unless an explicit stack is needed |
| Overhead | Function calls and possible stack overflow | Usually lower call overhead |
| Clarity | Can mirror recursive definitions | Can make control and limits explicit |

Every recursion can be simulated with an explicit stack because that stack stores the same frames. Tail-recursive calls can sometimes be optimized into jumps, but C++ and Java do not guarantee tail-call optimization.

**Board answer:** compare implementations, not slogans. For factorial, iteration is simpler and constant-space. For tree traversal, recursion directly follows the structure; an iterative version needs an explicit stack and remains $O(h)$ space.

## 2.3 Explicitly simulating recursion

Factorial can push the pending multipliers, then pop them:

```cpp
long long factorialWithStack(int n) {
    stack<int> pending;
    while (n > 1) pending.push(n--);
    long long ans = 1;
    while (!pending.empty()) {
        ans *= pending.top();
        pending.pop();
    }
    return ans;
}
```

For a general recursive algorithm, a frame may need fields such as parameters, local variables, and a "program counter" saying which recursive call should execute next.

## 2.4 Towers of Hanoi

To move (n) disks from source `A` to target `C` using auxiliary `B`:

1. move (n-1) from `A` to `B` using `C`;
2. move the largest disk from `A` to `C`;
3. move (n-1) from `B` to `C` using `A`.

```cpp
void hanoi(int n, char from, char aux, char to) {
    if (n == 0) return;
    hanoi(n - 1, from, to, aux);
    cout << from << " -> " << to << '\n';
    hanoi(n - 1, aux, from, to);
}
```

The recurrence is (T(n)=2T(n-1)+1), so (T(n)=2^n-1) moves and $\Theta(n)$ recursion depth. The lower bound follows because the largest disk can move only after all (n-1) smaller disks leave it, and they must then be rebuilt.

## 2.5 Solving recurrences

### Expansion/iteration

For merge sort:

$$
T(n)=2T(n/2)+cn.
$$

At recursion level (i), there are (2^i) subproblems of size (n/2^i), so the nonrecursive work is (2^i c(n/2^i)=cn). There are (log_2 n) levels, hence $\Theta(n\log n)$.

For (T(n)=T(n-1)+cn):

$$
T(n)=c(n+(n-1)+\cdots+1)+T(0)=\Theta(n^2).
$$

### Master theorem

For

$$
T(n)=aT(n/b)+f(n),\quad a\ge1,b>1,
$$

compare (f(n)) with (n^{\log_b a}):

1. If (f(n)=O(n^{\log_ba-\epsilon})), then (T(n)=\Theta(n^{\log_ba})).
2. If (f(n)=\Theta(n^{\log_ba}\log^k n)), then (T(n)=\Theta(n^{\log_ba}\log^{k+1}n)) for (k\ge0).
3. If (f(n)=\Omega(n^{\log_ba+\epsilon})) and the regularity condition (af(n/b)\le cf(n)) for some (c<1) holds, then (T(n)=\Theta(f(n))).

Examples:

- (2T(n/2)+n=\Theta(n\log n)).
- (T(n/2)+1=\Theta(\log n)).
- (4T(n/2)+n=\Theta(n^2)).
- (2T(n/2)+n^2=\Theta(n^2)).
- (3T(n/2)+n=\Theta(n^{\log_2 3})\approx\Theta(n^{1.585})).

**Trap:** the standard Master theorem does not directly solve (T(n)=T(n-1)+n), unequal subproblem sizes such as (T(n/3)+T(2n/3)+n), or every recurrence containing a logarithm.

### Generalized logarithmic form from the notes

For $T(n)=aT(n/b)+\Theta(n^c\log^p n)$, let $d=\log_ba$:

- if $d>c$, recursion leaves dominate: $T(n)=\Theta(n^d)$;
- if $d<c$ (with the usual regularity condition), combine work dominates: $T(n)=\Theta(n^c\log^p n)$;
- if $d=c$ and $p>-1$, $T(n)=\Theta(n^c\log^{p+1}n)$;
- if $d=c$ and $p=-1$, $T(n)=\Theta(n^c\log\log n)$;
- if $d=c$ and $p<-1$, $T(n)=\Theta(n^c)$.

This extension explains borderline logarithmic cases that the three-case classroom version does not state. Always verify that the recurrence actually has equal-sized subproblems before using it.

---

# 3. List ADT, arrays, linked lists, and free lists

## 3.1 List ADT and the current-position model

A list is a finite ordered sequence

$$
\langle a_0,a_1,\ldots,a_{n-1}\rangle.
$$

Position matters, and an empty list has length zero. The lecture ADT maintains one of (n+1) **current positions**--including the gaps before the first and after the last item. Core operations are:

```text
clear, insert, append, remove,
moveToStart, moveToEnd, prev, next,
length, currPos, moveToPos, getValue
```

Notation such as `<20, 23 | 12, 15>` places the cursor immediately before `12`; `insert(99)` produces `<20, 23 | 99, 12, 15>`.

Traversal under this contract:

```cpp
for (L.moveToStart(); L.currPos() < L.length(); L.next()) {
    auto item = L.getValue();
    use(item);
}
```

## 3.2 Array-based list

Representation:

```cpp
template<class E>
struct AList {
    vector<E> a;        // or fixed E a[maxSize]
    int listSize = 0;
    int curr = 0;       // gap/index of current element
};
```

Slide-aligned fixed-capacity operations:

```cpp
void insert(const E& x) {              // before a[curr]
    if (listSize == maxSize) throw overflow_error("full");
    for (int i = listSize; i > curr; --i)
        a[i] = a[i - 1];
    a[curr] = x;
    ++listSize;
}

void append(const E& x) {
    if (listSize == maxSize) throw overflow_error("full");
    a[listSize++] = x;
}

E remove() {
    if (curr < 0 || curr >= listSize) throw out_of_range("no current item");
    E removed = a[curr];
    for (int i = curr; i + 1 < listSize; ++i)
        a[i] = a[i + 1];
    --listSize;
    if (curr > listSize) curr = listSize;
    return removed;
}
```

Costs for length (n): random access $\Theta(1)$; append $\Theta(1)$ if capacity exists; insertion/removal at position (k), $\Theta(n-k)$ shifts; linear search $\Theta(n)$. A dynamic array occasionally reallocates and copies, so append is $O(1)$ amortized, not worst-case.

**Invariant for insertion:** before copying index `i-1` to `i`, cells `i..listSize` already contain the original elements from `i-1..listSize-1`. Backward copying prevents overwriting unread data.

## 3.3 Singly linked list

Each node stores an element and the address of the next node; physical memory need not be contiguous.

```cpp
template<class E>
struct Node {
    E value;
    Node* next;
    Node(const E& v, Node* n = nullptr) : value(v), next(n) {}
};
```

### Basic operations and edge cases

```cpp
void pushFront(Node*& head, int x) {
    head = new Node<int>(x, head);
}

void pushBack(Node*& head, Node*& tail, int x) {
    Node* p = new Node<int>(x);
    if (!head) head = tail = p;
    else { tail->next = p; tail = p; }
}

bool insertAfter(Node* p, int x) {
    if (!p) return false;
    p->next = new Node<int>(x, p->next);
    return true;
}

bool popFront(Node*& head, Node*& tail, int& out) {
    if (!head) return false;
    Node* dead = head;
    out = dead->value;
    head = head->next;
    if (!head) tail = nullptr;
    delete dead;
    return true;
}

bool eraseValue(Node*& head, Node*& tail, int x) {
    Node* prev = nullptr;
    Node* cur = head;
    while (cur && cur->value != x) {
        prev = cur;
        cur = cur->next;
    }
    if (!cur) return false;
    if (prev) prev->next = cur->next;
    else head = cur->next;
    if (tail == cur) tail = prev;
    delete cur;
    return true;
}
```

Search and access to position (k) are $O(n)$. Insertion/deletion is $O(1)$ **only when the necessary node/predecessor pointer is already known**. Finding that position may take $O(n)$. With a tail pointer, append is $O(1)$; without it, append requires traversal.

### Why the lecture cursor points before the current item

If `curr` points to the predecessor of the logical current item, inserting and removing at the current position only rewires `curr->next`. A dummy header makes "before the first item" an ordinary node and avoids special cases.

```cpp
// header carries no list element; tail == header in an empty list
void insertCurrent(const E& x) {
    curr->next = new Node<E>(x, curr->next);
    if (tail == curr) tail = curr->next;
    ++cnt;
}

E removeCurrent() {
    if (!curr->next) throw out_of_range("no current item");
    Node<E>* dead = curr->next;
    E x = dead->value;
    curr->next = dead->next;
    if (tail == dead) tail = curr;
    delete dead;
    --cnt;
    return x;
}
```

Representation invariant:

- `head` is a permanent dummy node;
- the data sequence starts at `head->next`;
- `tail` is the last node, or `head` if empty;
- `curr` is a reachable node immediately before the logical current element;
- exactly `cnt` data nodes are reachable.

### Worked pointer trace

For `head -> 4 -> 7 -> 9 -> null`, delete `7`:

1. `prev` points to `4`, `cur` points to `7`.
2. Save `cur` before changing links.
3. Set `prev->next = cur->next`, so `4` points to `9`.
4. Delete `cur`. Never dereference it afterward.

**Traps:** losing the rest of the list by overwriting `next` before saving it; forgetting the empty/singleton case; leaving `tail` dangling; using a freed node; claiming $O(1)$ deletion when only a value--not its predecessor--is given.

## 3.4 Free list / memory pool

The second list deck overloads unused nodes to form a **free list**. Allocation removes a node from the free-list head; deallocation returns it there. This can reduce repeated allocator overhead and fragmentation when nodes have one fixed size.

```cpp
Node* freeHead = nullptr;

Node* acquire(int x) {
    if (!freeHead) return new Node<int>(x);
    Node* p = freeHead;
    freeHead = freeHead->next;
    p->value = x;
    p->next = nullptr;
    return p;
}

void release(Node* p) {
    p->next = freeHead;
    freeHead = p;
}
```

The `next` field is interpreted as a data-list link while allocated and a free-list link while free. Never keep a node simultaneously in both lists.

## 3.5 Doubly linked list

```cpp
template<class E>
struct DNode {
    E value;
    DNode *prev, *next;
};

void insertAfter(DNode* p, DNode* x) {
    x->prev = p;
    x->next = p->next;
    p->next->prev = x;
    p->next = x;
}

void erase(DNode* x) {
    x->prev->next = x->next;
    x->next->prev = x->prev;
    delete x;
}
```

With head and tail sentinels, these functions need no endpoint branches. DLLs support backward traversal and $O(1)$ deletion given the node itself, but spend another pointer per node and perform more link updates.

## 3.6 Array versus linked representation

| Question | Array list | Linked list |
|---|---|---|
| Index access | $\Theta(1)$ | $\Theta(n)$ |
| Insert/delete at known index | shifts, $\Theta(n)$ worst case | must locate predecessor, then $\Theta(1)$ rewiring |
| Append | $\Theta(1)$ with spare capacity; amortized for dynamic array | $\Theta(1)$ with tail |
| Memory | reserved capacity may be unused | pointer overhead per node |
| Locality | excellent | usually poor |
| Growth | reallocate/copy or fixed limit | node-by-node |

The slide space comparison uses element size $E$, pointer size $P$, array capacity $D$, and current list length $n$: array storage is about $DE$; singly linked storage is about $n(E+P)$. The linked form uses less space when $n(E+P)<DE$. This is only a storage model; allocator metadata and alignment can change real values.

---

# 4. Stacks and their applications

## 4.1 Stack ADT and representations

A stack is **last in, first out (LIFO)**. Only the top is accessible.

```text
push(x): add x at top
pop(): remove and return top
top()/peek(): return top without removing
empty(), size(), clear()
```

Calling `pop` or `top` on an empty stack is an underflow error; pushing into a fixed full array is overflow.

### Array stack

Let `top` mean the first free index, so the current top element is `a[top-1]`.

```cpp
template<class E>
class ArrayStack {
    vector<E> a;
    int topIndex = 0;
public:
    explicit ArrayStack(int cap) : a(cap) {}

    bool empty() const { return topIndex == 0; }
    int size() const { return topIndex; }

    void push(const E& x) {
        if (topIndex == (int)a.size()) throw overflow_error("stack full");
        a[topIndex++] = x;
    }

    E pop() {
        if (empty()) throw underflow_error("empty stack");
        return a[--topIndex];
    }

    const E& top() const {
        if (empty()) throw underflow_error("empty stack");
        return a[topIndex - 1];
    }
};
```

Put the top at the array tail: push and pop then take $\Theta(1)$. Putting it at index zero shifts all elements and costs $\Theta(n)$.

### Linked stack

The head is the top, so no dummy header is necessary.

```cpp
template<class E>
class LinkedStack {
    Node<E>* head = nullptr;
    int cnt = 0;
public:
    void push(const E& x) { head = new Node<E>(x, head); ++cnt; }
    E pop() {
        if (!head) throw underflow_error("empty stack");
        Node<E>* dead = head;
        E x = dead->value;
        head = head->next;
        delete dead;
        --cnt;
        return x;
    }
    const E& top() const {
        if (!head) throw underflow_error("empty stack");
        return head->value;
    }
};
```

Both implementations have $\Theta(1)$ core operations. The array has locality and no link per element but may waste unused capacity; the linked form grows one node at a time but pays pointer and allocator overhead.

## 4.2 Two stacks in one array

Let stack 1 grow rightward from index `0`; stack 2 grow leftward from `n-1`. The free region lies between `top1` and `top2`.

```cpp
int top1 = -1, top2 = n;

void push1(int x) {
    if (top1 + 1 == top2) throw overflow_error("shared array full");
    a[++top1] = x;
}
void push2(int x) {
    if (top1 + 1 == top2) throw overflow_error("shared array full");
    a[--top2] = x;
}
```

This shares unused space and is especially useful when one stack grows as the other shrinks. It does not create more total capacity; simultaneous growth still exhausts the middle.

## 4.3 Dynamic resizing and amortized analysis

When a full array of capacity (m) grows:

- Increasing capacity by `1` (or any fixed constant) makes (n) pushes cost (1+2+\cdots+n=\Theta(n^2)), hence $\Theta(n)$ amortized.
- Multiplying capacity by a constant (r>1) copies (1+r+r^2+\cdots<n r/(r-1)=O(n)) elements across (n) pushes. Total time is $O(n)$, so append/push is $O(1)$ amortized.

For doubling, charge each push a small constant: one unit pays for its own write and saved credits pay for future copies. A single resize remains $O(n)$, while the sequence average is constant. The cost is some unused capacity, always below a constant fraction after geometric growth.

For a circular array, resizing must copy elements in **logical queue order**, because the old live segment may wrap around. After copying, set `front=0` and `rear=count` under the first-free convention.

## 4.4 Postfix / Reverse Polish notation

For each token:

- operand: push it;
- binary operator: pop **right operand**, then pop **left operand**, compute `left op right`, and push the result.

```cpp
double evalPostfix(const vector<string>& tokens) {
    stack<double> st;
    for (const string& t : tokens) {
        if (isNumber(t)) st.push(stod(t));
        else {
            if (st.size() < 2) throw invalid_argument("malformed expression");
            double right = st.top(); st.pop();
            double left  = st.top(); st.pop();
            st.push(apply(t[0], left, right));
        }
    }
    if (st.size() != 1) throw invalid_argument("malformed expression");
    return st.top();
}
```

Trace `5 6 2 + *`:

```text
5 -> [5]
6 -> [5,6]
2 -> [5,6,2]
+ -> pop 2,6; push 8 -> [5,8]
* -> pop 8,5; push 40 -> [40]
```

**Trap:** for subtraction/division, pop order matters: `8 2 /` is `8/2`, not `2/8`.

## 4.5 Delimiter/tag matching

Push opening symbols; on a closing symbol, require a nonempty stack and a matching opening symbol at the top. At the end the stack must be empty.

```cpp
bool balanced(const string& s) {
    stack<char> st;
    for (char c : s) {
        if (c=='(' || c=='[' || c=='{') st.push(c);
        else if (c==')' || c==']' || c=='}') {
            if (st.empty()) return false;
            char o = st.top(); st.pop();
            if ((c==')' && o!='(') || (c==']' && o!='[') ||
                (c=='}' && o!='{')) return false;
        }
    }
    return st.empty();
}
```

HTML/XML tags use the same idea, but the stack stores tag names and self-closing tags require special handling.

## 4.6 Stock-span problem and monotonic stack

For day (i), the span is the number of consecutive days ending at (i) whose price is at most `price[i]`.

A naive backward scan is $O(n^2)$. Keep indices in a stack whose prices are strictly greater after smaller/equal prices are popped:

```cpp
vector<int> stockSpan(const vector<int>& p) {
    vector<int> span(p.size());
    stack<int> st;                       // decreasing prices by index
    for (int i = 0; i < (int)p.size(); ++i) {
        while (!st.empty() && p[st.top()] <= p[i]) st.pop();
        span[i] = st.empty() ? i + 1 : i - st.top();
        st.push(i);
    }
    return span;
}
```

Trace prices `[100,80,60,70,60,75,85]` gives spans `[1,1,1,2,1,4,6]`.

**Why $O(n)$?** Every index is pushed once and popped at most once, so all inner-loop iterations across the entire algorithm are $O(n)$. This is aggregate amortized analysis.

**Source correction:** a slide rendering makes the last expression look like `i-j`; the implementable formula is `i - st.top()`.

## 4.7 Reversing order with a stack

A stack reverses a sequence. For example, to find the (k)-th item before a marker `G` in a one-way stream, push items until `G`; then pop (k) times if enough items exist. State clearly whether "first before" means the immediate predecessor and whether (k) is 1-based.

---

# 5. Queues, circular queues, deques, and priority queues

## 5.1 Queue ADT

A queue is **first in, first out (FIFO)**.

```text
enqueue(x): add at rear
dequeue(): remove and return front
front(): inspect front
empty(), size(), clear()
```

Real motivations include printer jobs, network packets awaiting service, BFS frontiers, and tasks waiting for a CPU. Queue order models arrival order, not importance.

## 5.2 Why a naive array queue fails

If every dequeue shifts all remaining elements left, dequeue costs $\Theta(n)$. If `front` simply drifts right and freed cells are never reused, the queue reports overflow despite free cells at the beginning. A circular array reuses them.

## 5.3 Circular queue: one-slot-empty design

Allocate `capacity + 1` cells. Let `front` index the first element and `rear` index the next free cell.

```cpp
template<class E>
class CircularQueue {
    vector<E> a;                   // requested capacity + 1
    int frontIndex = 0;
    int rearIndex = 0;
public:
    explicit CircularQueue(int capacity) : a(capacity + 1) {}

    bool empty() const { return frontIndex == rearIndex; }
    bool full() const { return (rearIndex + 1) % a.size() == frontIndex; }
    int size() const {
        return (rearIndex - frontIndex + a.size()) % a.size();
    }
    void enqueue(const E& x) {
        if (full()) throw overflow_error("queue full");
        a[rearIndex] = x;
        rearIndex = (rearIndex + 1) % a.size();
    }
    E dequeue() {
        if (empty()) throw underflow_error("queue empty");
        E x = a[frontIndex];
        frontIndex = (frontIndex + 1) % a.size();
        return x;
    }
    const E& front() const {
        if (empty()) throw underflow_error("queue empty");
        return a[frontIndex];
    }
};
```

Example with physical size `5`: enqueue at indices `3,4,0`; logical order crosses the array boundary. Modulo arithmetic maps the logical next position back to zero.

### Why sacrifice one slot? A pigeonhole argument

With an array of (n) cells and only `front` and `rear`, there are (n+1) possible queue sizes (0,1,\ldots,n). If `front` is fixed, `rear` has only (n) possible positions. By the pigeonhole principle, at least two sizes must share the same `(front,rear)` state--specifically, the ordinary modulo representation makes empty and full both look like `front==rear`. Therefore the representation needs extra information:

- reserve one cell, so maximum data size is (n-1);
- store a `count` from `0..n`;
- or keep a separate `full` flag.

This is also a concrete DSA use of the pigeonhole principle: it proves a representation with too few states cannot distinguish all abstract queue states.

## 5.4 Circular queue with a count

All array cells can be used if `count` disambiguates full and empty:

```cpp
int frontIndex = 0, rearIndex = 0, count = 0;

void enqueue(int x) {
    if (count == capacity) throw overflow_error("full");
    a[rearIndex] = x;
    rearIndex = (rearIndex + 1) % capacity;
    ++count;
}

int dequeue() {
    if (count == 0) throw underflow_error("empty");
    int x = a[frontIndex];
    frontIndex = (frontIndex + 1) % capacity;
    --count;
    return x;
}
```

Choose one convention and derive all conditions from it. Many circular-queue bugs come from mixing "rear points to last item" with "rear points to first free cell."

## 5.5 Linked queue with a sentinel

```cpp
template<class E>
class LinkedQueue {
    Node<E>* frontSentinel;
    Node<E>* rear;
    int cnt = 0;
public:
    LinkedQueue() {
        frontSentinel = rear = new Node<E>(E{});
    }

    void enqueue(const E& x) {
        rear->next = new Node<E>(x);
        rear = rear->next;
        ++cnt;
    }

    E dequeue() {
        if (cnt == 0) throw underflow_error("empty queue");
        Node<E>* first = frontSentinel->next;
        E x = first->value;
        frontSentinel->next = first->next;
        if (rear == first) rear = frontSentinel;
        delete first;
        --cnt;
        return x;
    }
};
```

Both operations are $\Theta(1)$. The empty invariant is `frontSentinel == rear` and `frontSentinel->next == nullptr`.

**Source correction:** one queue slide's `clear` code is internally inconsistent. The invariant above is the reliable specification: delete every data node, retain or recreate exactly one sentinel, and set `rear` to it.

## 5.6 Deque

A double-ended queue supports insertion and deletion at both front and rear:

```text
push_front, push_back, pop_front, pop_back, front, back
```

A circular array or doubly linked list implements all four updates in $\Theta(1)$. Deques support sliding-window algorithms and 0-1 BFS; they are not priority queues because selection still depends on an end, not a key.

## 5.7 Priority queue ADT

A max-priority queue selects by key, not arrival time:

```text
insert(x), maximum(), extractMax(), increaseKey(handle,newKey)
```

| Representation | `maximum` | `insert` | `extractMax` |
|---|---:|---:|---:|
| Unsorted array/list | $O(n)$ | $O(1)$ | $O(n)$ |
| Sorted array/list | $O(1)$ | $O(n)$ | $O(1)$ at the correct end |
| Binary max-heap | $O(1)$ | $O(\log n)$ | $O(\log n)$ |

This motivates heaps: they balance update and selection costs without fully sorting all items.

---

# 6. Binary trees and traversals

## 6.1 Definitions and vocabulary

A binary tree is either empty or consists of a root and two disjoint binary trees called its left and right subtrees. This recursive definition explains why recursive algorithms fit naturally.

- **Node, edge, root, parent, child, sibling.**
- **Leaf/external node:** no children. **Internal node:** at least one child.
- **Ancestor/descendant:** nodes along an upward/downward path.
- **Depth of a node:** number of edges from root to it; root depth is 0.
- **Height of a node:** longest downward edge path to a leaf. Under the edge convention, a leaf has height 0 and an empty tree has height (-1).
- **Height of tree:** height of its root / maximum depth.
- **Subtree:** a node with all descendants.

State the height convention because some texts count nodes rather than edges.

### Full, perfect, complete, and balanced

- **Full/proper/strict:** every internal node has exactly two children.
- **Perfect:** all internal nodes have two children and all leaves have one depth.
- **Complete:** every level is full except possibly the last, which is filled left to right.
- **Balanced:** height is $O(\log n)$, or a more specific local balance rule in a named balanced-tree family.

These terms are not interchangeable. A heap is complete but need not be perfect; a full tree need not be complete.

## 6.2 Counting facts and proofs

### Full binary tree: leaves = internal nodes + 1

Let (I) be internal nodes and (L) leaves. Each internal node contributes exactly two child edges, so a nonempty full tree has (2I) edges. Any tree with (I+L) nodes has (I+L-1) edges. Thus

$$
2I=I+L-1 \implies L=I+1.
$$

This can also be proved by structural induction.

### Null pointers in a binary linked tree

With (n) nodes there are (2n) child-pointer fields. A tree has (n-1) real edges, hence

$$
2n-(n-1)=n+1
$$

null child pointers.

### Perfect tree counts

At depth (d) there are (2^d) nodes. A perfect tree of height (h) has

$$
1+2+\cdots+2^h=2^{h+1}-1
$$

nodes and (2^h) leaves.

## 6.3 Linked and array representations

```cpp
template<class E>
struct BNode {
    E value;
    BNode *left = nullptr, *right = nullptr;
};
```

Linked representation fits arbitrary shapes but stores two pointers per node, many of which are null. A complete tree is compact in an array. Under 1-based indexing:

```text
parent(i) = floor(i/2)
left(i)   = 2i
right(i)  = 2i+1
```

Under 0-based indexing:

```text
parent(i) = floor((i-1)/2)
left(i)   = 2i+1
right(i)  = 2i+2
```

Do not mix conventions.

## 6.4 Traversals

```cpp
void preorder(BNode<int>* r) {
    if (!r) return;
    visit(r); preorder(r->left); preorder(r->right);
}

void inorder(BNode<int>* r) {
    if (!r) return;
    inorder(r->left); visit(r); inorder(r->right);
}

void postorder(BNode<int>* r) {
    if (!r) return;
    postorder(r->left); postorder(r->right); visit(r);
}

void levelOrder(BNode<int>* root) {
    if (!root) return;
    queue<BNode<int>*> q;
    q.push(root);
    while (!q.empty()) {
        auto* u = q.front(); q.pop();
        visit(u);
        if (u->left) q.push(u->left);
        if (u->right) q.push(u->right);
    }
}
```

- Preorder: root before subtrees; useful for copying/serialization with null markers.
- Inorder: left, root, right; yields sorted keys for a BST.
- Postorder: children before parent; useful for deleting a tree or computing subtree results.
- Level order: breadth first; uses a queue.

Example:

```text
        A
       / \
      B   C
     / \   \
    D   E   F
```

Preorder `A B D E C F`; inorder `D B E A C F`; postorder `D E B F C A`; level order `A B C D E F`.

Each visits each node exactly once: $\Theta(n)$ time. Recursive auxiliary space is $\Theta(h)$; worst case $\Theta(n)$, balanced case $\Theta(\log n)$. Level order can hold $\Theta(w)$ nodes where (w) is maximum width.

## 6.5 Recursive tree computations

```cpp
int nodeCount(BNode<int>* r) {
    if (!r) return 0;
    return 1 + nodeCount(r->left) + nodeCount(r->right);
}

int height(BNode<int>* r) {       // edge-height convention
    if (!r) return -1;
    return 1 + max(height(r->left), height(r->right));
}

void destroy(BNode<int>* r) {
    if (!r) return;
    destroy(r->left);
    destroy(r->right);
    delete r;                     // postorder: children first
}
```

Invariant/proof: recursive calls return correct results for the two smaller subtrees; the root formula combines them. The null guard is essential.

### Balanced-tree check

Computing height separately at every node can revisit subtrees and become $O(n^2)$ on a chain. Return height and failure together in one postorder traversal:

```cpp
int heightOrFail(BNode<int>* r) {
    if (!r) return 0;
    int L = heightOrFail(r->left);  if (L == -1) return -1;
    int R = heightOrFail(r->right); if (R == -1) return -1;
    if (abs(L - R) > 1) return -1;
    return 1 + max(L, R);
}
bool isHeightBalanced(BNode<int>* r) { return heightOrFail(r) != -1; }
```

This is $O(n)$: each node is processed once.

---

# 7. Binary search trees

## 7.1 Property, duplicate convention, and motivation

For every node with key $k$, the lecture BST convention is:

- every key in the left subtree is `< k`;
- every key in the right subtree is `>= k`.

Thus duplicates go right. Other implementations may reject duplicates or store a count, but the convention must be consistent in insertion, search, deletion, and validation.

A BST combines linked-tree flexibility with ordering. Operations follow one root-to-leaf path and therefore cost $\Theta(h)$, where $h$ is tree height--not automatically $\Theta(\log n)$.

## 7.2 Search, minimum, maximum, and insertion

```cpp
struct BSTNode {
    int key;
    BSTNode *left = nullptr, *right = nullptr;
};

BSTNode* search(BSTNode* r, int x) {
    while (r && r->key != x)
        r = (x < r->key) ? r->left : r->right;
    return r;
}

BSTNode* minimum(BSTNode* r) {
    if (!r) return nullptr;
    while (r->left) r = r->left;
    return r;
}

BSTNode* maximum(BSTNode* r) {
    if (!r) return nullptr;
    while (r->right) r = r->right;
    return r;
}

BSTNode* insert(BSTNode* r, int x) {
    if (!r) return new BSTNode{x};
    if (x < r->key) r->left = insert(r->left, x);
    else            r->right = insert(r->right, x); // duplicates right
    return r;
}
```

**Search invariant:** if key `x` occurs in the current subtree, the comparison identifies the only child subtree that can contain it. Discarding the other subtree cannot discard `x`.

Example insertion order `50, 30, 70, 20, 40, 60, 80`:

```text
        50
       /  \
     30    70
    / \    / \
   20 40  60 80
```

Search `60`: compare with 50 (go right), 70 (go left), then find 60. Inorder traversal is `20,30,40,50,60,70,80`.

### Why inorder is sorted

By induction, inorder of the left subtree is sorted and all its keys are smaller than the root. The root comes next. Inorder of the right subtree is sorted and all its keys are at least the root. Concatenating those three sequences is nondecreasing.

## 7.3 Predecessor and successor

The **inorder predecessor** of a node is the greatest key strictly before it in inorder order. The **successor** is the smallest key strictly after it. With duplicates, clarify whether you mean a neighboring node in inorder sequence or the next distinct key.

If parent pointers exist:

- If `x` has a left subtree, predecessor is `maximum(x->left)`.
- Otherwise move upward while `x` is a left child; the first ancestor for which `x` lies in its right subtree is the predecessor.
- If `x` has a right subtree, successor is `minimum(x->right)`.
- Otherwise move upward while `x` is a right child; the first ancestor for which `x` lies in its left subtree is the successor.

Using the tree above:

- predecessor of `50` is `40`; successor is `60`;
- predecessor of `60` is `50`; successor is `70`;
- predecessor of minimum `20` does not exist; successor of maximum `80` does not exist.

Without parent pointers, search from root while remembering a candidate:

```cpp
BSTNode* successor(BSTNode* root, int key) {
    BSTNode* candidate = nullptr;
    while (root) {
        if (key < root->key) {
            candidate = root;
            root = root->left;
        } else root = root->right;
    }
    return candidate;
}

BSTNode* predecessor(BSTNode* root, int key) {
    BSTNode* candidate = nullptr;
    while (root) {
        if (root->key < key) {
            candidate = root;
            root = root->right;
        } else root = root->left;
    }
    return candidate;
}
```

These functions return the next smaller/larger key relative to a query, not necessarily the neighboring duplicate node.

## 7.4 Deletion

There are three structural cases:

1. **Leaf:** replace it by null.
2. **One child:** replace it by its only child.
3. **Two children:** copy the minimum key from the right subtree (inorder successor) into the node, then delete that minimum from the right subtree.

```cpp
BSTNode* erase(BSTNode* r, int x) {
    if (!r) return nullptr;
    if (x < r->key) {
        r->left = erase(r->left, x);
    } else if (x > r->key) {
        r->right = erase(r->right, x);
    } else {
        if (!r->left) {
            BSTNode* replacement = r->right;
            delete r;
            return replacement;
        }
        if (!r->right) {
            BSTNode* replacement = r->left;
            delete r;
            return replacement;
        }
        BSTNode* s = minimum(r->right);
        r->key = s->key;
        r->right = erase(r->right, s->key);
    }
    return r;
}
```

Slide-style `deleteMin`:

```cpp
BSTNode* deleteMin(BSTNode* r) {
    if (!r->left) {
        BSTNode* replacement = r->right;
        delete r;
        return replacement;
    }
    r->left = deleteMin(r->left);
    return r;
}
```

**Why can the promoted minimum of the right subtree have no left child?** If it had a left child, that child would contain a still smaller key, contradicting minimality. It may have a right child, which must be reattached.

Worked deletion from the example tree:

- Delete leaf `20`: set `30.left=null`.
- Delete `30` after that: it has only child `40`, so `50.left=40`.
- Delete `50`: successor is `60`; copy `60` to the root, then remove the original `60` from under `70`. The ordering property remains true.

**Traps:** copying the successor key but forgetting to delete the original successor; failing to reconnect a successor's right child; and updating only a key but not its associated value in a key-value BST.

## 7.5 Height and degeneration

All operations above take $\Theta(h)$:

- in a height-balanced tree, $h=\Theta(\log n)$;
- inserting sorted keys into a plain BST can form a chain with $h=n-1$, giving $\Theta(n)$ search/insert/delete.

Random insertion often gives logarithmic expected height, but a plain BST has no logarithmic worst-case guarantee. The DSA-I slides motivate maintaining balance but do not teach AVL or red-black invariants/rotations. Do not pretend those are slide-covered here.

## 7.6 BST validation

Checking only each node against its immediate children is insufficient: a deep descendant can violate an ancestor bound. Under this chapter's "duplicates go right" rule, carry the half-open interval `[lowInclusive, highExclusive)`:

```cpp
bool validRange(BSTNode* r,
                optional<long long> lowInclusive,
                optional<long long> highExclusive) {
    if (!r) return true;
    long long k = r->key;
    if (lowInclusive && k < *lowInclusive) return false;
    if (highExclusive && k >= *highExclusive) return false;
    return validRange(r->left, lowInclusive, k) &&
           validRange(r->right, k, highExclusive);
}

bool validBST(BSTNode* root) {
    return validRange(root, nullopt, nullopt);
}
```

The left call makes the current key an exclusive upper bound; the right call makes it an inclusive lower bound. This also handles a duplicate that is in an ancestor's right subtree but later lies to the left of a larger descendant. Include `<optional>` and use `std::optional`/`std::nullopt` in non-pseudocode C++. Avoid `key+/-1`, which can overflow and mishandle noninteger keys. Another sound convention is to store `(key, insertion_id)` as a strict comparison key.

---

# 8. Binary heaps, priority queues, build-heap, and heapsort

## 8.1 Heap definition

A binary heap has two independent properties:

1. **Shape:** it is a complete binary tree.
2. **Order:** in a max-heap every parent key is at least its children; in a min-heap every parent is at most its children.

Consequences:

- the root is a global maximum/minimum;
- there is no ordering rule between siblings or across unrelated subtrees;
- searching for an arbitrary key can still be $\Theta(n)$;
- completeness gives height $\Theta(\log n)$ and compact array storage.

**Heap versus BST:** a max-heap quickly returns the maximum but cannot produce a search path for arbitrary keys. A BST orders the entire left/right relation and supports ordered search, predecessor, and successor when its height is controlled.

## 8.2 Height proof

For a complete tree of height $h$, levels `0..h-1` are full and the last level is nonempty:

$$2^h \le n \le 2^{h+1}-1.$$

Taking logarithms gives $h=\lfloor\log_2 n\rfloor=\Theta(\log n)$.

## 8.3 Sift up / insertion

Append at the next free array position to preserve completeness, then swap upward while heap order is violated.

```cpp
void pushMaxHeap(vector<int>& a, int x) { // 0-based
    a.push_back(x);
    int i = (int)a.size() - 1;
    while (i > 0) {
        int p = (i - 1) / 2;
        if (a[p] >= a[i]) break;
        swap(a[p], a[i]);
        i = p;
    }
}
```

Invariant: before each iteration, the only possible violation is between `i` and its parent; both child subheaps remain heaps. Each swap moves the new key one level, so time is $O(\log n)$.

Trace: push `50` into `[40,30,35,10,20]`:

```text
[40,30,35,10,20,50]
swap with 35 -> [40,30,50,10,20,35]
swap with 40 -> [50,30,40,10,20,35]
```

## 8.4 Heapify / sift down

`maxHeapify(i)` assumes the child subtrees are already max-heaps, but `a[i]` may violate heap order.

```cpp
void maxHeapify(vector<int>& a, int heapSize, int i) {
    while (true) {
        int largest = i;
        int left = 2*i + 1, right = 2*i + 2;
        if (left  < heapSize && a[left]  > a[largest]) largest = left;
        if (right < heapSize && a[right] > a[largest]) largest = right;
        if (largest == i) break;
        swap(a[i], a[largest]);
        i = largest;
    }
}
```

Swapping with the larger child fixes the root relative to both children. Only that child's subtree can now violate the property. The path has at most heap height, so time is $O(\log n)$. The slides also bound the recursive child subtree by at most $2n/3$:

$$T(n)\le T(2n/3)+\Theta(1)=\Theta(\log n).$$

**Source correction:** swap/recurse only when `largest != i`; otherwise an unconditional recursive call may not terminate.

## 8.5 Extract maximum and increase key

```cpp
int extractMax(vector<int>& a) {
    if (a.empty()) throw underflow_error("empty heap");
    int ans = a[0];
    a[0] = a.back();
    a.pop_back();
    if (!a.empty()) maxHeapify(a, a.size(), 0);
    return ans;
}

void increaseKey(vector<int>& a, int i, int larger) {
    if (larger < a[i]) throw invalid_argument("key decreased");
    a[i] = larger;
    while (i > 0 && a[(i-1)/2] < a[i]) {
        swap(a[i], a[(i-1)/2]);
        i = (i-1)/2;
    }
}
```

Replacing the root with the last item preserves completeness; sift-down restores order. `maximum` is $O(1)$; insert, extract, and increase-key are $O(\log n)$.

## 8.6 Build a heap in $O(n)$

Every index from `floor(n/2)` onward in a 1-based array is a leaf and already a one-element heap. Process internal nodes bottom-up:

```cpp
void buildMaxHeap(vector<int>& a) {        // 0-based
    for (int i = (int)a.size()/2 - 1; i >= 0; --i)
        maxHeapify(a, a.size(), i);
}
```

### Correctness invariant

Before processing index `i`, every subtree rooted at an index greater than `i` is a heap. Thus the child subtrees of `i` are heaps, exactly the precondition for `maxHeapify`. After it runs, the subtree at `i` is also a heap. When `i=0` finishes, the whole array is a heap.

### Tight running-time derivation

There are $O(n)$ calls and each is at most $O(\log n)$, so $O(n\log n)$ is a valid but loose upper bound. Most calls are near leaves and move zero or one level.

At most $\lceil n/2^{h+1}\rceil$ nodes have height $h$. Therefore

$$
T(n) \le \sum_{h=0}^{\lfloor\log n\rfloor}
\left\lceil\frac{n}{2^{h+1}}\right\rceil O(h)
=O\left(n\sum_{h\ge0}\frac{h}{2^{h+1}}\right)=O(n),
$$

because the infinite series converges to a constant. Reading the input is $\Omega(n)$, so bottom-up build-heap is $\Theta(n)$.

Starting empty and inserting all $n$ elements is correct but costs $O(n\log n)$ worst case.

## 8.7 Heapsort

```cpp
void heapSort(vector<int>& a) {
    buildMaxHeap(a);                         // Theta(n)
    for (int end = (int)a.size() - 1; end > 0; --end) {
        swap(a[0], a[end]);                  // maximum reaches final place
        maxHeapify(a, end, 0);               // live heap is [0,end)
    }
}
```

Loop invariant: `a[0..end]` is a max-heap and `a[end+1..n-1]` is sorted in final positions, with every suffix element at least every live-heap element. Each iteration extends the suffix by one maximum.

Total time is $\Theta(n)+(n-1)O(\log n)=O(n\log n)$, with a matching comparison-sort lower bound. It is in-place with iterative heapify and is not stable. The slides note that quicksort often wins in practice because of locality and constants.

---

# 9. Graph language and representations

## 9.1 Definitions

A graph is $G=(V,E)$, a set of vertices and edges.

- **Undirected edge** `{u,v}`: symmetric connection.
- **Directed edge** `(u,v)`: goes from `u` to `v`.
- **Weighted graph:** edges carry costs, distances, capacities, etc.
- **Adjacent vertices / incident edge.**
- **Degree** in an undirected graph: incident-edge count. In a digraph distinguish indegree and outdegree.
- **Walk:** vertices/edges may repeat. **Trail:** no repeated edge. **Path:** normally no repeated vertex. **Cycle:** closed nontrivial path.
- **Connected:** every pair has a path in an undirected graph. A disconnected traversal forms a forest.
- **Subgraph:** selected vertices and edges from another graph.
- **Tree:** connected acyclic undirected graph; equivalently, a connected $n$-vertex graph with $n-1$ edges, or one with a unique simple path between every pair.
- **Simple graph:** no self-loops or parallel edges.

### Handshake facts

For an undirected graph,

$$\sum_{v\in V}\deg(v)=2|E|,$$

because every edge contributes to two endpoint degrees. Therefore the number of odd-degree vertices is even. For a directed graph,

$$\sum_v indeg(v)=\sum_v outdeg(v)=|E|.$$

## 9.2 Representations

### Adjacency matrix

An $|V|\times|V|$ matrix stores whether or what edge connects each ordered pair.

- space $\Theta(V^2)$;
- edge-existence test $\Theta(1)$;
- enumerate neighbors of one vertex $\Theta(V)$;
- good for dense graphs or matrix-based algorithms;
- symmetric for a simple undirected graph.

### Adjacency list

For each vertex store its outgoing neighbors.

- space $\Theta(V+E)$ for directed graphs and $\Theta(V+2E)=\Theta(V+E)$ for undirected;
- enumerate neighbors in $\Theta(\deg(v))$;
- edge test $O(\deg(v))$ with a simple list, faster with a hash/set variant;
- good for sparse graphs and BFS/DFS.

### Edge list

Store `(u,v[,weight])` records: $\Theta(E)$ space, excellent for algorithms that scan/sort all edges, poor for repeated neighbor queries.

**Trap:** saying BFS is $O(V+E)$ assumes adjacency lists. With an adjacency matrix, scanning a row for every visited vertex is $O(V^2)$.

---

# 10. BFS, DFS, bipartite testing, cycles, and topological ordering

## 10.1 Breadth-first search

BFS expands the frontier by distance from a source. Colors encode state:

- white: undiscovered;
- gray: discovered/enqueued but not fully scanned;
- black: fully scanned.

```cpp
struct BFSResult {
    vector<int> distance;    // -1 means unreachable
    vector<int> parent;
};

BFSResult bfs(const vector<vector<int>>& adj, int s) {
    int n = adj.size();
    vector<int> color(n, 0), d(n, -1), parent(n, -1);
    queue<int> q;
    color[s] = 1; d[s] = 0; q.push(s);

    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : adj[u]) {
            if (color[v] == 0) {
                color[v] = 1;          // mark when enqueued
                d[v] = d[u] + 1;
                parent[v] = u;
                q.push(v);
            }
        }
        color[u] = 2;
    }
    return {d, parent};
}
```

Mark when enqueuing, not when dequeuing; otherwise multiple neighbors may enqueue the same vertex.

### Worked trace

Edges: `A-B, A-C, B-D, C-D, C-E`, source `A`.

```text
start: Q=[A], d(A)=0
remove A: discover B,C -> Q=[B,C], d=1
remove B: discover D   -> Q=[C,D], d(D)=2
remove C: D known; discover E -> Q=[D,E], d(E)=2
remove D, E: done
```

One valid BFS tree has parents `B<-A, C<-A, D<-B, E<-C`. Parent choice can depend on adjacency-list order, but distances do not.

### Shortest-path property and queue invariant

In an unweighted graph, `d[v]` equals the minimum number of edges from `s` to `v`. The lecture proves a useful queue invariant: queued distances are nondecreasing, and the last queued distance is at most the first queued distance plus 1. Newly discovered neighbors receive `d[u]+1`, so layers are processed in order. If there were a shorter path to `v`, its previous vertex would have been processed early enough to discover `v` at that shorter distance--a contradiction.

Reconstruct a path by following parents from target to source and reversing. If distance is `-1`, no source-to-target path exists.

### Complexity

Initialization is $O(V)$. Each vertex is enqueued/dequeued once; every adjacency-list entry is scanned once (directed) or twice (undirected). Thus time is $O(V+E)$ and auxiliary space is $O(V)$.

To traverse a disconnected graph, start BFS from every still-white vertex; the result is a BFS forest.

## 10.2 Depth-first search

DFS follows one path as deeply as possible, then backtracks.

```cpp
int timer = 0;
vector<int> color, parent, discover, finish;

void dfsVisit(int u, const vector<vector<int>>& adj) {
    color[u] = 1;
    discover[u] = ++timer;
    for (int v : adj[u]) {
        if (color[v] == 0) {
            parent[v] = u;
            dfsVisit(v, adj);
        }
    }
    color[u] = 2;
    finish[u] = ++timer;
}

void dfs(const vector<vector<int>>& adj) {
    int n = adj.size();
    color.assign(n, 0); parent.assign(n, -1);
    discover.resize(n); finish.resize(n); timer = 0;
    for (int u = 0; u < n; ++u)
        if (color[u] == 0) dfsVisit(u, adj);
}
```

Time is $O(V+E)$ with adjacency lists. Recursive space is $O(V)$ in the worst case; an explicit stack avoids call-stack overflow but not the need to remember the frontier.

### Timestamp / parenthesis theorem

Each vertex has interval `[discover[u], finish[u]]`. For any two vertices, their intervals are either disjoint or one is nested inside the other. Vertex `v` is a descendant of `u` exactly when

$$d[u]<d[v]<f[v]<f[u].$$

This follows because a recursive call for `u` cannot finish until all recursive descendants finish.

### White-path theorem

At discovery time of `u`, vertex `v` becomes a descendant of `u` iff a path from `u` to `v` consists entirely of white vertices at that moment (allowing `u`). This characterizes the DFS tree independent of syntax.

## 10.3 DFS edge classification

In a directed graph:

- **tree edge:** discovers a white vertex;
- **back edge:** goes to a gray ancestor;
- **forward edge:** goes to a black descendant but is not a tree edge;
- **cross edge:** connects other completed branches/subtrees.

A directed graph is acyclic iff DFS finds no back edge.

In an undirected DFS, every edge is a tree edge or a back edge when each physical edge is interpreted once. The apparent edge from a child back to its parent is the same undirected tree edge, so skip the parent when detecting a cycle.

## 10.4 Cycle detection

Directed:

```cpp
bool cycleDirected(int u, const vector<vector<int>>& adj, vector<int>& color) {
    color[u] = 1;
    for (int v : adj[u]) {
        if (color[v] == 1) return true;
        if (color[v] == 0 && cycleDirected(v, adj, color)) return true;
    }
    color[u] = 2;
    return false;
}
```

Undirected:

```cpp
bool cycleUndirected(int u, int p, const vector<vector<int>>& adj,
                     vector<bool>& seen) {
    seen[u] = true;
    for (int v : adj[u]) {
        if (!seen[v]) {
            if (cycleUndirected(v, u, adj, seen)) return true;
        } else if (v != p) return true;
    }
    return false;
}
```

Run from every unvisited vertex. A plain "visited neighbor means cycle" test is wrong for directed graphs and mistakes the parent edge in undirected graphs.

## 10.5 Bipartite graph testing

A graph is bipartite iff its vertices can be colored with two colors so every edge has different endpoint colors. Equivalently, an undirected graph is bipartite iff it has no odd cycle.

```cpp
bool isBipartite(const vector<vector<int>>& adj) {
    int n = adj.size();
    vector<int> side(n, -1);
    for (int s = 0; s < n; ++s) {
        if (side[s] != -1) continue;
        queue<int> q;
        side[s] = 0; q.push(s);
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (int v : adj[u]) {
                if (side[v] == -1) {
                    side[v] = side[u] ^ 1;
                    q.push(v);
                } else if (side[v] == side[u]) return false;
            }
        }
    }
    return true;
}
```

BFS level parity supplies the colors. A same-color edge plus the two BFS-tree paths gives an odd cycle. Conversely, colors must alternate around every cycle, so an odd cycle cannot return consistently to its starting color.

**Source correction:** the one-slide code starts from one source. That is sufficient only for its connected component. The outer loop is required for a disconnected graph.

## 10.6 Topological ordering

A topological order is a linear order of a directed graph in which every edge `u->v` places `u` before `v`. It exists iff the graph is a DAG.

### DFS method

Run cycle-detecting DFS and list vertices in decreasing finish time. For every DAG edge `u->v`, DFS ensures `finish[u] > finish[v]`.

### Kahn's algorithm

```cpp
vector<int> topo(const vector<vector<int>>& adj) {
    int n = adj.size();
    vector<int> indeg(n, 0), order;
    for (int u = 0; u < n; ++u)
        for (int v : adj[u]) ++indeg[v];

    queue<int> q;
    for (int u = 0; u < n; ++u) if (indeg[u] == 0) q.push(u);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        order.push_back(u);
        for (int v : adj[u]) if (--indeg[v] == 0) q.push(v);
    }
    if ((int)order.size() != n) throw logic_error("directed cycle");
    return order;
}
```

Invariant: the queue contains unprocessed vertices with no incoming edge from the remaining graph. Removing one is safe; decrementing neighbors simulates deleting its outgoing edges. Complexity is $O(V+E)$.

For the lexicographically smallest valid order, replace the FIFO queue with a min-heap. A normal DFS order does not generally guarantee lexicographic minimality.

## 10.7 BFS versus DFS

| Question | BFS | DFS |
|---|---|---|
| Frontier structure | queue | call stack / explicit stack |
| Unweighted shortest paths | yes | no |
| Memory tendency | may store a wide level | may store a deep path |
| Natural applications | levels, minimum-edge path, bipartite | timestamps, cycles, topological structure |
| Complexity with lists | $O(V+E)$ | $O(V+E)$ |

Neither is inherently "faster"; both scan the reachable representation once. Choose by the required property.

---

# 11. Searching and sorting

## 11.1 Linear and binary search

### Linear search

```cpp
int linearSearch(const vector<int>& a, int key) {
    for (int i = 0; i < (int)a.size(); ++i)
        if (a[i] == key) return i;
    return -1;
}
```

It works on unsorted sequential data. Best case is $\Theta(1)$; worst case is $\Theta(n)$; extra space is $\Theta(1)$. On a singly linked list this is the natural search because reaching the middle is not constant-time.

### Binary search

Contract: `a` is sorted in nondecreasing order. Maintain a half-open candidate interval `[lo,hi)`.

```cpp
int binarySearch(const vector<int>& a, int key) {
    int lo = 0, hi = a.size();
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] < key) lo = mid + 1;
        else if (key < a[mid]) hi = mid;
        else return mid;
    }
    return -1;
}
```

Invariant: if `key` exists, at least one occurrence lies in `[lo,hi)`. Each comparison discards a region that cannot contain it. The interval length strictly decreases. Recurrence $T(n)=T(n/2)+\Theta(1)=\Theta(\log n)$.

Trace on `[2,5,8,12,16,23,38]`, key `16`:

```text
[0,7), mid=3, a[3]=12 < 16 -> [4,7)
mid=5, a[5]=23 > 16      -> [4,5)
mid=4, a[4]=16            -> found
```

Use `lo + (hi-lo)/2` to avoid overflow. Binary search on a linked list is not useful in the usual form: locating each midpoint is linear, so the random-access benefit disappears.

### Lower bound / insertion position

`lower_bound` returns the first index whose value is at least `key`:

```cpp
int lowerBound(const vector<int>& a, int key) {
    int lo = 0, hi = a.size();
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] < key) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}
```

Invariant: all indices below `lo` are too small; all indices at or above `hi` are known candidates. `upper_bound` instead finds the first value strictly greater than the key.

## 11.2 Sorting vocabulary

- **Stable:** equal keys retain original relative order. Important when sorting records by multiple fields.
- **In-place:** uses $O(1)$ or very small auxiliary storage, depending on convention.
- **Adaptive:** runs faster when data is already/nearly sorted.
- **Comparison sort:** learns order only through comparisons.
- **Internal/external:** data fits in memory / requires external storage.

### Comparison table

| Algorithm | Best | Average | Worst | Extra space | Stable? | Main idea |
|---|---:|---:|---:|---:|---|---|
| Bubble | $O(n)$ with early stop | $O(n^2)$ | $O(n^2)$ | $O(1)$ | yes | swap adjacent inversions |
| Selection | $\Theta(n^2)$ | $\Theta(n^2)$ | $\Theta(n^2)$ | $O(1)$ | normally no | select minimum for each slot |
| Insertion | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | yes | grow sorted prefix |
| Merge | $\Theta(n\log n)$ | same | same | $\Theta(n)$ | yes if ties take left | split, sort, merge |
| Quicksort | $\Theta(n\log n)$ | expected $\Theta(n\log n)$ | $\Theta(n^2)$ | expected $O(\log n)$ stack | normally no | partition about pivot |
| Heapsort | $\Theta(n\log n)$ | same | same | $O(1)$ | no | repeatedly extract heap root |

The elementary three are included as recall prerequisites; the local algorithm PDF develops merge sort and quicksort in depth, while heap decks develop heapsort.

## 11.3 Insertion sort

```cpp
void insertionSort(vector<int>& a) {
    for (int i = 1; i < (int)a.size(); ++i) {
        int key = a[i], j = i - 1;
        while (j >= 0 && a[j] > key) {
            a[j + 1] = a[j];
            --j;
        }
        a[j + 1] = key;
    }
}
```

Invariant: before iteration `i`, `a[0..i-1]` is a sorted permutation of its original elements. Shift larger elements right and insert `key` into its unique position. The number of shifts equals the number of inversions involving the inserted item; therefore it is adaptive and runs in $\Theta(n+I)$ where $I$ is the inversion count.

## 11.4 Selection and bubble sort

```cpp
void selectionSort(vector<int>& a) {
    for (int i = 0; i < (int)a.size(); ++i) {
        int m = i;
        for (int j = i + 1; j < (int)a.size(); ++j)
            if (a[j] < a[m]) m = j;
        swap(a[i], a[m]);
    }
}

void bubbleSort(vector<int>& a) {
    for (int end = a.size() - 1; end > 0; --end) {
        bool changed = false;
        for (int i = 0; i < end; ++i) {
            if (a[i] > a[i + 1]) {
                swap(a[i], a[i + 1]);
                changed = true;
            }
        }
        if (!changed) break;
    }
}
```

Selection sort makes $\Theta(n^2)$ comparisons even when already sorted, but only $O(n)$ swaps. Bubble sort's pass moves the largest remaining value to `end`; with early stopping it detects sorted input in $O(n)$.

## 11.5 Merge sort

Divide into halves, recursively sort both, then merge two sorted ranges.

```cpp
void mergeRanges(vector<int>& a, vector<int>& tmp, int l, int m, int r) {
    int i = l, j = m, k = l;
    while (i < m && j < r) {
        if (a[i] <= a[j]) tmp[k++] = a[i++]; // <= preserves stability
        else              tmp[k++] = a[j++];
    }
    while (i < m) tmp[k++] = a[i++];
    while (j < r) tmp[k++] = a[j++];
    for (int p = l; p < r; ++p) a[p] = tmp[p];
}

void mergeSort(vector<int>& a, vector<int>& tmp, int l, int r) {
    if (r - l <= 1) return;
    int m = l + (r - l) / 2;
    mergeSort(a, tmp, l, m);
    mergeSort(a, tmp, m, r);
    mergeRanges(a, tmp, l, m, r);
}
```

Merge invariant: `tmp[l..k)` contains the smallest `k-l` elements of the two input prefixes in sorted order; `i` and `j` point to the smallest unmerged element of each half. Each merge costs $\Theta(r-l)$.

The handwritten trace begins with `[10,5,3,2,7,11,6,1]`: recursively obtain `[2,3,5,10]` and `[1,6,7,11]`, then merge to `[1,2,3,5,6,7,10,11]`.

Recurrence $T(n)=2T(n/2)+\Theta(n)=\Theta(n\log n)$. Standard array merge sort uses $\Theta(n)$ auxiliary memory and is stable when equal values come from the left first.

## 11.6 Quicksort with Lomuto partition

```cpp
int partition(vector<int>& a, int lo, int hi) { // inclusive hi
    int pivot = a[hi];
    int i = lo - 1;
    for (int j = lo; j < hi; ++j) {
        if (a[j] <= pivot) {
            ++i;
            swap(a[i], a[j]);
        }
    }
    swap(a[i + 1], a[hi]);
    return i + 1;
}

void quickSort(vector<int>& a, int lo, int hi) {
    if (lo >= hi) return;
    int q = partition(a, lo, hi);
    quickSort(a, lo, q - 1);
    quickSort(a, q + 1, hi);
}
```

Partition invariant during the scan:

- `a[lo..i] <= pivot`;
- `a[i+1..j-1] > pivot`;
- `a[j..hi-1]` is unclassified;
- pivot remains at `hi`.

After the final swap, the pivot is in its final rank position. Balanced partitions give $T(n)=2T(n/2)+\Theta(n)=\Theta(n\log n)$. Repeated extreme pivots give $T(n)=T(n-1)+\Theta(n)=\Theta(n^2)$. Randomly choosing the pivot gives expected $\Theta(n\log n)$ independent of original input order, but worst case remains quadratic.

Quicksort is normally in-place apart from its recursion stack and normally unstable. Tail-recursing on the smaller side and iterating over the larger limits stack depth to $O(\log n)$ even when partitions are poor.

## 11.7 Comparison-sort lower bound

A deterministic comparison sort corresponds to a decision tree whose leaves distinguish the $n!$ input permutations. A binary tree of height $h$ has at most $2^h$ leaves, so

$$2^h\ge n! \implies h\ge\log_2(n!)=\Omega(n\log n).$$

Therefore no comparison sort can guarantee asymptotically better than $\Omega(n\log n)$ for arbitrary distinct keys. Counting/radix methods can beat it only by exploiting additional key structure, not comparisons alone.

---

# 12. Divide and conquer

## 12.1 Pattern and proof method

Divide-and-conquer algorithms:

1. **divide** an instance into smaller independent instances;
2. **conquer** them recursively;
3. **combine** their answers.

The common recurrence is $T(n)=aT(n/b)+f(n)$. Correctness normally follows by strong induction: recursive calls solve smaller inputs, and the combine step is proved to transform their answers into the full answer.

## 12.2 Simultaneous maximum and minimum

A naive scan comparing every later value separately to maximum and minimum uses up to $2n-2$ comparisons. Divide into halves, obtain `(min,max)` for each, and combine with two comparisons.

```cpp
pair<int,int> minMax(const vector<int>& a, int l, int r) { // [l,r)
    int n = r - l;
    if (n == 1) return {a[l], a[l]};
    if (n == 2) {
        if (a[l] < a[l+1]) return {a[l], a[l+1]};
        return {a[l+1], a[l]};
    }
    int m = l + n/2;
    auto L = minMax(a, l, m);
    auto R = minMax(a, m, r);
    return {min(L.first, R.first), max(L.second, R.second)};
}
```

For even $n$ (and equivalently with pairwise scanning), the comparison count is about $3n/2-2$: one comparison within each pair, then each pair's smaller member competes for minimum and larger member for maximum. Time remains $\Theta(n)$, but comparisons improve over $2n-2$.

## 12.3 Maximum subarray by divide and conquer

Problem: find a contiguous nonempty subarray with maximum sum.

A maximum subarray lies entirely left, entirely right, or crosses the midpoint. A crossing optimum is the best suffix of the left half plus the best prefix of the right half.

```cpp
struct Segment { long long sum; int l, r; }; // inclusive endpoints

Segment maxCrossing(const vector<int>& a, int l, int m, int r) {
    long long sum = 0, bestL = LLONG_MIN, bestR = LLONG_MIN;
    int leftIndex = m, rightIndex = m + 1;
    for (int i = m; i >= l; --i) {
        sum += a[i];
        if (sum > bestL) { bestL = sum; leftIndex = i; }
    }
    sum = 0;
    for (int j = m + 1; j <= r; ++j) {
        sum += a[j];
        if (sum > bestR) { bestR = sum; rightIndex = j; }
    }
    return {bestL + bestR, leftIndex, rightIndex};
}

Segment maxSubarrayDC(const vector<int>& a, int l, int r) {
    if (l == r) return {a[l], l, r};
    int m = l + (r-l)/2;
    Segment L = maxSubarrayDC(a, l, m);
    Segment R = maxSubarrayDC(a, m+1, r);
    Segment C = maxCrossing(a, l, m, r);
    return max({L,R,C}, [](const Segment& x, const Segment& y) {
        return x.sum < y.sum;
    });
}
```

Recurrence $T(n)=2T(n/2)+\Theta(n)=\Theta(n\log n)$. The brute-force start/end enumeration is $O(n^2)$ if sums are extended incrementally, or $O(n^3)$ if every sum is recomputed. Kadane's DP later improves this to $O(n)$.

**Edge case:** do not initialize to zero if the subarray must be nonempty; an all-negative array should return its largest (least negative) element.

## 12.4 Counting inversions while merging

An inversion is a pair $(i,j)$ with $i<j$ but `a[i] > a[j]`. It measures how far a sequence is from sorted order and supports rank-disagreement analysis.

During merge, if `left[i] <= right[j]`, take the left value. Otherwise `right[j]` is smaller than every remaining left value, contributing `leftSize-i` cross inversions.

```cpp
long long sortAndCount(vector<int>& a, vector<int>& tmp, int l, int r) {
    if (r - l <= 1) return 0;
    int m = l + (r-l)/2;
    long long inv = sortAndCount(a, tmp, l, m)
                  + sortAndCount(a, tmp, m, r);
    int i=l, j=m, k=l;
    while (i<m && j<r) {
        if (a[i] <= a[j]) tmp[k++] = a[i++];
        else {
            tmp[k++] = a[j++];
            inv += m - i;
        }
    }
    while (i<m) tmp[k++] = a[i++];
    while (j<r) tmp[k++] = a[j++];
    for (int p=l; p<r; ++p) a[p]=tmp[p];
    return inv;
}
```

The handwritten example `[2,5,4,1,6,3]` has seven inversions:

```text
(2,1), (5,4), (5,1), (5,3), (4,1), (4,3), (6,3)
```

Left recursion counts 1, right counts 1, and the final merge counts 5 cross inversions. Time is $\Theta(n\log n)$ and extra space $\Theta(n)$.

## 12.5 Closest pair of points

Given $n$ points in the plane, find the pair with minimum Euclidean distance. Brute force checks $\binom n2=\Theta(n^2)$ pairs.

Divide-and-conquer outline:

1. Sort points by `x` once and split around median x-coordinate.
2. Recursively find best distances $\delta_L,\delta_R$; let $\delta=\min(\delta_L,\delta_R)$.
3. Only a cross pair can improve the result. Put points with horizontal distance below $\delta$ from the split into a vertical strip.
4. Process the strip in `y` order. For each point, compare only subsequent points whose y-difference is below $\delta$.

### Why only a constant number of strip comparisons?

Partition the relevant $2\delta \times \delta$ rectangle into small cells (or use the standard packing argument). Because each recursive half already has no pair closer than $\delta$, only a constant number of points can occupy the region. The course notes express the bound as at most six relevant opposite-side successors; many textbooks state at most seven next points under a slightly different counting convention. The important fact is **constant**, not the memorized 6/7.

```text
closest(Px, Py):
    if |Px| <= 3: brute force
    split Px into Qx,Rx; partition Py into Qy,Ry in linear time
    dl = closest(Qx,Qy); dr = closest(Rx,Ry); d = min(dl,dr)
    strip = points of Py with |x-midX| < d   // already y-sorted
    compare each strip point with next O(1) candidates
    return minimum distance found
```

If x-sorted and y-sorted lists are maintained and partitioned in linear time, the recurrence is

$$T(n)=2T(n/2)+\Theta(n)=\Theta(n\log n).$$

The two-page UBC note and handwritten note also show a simpler version that sorts the strip by y inside each recursive call. Its combine cost is $\Theta(n\log n)$, so

$$T(n)=2T(n/2)+\Theta(n\log n)=\Theta(n\log^2n).$$

**Viva trap:** do not claim $O(n\log n)$ while showing the re-sort-at-every-level implementation. State which implementation you analyze. Handle duplicate points immediately: the answer is zero.

## 12.6 Karatsuba integer multiplication

Split two $n$-digit numbers around base power $B^m$:

$$x=aB^m+b,\qquad y=cB^m+d.$$

Ordinary expansion needs four half-size multiplications:

$$xy=acB^{2m}+(ad+bc)B^m+bd.$$

Karatsuba computes only

```text
z2 = ac
z0 = bd
z1 = (a+b)(c+d) - z2 - z0 = ad+bc
answer = z2*B^(2m) + z1*B^m + z0
```

Thus

$$T(n)=3T(n/2)+\Theta(n)=\Theta(n^{\log_2 3})\approx\Theta(n^{1.585}),$$

instead of the four-product recurrence $4T(n/2)+\Theta(n)=\Theta(n^2)$. Base cases use ordinary machine multiplication; unequal digit lengths are padded conceptually. The asymptotic advantage appears for large integers because additions and splitting also have cost.

## 12.7 $k$-th element of two sorted arrays

Discard a prefix that cannot contain the $k$-th smallest. The version below uses 1-based `k` among the remaining elements:

```cpp
int kth(const vector<int>& A, int i,
        const vector<int>& B, int j, int k) {
    if (i == (int)A.size()) return B[j+k-1];
    if (j == (int)B.size()) return A[i+k-1];
    if (k == 1) return min(A[i], B[j]);

    int takeA = min(k/2, (int)A.size()-i);
    int takeB = min(k/2, (int)B.size()-j);
    if (A[i+takeA-1] <= B[j+takeB-1])
        return kth(A, i+takeA, B, j, k-takeA);
    return kth(A, i, B, j+takeB, k-takeB);
}
```

Proof idea: if `A[i+takeA-1] <= B[j+takeB-1]`, the first `takeA` remaining elements of `A` cannot extend beyond the desired rank, so they can be discarded while reducing `k`. With careful balanced partitions this takes $O(\log n+\log m)$ / $O(\log(k))$ style time, depending on formulation. Validate `1 <= k <= remaining total`.

---

# 13. Greedy algorithms

## 13.1 What makes a greedy algorithm valid?

A greedy algorithm commits to the locally best available choice and does not revise it. Greedy is not justified by speed or intuition alone. A proof usually needs:

- **greedy-choice property:** some optimal solution contains the proposed first choice;
- **optimal substructure:** after that choice, the remaining decisions form the same problem on a smaller instance.

Common proof patterns are an exchange argument, stays-ahead argument, cut property, or induction. A counterexample is enough to refute a proposed greedy rule.

## 13.2 Activity / interval selection

Given activities with start and finish times, select the largest mutually compatible subset. Sort by nondecreasing finish time, choose the first, then choose every next activity whose start is at least the last selected finish.

```cpp
struct Activity { int start, finish, id; };

vector<Activity> activitySelection(vector<Activity> a) {
    sort(a.begin(), a.end(), [](auto& x, auto& y) {
        return tie(x.finish,x.start) < tie(y.finish,y.start);
    });
    vector<Activity> chosen;
    int lastFinish = INT_MIN;
    for (auto x : a) {
        if (x.start >= lastFinish) {
            chosen.push_back(x);
            lastFinish = x.finish;
        }
    }
    return chosen;
}
```

### Exchange proof

Let `g` be the earliest-finishing activity and let `o` be the first activity of an optimal solution. Since `finish(g) <= finish(o)`, replacing `o` by `g` cannot make any later chosen activity incompatible. Thus an optimal solution exists that starts with `g`. After choosing `g`, only activities starting after it finishes matter; that is the same problem on a smaller set. Induction proves the algorithm optimal.

Equivalent stays-ahead view: the $i$-th greedy-selected activity finishes no later than the $i$-th activity of any other feasible schedule, leaving at least as much room for the future.

Sorting costs $O(n\log n)$; the scan is $O(n)$. If input is already sorted by finish time, the selection phase is $O(n)$.

**Counterexamples to other rules:** earliest start can choose a very long activity; shortest duration can block two compatible activities; fewest conflicts is not generally a safe local proof.

## 13.3 Fractional knapsack

Item $i$ has value $v_i$, weight $w_i>0$, and density $r_i=v_i/w_i$. A fraction $x_i\in[0,1]$ may be taken:

$$
\max \sum_i v_ix_i
\quad\text{subject to}\quad
\sum_i w_ix_i\le W.
$$

Sort by decreasing density, take each whole item while it fits, then take just enough of the next item to fill the remaining capacity.

```cpp
struct Item { double value, weight; int id; };

double fractionalKnapsack(vector<Item> items, double W) {
    sort(items.begin(), items.end(), [](const Item& a, const Item& b) {
        return a.value/a.weight > b.value/b.weight;
    });
    double answer = 0;
    for (auto item : items) {
        if (W == 0) break;
        double take = min(item.weight, W);
        answer += take * (item.value / item.weight);
        W -= take;
    }
    return answer;
}
```

Only the last selected positive-weight item can be fractional: once capacity fills, no later item is taken.

### Exchange proof

Suppose a feasible solution takes some positive weight from a lower-density item `j` while not taking all available weight from a higher-density item `i`. Move a small weight $\epsilon$ from `j` to `i`. Total weight stays unchanged, while value changes by $\epsilon(r_i-r_j)\ge0$ and strictly improves when densities differ. Repeating exchanges transforms an optimal solution into greedy density order without reducing value.

Complexity is $O(n\log n)$ for sorting and $O(n)$ for scanning. If density order is precomputed, the fill is linear.

### Handwritten-note example

Capacity is 10 and the scan compares values, weights, and ratios. With an item of value 20 and weight 2 (density 10), one of value 15 and weight 3 (density 5), then lower-density choices, the fractional solution takes the highest densities first and a final fraction, obtaining value 55 in the note. The exact lesson is the unit-value exchange argument, not memorizing the item labels.

## 13.4 Why the same greedy rule fails for 0/1 knapsack

In 0/1 knapsack, $x_i\in\{0,1\}$; fractions are forbidden. Replacing a small amount is no longer allowed, so the exchange proof collapses.

Counterexample: capacity 50, items `(weight,value)`

```text
(10,60), (20,100), (30,120)
```

Density greedy takes the first two for value 160, but the last two fit exactly and give 220. Therefore 0/1 knapsack needs DP, exhaustive search, branch-and-bound, or approximation depending on constraints.

## 13.5 Job sequencing with deadlines and profits

In the unit-time version, job `j` earns profit only if scheduled in one slot no later than deadline `d[j]`. Greedy order is descending profit; place each job in the latest still-free slot at or before its deadline.

```cpp
struct Job { int deadline, profit, id; };

vector<int> scheduleJobs(vector<Job> jobs) {
    sort(jobs.begin(), jobs.end(), [](auto a, auto b) {
        return a.profit > b.profit;
    });
    int D = 0;
    for (auto j : jobs) D = max(D, j.deadline);
    vector<int> slot(D + 1, -1);
    for (auto j : jobs) {
        for (int t = min(D,j.deadline); t >= 1; --t) {
            if (slot[t] == -1) { slot[t] = j.id; break; }
        }
    }
    return slot;
}
```

Why latest slot? It preserves earlier slots for jobs with tighter deadlines. The slide-note implementation is $O(n\log n+nD)$, often written $O(n^2)$ when $D\le n$. A disjoint-set predecessor structure can find the latest free slot much faster after sorting.

Assumptions matter: jobs take one unit, deadlines are discrete, and profits are independent. Arbitrary durations make this a different scheduling problem.

## 13.6 Minimum railway platforms / maximum overlap

Given arrival and departure times, the required platform count is the maximum number of simultaneously active intervals. The notes include an $O(n^2)$ direct comparison; a sorted sweep is stronger:

```cpp
int minPlatforms(vector<int> arrival, vector<int> departure) {
    sort(arrival.begin(), arrival.end());
    sort(departure.begin(), departure.end());
    int i=0, j=0, active=0, best=0;
    while (i < (int)arrival.size()) {
        if (arrival[i] <= departure[j]) { // chosen tie convention
            ++active; best=max(best,active); ++i;
        } else {
            --active; ++j;
        }
    }
    return best;
}
```

Time is $O(n\log n)$; scan invariant: `active` equals arrivals already processed minus departures already processed. Explicitly define ties: if a departure at time `t` frees a platform before an arrival at `t`, use `<` instead of `<=` in the arrival branch.

## 13.7 Greedy checklist for a viva

When asked "can we use greedy?", do not immediately say yes. State:

1. the precise local rule;
2. a proof exchange/stays-ahead invariant;
3. a counterexample search;
4. constraints that make the proof valid;
5. implementation and cost.

---

# 14. Dynamic programming

## 14.1 When DP applies

Dynamic programming solves problems with:

- **optimal substructure:** an optimal answer can be formed from optimal answers to subproblems;
- **overlapping subproblems:** the same state is requested repeatedly.

The design recipe:

1. define a state in a complete sentence;
2. identify the decision made at that state;
3. write a recurrence from smaller states;
4. specify base cases;
5. choose memoization or a valid table order;
6. recover choices if the actual solution--not only its value--is required;
7. count states times work per state and account for memory.

**DP versus divide-and-conquer:** D&C subproblems are usually independent; DP caches repeated states. **DP versus greedy:** DP considers competing choices and retains their best result; greedy commits to one choice and needs a special proof.

## 14.2 Fibonacci: the smallest overlap example

Naive recursion:

```cpp
long long fib(int n) {
    if (n <= 1) return n;
    return fib(n-1) + fib(n-2);
}
```

It recomputes the same values and takes exponential time (more tightly $\Theta(\varphi^n)$), with $O(n)$ stack depth.

### Memoization: top down

```cpp
long long fibMemo(int n, vector<long long>& memo) {
    if (n <= 1) return n;
    if (memo[n] != -1) return memo[n];
    return memo[n] = fibMemo(n-1,memo) + fibMemo(n-2,memo);
}
```

### Tabulation: bottom up

```cpp
long long fibTab(int n) {
    if (n <= 1) return n;
    long long prev2=0, prev1=1;
    for (int i=2; i<=n; ++i) {
        long long cur=prev1+prev2;
        prev2=prev1; prev1=cur;
    }
    return prev1;
}
```

Both take $O(n)$ time. Memoization computes only reached states but pays recursion; tabulation controls order and can compress space to $O(1)$ because only two earlier states are needed.

## 14.3 Longest common subsequence (LCS)

A subsequence preserves order but need not be contiguous. Define

$$dp[i][j]=\text{length of an LCS of }X[0..i)\text{ and }Y[0..j).$$

Recurrence:

$$
dp[i][j]=
\begin{cases}
0,&i=0\text{ or }j=0,\\
1+dp[i-1][j-1],&X[i-1]=Y[j-1],\\
\max(dp[i-1][j],dp[i][j-1]),&X[i-1]\ne Y[j-1].
\end{cases}
$$

```cpp
pair<int,string> lcs(const string& X, const string& Y) {
    int n=X.size(), m=Y.size();
    vector<vector<int>> dp(n+1, vector<int>(m+1));
    for (int i=1; i<=n; ++i) {
        for (int j=1; j<=m; ++j) {
            if (X[i-1]==Y[j-1]) dp[i][j]=1+dp[i-1][j-1];
            else dp[i][j]=max(dp[i-1][j],dp[i][j-1]);
        }
    }
    string answer;
    int i=n,j=m;
    while (i>0 && j>0) {
        if (X[i-1]==Y[j-1]) {
            answer.push_back(X[i-1]); --i; --j;
        } else if (dp[i-1][j] >= dp[i][j-1]) --i;
        else --j;
    }
    reverse(answer.begin(),answer.end());
    return {dp[n][m],answer};
}
```

For `X=ABCBDAB`, `Y=BDCABA`, the length is 4; valid LCSs include `BCBA` and `BDAB`. Multiple optimal answers are normal.

Correctness: if last characters match, an optimal solution can include that common character after an LCS of both prefixes. If not, any common subsequence omits at least one of those two last characters, so the maximum of the two smaller states is exhaustive.

Time and table space are $O(nm)$. If only length is needed, retain two rows for $O(\min(n,m))$ space; ordinary reconstruction needs the table or extra techniques.

## 14.4 Minimum coin change

Given denominations `coins` and target amount $M$, find the minimum number of coins with unlimited reuse. Greedy is not valid for arbitrary denominations: for coins `{1,3,4}` and amount 6, greedy takes `4+1+1` (3 coins), but `3+3` uses 2.

Define `dp[x]` as the fewest coins making exactly amount `x`:

$$dp[0]=0,\qquad dp[x]=1+\min_{c\le x}dp[x-c].$$

```cpp
int minCoins(const vector<int>& coins, int M) {
    const int INF=M+1;
    vector<int> dp(M+1,INF), choice(M+1,-1);
    dp[0]=0;
    for (int x=1; x<=M; ++x) {
        for (int c:coins) if (c<=x && dp[x-c]!=INF) {
            if (dp[x-c]+1 < dp[x]) {
                dp[x]=dp[x-c]+1;
                choice[x]=c;
            }
        }
    }
    return dp[M]==INF ? -1 : dp[M];
}
```

There are $M+1$ states and $d$ denominations, so time is $O(Md)$ and space $O(M)$. This is pseudo-polynomial: it is polynomial in numeric value $M$, not in the bit length $\log M$.

Do not confuse "minimum number of coins" with "number of ways to make the amount"; that problem changes the recurrence and loop-order interpretation.

## 14.5 0/1 knapsack

Each item may be chosen at most once. Define

$$dp[i][w]=\text{maximum value using the first }i\text{ items within capacity }w.$$

For item `i-1` of weight $w_i$ and value $v_i$:

$$
dp[i][w]=
\begin{cases}
dp[i-1][w],&w_i>w,\\
\max(dp[i-1][w],v_i+dp[i-1][w-w_i]),&w_i\le w.
\end{cases}
$$

```cpp
pair<int,vector<int>> knapsack01(const vector<int>& wt,
                                 const vector<int>& val, int W) {
    int n=wt.size();
    vector<vector<int>> dp(n+1,vector<int>(W+1));
    for (int i=1; i<=n; ++i) {
        for (int w=0; w<=W; ++w) {
            dp[i][w]=dp[i-1][w];
            if (wt[i-1]<=w)
                dp[i][w]=max(dp[i][w],val[i-1]+dp[i-1][w-wt[i-1]]);
        }
    }

    vector<int> chosen;
    for (int i=n,w=W; i>0; --i) {
        if (dp[i][w] != dp[i-1][w]) {
            chosen.push_back(i-1);
            w -= wt[i-1];
        }
    }
    reverse(chosen.begin(),chosen.end());
    return {dp[n][W],chosen};
}
```

The image-only notes use capacity 5, weights `[2,3,4,5]`, values `[3,4,5,6]`. The optimum is 7 by taking weights 2 and 3. A brute-force subset search has $2^n$ choices; DP has $O(nW)$ time and $O(nW)$ table space.

### One-dimensional compression and the crucial loop direction

```cpp
vector<int> dp(W+1,0);
for (int i=0; i<n; ++i)
    for (int w=W; w>=wt[i]; --w)
        dp[w]=max(dp[w],val[i]+dp[w-wt[i]]);
```

Capacity runs **downward** so an item is not reused in the same iteration. Running upward instead implements unbounded reuse. This is a classic viva trap.

Like coin change, $O(nW)$ is pseudo-polynomial.

## 14.6 Unbounded knapsack

Items may be reused. A 1-D recurrence is

$$dp[w]=\max_{i:w_i\le w}(v_i+dp[w-w_i]).$$

```cpp
for (int i=0; i<n; ++i)
    for (int w=wt[i]; w<=W; ++w)
        dp[w]=max(dp[w],val[i]+dp[w-wt[i]]);
```

The increasing capacity loop makes the current item's newly updated state available again. Clearly state whether reuse is allowed before choosing a loop order.

## 14.7 Weighted interval scheduling

Each interval `j` has start, finish, and value. Sort by finish time. Let `p(j)` be the largest earlier index whose finish is at most `start[j]`, found by binary search. Define `OPT(j)` as maximum value using intervals `1..j`:

$$OPT(j)=\max(OPT(j-1),\ value_j+OPT(p(j))).$$

```cpp
for (int j=1; j<=n; ++j)
    dp[j]=max(dp[j-1], jobs[j].value + dp[p[j]]);
```

The two cases are exhaustive: an optimum excludes `j`, or includes it and can then use only compatible intervals up through `p(j)`. Sorting and all binary searches cost $O(n\log n)$; DP is $O(n)$. Store the chosen branch to reconstruct the schedule.

Unweighted activity selection is greedy; adding weights breaks the earliest-finish greedy proof and leads to DP.

## 14.8 Subset sum

Question: can some subset of positive integers sum exactly to target $S$? Define `possible[s]` and update downward per item:

```cpp
vector<char> possible(S+1,false);
possible[0]=true;
for (int x:a)
    for (int s=S; s>=x; --s)
        possible[s] = possible[s] || possible[s-x];
```

Time is $O(nS)$, space $O(S)$, pseudo-polynomial. Downward order enforces 0/1 use. With negative elements or huge targets, this table design needs modification.

## 14.9 Kadane's maximum-subarray DP

Define `bestEnd[i]` as the maximum sum of a nonempty subarray ending exactly at `i`:

$$bestEnd[i]=\max(a[i],a[i]+bestEnd[i-1]).$$

The global answer is the maximum of all `bestEnd[i]`.

```cpp
long long kadane(const vector<int>& a) {
    if (a.empty()) throw invalid_argument("nonempty array required");
    long long ending=a[0], best=a[0];
    for (int i=1;i<(int)a.size();++i) {
        ending=max<long long>(a[i],ending+a[i]);
        best=max(best,ending);
    }
    return best;
}
```

At index `i`, a best ending subarray either starts at `i` or extends the best one ending at `i-1`; no other start can do better. Time is $O(n)$ and auxiliary space $O(1)$. Initializing to `0` incorrectly permits the empty subarray on all-negative input.

## 14.10 Edit distance

Levenshtein distance is the minimum number of unit-cost insertions, deletions, and substitutions needed to transform one string into another. Define

$$dp[i][j]=\text{distance from }A[0..i)\text{ to }B[0..j).$$

Base cases: transforming a length-$i$ string to empty needs $i$ deletions; transforming empty to length $j$ needs $j$ insertions.

$$
dp[i][j]=
\begin{cases}
dp[i-1][j-1],&A[i-1]=B[j-1],\\
1+\min(dp[i-1][j],dp[i][j-1],dp[i-1][j-1]),&A[i-1]\ne B[j-1].
\end{cases}
$$

The three mismatching-character predecessors mean delete from `A`, insert into `A`, or substitute.

```cpp
int editDistance(const string& A,const string& B) {
    int n=A.size(),m=B.size();
    vector<vector<int>> dp(n+1,vector<int>(m+1));
    for(int i=0;i<=n;++i) dp[i][0]=i;
    for(int j=0;j<=m;++j) dp[0][j]=j;
    for(int i=1;i<=n;++i) {
        for(int j=1;j<=m;++j) {
            if(A[i-1]==B[j-1]) dp[i][j]=dp[i-1][j-1];
            else dp[i][j]=1+min({dp[i-1][j],dp[i][j-1],dp[i-1][j-1]});
        }
    }
    return dp[n][m];
}
```

Example `kitten -> sitting` has distance 3: substitute `k->s`, substitute `e->i`, insert `g`. The 22-page image scan derives exactly this "compare last characters" recurrence using alignment pictures.

Time and table space are $O(nm)$. Two rows reduce value-only space to $O(m)$. Different operation costs simply replace the added `1` values; allowing transposition produces a different distance.

## 14.11 Matrix-chain multiplication

Matrices are fixed in order but may be parenthesized differently. If matrix $A_i$ has dimensions $p_{i-1}\times p_i$, multiplying a chain split at $k$ costs:

- optimal cost for $A_i\cdots A_k$;
- optimal cost for $A_{k+1}\cdots A_j$;
- $p_{i-1}p_kp_j$ scalar multiplications to multiply the two results.

Define $m[i][j]$ as minimum scalar multiplications for $A_i\cdots A_j$:

$$
m[i][i]=0,
\qquad
m[i][j]=\min_{i\le k<j}
\{m[i][k]+m[k+1][j]+p_{i-1}p_kp_j\}.
$$

```cpp
pair<long long,vector<vector<int>>> matrixChain(const vector<int>& p) {
    int n=p.size()-1;
    const long long INF=LLONG_MAX/4;
    vector<vector<long long>> m(n+1,vector<long long>(n+1));
    vector<vector<int>> split(n+1,vector<int>(n+1,-1));

    for(int len=2;len<=n;++len) {
        for(int i=1;i+len-1<=n;++i) {
            int j=i+len-1;
            m[i][j]=INF;
            for(int k=i;k<j;++k) {
                long long q=m[i][k]+m[k+1][j]+1LL*p[i-1]*p[k]*p[j];
                if(q<m[i][j]) { m[i][j]=q; split[i][j]=k; }
            }
        }
    }
    return {m[1][n],split};
}

void printParens(const vector<vector<int>>& s,int i,int j) {
    if(i==j) { cout<<"A"<<i; return; }
    cout<<"(";
    printParens(s,i,s[i][j]);
    printParens(s,s[i][j]+1,j);
    cout<<")";
}
```

There are $O(n^2)$ interval states and up to $O(n)$ split choices per state, giving $O(n^3)$ time and $O(n^2)$ space.

Worked contrast: dimensions `[10,30,5,60]`.

```text
(A1 A2) A3: 10*30*5 + 10*5*60 = 4,500
A1 (A2 A3): 30*5*60 + 10*30*60 = 27,000
```

Matrix multiplication is associative in result but not in computational cost. The split table reconstructs the optimal parentheses.

## 14.12 Memoization versus tabulation

| Point | Memoization | Tabulation |
|---|---|---|
| Direction | top down | bottom up |
| States | only reached states | usually all table states |
| Dependencies | implicit through recursion | must choose valid order |
| Overhead | function calls/stack | loops, often better locality |
| Reconstruction | store choices | store choices |

Both implement the same recurrence. A memoized algorithm is not automatically polynomial: count the number of distinct states and work per state.

---

# 15. Viva delivery, whiteboard scripts, comparisons, and traps

## 15.1 The pigeonhole principle -- a solid answer

**Basic principle:** if more than $k$ objects are placed into $k$ boxes, some box contains at least two objects.

**Generalized form:** if $N$ objects are placed into $k$ boxes, some box contains at least

$$\left\lceil\frac Nk\right\rceil$$

objects.

This is an existence theorem: it proves that a collision or concentration **must** occur, but does not identify which box.

### Three defensible applications

1. **Circular queue state representation:** an $n$-cell array queue has $n+1$ logical sizes but, for a fixed front, only $n$ rear positions. Two sizes must share a representation unless we reserve a cell or store an extra count/full bit. This directly justifies the lecture design.
2. **Hash collision:** an $m$-bit hash has only $2^m$ possible outputs. Among $2^m+1$ distinct inputs, at least two necessarily have the same output. This does not mean cryptographic collision search is easy; it proves collisions exist because the input domain is larger.
3. **Capacity planning:** assigning $N$ jobs to $k$ identical servers forces at least one server to receive at least $\lceil N/k\rceil$ jobs. This gives an unavoidable lower bound on maximum load, regardless of scheduling cleverness.

**Board answer:** "Objects are pigeons and categories are holes. With 13 people and 12 birth months, two share a birth month. In DSA, a circular queue gives a stronger use: $n+1$ possible occupancies cannot be encoded by only $n$ rear positions for fixed front, so empty and full collide unless we add state."

**Trap:** the principle says "at least one," not "exactly one," and it requires mapping every object to a defined box.

## 15.2 Whiteboard narration template

When asked to teach an algorithm, speak while writing:

1. "My input is ..., my output is ..., and I assume ... ."
2. Draw a six-element example and name the state variables.
3. State one invariant/recurrence before code.
4. Write the base/empty/error case first.
5. Trace one important update and one edge case.
6. Count operations from the structure: levels, vertices plus edges, shifts, or DP states times transitions.
7. State alternatives and when the chosen method fails.

### Example: teach a function using sum from 1 to n

Motivation: if the same calculation is needed from several places, copying the loop repeats logic and invites inconsistent fixes. A function names a reusable contract.

```cpp
long long sumTo(int n) {
    long long total=0;
    for(int x=1;x<=n;++x) total+=x;
    return total;
}
```

Explain parameter `n`, local state `total`, returned result, and precondition `n>=0`. Then call `sumTo(5)` and trace `0,1,3,6,10,15`. Mention the closed form only after the function concept is clear.

## 15.3 Required board algorithms

Be able to write these from memory:

- binary search with one interval convention;
- array insert/remove and linked-list insert/delete;
- stack push/pop and circular queue enqueue/dequeue;
- tree traversals and node count;
- BST search/insert/delete plus predecessor/successor;
- heapify, build-heap, and the $O(n)$ proof;
- BFS, DFS, bipartite coloring;
- merge sort, quicksort partition, inversion count;
- activity selection and fractional knapsack;
- 0/1 knapsack, LCS, edit distance, coin change, Kadane, matrix chain.

For each, test empty input, one element, duplicates, boundary indices, and all-negative/all-unreachable cases where relevant.

## 15.4 High-frequency comparisons

### Array versus linked list

Array: contiguous, constant-time indexing, strong locality, costly middle shifts. Linked: scattered nodes, sequential access, pointer overhead, constant-time rewiring only with the right pointer already known.

### Stack versus queue versus priority queue

Stack chooses newest (LIFO); queue chooses oldest (FIFO); priority queue chooses best key. The difference is an access policy, not a specific representation.

### Complete tree versus BST versus heap

Complete describes shape; BST describes global left/right key order; heap combines complete shape with only parent-child order. A tree can satisfy more than one property, but none implies the others in general.

### BFS versus Dijkstra

BFS is sufficient when every edge has equal unit cost. Dijkstra chooses the currently smallest tentative distance via a priority queue and supports nonnegative unequal weights. BFS on weighted edges can return a path with fewer edges but greater total cost.

### Recursion versus iteration

Compare clarity and required state. Both can have the same asymptotic time; recursion uses call-stack depth, iteration may use constant state or an explicit stack. Always state the concrete algorithm.

### Greedy versus DP

Greedy commits to one locally optimal choice and needs a greedy-choice proof. DP evaluates alternative transitions among overlapping states. Fractional knapsack is greedy; 0/1 knapsack is DP because indivisibility breaks the exchange.

### Memoization versus tabulation

Same recurrence, different evaluation order. Memoization is demand-driven; tabulation is explicitly ordered and often easier to compress.

## 15.5 Fast complexity derivations

Do not answer with only the final symbol:

- **Linked-list search:** may inspect every node once $\Rightarrow O(n)$.
- **BST operation:** follows one path $\Rightarrow O(h)$; balanced $O(\log n)$, chain $O(n)$.
- **Heapify:** moves down one root-to-leaf path $\Rightarrow O(\log n)$.
- **Build-heap:** about $n/2^{h+1}$ nodes of height $h$ $\Rightarrow n\sum h/2^{h+1}=O(n)$.
- **BFS/DFS:** each vertex initialized once and adjacency entry scanned once $\Rightarrow O(V+E)$.
- **Merge sort:** $\log n$ levels times $n$ merge work per level $\Rightarrow O(n\log n)$.
- **Quicksort:** partition is linear; balanced recursion $O(n\log n)$, extreme pivot chain $O(n^2)$.
- **DP:** number of states times transitions; LCS has $nm$ states and $O(1)$ transition $\Rightarrow O(nm)$.
- **Edmonds-Karp is not in these DSA-I sources:** do not mix it into a source-specific answer; its familiar $O(VE^2)$ belongs to later graph material.

## 15.6 Common traps with corrected answers

1. **"A BST search is always $O(\log n)$."** False; it is $O(h)$ and can be $O(n)$ without balancing.
2. **"A heap is sorted."** False; only parent-child order is guaranteed.
3. **"Build-heap calls heapify $n$ times, so it is $n\log n$."** That is loose; most nodes have tiny height, giving $\Theta(n)$.
4. **"Deleting a linked node is $O(1)$."** Only if the needed node/predecessor is already available.
5. **"Nested loops mean $n^2$."** Count ranges; doubling loops give logarithms and triangular loops give sums.
6. **"BFS gives shortest paths."** Only minimum-edge paths in unweighted/equal-weight graphs.
7. **"Visited neighbor means a cycle."** Not without directed colors or undirected parent handling.
8. **"Bipartite BFS from vertex 0 checks the graph."** Only its component; loop over components.
9. **"Greedy by value/weight solves every knapsack."** It solves fractional, not general 0/1.
10. **"DP is automatically polynomial."** Knapsack $O(nW)$ is pseudo-polynomial; count input encoding size.
11. **"Quicksort is always $n\log n$."** Average/expected yes under suitable pivots; worst case $n^2$.
12. **"Inorder traversal is sorted for every binary tree."** Only for a BST with a consistent duplicate rule.
13. **"Queue front equals rear means empty."** It is ambiguous with full unless one slot or extra state is used.
14. **"Amortized means probability average."** No; it bounds every operation sequence in aggregate.
15. **"Closest pair is $n\log n$ even if I sort the strip at every recursion."** That shown variant is $n\log^2 n$; preserve y-order for $n\log n$.
16. **"Edit distance mismatch always means substitution."** Insertion and deletion can be better; take the minimum of three predecessor states.
17. **"0/1 knapsack can update capacity upward."** Upward reuse changes it into unbounded knapsack.

## 15.7 Rapid oral drill

**What is an invariant?** A property true at a defined point before and after every iteration; initialization, maintenance, and termination turn it into a correctness proof.

**Why is array access $O(1)$?** Address equals base plus `index * elementSize`, a constant number of arithmetic/memory operations under the RAM model.

**Why is linked-list indexing not $O(1)$?** A node has no address formula for its $k$-th successor; links must be followed sequentially.

**Why does a sentinel help?** It represents a boundary as an ordinary node, reducing empty/front special cases and strengthening invariants.

**Why mark BFS visited on enqueue?** It prevents the same vertex entering the queue through several frontier edges.

**Can DFS find shortest paths?** Not generally; its first path depends on adjacency order and need not use fewest edges.

**Why is a tree with $n$ vertices and connectedness guaranteed to have at least $n-1$ edges?** Each new vertex needs an edge to join the existing connected component; a tree reaches the lower bound without cycles.

**Why is heap arbitrary search $O(n)$?** If the key is below the root bound, either child may contain it; heap order does not choose one search branch.

**What is stable sorting useful for?** Sort by a secondary field first and then stably by a primary field; equal primary keys retain secondary order.

**What is optimal substructure?** An optimal solution contains optimal solutions to the subproblems induced by its decisions; otherwise substituting a better subsolution would improve it.

**What is the difference between subsequence and substring/subarray?** A subsequence may skip positions but preserves order; a substring/subarray is contiguous.

## 15.8 Self-test prompts

Answer aloud, then check the relevant section:

1. Derive all four 0-based heap index formulas and build a max-heap from `[4,1,3,2,16,9,10,14,8,7]`.
2. Delete a BST node having two children and prove the promoted successor has no left child.
3. Give a graph where DFS fails to find a minimum-edge path.
4. Give an odd cycle and trace bipartite coloring until conflict.
5. Show why geometric resizing is amortized constant but fixed-increment resizing is not.
6. Count inversions in `[3,1,2,5,4]` during merge.
7. Give a density-greedy counterexample for 0/1 knapsack and explain why fractional exchange works.
8. Fill the LCS table for `ABC` and `BAC`; reconstruct both possible length-2 answers.
9. Fill edit-distance rows for `cat` and `cut` and name the selected operation.
10. Explain the circular-queue empty/full ambiguity using pigeonhole principle, not only an implementation diagram.

---

# 16. Current local-source coverage and correction ledger

## 16.1 Current four-source coverage: 523 pages

| Current source | Pages | Material incorporated here |
|---|---:|---|
| `Algorithms.pdf` | 219 | min/max, maximum subarray, merge/quick sort, recurrences, activity selection, knapsack distinction, Fibonacci, LCS, coin change, 0/1 knapsack, and matrix-chain multiplication |
| `Dsa bayezid sir.pdf` | 22 | visually inspected handwritten treatment of heaps/PQ, greedy selection, divide-and-conquer, recurrence/DP examples, weighted intervals, Kadane, edit distance, and Karatsuba |
| `DSA Merged Part1.pdf` | 254 | asymptotic analysis, lists, stacks, queues, trees/BSTs, heaps, graph representation, BFS/DFS, and the main state/trace diagrams |
| `DSA_note_by_Promi.pdf` | 28 | compact code/derivation cross-check for structures, traversal, heap, greedy, divide-and-conquer, and DP |
| **Total** | **523** | current reduced source set |

The four PDFs overlap substantially. The page total records the files actually present; it is not a claim of 523 unique lecture topics.

## 16.2 Corrections and deliberate clarifications

The aim is to remember course content **correctly**, not reproduce accidental slide errors.

| Source issue | Correct treatment in this book |
|---|---|
| Bipartite slide starts from one source | outer loop checks every connected component |
| Queue `clear` snippet/diagram has inconsistent pointer handling | re-establish exactly one sentinel; rear points to it when empty |
| Span pseudocode rendering has an ambiguous `i-j` expression | distance is `i - stack.top()` after popping smaller/equal prices |
| Some heapify snippets make the final swap/recursion visually ambiguous | swap and continue only if the selected child differs from the current node |
| A note's naive DFS cycle test treats any visited neighbor as a cycle | directed DFS uses gray back edges; undirected DFS excludes the parent edge |
| A note suggests a DFS route for lexicographically smallest topological order | Kahn's algorithm with a min-heap gives the direct guarantee |
| Repeated-height balance check is described too cheaply | naive repeated heights can be $O(n^2)$; fused postorder is $O(n)$ |
| Fractional-knapsack proof notation mixes amount/fraction in a line | exchange an equal **weight** $\epsilon$ from lower to higher density |
| Closest-pair sources show two combine implementations | re-sorting per level is $\Theta(n\log^2n)$; maintaining y-order is $\Theta(n\log n)$ |
| Height terminology varies across texts | this book declares edge height: leaf 0, empty tree -1, and flags the convention |

## 16.3 Deliberately absent from this DSA-I volume

Red-black rotations, AVL rotations, MST, Dijkstra, Bellman-Ford, max flow, string matching, hashing, disjoint sets, and complexity classes do not appear as taught topics in the audited DSA-I source set. Some belong to DSA-II or other volumes. The BST slides only state why balance is desirable. Keeping that boundary prevents a long generic note from crowding out the material actually in the academic slides.

---

## Final 60-second DSA-I answer shape

For almost any question, answer in this order:

> "The structure/algorithm is ... . Its representation or state is ... . The invariant is ... . On this example, the next step is ... . Each element/node/state is processed ... times, so time is ... and extra space is ... . The important edge case or alternative is ... ."

That shape demonstrates understanding, proof awareness, implementation ability, and engineering judgment--not just memorized terminology.

<!-- DSA1_END -->
