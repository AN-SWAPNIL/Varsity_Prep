# Bismillah.

# Last-Day Recall, Reported Questions, and Mock Vivas

This is the retrieval layer, not a replacement for the subject chapters. Say each answer aloud, draw the marked diagrams, and then follow the cross-reference when an answer feels weak.

---

# 1. Two questions that must never fail again

## 1.1 Bias–variance decomposition

Assume

$$
Y=f(x)+\varepsilon,\qquad \mathbb E[\varepsilon]=0,
\qquad \operatorname{Var}(\varepsilon)=\sigma^2.
$$

The fitted model `f_hat_D(x)` depends on random training set `D`. For squared prediction error at a fixed `x`:

$$
\boxed{
\mathbb E_{D,\varepsilon}
[(Y-\hat f_D(x))^2]
=
\sigma^2+
(\mathbb E_D[\hat f_D(x)]-f(x))^2+
\mathbb E_D[(\hat f_D(x)-\mathbb E_D[\hat f_D(x)])^2]
}
$$

or

$$
\boxed{\text{expected test MSE}=\text{irreducible noise}+\text{bias}^2+\text{variance}.}
$$

- **Bias:** systematic difference between the average learned prediction and the true regression function.
- **Variance:** sensitivity of the learned prediction to which training sample was used.
- **Noise:** randomness in the target that cannot be removed from the supplied features.

Underfitting/overfitting are **learning behaviors**, not alternate names for bias/variance:

- underfitting often has high bias and both training/test error high;
- overfitting often has high variance, very low training error, and a large generalization gap;
- the mapping is typical, not a definition or strict equivalence.

### Board derivation

Let `m(x)=E_D[f_hat_D(x)]`. Add and subtract `m(x)` and use zero-mean cross terms:

$$
Y-\hat f=(f-m)+(m-\hat f)+\varepsilon.
$$

Squaring and taking expectation gives:

$$
(f-m)^2+\mathbb E_D[(\hat f-m)^2]+\mathbb E[\varepsilon^2].
$$

That is bias squared, variance, and noise.

### One concrete example

Repeatedly fit models to different samples from a curved true relationship:

- a straight line misses the curve similarly each time: high bias, low variance;
- a high-degree polynomial follows each sample’s noise differently: lower training bias but high variance;
- a regularized intermediate model may minimize test error.

More data primarily reduces variance. More expressive features may reduce bias but increase variance. Stronger regularization generally raises bias and lowers variance.

## 1.2 Pigeonhole principle

**Basic form:** placing `n+1` objects into `n` boxes forces some box to contain at least two objects.

**Generalized form:** placing `N` objects into `k` boxes forces some box to contain at least

$$
\boxed{\left\lceil\frac Nk\right\rceil}
$$

objects.

### Proof

If every box held at most `ceil(N/k)-1`, the total would be at most

$$
k(\lceil N/k\rceil-1)<N,
$$

contradicting that `N` objects were placed.

### Solid computing use case: hash collisions

A hash function maps a much larger key universe to `m` table indices:

$$
h:U\to\{0,1,\dots,m-1\}.
$$

If more than `m` distinct keys are stored, at least two must map to the same bucket. More generally, among `N` keys some bucket has at least `ceil(N/m)` keys. Therefore collisions are mathematically unavoidable; chaining or probing is required. A good hash distributes collisions—it cannot eliminate them for an unbounded/larger universe.

Other concrete examples:

- among 367 people, two share a birthday even including leap day;
- among `n+1` integers, two have the same remainder modulo `n`;
- a lossless compressor cannot make every possible `n`-bit file shorter, because there are fewer shorter bit strings than input strings;
- if `N` processes are assigned to `k` identical servers, some server receives at least `ceil(N/k)` processes.

When asked for a use case, identify objects, boxes, and the forced conclusion explicitly.

---

# 2. Reported BRACU questions — direct answers

## 2.1 Networking and security

