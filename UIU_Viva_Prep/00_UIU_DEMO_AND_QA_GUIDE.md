# Bismillah.

# UIU Random-Topic Whiteboard Demo and Interview Guide

This guide is tailored to the email supplied in this conversation and the
current `My_Resume/main.tex`. The ten copied subject books provide the depth;
this opening guide helps turn that knowledge into a short class.

# 1. Your actual session format

| Item | Information from the supplied UIU email |
|---|---|
| Position | Lecturer, Department of CSE |
| Selection phase | Second phase, out of three |
| Session label | Demo Session D |
| Date | September 14, 2026 |
| Reporting time | 1:30 PM |
| Candidate waiting room | 408 |
| Venue | UIU, United City, Madani Avenue, Badda, Dhaka |
| Introduction | 30 seconds–1 minute |
| Teaching | 4–5 minutes; randomly assigned topic; marker and whiteboard |
| Follow-up questions | 4–5 minutes, related to the teaching topic |

The email does not give the exact assigned topic or promise a topic choice.
Prepare breadth across all nine listed domains. In this pack, AI preparation
explicitly includes both classical AI and ML, as you requested. The Green
University NP-completeness slide deck is a separate preparation task.

# 2. Self-introduction using your current résumé

## 2.1 Approximately 30 seconds

> Good afternoon. I am Ahmmad Nur Swapnil. I completed my BSc in Computer
> Science and Engineering at BUET with a CGPA of 3.94 out of 4.00. I currently
> work as a Lecturer in CSE at Presidency University. My strengths include
> data structures, algorithms, and AI. I have research and industry experience
> in AI and software development, and I enjoy helping students understand
> computing concepts through clear examples and practical problem-solving.

## 2.2 Approximately 50–60 seconds

> Good afternoon. I am Ahmmad Nur Swapnil. I completed my BSc in Computer
> Science and Engineering at BUET with a CGPA of 3.94 out of 4.00. I currently
> serve as a Lecturer in the Department of CSE at Presidency University,
> teaching theory and sessional courses. I have also mentored students in
> programming, algorithms, and machine learning. My achievements include
> multiple Dean's List recognitions and a Codeforces Expert rating. My research
> includes LLM-guided security analysis and visual verification of graph
> properties, and I have worked in AI engineering and software development.
> I particularly enjoy explaining difficult ideas through small examples,
> tracing algorithms on the board, and connecting theory with implementation.

Rehearse at your natural pace; these times are approximate. Choose a few
achievements you can explain, rather than trying to list every résumé item.

## 2.3 Facts to keep consistent if asked

- Current role: Lecturer, CSE, Presidency University, June 2026–present.
- SysModeler: Junior AI Engineer, April–June 2026; discuss this as a previous role.
- SocioFi: internship/research and AI software development, May–October 2025.
- Teaching/mentoring: freelance programming instruction since 2023.
- Graph research: a 24,000-image benchmark over eight graph properties, according to the résumé. Be ready to explain split design and what visual certificates contribute.
- Thesis: LLM-guided Matter specification analysis, property extraction, state-machine modeling, GraphRAG and SDK/chip-tool testing. Distinguish a specification finding from a demonstrated implementation exploit.
- Research status: the graph and Matter manuscripts are described as submitted and under review. Do not describe them as accepted publications.
- EEG work: accepted as a poster at the NeurIPS 2025 **TS4H workshop**, according to the résumé; do not call it a NeurIPS main-conference paper.
- Bengali-Loop: a preprint/community benchmark contribution, according to the résumé.

The opening should focus on education, teaching and strengths. Detailed project
walkthroughs are not necessary unless the panel asks. For any research number,
know exactly what it counts and what your own contribution was.

# 3. A reusable 4–5 minute board plan

Use one learning objective: “By the end, you should be able to trace binary
search,” rather than “I will cover searching algorithms.”

| Time | What to do | What students should see |
|---|---|---|
| 0:00–0:30 | Motivate the topic and state the objective | A small problem or question |
| 0:30–1:15 | Define the idea and essential assumptions | Definition and input conditions |
| 1:15–3:15 | Work one example slowly | A diagram, trace, state table, or short code |
| 3:15–4:00 | State the rule/invariant, result, and relevant complexity | One compact summary |
| 4:00–4:40 | Check understanding with a nearby variation | A question with a verifiable answer |
| 4:40–5:00 | Close or handle a short interruption | One-sentence takeaway |

