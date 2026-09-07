# Bismillah.

# Seniors' workbook coverage audit — September 2026

Source: `Varsity_Topics_List_In Memory of Masud.xlsx`, supplied by the user.
All **15 sheets**, including hidden **Niche Topics**, were read. All **17
embedded screenshots** were visually inspected. The sheet titled “DB” contains
only “Work in progress”; important database questions appear elsewhere.

This is a **topic-by-topic workbook-to-notes audit**, not a fresh claim of
reading all 18,977 academic PDF pages again. Existing slide-based material was
retained; gaps were filled as labeled workbook supplements. External Google
Docs/Drive/YouTube links listed in the workbook were inventoried, not all opened
or transcribed. They are additional resources, not silently audited sources.
No finite preparation set can guarantee every possible interview question.

## How to follow the mapping

Volume numbers refer to the existing filenames in this folder. “Retained” means
the relevant explanation/code/example already existed and was inspected for
this checklist; “expanded” means a new worked explanation or correction was
added. Sections with prefix N/W/H/A below are named workbook supplements.
ASCII diagrams and trace tables are deliberate: they can be redrawn on a
whiteboard and remain readable without relying on color.

## 1. DSA sheet, including cross-course entries

| Source cells | Topic(s) | Destination and reviewed evidence |
|---|---|---|
| B5 | undirected cycle with disjoint sets | 02 §3.1 expanded: DSU code, component trace, proof, directed counterexample |
| B7/B9 | quicksort simulation/randomization | 01 §§11.6/17.1 expanded: every partition step, recurrence, 3-way pseudocode, duplicate caveat |
| B11 | underflow/overflow | 01 stacks/queues and §17.6: bounded capacity, empty operations, numeric distinction |
| B13, D33 | full/perfect/complete/degenerate/skewed/balanced tree | 01 §6.1 and §17.6 expanded shape diagrams |
| B15/B17 | BFS/DFS complexity, completeness, optimality | 01 §10 code/traces; 09 A1 expanded finite-graph versus infinite-tree counterexample |
| B19/B21/H21 | heap, heapify, build-heap, heapsort | 01 §8 proof/code and §17.2 full build/extraction trace; disk-sorting caveat |
| B23 | merge sort/stability/external sorting | 01 §11.5 merge code/invariant; §17.5 external-run explanation; 05 external sorting I/O |
| B25/C25/C26 | BST lookup/deletion/predecessor/successor | 01 §7 diagrams/code; §17.6 clarifies node/parent availability and height bound |
| B30/C30 | ordinary binary-tree deletion | 01 §17.6 repairs incorrect balanced-tree complexity statement |
| B32/C33/C34 | binary, linear and infinite/unknown-length search | 01 §§11.1/17.3 expanded safe accessor contract, exponential-search code/trace, query trade-offs |
| B36/B38 | divide-and-conquer versus DP | 01 §§12–14 independent/overlapping states, examples and DP implementations; 02 §21 alternatives for hardness |
| B40 | basic OOP | 03 Part I definitions, encapsulation example, relationships and dispatch |
| B42 | value/reference passing | 04 §11.4 pointer code; 03 parameter passing and workbook language-semantics correction |
| B44 | constant versus nearly constant | 02 §3.1 expanded log-star example and inverse-Ackermann distinction |
| B46 | hash table/perfect hashing/load | 02 §17 implementations; expanded fixed-set versus universal-key distinction |
| B48 | hash table versus array | 02 hashing supplement: sparse keys, locality, storage/resize trade-offs |
| B50 | hash code/compression, clustering | 02 §§17.1/17.5 and supplement: primary/secondary clustering |
| B52 | practical versus uniform hashing | 02 supplement distinguishes two probability models rather than inventing two algorithms |
| B54 | double hashing | 02 §17.5 coprimality plus good/bad probe sequences |
| B56 | rehashing thresholds | 02 supplement corrects universal .9/.5 claim; live versus tombstone load |
| B58 | time-complexity measurement | 01 §1 counting, worst/average/amortized; §2 recurrences; 02 §13 aggregate/accounting/potential |
| B62 | overloading versus overriding | 03 dispatch code and Part IV contrasts; unrelated concepts kept separate |
| B64 | shallow/deep copy | 03 C++ Lecture 3 runnable ownership/copy example; Java copying/identity |
| B66 | diamond with Java | 03 workbook supplement adds compiling interface-default conflict resolution |
| B68/B70/B72 | virtual/pure virtual/abstract | 03 C++ Lecture 10 and Java abstract/interface rules; screenshot language caveats |