**NAT:** Network Address Translation rewrites address/port fields between address realms, commonly allowing many private hosts to share one public IPv4 address through port mapping. It conserves public IPv4 space but breaks end-to-end addressing and complicates inbound connections, protocols carrying addresses, and some security designs.

**TCP:** Transmission Control Protocol. Connection-oriented reliable ordered byte stream, using sequence numbers, acknowledgments, retransmission, checksum, flow control, and congestion control.

**UDP:** User Datagram Protocol. Connectionless message-oriented best-effort delivery with checksum and ports but no built-in ordering, retransmission, flow control, or congestion control.

**Which is faster?** UDP has less built-in setup/state/overhead, so it can have lower latency. That does not guarantee an application finishes faster: applications needing reliability may have to rebuild TCP-like mechanisms. Compare requirements, not slogans.

**UDP examples:** DNS queries, DHCP, real-time media, gaming, and QUIC’s transport substrate. Modern DNS may also use TCP/DoT/DoH; one example does not mean exclusive use.

**SYN:** synchronize sequence numbers and request/create TCP connection state.

**ACK:** acknowledgment flag; the acknowledgment number means “the next byte sequence number I expect,” cumulatively acknowledging earlier bytes.

```text
client                         server
SYN, seq=x        ---------->
                  <---------- SYN+ACK, seq=y, ack=x+1
ACK, ack=y+1      ---------->
```

**Flow control:** prevents a fast sender from overflowing the receiver. TCP’s advertised receive window `rwnd` reflects receiver buffer capacity.

**Congestion control:** prevents excessive traffic from overloading the network. TCP controls congestion window `cwnd` using feedback such as ACKs, delay/loss, slow start, congestion avoidance, and recovery. Effective outstanding data is bounded roughly by

$$
\min(rwnd,cwnd).
$$

**DHCP:** Dynamic Host Configuration Protocol supplies configuration such as IP address, prefix mask, default gateway, DNS server, and lease time. Classic DORA:

```text
DISCOVER -> OFFER -> REQUEST -> ACK
```

It normally uses UDP ports 68 (client) and 67 (server). Relay agents carry messages across routed networks. A lease is temporary; renewal avoids address conflicts and recovers unused addresses.

**IPv4 versus IPv6:** 32-bit versus 128-bit addresses; dotted decimal versus hexadecimal colon notation; IPv6 removes router fragmentation and header checksum, has a simpler fixed base header plus extension headers, uses Neighbor Discovery rather than ARP, supports address autoconfiguration, and uses multicast rather than broadcast. Security is not automatic merely because IPv6 exists.

**TLS:** Transport Layer Security establishes an authenticated, encrypted, integrity-protected channel over a transport such as TCP. In a typical modern handshake the client and server negotiate parameters, exchange ephemeral key material, the server proves identity using a certificate/signature, both derive symmetric traffic keys, and Finished messages authenticate the transcript. TLS protects data in transit, not a compromised endpoint or plaintext after decryption. HTTPS is HTTP over TLS.

**CIA triad:** **confidentiality** means unauthorized parties cannot read the data; **integrity** means unauthorized or undetected modification is prevented/detectable; **availability** means authorized users can obtain the service/data when needed. Typical controls are encryption and access control for confidentiality, hashes/MACs/signatures plus authorization and audit for integrity, and redundancy/backups/failover/rate limiting/incident recovery for availability. One control can support several properties, but encryption alone does not guarantee integrity or availability.

**Confidentiality:** ensure only authorized parties can read information through access control, encryption in transit/at rest, sound key management, least privilege, secure deletion/backup, and endpoint hardening. Encryption without protecting keys does not ensure confidentiality.

**Files on your system:** use OS permissions/ACLs, full-disk encryption for stolen-device risk, file/container encryption for finer isolation, separate accounts, MFA where relevant, encrypted backups, key recovery/rotation, locking and patching, and audit access. Full-disk encryption is weakest after the machine is unlocked and compromised.