```text
LEFT: problem and definitions | CENTER: worked example | RIGHT: result/check
Keep these visible           | Update the state here  | Preserve the conclusion
```

Write large enough to read from the back. Name variables before using them.
Turn toward the class when explaining; do not speak continuously into the board.
State assumed prior knowledge. If the assigned topic is broad, state a narrow,
representative objective within it; do not replace it with a different subject.

For the Q&A, answer directly, then justify: definition, mechanism, example,
assumptions, and trade-off. When asked an equation, write it and explain the
symbols. When asked an algorithm, be ready with its invariant and code.

# 4. Structured programming: functions and a loop invariant

**Objective:** package a repeated calculation in a function and trace it.

**Motivation:** “Several parts of our program need the sum from 1 to n. Should
we duplicate the loop every time?” Explain a function's input, return value,
reuse, and one place to maintain its behavior.

```c
/* Contract: 0 <= n <= 1000000. */
long long sum_to_n(int n) {
    long long total = 0;
    for (int i = 1; i <= n; ++i) {
        total += i;
    }
    return total;
}
```

Trace `n=4`: totals `0 -> 1 -> 3 -> 6 -> 10`.
Before iteration `i`, `total` equals the sum from 1 through `i-1`.
The update preserves the invariant; exit occurs after `i=n`, so the result is
the desired sum. Time is Θ(n), auxiliary space Θ(1) under the stated bounds.

**Check:** “What does the function return for n=0?” Answer: zero; the loop does
not execute.

**Follow-ups:** C passes arguments by value; pointers can let a function modify
an object supplied by the caller. Scope and lifetime are different. The formula
$n(n+1)/2$ uses constant many arithmetic operations, but fixed-width overflow
still matters. A recursive version uses stack frames unless optimized; neither
recursion nor iteration is universally superior.

**Alternative board topics:** value versus address, arrays and pointers, string
termination, selection/loops, structure members, scope/lifetime, safe file input.
Read volume 04 for complete examples and C pitfalls.

# 5. OOP: runtime polymorphism

**Objective:** predict which overridden method executes through a base reference.

```java
class Animal {
    String sound() { return "unknown"; }
}
class Cat extends Animal {
    @Override String sound() { return "meow"; }
}
Animal a = new Cat();
System.out.println(a.sound()); // meow
```

Draw `a: Animal` as a reference pointing to an object whose actual class is
`Cat`. The reference's declared type governs which members can be used at
compile time; dynamic dispatch chooses the overriding instance method from
the runtime object's class.

**Check:** “Did declaring a as Animal turn the Cat object into an Animal
object?” No. The declared reference type and runtime object class differ.

**Follow-ups:** overloading is selected at compile time; overriding supports
runtime dispatch. Java static methods are hidden, not dynamically overridden.
Fields are not dynamically dispatched like instance methods. Encapsulation
protects representation and invariants; abstraction presents the relevant
contract. In C++, runtime dispatch requires a virtual method; deleting through
a polymorphic base pointer generally requires a virtual destructor.

**Alternatives:** encapsulation through a bank-account invariant, composition
versus inheritance, interface versus abstract class, equality/hashCode, exceptions,
collections and generics. Read volume 03.

# 6. Discrete mathematics: pigeonhole with an actual computing example

**Objective:** identify the objects and boxes and prove an unavoidable collision.

If more than $k$ objects are placed in $k$ boxes, at least one box contains at
least two objects. More generally, for $N$ objects and $k>0$ boxes, one box
contains at least $\lceil N/k\rceil$ objects.

**Concrete example:** a hash function maps every key to one of ten bucket
indices, 0 through 9. Insert eleven distinct keys. The keys are the objects;
the ten possible indices are the boxes. At least two keys must hash to the
same index. For the illustrative function $h(x)=x\bmod10$, keys `12` and `22`
both map to bucket 2. Chaining or probing is needed to handle collisions.

**Proof:** assume each bucket contains at most one of the eleven keys. Then
ten buckets hold at most ten keys, a contradiction.

**Check:** “Must there be a collision with only nine keys?” The principle does
not force one, but a collision can still occur. It establishes necessity in
one direction, not a collision-free guarantee for smaller inputs.

**Follow-ups:** 101 integers and 100 possible remainders force two with equal
remainders modulo 100; their difference is divisible by 100. With a hash table,
distinguish the initial hash index from the final storage slot under probing.

**Alternatives:** induction, contrapositive, quantified negation, relations,
counting, inclusion-exclusion, recurrence, Euler versus Hamilton. Read volume 10.