## 2. Machine-learning sheet

| Source cells | Topic(s) | Destination and reviewed evidence |
|---|---|---|
| B5/B7 | ML and learning settings | 11 §1 definitions/examples; W5 corrects ensemble as an orthogonal design choice |
| B9 | train/validation/test | 11 §2 leakage examples; W5 fold/refit/test diagram |
| B11/B13/B45 | hypothesis, hypothesis space, consistency | 11 W1 threshold/version-space simulation and statistical-consistency distinction |
| B15/B17 | generalization, overfitting, bias/variance | 11 §§4/7 full fixed-x squared-error derivation, assumptions, numeric example and learning curves retained |
| B19 | Ockham/Occam | 11 W1 precise preference, regularized risk/MAP connection and underfitting caveat |
| B21/B79 | L1/L2/regularization | 11 §8 formulas, sparsity, gradients, Elastic Net, penalty conventions |
| B23/B25/B47/B49/A54 | confusion matrix/classification metrics | 11 §5 numeric TP/FP/FN/TN; W4 threshold simulation and screenshot corrections |
| A60 | regression metrics | 11 §6 MSE/RMSE/MAE/R², units and negative R²; W4 constant-target caveat |
| A64 | clustering metrics | 11 W3 silhouette calculation, ARI relabeling example, inertia/DB/CH/NMI roles |
| B27 | linear regression | 11 §9 objective, normal-equation derivation, gradient code |
| B29/B31/B33 | GD/batch/SGD | 11 §§9/24 update equations, minibatch, optimizer and convergence caveats |
| B35/B66 | ensemble model | 11 §§16–19 definitions/mechanisms; W5 taxonomy correction |
| B37 | linear classification versus logistic | 11 §§10–12 perceptron, sigmoid/cross-entropy, softmax; logistic is itself linear in its logit/features |
| B39/B41 | PCA, curse of dimension, regression comparison | 11 W2 covariance/eigenvector/projection calculation, code and signal-discard counterexample |
| B43 | K-fold CV | 11 §2 and W5 corrected validation terminology, refit and nested-CV boundary |
| B68 | boosting | 11 §§17/18 AdaBoost weights, gradient residuals, code, XGBoost; W8 second-order leaf calculation |
| B70 | bagging | 11 §16 bootstrap/OOB/random forest; §7 correlated-error variance equation |
| B72 | stacking | 11 §19 and W5 out-of-fold meta-training diagram |
| B75/B77 | small/large-scale learning | 11 W8 sample/feature/model/compute dimensions, no universal sample cutoff |
| B81/B83/B85 | RL/value/policy learning | 11 §§41–45 Bellman/TD/Q-learning; W6 policy-gradient pseudocode and numerical bandit update |
| B87 | horizon effect | 09 §28 and 11 W6 delayed-loss example; distinguishes game cutoff from training-data instability |

## 3. AI, OS, network and architecture tabs