**Encrypt database entries?** Use layered, risk-based protection. TLS protects transit; disk/TDE protects stolen media/backups; field/application-level encryption protects selected sensitive columns from broader DB/storage access. Passwords should be salted and hashed with a password KDF, not reversibly encrypted. Encryption harms search/index/range operations and complicates rotation; do not encrypt blindly.

**FDM versus TDM:** Frequency Division Multiplexing gives users simultaneous non-overlapping frequency bands and needs guard bands/filters. Time Division Multiplexing gives users recurring time slots on a shared channel and needs synchronization; statistical TDM assigns slots on demand. Neither is universally better—choose by traffic, channel, synchronization, latency, and hardware.

## 2.2 DSA and discrete

**Recursion:** a function solves a problem using smaller instances of the same problem. It needs base case, progress toward base, and correct combination of subresults.

```cpp
long long sum(long long n) {
    if (n == 0) return 0;
    return n + sum(n - 1);
}
```

For this example: recurrence `T(n)=T(n-1)+Θ(1)=Θ(n)`, call-stack space `Θ(n)`. The loop version uses `Θ(1)` auxiliary space, and the closed form `n(n+1)/2` uses `Θ(1)` time under fixed-width arithmetic. Recursion is better when it mirrors recursive structure and remains safe/readable; iteration is often better for simple linear repetition and avoids stack overflow. “One is always better” is wrong.

**Function motivation for freshers:** show duplicated summation code for several `n`; name the reusable idea `sumTo(n)`; explain input, output, contract, call, return, reuse, testing, and abstraction. First implement with their known loop, trace `sumTo(5)`, then separate caller from callee.

**Search in a list:** unsorted list requires linear search `O(n)` worst case; sorted random-access array permits binary search `O(log n)`; repeated equality queries may justify a hash table with expected `O(1)` lookup; ordered predecessor/range queries favor a balanced BST.

**Build heap in `O(n)`:** put the array in complete-tree order and call `siftDown` from the last internal node to the root. Although one sift can cost `O(log n)`, most nodes are near leaves. At height `h` there are at most `n/2^{h+1}` nodes, so

$$
T(n)\le \sum_{h\ge0}\frac{n}{2^{h+1}}O(h)=O(n).
$$

Repeated insertion is `O(n log n)`; bottom-up heapify is `Θ(n)`.

**BST predecessor:** largest key smaller than `x`. If `x` has a left subtree, take its maximum; otherwise climb until moving up from a right child.

**BST successor:** smallest key larger than `x`. If `x` has a right subtree, take its minimum; otherwise climb until moving up from a left child.

Example BST:

```text
        20
       /  \
     10    30
    / \    / \
   5  15  25 40
```

Predecessor of 20 is 15; successor is 25. Predecessor of 15 is 10; successor of 15 is 20. Minimum has no predecessor and maximum has no successor.

**Red-black tree:** BST plus color invariants: root black, NIL leaves black, no red node has a red child, and every path from a node to descendant NIL has equal black height. These imply height `O(log n)`. Rotations preserve inorder order and locally restructure links; recoloring/rotations restore invariants after insert/delete.

```text
right rotate at y:              left rotate at x:
      y          x                   x          y
     / \        / \                 / \        / \
    x   C  ->  A   y               A   y  ->  x   C
   / \            / \                 / \    / \
  A   B          B   C               B   C  A   B
```

For insertion, insert red, then repair red-red conflict using uncle color: red uncle → recolor and move upward; black uncle → rotate triangle into a line, rotate grandparent, recolor. Deletion repairs a black-height deficit with sibling/near/far-nephew cases.

**Edmonds–Karp:** Ford–Fulkerson using BFS to find a shortest-in-edge-count augmenting path in the residual graph. Each BFS costs `O(E)`. A critical residual edge’s shortest-level distance strictly increases before it can become critical again, so there are `O(VE)` augmentations. Total:

$$
O(E)\cdot O(VE)=O(VE^2).
$$