# 7. Data structures: stack and balanced brackets

**Objective:** use LIFO to match nested opening and closing brackets.

Trace `([])` using a stack: push `(`, push `[`, encounter `]` and pop `[`,
encounter `)` and pop `(`. The stack finishes empty. For `([)]`, the `)`
does not match the most recent unmatched opening bracket `[`, so reject.

```text
for each bracket c:
    if c is opening: push(c)
    otherwise:
        if stack is empty: reject
        if top does not match c: reject
        pop()
accept exactly when stack is empty
```

The invariant is that the stack holds the unmatched opening brackets of the
processed prefix in their order of occurrence. Time Θ(n), worst-case space
Θ(n). A queue cannot directly replace it because nesting needs the latest
unmatched opening symbol.

**Check:** “Why reject `(()`?” An opening bracket remains unmatched at the end.

**Follow-ups:** stack as an ADT versus an array/linked-list implementation;
overflow in a fixed-size array stack; amortized cost of a resizing stack;
recursion and call stacks. For BSTs, know predecessor/successor cases and rotations.

**Alternatives:** queues/circular queues, linked-list insertion, BST operations,
heap/priority queue, hashing. Read volumes 01 and 02.

# 8. Algorithms: binary search with a defensible invariant

**Objective:** trace binary search and justify the discarded half.

Use sorted array `[3, 7, 11, 15, 19, 23, 27]`, target 19. With inclusive bounds:
`lo=0, hi=6, mid=3` gives 15, so set `lo=4`; `mid=5` gives 23, so set `hi=4`;
`mid=4` gives 19, so return 4.

```cpp
int binary_search_index(const vector<int>& a, int target) {
    int lo = 0, hi = (int)a.size() - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == target) return mid;
        if (a[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}
```

Assume the vector length fits in `int`. If the target is present and not yet
returned, it remains in the candidate interval. Sortedness justifies the
discarded part. The interval strictly shrinks, proving termination. Worst-case
time is Θ(log n) for nonempty random-access input; auxiliary space Θ(1).

**Check:** “What changes if the list is unsorted?” The discard rule is invalid.
Use linear search, or account for sorting/index-building costs if many queries
justify preprocessing. On a linked list, midpoint access is not constant time.

**Follow-ups:** duplicates, lower_bound/first occurrence, empty input, boundary
conditions, recursion, preprocessing trade-offs. Also know BFS/DFS, sorting,
greedy versus DP, shortest paths, MST, and linear-time bottom-up heap building.
Read volumes 01 and 02.

# 9. DBMS: functional dependency and normalization

**Objective:** identify an update anomaly and remove a specific redundancy.

Use `Enrollment(StudentID, StudentName, CourseID, Grade)`, assuming a student
has one row per course and one grade for that course. A candidate key is
`(StudentID, CourseID)`, and `StudentID -> StudentName`. The name repeats across
the same student's courses, creating inconsistent-update risk.

Decompose into `Student(StudentID, StudentName)` and
`Enrollment(StudentID, CourseID, Grade)`. The repeated student name is stored
once. The common attribute `StudentID` determines all of the Student relation,
which gives the standard binary lossless-join condition under these FDs.

**Check:** “Does decomposition mean losing the ability to show names with
grades?” No; join on StudentID.

```sql
SELECT s.StudentName, e.CourseID, e.Grade
FROM Student AS s
JOIN Enrollment AS e ON e.StudentID = s.StudentID;
```

**Follow-ups:** a functional dependency describes a constraint on legal relation
instances, not a pattern inferred safely from a tiny sample. 2NF removes partial
dependencies of non-prime attributes on candidate keys; 3NF and BCNF impose
stronger FD conditions. Always state all assumed FDs before claiming a normal form.

**Alternatives:** joins, GROUP BY/HAVING, keys, ER cardinality, ACID, serializability,
indexes/B+ trees, isolation anomalies, WAL. Read volume 05.

# 10. Software engineering: equivalence partitions and boundary tests

**Objective:** derive tests from a requirement, not from guesswork.

Requirement: an integer mark from 0 through 100 is valid; other integers are
rejected. Identify partitions `<0`, `0..100`, `>100`. Representative partition
tests include `-10, 50, 110`. Boundary tests include `-1, 0, 1, 99, 100, 101`.

Show how `0 < mark && mark < 100` incorrectly rejects the valid endpoints,
while `0 <= mark && mark <= 100` implements the stated range.