| Source | Topic(s) | Destination and reviewed evidence |
|---|---|---|
| AI B4/C4–C8/B10 | agents, rationality, autonomy, percept | 09 §§3–6; A2 adds agent loop and ideal/discrete terminology clarification |
| AI B12/C12–C17 | observability/determinism/episodes/static/discrete/multi-agent | 09 §5 contrasted environment dimensions with taxi/chess examples |
| AI B19 | uninformed search | 09 §§10–16 BFS/UCS/DFS/DLS/IDS algorithms, frontier and iteration examples |
| AI B21/B23 | optimality/completeness | 09 A1 repairs finite/infinite and depth-limit assumptions |
| AI B25/B28 | informed search/admissible heuristic | 09 §§17–20 Romania trace, A* proof, consistency/reopening counterexample |
| AI B30 | PEAS | 09 §4 taxi/medical examples, A2 vacuum example |
| AI B32/B34 | zero sum/minimax | 09 §§25–28 code/tree/alpha-beta; A3 chance/multiplayer/infinite-tree caveats |
| OS B3 | monolithic/microkernel | 06 §1 privilege boundaries, modular Linux and IPC trade-offs |
| OS B5 | user/kernel mode | 06 §1 and workbook supplement: syscall is not always a context switch |
| OS B7/B9/B11 | program/process, PCB, life cycle | 06 §2 and expanded labeled state diagram |
| OS B13/B15 | multiprogramming/processes/threads/single core | 06 workbook supplement: execution timeline, concurrency versus parallelism |
| Computer Network B3/C3 | OSI model | 07 Part I layer responsibilities and encapsulation diagram; expansion is Open Systems Interconnection |
| Computer Archi B8/D8 | IEEE754 single/double | 14 H1 field table, -13.25 bits, biased exponent, subnormal/NaN/infinity cases |
| Computer Archi B10 | RISC/CISC | 14 §7 and H2 ISA versus implementation, no universal speed claim |
| Computer Archi B12 | single/multicycle | 14 H2 timing comparison and pipeline overlap diagram |

## 4. “Things to Explain on Board” tab

| Rows/cells | Topic(s) | Destination and demo evidence |
|---|---|---|
| B3 | RSA | 13 §16.3 complete key generation/encrypt/decrypt modular example; §26 identity/security cautions |
| B5 | AES | 13 §14.5 plus §26.2 state layout, ShiftRows, MixColumns example and round pseudocode |
| B7 | MITM | 13 §26.1 two-key message diagram with calculated DH values |
| B9/F9 | Bellman–Ford/negative-cycle detection | 02 §§4.4/24 executable core, multi-pass trace and reachable/global detection |
| B11/F11 | Floyd–Warshall | 02 §§5.2/24 matrix recurrence, code, 3-vertex matrix trace and affected-pair caveat |
| B13 | Dijkstra/negative weights | 02 §§4.3/24 heap code, proof and negative-edge counterexample without a cycle |
| B15 | negative cycles and response | 02 §24 repeatable walk explanation, propagation of -infinity, super-source |
| B17/B19/B21/B23/B25/B27 | IP/DNS/HTTP spoofing, email hijack, Wi-Fi, cache poisoning | 13 §26.3 distinguishes mechanisms and defenses; §§22/25 retain protocol detail |
| B29 | authentication/authorization | 13 §8 and §26; identity versus action/object decision |
| B31 | MAC/IP | 07 addressing/ARP/routing: local next-hop delivery versus routed network addressing |
| B33 | symmetric/asymmetric | 13 §4/§16/§26: bulk speed, key establishment, authentication and hybrid use |
| B35/B37 | quicksort/heapsort worked | 01 §§17.1/17.2 full traces, not just final arrays |
| B39 | buffer overflow | 13 §21 safe-code comparison; §26.4 buffer-cell drawing and isolated diagnostic demo |
| B41 | SQL injection | 13 §§11.1/19.4 parameter binding, identifier caveat and query/data distinction |

## 5. BRAC question-bank cells — additional coverage and interview scope

Repeated topics map above; this table also accounts for CV and systems questions
that do not appear in the subject tabs. These are seniors' anecdotes, **not**
promises about a particular board, teacher, outcome or university policy.