Residual reverse edges allow cancellation/rerouting. At termination, no `s-t` residual path exists and the reachable/nonreachable cut certifies maximum flow by max-flow min-cut.

**Pigeonhole:** use the formal statements and hash-table example in §1.2.

## 2.3 AI and ML

**A\*:** evaluates `f(n)=g(n)+h(n)`. Tree-search optimality typically requires admissible `h`; graph-search without reopening usually requires consistency. If `h(n)=0`, A* becomes uniform-cost search, equivalent to Dijkstra under nonnegative edge costs. It remains optimal under those assumptions but explores without heuristic guidance.

**Minimax at infinite depth:** for a finite deterministic zero-sum perfect-information game, a complete exact tree and correct terminal utilities yield optimal play. A human cannot obtain a better game-theoretic outcome against the optimal agent, though the human may draw or also achieve the optimal outcome. “Infinite amount of depth” is ill-posed for a finite game; games with infinite state/play require additional assumptions about utility, termination, and computability.

**Bias–variance:** state the equation in §1.1. Do not say only “bias is underfitting and variance is overfitting.”

**Vision Transformer:** split image into patches, linearly embed them, add positional information, and process token sequence with transformer attention; a class token or pooled representation supports classification. Attention gives global interactions but naive cost is quadratic in token count.

**Mamba:** a selective state-space sequence model family designed for linear-time sequence processing, using input-dependent state updates/selective scanning rather than full quadratic self-attention. If you have not worked with it, say so and explain only the high-level distinction.

## 2.4 OOP and Java

**Polymorphism:** one interface/reference can represent objects of different concrete types, and the selected behavior depends on the actual object for overridden instance methods. Compile-time polymorphism includes overloading; runtime subtype polymorphism uses overriding/dynamic dispatch.

**Early versus late binding:** overloaded/static/private/final method selection is determined statically where applicable; overridden instance method dispatch is determined at runtime from the object’s dynamic type.

**Equality:** Java `==` compares primitive values or reference identity. `equals` represents logical equality when overridden. Equal objects must have equal `hashCode`; this is required for `HashMap`/`HashSet`. Use null-safe `Objects.equals` where appropriate.

**Exceptions:** checked exceptions must be caught or declared; unchecked `RuntimeException` commonly signals programming/precondition failures. `throw` creates/raises an exception; `throws` declares possibility. `finally` normally runs during exit; try-with-resources closes `AutoCloseable` resources and preserves suppressed exceptions.

**Generics:** provide compile-time type safety and reuse. Java generics use erasure, so `new T()`, `T.class`, generic arrays, and `instanceof List<String>` are restricted. PECS: producer extends, consumer super.

**Collections and sorting:**

```java
Collections.sort(names);                     // natural order
names.sort(Comparator.reverseOrder());       // reverse order
students.sort(Comparator
    .comparingInt(Student::getScore)
    .reversed()
    .thenComparing(Student::getName));
```

`List` is ordered and allows duplicates; `Set` enforces uniqueness; `Map` maps unique keys to values; `Queue/Deque` model processing order. `ArrayList` gives `O(1)` random access and amortized append; linked lists do not make indexed access fast; `HashMap` expected `O(1)` equality lookup; `TreeMap` `O(log n)` ordered operations.

## 2.5 OS, DBMS, and hardware

**Multilevel feedback queue:** multiple ready queues with different priorities/time quanta; new/interactive jobs start high, CPU-heavy jobs are demoted, and periodic priority boost/aging prevents starvation. It approximates shortest-job behavior from observed CPU bursts without knowing them in advance.

**Cache purpose:** exploit temporal and spatial locality to reduce average access time. It improves average latency/throughput; it does not make main memory physically faster.

**Microprocessor versus microcontroller:** a microprocessor emphasizes a CPU and often relies on external memory/peripherals; a microcontroller integrates CPU, flash/RAM, GPIO, timers, ADC, and communication peripherals for embedded control. Integration, simpler cores, modest frequency/memory, mature process nodes, low component/PCB cost, and volume often make MCU systems cheap. “Every MCU is cheaper than every MPU” is false.