**Check:** “Are these tests enough if the input is a string from a form?” No;
parsing, empty input, nonnumeric input, and noninteger values need requirements
and tests. Do not silently extend the integer-input contract.

**Follow-ups:** equivalence partitioning reduces test selection based on assumed
similar behavior within a class; it does not prove all inputs work. Verification
checks conformance to specifications; validation checks whether the product
meets actual user needs. Unit, integration, system, and acceptance tests operate
at different scopes. Regression testing checks behavior after changes.

**Alternatives:** functional/nonfunctional requirements, use cases, UML class
diagrams, cohesion/coupling, SOLID, waterfall/Agile, patterns, CI/CD. Read volume 08.

# 11. Operating systems: Round Robin scheduling

**Objective:** build a Gantt chart and compute waiting/turnaround times.

Assume all processes arrive at time 0, bursts `P1=5, P2=3, P3=1`, initial queue
order `P1,P2,P3`, quantum 2, and negligible context-switch overhead.

```text
Time: 0     2     4  5     7  8  9
      | P1  | P2  |P3| P1  |P2|P1|
```

Completion times are P1=9, P2=8, P3=5. Turnaround is completion minus arrival,
so the same values apply. With no I/O, waiting is turnaround minus CPU burst:
P1=4, P2=5, P3=4. Average waiting time is $13/3$ time units.

**Check:** “What if the quantum is larger than every burst?” With these arrival
conditions and queue order, it behaves as FCFS.

**Follow-ups:** small quantum improves responsiveness but increases switching
overhead. First-response time differs from total waiting. With nonzero arrival
times, show the ready-queue updates explicitly. Arrival during a time slice
normally joins the queue; it does not automatically preempt the running slice.

**Alternatives:** process/thread, process states, race condition and mutex,
deadlock conditions, paging/TLB, page replacement, files and system calls.
Read volume 06.

# 12. Classical AI: A* and the role of the heuristic

**Objective:** distinguish cost already paid from estimated cost remaining.

$$f(n)=g(n)+h(n).$$

Use edges `S-A=1`, `S-B=4`, `A-G=6`, `B-G=1`. The two routes cost 7 and 5.
Choose `h(S)=5, h(A)=6, h(B)=1, h(G)=0`. After expanding S, A has `g=1,f=7`
and B has `g=4,f=5`; A* expands B next and reaches G with total cost 5.
The example's heuristic is admissible and consistent.

**Check:** “What if h is always zero?” Selection depends only on g: uniform-cost
search, equivalent in its shortest-path ordering to Dijkstra under the usual
nonnegative-cost assumptions.

**Follow-ups:** admissibility means never overestimating true remaining optimal
cost; consistency means $h(u)\le c(u,v)+h(v)$ for every relevant edge. For graph
search with a consistent heuristic, the usual closed-set implementation is
optimal under standard conditions. An admissible but inconsistent heuristic
can require reopening nodes. Stop when the goal is selected for expansion
under the algorithm's assumptions, not merely when it is first generated.

**Alternatives:** agent/rationality, BFS/DFS/UCS/greedy search, minimax/alpha-beta,
CSP, Bayesian networks, MDPs and reinforcement learning. Read volume 09.

# 13. ML: bias–variance, with the actual equation

**Objective:** explain what varies across training sets and separate errors from
the observed behaviors called underfitting and overfitting.

At fixed input $x$, let $Y=f(x)+\varepsilon$, with zero conditional mean noise
and conditional variance $\sigma^2(x)$. Let $\hat f_D(x)$ be the predictor learned
from random training set $D$, and use an independent test outcome.

$$\mathbb E_{D,\varepsilon}[(Y-\hat f_D(x))^2]
=\underbrace{(\mathbb E_D[\hat f_D(x)]-f(x))^2}_{\text{bias}^2}
+\underbrace{\mathbb E_D[(\hat f_D(x)-\mathbb E_D[\hat f_D(x)])^2]}_{\text{variance}}
+\underbrace{\sigma^2(x)}_{\text{irreducible noise}}.$$

Draw one fixed x, a horizontal line at the true value $f(x)$, and several
predictions from models trained on different datasets. Their mean's distance
from the truth is bias; their spread around their own mean is variance.

**Tiny calculation:** true value 10; learned predictions 8 and 12, equally
likely. Mean=10, bias=0, variance=$((8-10)^2+(12-10)^2)/2=4$. If noise variance
is 1, expected test squared error is 5. A predictor always returning 8 has
bias=-2, bias squared=4, variance=0, and the same total error 5 in this example.