| Source cell | Additional prompts and destination |
|---|---|
| C3 | thesis/network project, crypto, course preference: 00/17 and 07/13; no invented answer about an unnamed teacher's prior work |
| C5 | Agile/waterfall: 08 §§3–4; RGB/CMYK: 12 §32 expanded mixing/conversion; Diophantine: 10 N3 |
| C7 | lay thesis explanation: 17 §1; CIA: 13 §1 (not “ICA”); ray tracing: 12 ray/lighting chapters; structure underflow and arrays/lists: 01 §§3–4/17.6 |
| C9 | pass semantics: 03/04; IPv4 limits: 07; DP/D&C: 01; signed addition: 14 §1 with 4-bit overflow |
| C11 | hashing/salt/ethics/access: 13; deadlock/paging/replacement/scheduling: 06 §§3–6 and calculation workshops; XGBoost: 11 §§18/W8; NLP alternatives and owned role: 17 |
| C13 | array/list, DP/D&C/Bellman–Ford: 01/02; exponent bias: 14 H1; semaphores: 06 §4; research aspiration: 00/17 |
| C19 | memory hierarchy/cache: 14 §§11/25 and 06; NAT/TCP loss: 07; CIA/crypto: 13; ACID: 05 transactions; circular arrays: 01 §5; ongoing-CV claims: 17 §12.5 |
| C21 | k-means: 11 §39 algorithm/assign-update; MITM/RSA/access: 13 §26; completeness: 09 A1; one-buy/sell code: 01 §17.4 |
| C23 | graph traversals/complexity and DP alternatives: 01 §10/14, 02 §21; no unconditional DFS-faster claim |
| C25 | negative cycles and Bellman–Ford: 02 §24; honest course breadth: 00 |
| C29 | rational agent: 09 A2; MLE/EM: 11 §§34–38/W8; TCP: 07; thesis depth and formal introduction: 17/00 |
| C31 | Dijkstra/toposort/Bellman–Ford: 02 §§2/4; alpha-beta: 09 §27; scheduling/paging/replacement: 06; extracurricular claim ownership: 17 |
| C35 | asynchronous sequential circuits: 14 §23.7 races/flow tables; do not invent the unspecified graphics question |
| C37 | bias/variance: 11 §7; process/page tables: 06; graph/tree: 10 §§106–113; DP/D&C: 01; encapsulation demo: 03/ UIU guide |
| C39 | already-sorted sorting decision: 01 §17.5; thesis and English practice: 17/00 |
| C41 | TCP/UDP/IP/MAC/IPv6: 07; NoSQL→SQL: 05 §26 new schema/code/migration simulation; AdaBoost/GD/Transformer: 11; LSTM: 11 W7 new gates/code/calculation |
| C43 | named core preferences: 00; network/architecture/ML/discrete sections above, without assuming hardware weakness |
| C45 | compiler stages: 15 compiler pipeline (not universally four stages); OOP: 03; OS: 06; all named subjects retained in BRACU |
| C47 | detection/hunting: 13 §26.5; LM/LLM mini-lesson: 11 W8; scheduling/context switch: 06; competition/research status: 17 §12.5 |
| C49 | RR quantum/context/locality/replacement: 06 supplement and memory chapter; research outcome/data/impact: 17 |
| C51 | ambient/light models: 12 §§33–34 including Phong calculation; NAT/PAT/ports: 07; competitive programming: 00/01/02 |

An unspecified “algorithm I hadn't heard of,” unidentified graphics question or
unremembered distance question cannot be reconstructed from this workbook.
The books retain broad algorithms/graphics/ML distance coverage; this audit
does not invent the missing interview wording.

## 6. Screenshot and hidden-sheet ledger

Names below match the extracted files in `build/seniors_audit/`.