**Four-stage ripple counter at 32 kHz:** each actual toggle flip-flop divides by 2:

```text
Q1=16 kHz, Q2=8 kHz, Q3=4 kHz, Q4=2 kHz
```

Therefore the fourth flip-flop output is 2 kHz under ordinary stage numbering. The reported 4 kHz answer corresponds to the third output or counts the input as a stage. Draw and label before answering.

**ACID:** atomicity, consistency, isolation, durability. Consistency is application/database invariants, not the same as replica consistency.

**Normalization:** use functional dependencies to reduce anomalies. 3NF permits a dependency `X→A` when `X` is a superkey or `A` is prime; BCNF requires every nontrivial determinant `X` to be a superkey. Decomposition should be lossless; dependency preservation is desirable.

**B+ tree versus hash index:** B+ tree supports equality, range, ordering, and logarithmic search; hash excels at expected equality lookup but does not preserve order. Index choice depends on query workload and maintenance/storage cost.

## 2.6 Data Communication

**Sampling theorem:** for a signal band-limited to `B` Hz, sample above `2B` samples/s for ideal reconstruction. Sampling below this lets spectral replicas overlap, causing aliasing; an anti-alias low-pass filter is used before sampling.

**PCM:** filter → sample → quantize → binary encode. With `L=2^n` levels and sampling rate `f_s`,

$$R_b=nf_s,\qquad \Delta=\frac{V_{\max}-V_{\min}}{L},\qquad
P_q\approx\frac{\Delta^2}{12}.$$

**Line coding:** NRZ is bandwidth-efficient but long unchanged runs hurt clock recovery/DC behavior. Manchester always has a mid-bit transition and self-clocks but needs more signaling bandwidth. AMI alternates the polarity of `1`s and has no DC but long zero runs; B8ZS/HDB3 replace zero runs with recognizable violations.

**AM/FM:** conventional AM is $A_c[1+\mu m_n(t)]\cos(2\pi f_ct)$; require $\mu\le1$ for ordinary envelope detection, and bandwidth is $2B_m$. FM has $f_i(t)=f_c+k_fm(t)$ and Carson bandwidth $2(\Delta f+B_m)$. AM varies amplitude; FM keeps a constant envelope and varies instantaneous frequency, usually trading more bandwidth for noise robustness.

**Nyquist versus Shannon:** noiseless symbol/level limit:

$$C=2B\log_2M.$$

Noisy information-capacity ceiling:

$$C=B\log_2(1+S/N).$$

They answer different questions; a real design must respect both.

## 2.7 TOC and Compiler

**Regular versus context-free:** a finite automaton has finite memory and recognizes regular languages; a PDA adds a stack and recognizes CFLs. `0^n1^n` is context-free but not regular; `a^n b^n c^n` is not context-free.

**Pumping lemma warning:** it gives a necessary property of regular/CFL languages and is mainly used by contradiction to prove nonmembership. Satisfying it does not prove regularity/context-freeness.

**Compiler phases:** characters → lexer/tokens → parser/AST → semantic analysis/types/bindings → IR/TAC → optimization → instruction selection/register allocation → target code. Symbol table and error handling support several phases.

**FIRST/FOLLOW and LL(1):** `FIRST(α)` says which terminals can begin strings from `α`; `FOLLOW(A)` says what can immediately follow `A`. Fill `M[A,a]` from `FIRST(RHS)` and, for nullable RHS, `FOLLOW(A)`. Multiple productions in one cell are a conflict.

**LR versus LL:** LL predicts a leftmost derivation top-down; LR recognizes handles and constructs a rightmost derivation in reverse bottom-up. LR accepts a larger practical grammar class. SLR uses LR(0) states plus global FOLLOW sets; canonical LR(1) has item-specific lookaheads; LALR merges equal LR(0) cores.

**Liveness:** backward equations:

$$OUT[B]=\bigcup_{S\in succ(B)}IN[S],\qquad
IN[B]=USE[B]\cup(OUT[B]-DEF[B]).$$

Overlapping live ranges interfere and cannot share a register; graph-coloring allocation assigns registers and spills when necessary.

## 2.8 Deeper security and hardware

**OTP:** `C=M xor K` is perfectly secret only when the key is uniform, message-length, secret, and never reused. Reuse reveals `C1 xor C2 = M1 xor M2`; OTP also does not authenticate.

**ECB/CBC/CTR/GCM:** ECB leaks equal-block patterns. CBC needs an unpredictable fresh IV and authentication. CTR needs a never-reused nonce/counter and authentication. GCM is AEAD but nonce reuse can break both confidentiality and tags.

**DH:** Alice sends `g^a`, Bob `g^b`, both derive `g^(ab)`. Unauthenticated DH is vulnerable to MITM; certificates/signatures/PSK authenticate it. Ephemeral DH gives forward secrecy.

**DNSSEC versus DoT/DoH:** DNSSEC signs DNS data and builds a DS/DNSKEY/RRSIG chain of trust; it does not hide queries. DoT/DoH encrypt client-to-resolver transport but shift trust to that resolver.

**MIPS branch target:** `PC+4+(sign-extended immediate << 2)`. A classic load-use dependency needs one stall even with forwarding because load data appears after MEM.

**8086 address:** physical address = `(segment << 4) + offset`; `1234h:5678h = 179B8h`. `CALL` saves return state; `RET` restores it; an interrupt vector `n` starts at byte address `4n` in the IVT.

**ATmega32 GPIO/timer:** `DDRx` chooses direction, `PORTx` writes output or enables pull-up, `PINx` reads. In CTC:

$$OCR=\frac{f_{CPU}}{Nf_{interrupt}}-1.$$

---

# 3. Formula and invariant sweep

## 3.1 DSA

- binary search: `O(log n)`, sorted random-access data;
- merge sort: `Θ(n log n)` time, `Θ(n)` auxiliary array, stable in standard merge;
- quicksort: expected `Θ(n log n)`, worst `Θ(n²)`, typically in-place, not normally stable;
- heap operations: `O(log n)`; peek `O(1)`; bottom-up build `Θ(n)`;
- BFS/DFS adjacency list: `Θ(V+E)`;
- topological order exists iff directed graph is acyclic;
- Kruskal: `O(E log E)` plus near-linear DSU;
- Dijkstra: nonnegative weights; binary heap `O((V+E)log V)`;
- Bellman–Ford: `O(VE)`, detects reachable negative cycle;
- Floyd–Warshall: `Θ(V³)` time, `Θ(V²)` space;
- max-flow conservation for internal `v`: inflow = outflow;
- Edmonds–Karp: `O(VE²)`;
- AVL balance factor in `{-1,0,1}`; height `O(log n)`;
- red-black height at most twice black-height, hence `O(log n)`.

## 3.2 ML/math

- MSE: `n^{-1} Σ(y-y_hat)^2`;
- binary cross-entropy: `-[y log p+(1-y)log(1-p)]`;
- gradient descent: `θ ← θ-η∇J(θ)`;
- Bayes: `P(A|B)=P(B|A)P(A)/P(B)`;
- precision `TP/(TP+FP)`; recall `TP/(TP+FN)`;
- F1 `2PR/(P+R)`;
- entropy `-Σp log p`; information gain = parent impurity − weighted child impurity;
- L2 adds `λ||w||²`; L1 adds `λ||w||₁`;
- bias–variance: noise + bias² + variance;
- generalized pigeonhole: `ceil(N/k)`;
- conditional probability/product rule and independence are distinct.

## 3.3 OS/architecture