**Check:** “Does zero bias imply zero prediction error?” No; variance and noise
can remain. Similarly, no variability across training sets does not imply the
mean prediction is correct.

**Derivation for Q&A:** add and subtract
$\mu(x)=\mathbb E_D[\hat f_D(x)]$, expand the square, and take expectations.
The centered estimator term has zero mean. Independent, zero-mean test noise
makes the noise cross terms vanish. This is the classical squared-error
decomposition; do not apply the same identity unmodified to every loss.

High bias often accompanies underfitting; high variance often accompanies
overfitting. They are related, not definitions of one another. Under/overfitting
describe fitting and generalization behavior; bias/variance are statistical
properties of the learning procedure across training samples.

**Alternatives:** train/validation/test split, linear/logistic regression,
gradient descent, regularization, decision trees/information gain, confusion
matrix, kNN/k-means, neural-network backpropagation. Read volume 11.

# 14. A breadth-first rehearsal plan

Prepare several topics per domain rather than betting on the ten examples
above. Those examples are practice choices, not a prediction of UIU's topics.

| Rehearsal block | Subjects | Minimum performance target |
|---|---|---|
| First pass | C, OOP, discrete | One concept, trace/code, common misconception, follow-up |
| Second pass | Data structures, algorithms | Invariant, complexity, boundary case, board trace |
| Third pass | DBMS, SWE, OS | State/diagram, worked calculation or query, trade-off |
| Fourth pass | AI and ML | Search trace, equation assumptions, numerical interpretation |
| Final passes | Random selection across all domains | 1-minute introduction + 5-minute class + 5-minute Q&A |

Choose a topic randomly, give yourself only enough time to organize a board,
and teach aloud. Afterward score factual accuracy, legibility, example quality,
student engagement, timing, and follow-up depth separately. When one is weak,
return to that copied subject book and rehearse again.

For every likely algorithm, know input assumptions, state, invariant, code,
termination, correctness, time/space, and one failing counterexample to a
tempting shortcut. For every formula, know the random variables, conditioning,
units, assumptions and interpretation. These habits generalize to questions
that no preparation list can enumerate.

# 15. Interview preparation after the demonstration

The email explicitly schedules follow-ups to the demo. This pack additionally
prepares your wider academic/research defense, without claiming the panel will
ask all of it. Use the copied volume 17 for detailed thesis, research and
industry answers, and volume 19 for subject-wise oral questions.

For any teaching topic expect: define precisely → explain why → simulate a
variation → state the equation/invariant → analyze complexity or trade-offs →
identify a failure case. If a premise is wrong, qualify it respectfully:
“On a finite graph with a visited set DFS is complete; the usual counterexample
is an infinite-depth tree.” Do not agree with a false statement just because it
appears in a seniors' recollection.

## Research and industry answers to rehearse aloud

1. **What was your thesis question?** Explain the gap in Matter specification
   security, why state transitions/security properties matter, your section-wise
   LLM/GraphRAG workflow and SDK testing. Separate candidate model outputs from
   validated findings; the résumé reports 17 specification-level findings,
   including 8 major ones. Supply one real manuscript example, not an invented one.
2. **What did you contribute?** Use one concrete artifact, method or experiment.
   Distinguish your work from collaborators' work; explain how it was evaluated.
3. **What is the strongest limitation?** Choose a real boundary: spec/SDK version,
   data coverage, leakage risk, false positives, generalization or validation scope.
   State the follow-up experiment that could address it.
4. **How does your graph research connect to DSA?** Explain graph properties,
   visual certificates/counter-certificates, same-layout negatives, the 24,000-image
   benchmark and the difference between visual recognition and algorithmic proof.
   Read the exact VPG equation from your manuscript before the interview.
5. **What did industry teach you?** Give one actual validation/retry/idempotency/
   security or deployment problem from your previous AI/software roles, how you
   handled it, and evidence it worked. Do not claim a proposed design was deployed.
6. **Why teaching / why UIU?** Connect current university teaching and mentoring
   to clear explanations, assessment and research supervision. State genuine
   reasons for applying without inventing institutional promises or criticizing
   your current employer. Give one real student misconception you helped repair.

The seniors' workbook checklist in volume 20 helps you find overlooked topics.
It is not a reason to spend most of a five-minute demo on advanced number theory
or every variant of an algorithm. Start at the level of the assigned topic and
use deeper material when the panel asks for it.