| Sheet/image | What was actually visible | Decision |
|---|---|---|
| Some Words / image8 | decorative anime/motto image | inspected; not a technical topic or needed PDF illustration |
| BRAC / image11 | achievements, certificates, coding/two pointers | 00/17 honesty and English practice; 01 stock-profit example |
| BRAC / image13 | board may read all CV lines/hobbies | 17 §12.5; do not repeat personal chat verbatim |
| BRAC / image14 | course comfort, buffer setup, crypto/key exchange, thesis, cycles/SSSP | 13 §26, 17, 02 §§4/24 |
| BRAC / image7 | research depth, projects versus thesis, achievements | 17 framework and compact project boundary |
| Random / image1 | default/parameterized/copy constructors | 03 supplement adds move/assignment distinction |
| Random / image12 | abstract-class properties | 03 supplement corrects Java/C++ and abstract-method restrictions |
| Random / image3 | C++ friend class | 03 supplement supplies initialized, compiling program |
| Random / image6 | inheritance types | 03 original inheritance/diamond diagrams and new Java conflict code |
| Random / image5 | ambiguous Moore/Mealy drawing | 14 H3 complete input/output tables and overlapping-101 simulation |
| Random / image2 | classification/regression metric high/low chart | 11 W4 corrects AUC=.5 versus 0 and count/rate interpretation |
| Random / image9 | TP/FP/FN/TN, task-dependent costs | 11 §5/W4 concrete positive class and threshold trade-off |
| Runtime / image15 | Prim/Kruskal comparison | 02 §3/§24 correct heap-specific bounds and forest handling |
| Runtime / image16 | Bellman–Ford/Dijkstra table | 02 §24 distinguishes graph storage, dense version, reachable negative cycle |
| Runtime / image17 | bubble/selection/insertion/merge/quick/heap/counting/radix/bucket/Shell | 01 §§11/17 full coverage, parameters and distribution/gap assumptions |
| Runtime / image10 | supervised/unsupervised/RL/ensemble | 11 §1/W5: ensemble is not a mutually exclusive learning signal |
| Runtime / image4 | Diophantine, modular, CRT, Euler, Fermat, Hensel, Wilson, reciprocity, Euclid, bigmod, inverse, sieve, factorization | 10 N1–N10, equations, examples, algorithm code and advanced-topic labels |
| Hidden Niche Topics C4 | Johnson | 02 §5.3 expanded reweighting table, Dijkstra result and sign restoration |
| Hidden Niche Topics C6 | Kleene algorithm | 15 §4.3 expanded recurrence, diagram, pseudocode and expression-size caveat |

## 7. Non-topic tabs and evidence limits

“Some Words from me” is the dedication and preparation advice. “Useful Links”
is an index of outside notes/resources; “Industry Prep” lists external problem
banks and recommends writing code on paper, optimizing with justification, and
explaining it aloud. These practices are reflected in 17 §12.5 and the demo
guide. The linked collections were **not** exhaustively solved or audited.
The workbook has no substantive numerical-methods topic list; volume 16 remains
the existing source-based numerical-methods reference, not a newly checked set
of senior questions. DB and network sheets are unfinished, so their sparse
entries never justify removing the full core chapters.

## 8. Practical verification and UIU selection

`python .\build\test_seniors_additions.py` runs the new search/sort/number-theory
functions extracted from Markdown against independent expected results. It also
checks both 101 detector tables over binary strings, floating-point bits, DH
arithmetic, the migration schema/constraints with SQLite, PCA/LSTM when NumPy
is installed, and the complete C++ friend example when g++ is installed.
The September 2026 run passed **9,581 assertions**. This does not claim that
every older snippet in the entire multi-volume pack has been executed.

UIU receives the updated full C, OOP, Discrete, DSA I/II, DBMS, SWE, OS, AI,
and ML books, plus the résumé-refreshed thesis/research/industry chapter, the
targeted interview question bank, and its new demo-and-interview guide. This
audit is also copied for traceability; the non-UIU subject references in it
refer back to BRACU, not to chapters secretly included in the UIU PDF.

For the UIU **demo**, select one small example and teach it in 4–5 minutes.
For the **interview**, use the next layer: equations, invariants, implementation,
counterexample, assumptions, complexity, research ownership and limitations.