- CPU utilization under simple multiprogramming estimate: `1-p^n` when each of `n` processes independently waits with probability `p`;
- turnaround = completion − arrival;
- waiting = turnaround − CPU burst for a simple one-burst model;
- response = first run − arrival;
- effective access time is weighted hit/miss cost;
- AMAT = hit time + miss rate × miss penalty;
- CPU time = instruction count × CPI × clock-cycle time;
- speedup bounded by Amdahl: `1/((1-p)+p/s)`;
- `n`-stage ripple divider output `f/2^n`;
- cache sets = capacity/(block size × associativity);
- page offset bits = `log2(page size)`.
- MIPS branch target = `PC+4+(signext(imm)<<2)`;
- 8086 physical address = `(segment<<4)+offset`;
- AVR CTC `f_interrupt=f_CPU/[N(1+OCR)]`.

## 3.4 Networking/DBMS/security

- IPv4 usable hosts in ordinary subnet: often `2^h-2`, but `/31` point-to-point and `/32` are special;
- transmission delay `L/R`; propagation delay `d/s`;
- bandwidth-delay product = bandwidth × RTT;
- TCP sender window approximately `min(rwnd,cwnd)`;
- conflict serializability iff precedence graph is acyclic;
- two-phase locking: growing phase acquires, shrinking phase releases; strict 2PL holds exclusive locks to commit/abort;
- `X→Y`: equal `X` values imply equal `Y` values;
- relation decomposition lossless when spurious tuples cannot appear after join;
- password storage: unique salt + memory-hard/approved password KDF, never plaintext or plain fast hash;
- authenticated encryption protects confidentiality and integrity but still needs nonce discipline and key management.
- sampling: `f_s>2B`; PCM bit rate `n f_s`;
- Nyquist `2B log2 M`; Shannon `B log2(1+S/N)`;
- CBC `C_i=E_K(P_i xor C_{i-1})`; CTR/GCM nonce must not repeat under a key;
- live variables: `IN=USE union (OUT-DEF)`, `OUT=union successor IN`.

---

# 4. Whiteboard drills

Draw each without notes:

1. recursion call stack for `sum(4)` and its recurrence;
2. BST with predecessor/successor cases;
3. bottom-up heapify and its height-sum proof;
4. AVL LL/LR/RR/RL rotations;
5. one red-black insertion repair;
6. BFS/DFS and topological ordering;
7. Dijkstra relaxations and why a negative edge breaks finalization;
8. residual graph and one Edmonds–Karp augmentation;
9. hash-table collision as pigeonhole application;
10. bias–variance derivation and typical model-complexity curves;
11. function lesson for summing `1..n`;
12. graph motivation using maps, dependencies, and social networks;
13. TCP three-way handshake and sequence/ACK meaning;
14. receiver window versus congestion window;
15. DHCP DORA and NAT mapping;
16. TLS trust/key-establishment/data phases;
17. process state diagram and context switch;
18. MLFQ with demotion and priority boost;
19. paging/TLB/page fault path;
20. deadlock resource-allocation or wait-for graph;
21. ER diagram to normalized relations;
22. precedence graph and serializability;
23. B+ tree leaf/index structure;
24. five-stage pipeline with forwarding/stall/flush;
25. cache tag/index/offset split;
26. ripple counter frequency chain;
27. Moore versus Mealy state machine;
28. Matter commissioning from PASE to CASE;
29. graphics model/view/projection pipeline;
30. ray–sphere or line-clipping calculation.

---

# 5. Three-day compression plan

## Day 1 — strongest identity

- DSA I/II: explain invariants and trace code, not just complexity.
- Thesis/research: exact problem, method, metrics, results, personal role, limitation.
- Discrete: logic/proof, relations/counting, pigeonhole, recurrence/graph essentials.
- ML: bias–variance derivation, objectives, evaluation/leakage, major algorithms.

## Day 2 — systems core

- OOP: binding, polymorphism, equality/hash, exceptions, generics/collections, threads.
- OS: scheduling/synchronization/deadlock/memory/files/I/O.
- DBMS: SQL/ER/FD-normalization/index/transaction/recovery.
- Network/Data Communication: TCP/IP/subnet/DHCP/NAT/routing plus sampling/PCM/line coding.
- Security: CIA/threat model, crypto/modes/PKI/TLS, web, memory/network/DNS attacks.

## Day 3 — breadth and delivery

- architecture/DLD/micro and MIPS/8086/ATmega32 calculation cards;
- AI, graphics, SWE/ISD, TOC/Compiler, C, numerical methods;
- industry/project one-minute answers;
- two timed English mock vivas;
- repair only missed concepts; do not passively reread everything.

Use active recall cycles: answer → check chapter → correct aloud → re-answer later.

---

# 6. Mock viva A — technical panel

1. Introduce yourself in 45 seconds.
2. Which core course do you prefer and why?
3. Teach recursion to a first-year student.
4. Recursion versus iteration—which is better?
5. Prove bottom-up heap construction is linear.
6. Give predecessor and successor of a node in a BST.
7. Why does a red-black tree remain logarithmic?
8. Derive Edmonds–Karp complexity.
9. State the pigeonhole principle and one computing application.
10. State and derive bias–variance decomposition.
11. Is bias the same as underfitting?
12. Explain polymorphism and Java late binding.
13. Why must equal Java objects have equal hash codes?
14. Compare checked and unchecked exceptions.
15. Sort custom objects by two fields.
16. Compare TCP and UDP; expand both names.
17. What exactly do SYN and ACK mean?
18. Compare flow and congestion control.
19. Explain DHCP and NAT.
20. What security guarantee does TLS not provide?
21. Explain MLFQ and starvation prevention.
22. Why do we need a cache?
23. Explain conflict serializability.
24. Compare B+ tree and hash index.
25. Four ripple flip-flops receive 32 kHz. Label every output.
26. Explain sampling, quantization and PCM bit rate.
27. Compare NRZ, Manchester and AMI; why B8ZS/HDB3?
28. Compute FIRST/FOLLOW and one LL(1) table row.
29. Compare SLR, canonical LR(1), and LALR.
30. Draw the compiler pipeline and explain liveness/register interference.
31. Compare ECB/CBC/CTR/GCM and state nonce/IV rules.
32. Draw TLS 1.3 certificate/key/Finished flow.
33. Compute one 8086 segment:offset and one AVR CTC value.

# 7. Mock viva B — teaching and research panel

1. Why do you want to teach at BRAC University?
2. What evidence says you can teach?
3. Teach functions using sum from 1 to `n` to loop-aware freshers.
4. Motivate graphs using three real systems.
5. How would you help a class in which half the students are lost?
6. State your thesis question without jargon.
7. Why is Matter security analysis a state-machine problem?
8. Why GraphRAG rather than a single long prompt?
9. Can an LLM prove a vulnerability?
10. How did you validate a candidate with chip-tool?
11. Why are the 17 findings not merely 17 model outputs?
12. What did you personally do?
13. Define a visual certificate and same-layout negative.
14. State the exact VPG formula from your manuscript.
15. How did you prevent split leakage?
16. Why is NEUROSKY-EPI not a diagnostic claim?
17. Explain patient-level versus window-level splitting.
18. Derive WER and DER.
19. What exactly was your Bengali-Loop contribution?
20. Describe one industry failure mode and how you handled it.

---

# 8. Delivery checklist

- Answer the exact question in the first sentence.
- Define before comparing; state assumptions before saying “optimal” or “faster.”
- For algorithms: input/output → idea → invariant → trace → complexity → edge case.
- For equations: name every expectation, variable, and denominator.
- For systems: say which layer/component provides the guarantee.
- For security: name asset, adversary, control, and residual risk.
- For research: distinguish observation, result, conclusion, and claim.
- For personal work: use “I” only for your contribution.
- If a premise is wrong, correct it respectfully and calculate visibly.
- If you do not remember a number, do not fabricate it; state the concept and offer the exact source/version.
- Speak slowly enough to leave room for interruption.
