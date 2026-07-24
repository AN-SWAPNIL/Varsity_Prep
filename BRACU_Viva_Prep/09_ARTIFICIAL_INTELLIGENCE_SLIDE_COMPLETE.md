# Bismillah.

# Artificial Intelligence — complete slide-grounded viva recall

This is the Artificial Intelligence volume of the viva pack. It is written from the local CSE317 resources, not from a generic question list. It explains the model, equation, invariant, algorithm, trace, assumptions, complexity, failure mode, and likely viva trap. Machine-learning material that actually appears in the AI slides—learning agents and decision trees—is retained here; the much larger standalone ML course remains in `11_MACHINE_LEARNING_SLIDE_COMPLETE.md`.

## Source grounding

| Current source | Pages audited | Material represented here |
|---|---:|---|
| `CSE317_MMI_Merged.pdf` | 521/521 | history; agents; problem formulation; uninformed/informed/memory-bounded/local search; GA; games; CSP |
| `CSE317_SB_Merged.pdf` | 214/214 | Bayesian networks; HMMs; MDPs; learning; decision trees |
| **Total current source** | **735/735** | **all selected AI slide pages** |

The removed legacy copies are no longer counted. A subsection marked **Standard-core supplement** is important viva knowledge but is not developed as a full lecture in the current slides; this mainly applies to formal logic, planning, and ethics.

## The 30-second map

AI studies agents that perceive an environment and select actions. The course builds this in layers: define the agent/performance/environment; formulate states/actions/goals/cost; search blindly or with a heuristic; optimize a state; handle opponents and constraints; represent uncertainty with Bayesian networks/HMMs; choose policies under stochastic action effects with MDPs; and learn from examples. A strong viva answer names the **model assumptions** before promising completeness or optimality.

---

# Part I — AI history, definitions, and agents

## 1. Four views of AI

| View | Goal | Typical basis | Limitation |
|---|---|---|---|
| thinking humanly | model how people actually think | cognitive science | thought is hard to observe; humans are not always rational |
| acting humanly | behavior indistinguishable from humans | Turing test | imitation is not understanding or optimality |
| thinking rationally | derive correct conclusions | logic/laws of thought | uncertainty and intractability remain |
| acting rationally | choose actions with best expected performance | rational-agent approach | needs performance measure/model/resource assumptions |

The course chiefly uses the rational-agent view. Rational does not mean omniscient or always successful: it means maximizing expected performance from the percept history, prior knowledge, available actions, and computational resources. Bad luck does not prove irrationality.

To act humanly in a text Turing test, a system needs NLP, knowledge representation, reasoning, and learning. A total Turing test adds vision/perception and robotics. Passing establishes behavioral indistinguishability under a test, not consciousness.

## 2. High-yield history and conceptual arc

The 105-page history deck is broad. Remember the progression:

- roots in Aristotelian logic, Pascal/Leibniz calculators, Babbage and Lovelace, Boolean logic, Hilbert, Gödel, Turing, ENIAC, and stored-program computers;
- Turing's 1950 imitation-game question and the 1956 Dartmouth naming of artificial intelligence;
- early symbolic successes in games, Logic Theorist/theorem proving, planning, and knowledge represented by logic, semantic networks, and production rules;
- expert systems such as DENDRAL and MYCIN: strong narrow knowledge plus inference, but costly knowledge acquisition, maintenance, uncertainty, and brittleness;
- subsymbolic lineage from McCulloch–Pitts neural models to connectionist/statistical learning;
- robotics examples: light-seeking tortoises, Shakey, Stanford cart, Dante, Sojourner/rovers, DARPA vehicles, Aibo, Cog, and Roomba;
- NLP examples: speech, translation, retrieval, and ambiguity (`bass`, attachment, context/world knowledge);
- chess: simple rules do not imply a small state space; Deep Blue was major narrow-AI engineering, not general intelligence.

**Symbolic AI** manipulates explicit rules/symbols and is often interpretable/compositional but can be brittle. **Subsymbolic AI** learns numerical/distributed mappings and handles perception/noise well but can be data-hungry and opaque. Modern systems can combine them.

Early predictions underestimated combinatorial explosion, compute/data needs, and hidden commonsense/domain knowledge. A tree growing as $b^d$ becomes enormous after a modest depth increase.

## 3. Agent, percept, action, rationality

An agent perceives through sensors and acts through actuators. A percept is current input; a percept sequence is the full history. An abstract agent function is

$$f:P^*\rightarrow A.$$

An agent program implements that function on an architecture. Rationality depends on performance measure, percept history, prior knowledge/model, and available actions. Autonomy means behavior increasingly reflects experience, not that an agent begins with zero built-in knowledge.

## 4. PEAS

PEAS = **Performance measure, Environment, Actuators, Sensors**.

Autonomous taxi:

- P: safety, legality, time, comfort, fuel/cost;
- E: road, traffic, pedestrians, weather, passengers;
- A: steering, accelerator, brake, indicators, display/speech;
- S: camera/lidar/radar, GPS, speed/engine sensors, microphone.

Medical diagnosis:

- P: accuracy/outcome, low risk/cost, timely decision;
- E: patient, diseases, clinic/lab;
- A: questions, tests, diagnosis/treatment recommendation;
- S: symptoms, history, physical findings, results.

Do not list a sensor as a performance measure or confuse the environment with observations of it.

## 5. Environment dimensions

| Dimension | Contrast | Question |
|---|---|---|
| observability | fully vs partially observable | does the percept expose all relevant state? |
| determinism | deterministic vs stochastic | do state+action uniquely fix next state? |
| episode relation | episodic vs sequential | does today's action affect later decisions? |
| change | static vs dynamic/semidynamic | can the world/performance change while deliberating? |
| representation | discrete vs continuous | are state/action/time/percepts discrete? |
| participants | single vs multi-agent | do strategic others affect performance? |
| model | known vs unknown | are action outcomes initially known? |

Crossword solving is mostly fully observable, deterministic, sequential, static, discrete, single-agent. Driving is partially observable, stochastic, sequential, dynamic, mostly continuous, multi-agent. A chess clock makes performance semidynamic even while the board waits.

## 6. Agent architectures

1. table-driven: conceptual percept-history lookup, not scalable;
2. simple reflex: condition–action rules from current percept;
3. model-based reflex: internal state plus transition/sensor model;
4. goal-based: consider future states to reach a goal;
5. utility-based: rank trade-offs/uncertainty by expected utility;
6. learning agent: performance element acts, learning element improves, critic supplies feedback, problem generator encourages exploration.

A goal says acceptable/unacceptable; utility says how desirable outcomes are, enabling trade-offs.

---

# Part II — Problem formulation and generic search

## 7. Search-problem formulation

A classical problem needs initial state $s_0$, actions $A(s)$, transition $Result(s,a)$, goal test, and step cost $c(s,a,s')$ whose sum is path cost $g(n)$. A **state** is a world configuration; a **node** is a record containing state, parent, action, depth, and cost. Different nodes may contain the same state.

Slide examples:

- Romania: state=current city, action=connected road, goal=Bucharest, cost=distance;
- 8-puzzle: tile arrangement and legal blank moves, usually unit cost;
- 8-queens: incremental placements or complete-state local search;
- water jugs: $(x,y)$ amounts with fill/empty/pour actions;
- TSP: current city+visited set, goal=tour, cost=distance;
- assembly/VLSI: configurations and geometry/quality cost;
- classifier learning as optimization over parameter settings.

Abstraction discards irrelevant details while retaining solution validity. Too much detail is infeasible; too little yields plans invalid in reality.

## 8. Tree search versus graph search

Tree search can regenerate states and loop. Graph search uses explored/frontier records, but duplicates are cost-sensitive: BFS with unit costs can mark on first discovery; UCS/A* must replace a state when a cheaper $g$ is found; A* with an inconsistent heuristic may need to reopen an expanded state. Failure to detect repeats can turn a small state space into an exponential/infinite tree.

```text
State graph:                         Tree-search nodes:

      S                                   S
     / \                                 / \
    A   B                               A   B
     \ /                                 \ /
      C                              C(copy 1) C(copy 2)

The world has one state C. Tree search may create two node records for it.
Graph search keeps a state-keyed best record, but may replace/reopen it when
a cheaper path is discovered.
```

## 9. Generic best-first graph search

Invariant: `best_g[s]` is the cheapest discovered cost to `s`; stale queue entries are ignored and improvements reopen states.

```python
from dataclasses import dataclass
from heapq import heappush, heappop
from itertools import count
from math import inf

@dataclass
class Node:
    state: object
    parent: "Node | None"
    action: object
    g: float
    depth: int

def best_first(start, is_goal, successors, priority):
    ticket = count()
    root = Node(start, None, None, 0, 0)
    frontier = [(priority(root), next(ticket), root)]
    best_g = {start: 0}
    while frontier:
        _, _, node = heappop(frontier)
        if node.g != best_g.get(node.state, inf):
            continue
        if is_goal(node.state):       # pop, not merely generate, for UCS/A*
            return node
        for action, nxt, cost in successors(node.state):
            new_g = node.g + cost
            if new_g < best_g.get(nxt, inf):
                child = Node(nxt, node, action, new_g, node.depth + 1)
                best_g[nxt] = new_g
                heappush(frontier, (priority(child), next(ticket), child))
    return None
```

Use priority $g$ for UCS, $h$ for greedy, and $g+h$ for A*. Goal testing on generation only proves some path reached the goal; popping the valid minimum establishes the cost-ordering claim.

---

# Part III — Uninformed search

## 10. Criteria and notation

$b$=branching factor, $d$=shallowest-goal depth, $m$=maximum depth, $\ell$=depth limit, $C^*$=optimal cost, and $\epsilon>0$=minimum positive step cost. Judge completeness, optimality, time, and space; complexity can differ slightly by goal-test convention.

## 11. Breadth-first search

BFS expands the shallowest node with FIFO.

```python
from collections import deque

def bfs(start, is_goal, neighbors):
    q, parent = deque([start]), {start: None}
    while q:
        u = q.popleft()
        if is_goal(u): return parent, u
        for v in neighbors(u):
            if v not in parent:
                parent[v] = u
                q.append(v)
    return parent, None
```

For finite $b$: complete; optimal only for equal/unit costs (or the corresponding monotone-by-depth condition); time and space $O(b^{d+1})$ in the slide convention. On `A:{B,C}`, `B:{D,E}`, `C:{F,G}`, the frontier is `[A]`, `[B,C]`, `[C,D,E]`, `[D,E,F,G]`.

## 12. Uniform-cost search

UCS expands minimum $g(n)$. It is complete if each step costs at least $\epsilon>0$ and relevant branching is finite; optimal with nonnegative costs and correct duplicate/decrease handling; common bound $O(b^{1+\lfloor C^*/\epsilon\rfloor})$ time/space. It equals BFS when all costs are equal.

Counterexample to generation-goal testing: `S-G=10`, `S-A=1`, `A-G=2`. UCS pops A, improves G to 3, then pops G. Negative edges invalidate the settled-minimum argument; infinite zero-cost regions break the usual $\epsilon$ completeness proof.

## 13. Depth-first search

DFS uses recursion/LIFO and expands deepest first. Tree DFS is incomplete in infinite-depth/cyclic spaces, not optimal, takes $O(b^m)$ time and $O(bm)$ depth-first space. Its benefit is memory and sometimes fast discovery when solutions are dense.

## 14. Depth-limited and iterative deepening search

DLS does not expand below $\ell$ and distinguishes **cutoff** from definitive failure.

```python
CUTOFF = object()

def dls(s, is_goal, neighbors, limit, path=frozenset()):
    if is_goal(s): return [s]
    if limit == 0: return CUTOFF
    cut = False
    for v in neighbors(s):
        if v in path: continue
        r = dls(v, is_goal, neighbors, limit - 1, path | {s})
        if r is CUTOFF: cut = True
        elif r is not None: return [s] + r
    return CUTOFF if cut else None
```

DLS costs $O(b^\ell)$ time and $O(b\ell)$ space, and is complete only with sufficient limit. IDS runs limits $0,1,2,\ldots$:

$$N_{IDS}=(d+1)b^0+d b^1+\cdots+b^d=O(b^d).$$

For the slide's $b=10,d=5$, one DLS through depth 5 generates

$$1+10+10^2+10^3+10^4+10^5=111{,}111$$

nodes, while IDS generates

$$6+50+400+3{,}000+20{,}000+100{,}000=123{,}456.$$

The slide prints `123,450`; that is an arithmetic typo. Its printed BFS value `1,111,100` is also inconsistent with the geometric sum: BFS through depth 6 generates $1{,}111{,}111$ nodes including the root, or $1{,}111{,}110$ excluding it. IDS is complete for finite $b$, optimal for unit/increasing-by-depth cost, $O(b^d)$ time, and $O(bd)$ space.

## 15. Bidirectional search

Search from start and explicit goal until frontiers meet. Balanced BFS costs $O(b^{d/2})$ time and space. It requires computable predecessors/reverse actions, correct intersection checks, and manageable explicit goals. Multiple/implicit goals, directed/weighted transitions, and predecessors of checkmate complicate it; two naive BFSs do not solve a weighted problem optimally.

## 16. Comparison

| Strategy | Selection | Complete? | Optimal? | Time | Space |
|---|---|---|---|---:|---:|
| BFS | shallowest | finite $b$ | equal costs | $O(b^{d+1})$ | $O(b^{d+1})$ |
| UCS | minimum $g$ | $c\ge\epsilon$ | nonnegative costs | cost-contour bound | same order |
| DFS | deepest | no in general | no | $O(b^m)$ | $O(bm)$ |
| DLS | depth up to $\ell$ | if sufficient | no generally | $O(b^\ell)$ | $O(b\ell)$ |
| IDS | increasing limits | yes | equal costs | $O(b^d)$ | $O(bd)$ |
| bidirectional BFS | two frontiers | conditional | unit costs | $O(b^{d/2})$ | $O(b^{d/2})$ |

# Part IV — Informed and memory-bounded search

## 17. Greedy and A*

A heuristic $h(n)$ estimates cheapest remaining goal cost. Greedy uses $f=h$, UCS $f=g$, and A* $f=g+h$. Greedy ignores money already spent, so it is not generally optimal or complete in unbounded spaces.

### Romania trace

Greedy follows Arad→Sibiu ($h=253$)→Făgăraș ($176$)→Bucharest, cost $450$. A* orders:

| Candidate | $g$ | $h$ | $f$ |
|---|---:|---:|---:|
| Arad | 0 | 366 | 366 |
| Sibiu | 140 | 253 | 393 |
| Rîmnicu via Sibiu | 220 | 193 | 413 |
| Făgăraș via Sibiu | 239 | 176 | 415 |
| Pitești via Rîmnicu | 317 | 100 | 417 |
| Bucharest via Pitești | 418 | 0 | 418 |
| Bucharest via Făgăraș | 450 | 0 | 450 |

It returns Arad–Sibiu–Rîmnicu–Pitești–Bucharest at 418.

## 18. Admissibility, consistency, reopening

Admissible means

$$0\le h(n)\le h^*(n).$$

Consistent means for every edge

$$h(n)\le c(n,a,n')+h(n').$$

Then $f(n')=g(n)+c+h(n')\ge g(n)+h(n)=f(n)$, so $f$ is nondecreasing on a path. A* tree search is optimal with admissible $h$ under standard conditions. Graph A* can permanently close a popped node with consistent $h$; with admissible but inconsistent $h$, reopen a state when a better $g$ appears. Consistency normally implies admissibility when $h(goal)=0$ and goals are reachable.

Example: edges `S-A:2,S-B:2,A-C:2,B-C:1,C-G:2`, with $h(A)=3,h(B)=3,h(C)=0,h(G)=0$. These are admissible, but $h(B)>1+h(C)$. A tie can expand A then C at $g=4$; B later reveals C at $g=3$. Refusing to reopen can retain goal cost 6 instead of optimum 5.

Dominance: if admissible $h_2(n)\ge h_1(n)$ everywhere, $h_2$ dominates $h_1$ and under comparable conditions expands no more nodes. A costly heuristic may still increase total runtime.

## 19. A* optimality proof and the reported $h=0$ question

Suppose A* is about to pop suboptimal goal $G_2$, so $f(G_2)=g(G_2)>C^*$. Some frontier node $n$ remains on an optimal route. By admissibility,

$$f(n)=g(n)+h(n)\le g(n)+h^*(n)=C^*<f(G_2),$$

a contradiction. For graph search add consistency/permanent closing or correct reopening. Completeness also needs finite branching/positive-cost assumptions so only finitely many nodes lie in the relevant $f$ contour.

If $h(n)=0$, then $f=g$: A* becomes UCS, equivalent to Dijkstra ordering for nonnegative graph edges. It remains optimal under UCS assumptions but loses heuristic direction. It is not universally "inefficient"; it simply cannot exploit heuristic information.

## 20. Building heuristics

For 8-puzzle, misplaced tiles $h_1$ and Manhattan distance $h_2$ are admissible relaxed-problem costs; Manhattan dominates misplaced tiles. Other methods: abstractions, pattern databases, and $\max(h_1,\ldots,h_k)$ (admissible if components are). Arbitrary sums can overestimate unless costs are safely partitioned/additive.

Effective branching factor solves

$$N+1=1+b^*+(b^*)^2+\cdots+(b^*)^d.$$

Lower $b^*$ means stronger guidance. A* remains exponential in worst-case time and especially memory.

## 21. RBFS and SMA*

RBFS follows the best $f$ child depth-first, remembers the best alternative bound, backs up a branch's best descendant value, and switches when the branch exceeds the limit:

```text
RBFS(node, f_limit):
    if goal: return node
    successors = expand(node); if none return failure,infinity
    for s: s.f = max(g(s)+h(s), node.f)
    loop:
        best = least-f successor
        if best.f > f_limit: return failure,best.f
        alternative = second-least f
        result,best.f = RBFS(best, min(f_limit,alternative))
        if result succeeds: return result,best.f
```

It uses linear memory but may regenerate/change its mind; standard RBFS is optimal with admissible $h$. SMA* uses available memory like A*, then deletes the worst leaf, backs its value into its parent, and can regenerate it. It returns the best solution reachable within memory; if one root-goal path cannot fit, that goal is not memory-reachable. Time may remain exponential.

---

# Part V — Local search and metaheuristics

## 22. Hill climbing, beam search, gradient descent

Local search retains complete candidate states rather than paths, so memory is small. Landscapes contain global/local optima, plateaus, shoulders, and ridges.

```python
def hill_climb(initial, neighbors, value):
    current = initial
    while True:
        candidate = max(neighbors(current), key=value, default=current)
        if value(candidate) <= value(current): return current
        current = candidate
```

Variants include stochastic, first-choice, bounded sideways moves, and random restart. With independent success probability $p$, expected trials are $1/p$ and failed restarts $(1-p)/p$.

Local beam search keeps $k$ states, generates all successors, and retains the best $k$ globally. It shares information, unlike $k$ independent climbers, but can lose diversity.

For differentiable cost,

$$\theta_{t+1}=\theta_t-\eta\nabla J(\theta_t).$$

Large $\eta$ can overshoot/diverge; small $\eta$ is slow. Gradient dependence motivates derivative-free alternatives for nonsmooth objectives/local traps.

## 23. Simulated annealing

For minimizing energy, $\Delta=E_{new}-E_{current}$:

$$P(accept)=\begin{cases}1,&\Delta\le0,\\e^{-\Delta/T},&\Delta>0.\end{cases}$$

High $T$ explores; $T\to0$ approaches hill climbing. Rapid cooling (quenching) can freeze a metastable solution.

```python
from math import exp
from random import random, choice

def simulated_annealing(initial, neighbors, cost, schedule, steps):
    current = best = initial
    for t in range(steps):
        T = schedule(t)
        if T <= 0: break
        nxt = choice(list(neighbors(current)))
        delta = cost(nxt) - cost(current)
        if delta <= 0 or random() < exp(-delta/T):
            current = nxt
            if cost(current) < cost(best): best = current
    return best
```

For maximization, define $\Delta=value(new)-value(current)$ and accept worse ($\Delta<0$) with $e^{\Delta/T}$; do not mix signs.

The alternative-learning excerpt gives continuous proposals. Gaussian:

$$q(\Delta x)=\frac1{\sqrt{2\pi T}}e^{-\Delta x^2/(2T)};$$

Cauchy:

$$q(\Delta x)=\frac1\pi\frac{T}{T^2+\Delta x^2}.$$

Cauchy heavy tails allow larger jumps; shrinking scale moves exploration to exploitation. A CDF $F(x)=P(X\le x)$ is nondecreasing/right-continuous with limits 0 and 1.

Schedules in the excerpt:

$$T_t=\alpha^tT_0,\quad T_t=T_0-\beta t,\quad T_t=\frac{T_0}{\log(1+t)},\quad T_t=\frac{T_0}{1+t}.$$

A schedule defines initial temperature, trials per temperature, decrement, and stop. For target initial worse-move acceptance $\chi_0$, $T_0=-\overline{\Delta E}/\ln\chi_0$ (the minus is required since $\ln\chi_0<0$). Log cooling has asymptotic global-convergence results under strong conditions but is impractically slow; finite SA has no ordinary global-optimum guarantee.

For neural training, flatten weights/biases to a vector, use network error as energy, perturb weights, and retain the best. It is derivative-free/nondifferentiable-friendly but evaluation-intensive.

## 24. Genetic algorithms

```text
randomly initialize population
evaluate fitness
repeat until budget/quality stop:
    select parents biased by fitness
    crossover/recombine
    mutate with small probability
    evaluate offspring
    select survivors (possibly retain elite)
return best seen
```

Genotype/chromosome is encoding; phenotype is decoded solution; fitness is selection score. Roulette, tournament, and rank selection are alternatives. Crossover combines parents; mutation restores variation; replacement determines next generation.

Slide roulette example: fitnesses 23,12,25,5,17 sum 82, probabilities about `.28,.15,.30,.06,.21`, cumulative `.28,.43,.73,.79,1.00`. Draw $r\in[0,1)$ and choose its interval. Negative/zero raw scores need transformation or another method.

Selection alone destroys diversity; selection+crossover can prematurely converge; mutation alone resembles random walk; excessive mutation destroys inheritance. Permutation encodings require specialized crossover to avoid duplicate/missing items. The graph-partition example assigns a bit per node; the two bit values indicate partitions and fitness reflects cut/balance. Neural weights/architectures can be chromosomes, but functionally equivalent hidden-neuron permutations cause alignment problems.

Related excerpt methods: evolutionary programming emphasizes mutation/survivor selection; evolution strategies often use real vectors and self-adaptive mutation; genetic programming evolves program trees. GAs/metaheuristics are broad derivative-free search, not automatic global-optimum machines.

### Mapping alternative search to neural-network training

The source’s alternative-learning excerpt is not a separate neural-network architecture lesson; it maps the search algorithms above onto weight optimization:

```text
search state / chromosome     = all trainable weights (and sometimes architecture)
objective / energy            = training loss L(w)
neighbor or mutation          = perturb selected weights: w' = w + delta
fitness                       = a monotone transformation of validation/training quality
best-seen state               = lowest-loss parameter vector encountered
```

Simulated annealing accepts an improving weight vector and may accept a worse one with probability $e^{-[L(w')-L(w)]/T}$. A genetic algorithm keeps a population of encoded weight vectors, then selects, crosses, and mutates them. These methods do not require a differentiable activation/loss and may escape some local basins, but high-dimensional neural weights make blind proposals expensive. Ordinary backpropagation exploits gradient structure and is usually far more sample/compute efficient. Neither finite SA nor an ordinary GA guarantees the global neural-network optimum.

---

# Part VI — Adversarial search

## 25. Game model and minimax

Main assumptions: two-player, alternating, deterministic, zero-sum, finite, perfect information. Define initial state/player, actions/result, terminal test, and terminal utility. MAX wants high utility; MIN low.

$$V(s)=\begin{cases}Utility(s),&terminal,\\\max_aV(Result(s,a)),&MAX,\\\min_aV(Result(s,a)),&MIN.\end{cases}$$

```python
def minimax_decision(state, actions, result, terminal, utility):
    def value(s, maximizing):
        if terminal(s): return utility(s)
        vals = (value(result(s,a), not maximizing) for a in actions(s))
        return max(vals) if maximizing else min(vals)
    return max(actions(state), key=lambda a: value(result(state,a), False))
```

If root MIN children have leaves A=`[3,12,8]`, B=`[2,4,6]`, C=`[14,5,2]`, their values are 3,2,2 and MAX chooses A—not visible leaf 14. Full minimax is complete for a finite tree, optimal against optimal play, $O(b^m)$ time and depth-first $O(bm)$ space.

```text
                         MAX = 3
                         /     \
                    MIN A=3   MIN B<=2
                     /  \       / | \
                    3    5     2  ×  ×

Search A first: root alpha becomes 3.
At B, the first leaf makes beta=2. Since beta <= alpha, the remaining
B leaves cannot make MAX prefer B, so alpha-beta prunes them.
```

A minimax strategy guarantees the game value against every legal response. A weak opponent may allow better, but pure minimax does not explicitly model or maximally exploit their mistake pattern.

## 26. Reported infinite-depth question

1. Finite completely generated tree with correct utilities: minimax computes game-theoretic value. A human cannot force better than that value. If agent can force win it wins; if it can force draw, human cannot force win; if its starting position is theoretically lost, perfect human can beat it because no saving move exists.
2. Literal infinite generation cannot finish. A nonterminating/cyclic game needs draws, limits, discounting, or mathematical fixed-point/value conditions; ordinary terminal backup may be undefined.
3. Real cutoff depth, imperfect evaluation, time/memory, hidden information, stochasticity, or bugs can be exploited.

Short answer: exact minimax cannot make a game-theoretic mistake, but the outcome is bounded by the position's value; literal infinite search is not computable.

## 27. Alpha–beta pruning

$\alpha$ is MAX's best guaranteed ancestor value; $\beta$ is MIN's best. Prune when $\alpha\ge\beta$.

```python
from math import inf

def alpha_beta(s, maximizing, alpha, beta, actions, result, terminal, utility):
    if terminal(s): return utility(s)
    if maximizing:
        v = -inf
        for a in actions(s):
            v = max(v, alpha_beta(result(s,a), False, alpha, beta,
                                  actions,result,terminal,utility))
            if v >= beta: return v
            alpha = max(alpha,v)
        return v
    v = inf
    for a in actions(s):
        v = min(v, alpha_beta(result(s,a), True, alpha, beta,
                              actions,result,terminal,utility))
        if v <= alpha: return v
        beta = min(beta,v)
    return v
```

Trace: first MIN child `[3,5]` returns 3, so root $\alpha=3$. Next MIN child sees 2, so $\beta=2\le\alpha$ and its remaining leaves are irrelevant. Alpha–beta returns identical minimax choice. Worst $O(b^m)$; ideal ordering $O(b^{m/2})$, roughly double depth. Ordering changes work, not correctness.

## 28. Cutoff, evaluation, horizon, chance

Practical search replaces terminal utility at a cutoff with

$$Eval(s)=w_1f_1(s)+\cdots+w_kf_k(s).$$

Non-quiescence means cutoff in an unstable tactic; quiescence search extends volatile positions. Horizon effect postpones unavoidable harm beyond cutoff. Iterative deepening always retains the last completed move and improves ordering.

Chance node:

$$V(s)=\sum_iP(i\mid s)V(Result(s,i)).$$

Expectiminimax maximizes at MAX, minimizes at MIN, averages at chance. Multiplayer games can back up a utility vector and let player $i$ maximize component $i$. Hidden-information/stochastic games do not satisfy ordinary minimax assumptions.

---

# Part VII — Constraint satisfaction

## 29. CSP model and examples

$$CSP=(X,D,C),$$

variables, domains, constraints. A solution is complete and consistent. Constraints can be unary, binary (constraint graph edge), or global/higher-order such as `AllDifferent`. Examples: map coloring, cryptarithmetic, scheduling, assignment, configuration, queens.

Australian map variables `WA,NT,Q,NSW,V,SA,T` use `{R,G,B}` and adjacent regions differ. If `WA=R`, forward checking removes R from `NT,SA`; if `NT=G`, `SA` is forced B.

## 30. Backtracking and heuristics

Backtracking does DFS over partial assignments; assignments commute, so it assigns one variable per level rather than permuting assignment order.

```python
def backtrack(assignment, variables, domains, neighbors, consistent):
    if len(assignment) == len(variables): return assignment.copy()
    unassigned = [x for x in variables if x not in assignment]
    var = min(unassigned, key=lambda x:(len(domains[x]),
              -sum(y not in assignment for y in neighbors[x])))
    for value in domains[var]:
        if all(y not in assignment or consistent(var,value,y,assignment[y])
               for y in neighbors[var]):
            assignment[var]=value
            r=backtrack(assignment,variables,domains,neighbors,consistent)
            if r is not None: return r
            del assignment[var]
    return None
```

MRV chooses fewest legal values (fail first); degree breaks ties by most constraints on unassigned variables; LCV tries the value eliminating fewest neighbor values. Worst case remains $O(d^n)$.

## 31. Forward checking and AC-3

Forward checking removes values from unassigned neighbors after assignment; it misses contradictions solely among unassigned variables. Arc $X_i\to X_j$ is consistent if every $x\in D_i$ has supporting $y\in D_j$.

```python
from collections import deque

def ac3(domains, neighbors, allowed):
    q=deque((x,y) for x in domains for y in neighbors[x])
    while q:
        x,y=q.popleft(); revised=False
        for vx in set(domains[x]):
            if not any(allowed(x,vx,y,vy) for vy in domains[y]):
                domains[x].remove(vx); revised=True
        if revised:
            if not domains[x]: return False
            for z in neighbors[x]-{y}: q.append((z,x))
    return True
```

Standard time $O(ed^3)$; slide dense form $O(n^2d^3)$. Arc consistency does not imply a globally consistent complete assignment.

## 32. Cryptarith and min-conflicts

For `TWO+TWO=FOUR`, letters are distinct digits, leading `T,F` nonzero, carries small-domain:

$$2O=R+10c_1,$$
$$2W+c_1=U+10c_2,$$
$$2T+c_2=O+10F.$$

Min-conflicts begins with a complete assignment, chooses a conflicted variable, assigns a minimum-conflict value, and restarts if necessary. It is highly effective for large queens but not complete in a bounded run. Backtracking is systematic/complete for finite CSPs; min-conflicts is repair-based.

# Part VIII — Probability and Bayesian networks

## 33. Probability foundation

$$P(A\mid B)=\frac{P(A\cap B)}{P(B)},\qquad P(A,B)=P(A\mid B)P(B),$$

$$P(A\mid B)=\frac{P(B\mid A)P(A)}{P(B)},\qquad P(B)=\sum_iP(B\mid H_i)P(H_i).$$

Prior $P(H)$ is belief before evidence; likelihood $P(E\mid H)$ is evidence probability under hypothesis; $P(E)$ normalizes; posterior $P(H\mid E)$ is updated belief.

Base-rate example: prevalence 1%, sensitivity 99%, false-positive 5%:

$$P(D\mid +)=\frac{.99(.01)}{.99(.01)+.05(.99)}\approx.1667.$$

Sensitivity $P(+\mid D)$ is not posterior $P(D\mid+)$. Independence $X\perp Y$ means factorization; conditional independence $X\perp Y\mid Z$ is a different statement and need not imply marginal independence.

## 34. Bayesian-network definition and factorization

A BN is a DAG of random variables plus CPD/CPT $P(X_i\mid Parents(X_i))$ per node. For a topological order,

$$P(x_1,\ldots,x_n)=\prod_iP(x_i\mid parents(X_i)).$$

The local Markov property is: a node is independent of its **nondescendants** given parents—not literally every other node. Edges are probabilistic dependency; causal meaning requires a justified causal model.

If a child has $r$ values and parent cardinalities $q_1,\ldots,q_k$, rows are $\prod q_j$, full displayed cells $r\prod q_j$, and independent stored probabilities $(r-1)\prod q_j$. Thus a Boolean child with $k$ Boolean parents stores $2^k$ independent values. Slide exercise: four-state A with 3-state and Boolean parents has 6 rows, 24 cells, or 18 independent entries. State the convention.

## 35. Alarm network and worked joint

```text
Burglary ---> Alarm <--- Earthquake
                |  \
                v   v
          JohnCalls  MaryCalls
```

$$P(B,E,A,J,M)=P(B)P(E)P(A\mid B,E)P(J\mid A)P(M\mid A).$$

The diagram's numbers:

- $P(B)=.001$, $P(E)=.002$;
- $P(A\mid B,E)=.95$, $P(A\mid B,\neg E)=.94$, $P(A\mid\neg B,E)=.29$, $P(A\mid\neg B,\neg E)=.001$;
- $P(J\mid A)=.90$, $P(J\mid\neg A)=.05$;
- $P(M\mid A)=.70$, $P(M\mid\neg A)=.01$.

Ten independent values are stored. Slide calculation:

$$P(a,\neg b,\neg e,j,m)=.999(.998)(.001)(.9)(.7)\approx.000628.$$

This is a complete-assignment joint, not burglary posterior. $J\perp M\mid A$. Roots B and E are marginally independent, but conditioning on their common effect A makes them dependent (**explaining away**). Chains/forks are blocked by conditioning on the middle; a collider is normally blocked but becomes active when collider/descendant is observed.

## 36. Enumeration and variable elimination

For query B given calls, hidden A,E:

$$P(B\mid j,m)=\alpha P(B)\sum_eP(e)\sum_aP(a\mid B,e)P(j\mid a)P(m\mid a).$$

The slide gets unnormalized $\langle.00059224,.0014919\rangle$ and normalized $\langle.284,.716\rangle$. Calls raise burglary from .001 to .284 but do not prove it.

VE steps: make factors; restrict evidence; choose hidden-variable order; multiply all factors containing a hidden variable; sum it out; multiply remaining factors; normalize.

```text
VARIABLE-ELIMINATION(X,e,BN):
    factors = [restrict each CPT by e]
    for hidden Z in chosen order:
        bucket = factors mentioning Z
        replace bucket by sum_out(Z, multiply(bucket))
    return normalize(multiply(factors) over X)
```

For alarm, restrict J/M factors, eliminate E, eliminate A, multiply by P(B), normalize. Multiplying factors joins compatible rows; summing groups rows differing only in eliminated variable. Order controls largest intermediate factor/treewidth; optimal order is NP-hard. Exact marginal inference is #P-hard in general (the slide's `#NP` wording is not a standard correct class label). Repeatedly remove leaves that are neither query/evidence nor their ancestors.

---

# Part IX — Hidden Markov models

## 37. Model and queries

$X_t$ is hidden state; $E_t$ observed emission. First-order transition $P(X_t\mid X_{t-1})$, sensor $P(E_t\mid X_t)$, stationary parameters when unchanged over time. Joint:

```text
hidden chain:       X1  --->  X2  --->  X3  ---> ... ---> XT
                     |         |         |               |
observations:        v         v         v               v
                    E1        E2        E3              ET

Each Xt depends on Xt-1; each Et depends on Xt.
The observed evidence does not make the hidden states independent.
```

$$P(x_{1:T},e_{1:T})=P(x_1)P(e_1\mid x_1)\prod_{t=2}^TP(x_t\mid x_{t-1})P(e_t\mid x_t).$$

Higher-order dependence can expand the state/history. The slides use hidden Rain and observed Umbrella.

| Query | Expression |
|---|---|
| filtering | $P(X_t\mid e_{1:t})$ current |
| prediction | $P(X_{t+k}\mid e_{1:t})$ future |
| smoothing | $P(X_k\mid e_{1:t}),k<t$ past with later evidence |
| most likely explanation | $\arg\max_{x_{1:t}}P(x_{1:t}\mid e_{1:t})$ whole path |

## 38. Forward filtering and umbrella trace

$$f_t(i)=\alpha P(e_t\mid X_t=i)\sum_jP(X_t=i\mid X_{t-1}=j)f_{t-1}(j).$$

Predict through transition, correct by emission, normalize.

```python
def normalize(v):
    z=sum(v); return [x/z for x in v]

def hmm_filter(prior, transition, emissions):
    if not emissions: return prior[:]
    belief=normalize([emissions[0][i]*prior[i] for i in range(len(prior))])
    for emit in emissions[1:]:
        predicted=[sum(belief[j]*transition[j][i]
                       for j in range(len(belief)))
                   for i in range(len(belief))]
        belief=normalize([emit[i]*predicted[i] for i in range(len(belief))])
    return belief
```

Dense time $O(TN^2)$; rolling space $O(N)$. Source model:

$$P(R_t\mid R_{t-1})=.7,\;P(R_t\mid\neg R_{t-1})=.3,$$
$$P(U_t\mid R_t)=.9,\;P(U_t\mid\neg R_t)=.2,$$

prior $\langle.5,.5\rangle$. Day1 umbrella gives $\alpha\langle.45,.1\rangle=\langle.818,.182\rangle$. Predict day2 gives $\langle.627,.373\rangle$; another umbrella gives $\alpha\langle.565,.075\rangle=\langle.883,.117\rangle$.

Prediction omits emission:

$$P(X_{t+1}\mid e_{1:t})=\sum_{x_t}P(X_{t+1}\mid x_t)P(x_t\mid e_{1:t}).$$

Repeated prediction approaches stationary distribution for an ergodic chain; rate relates to mixing time. Unnormalized forward $\tilde f_t(i)=P(e_{1:t},X_t=i)$ uses same recurrence without $\alpha$, and $P(e_{1:T})=\sum_i\tilde f_T(i)$.

## 39. Smoothing and Viterbi

Backward message

$$b_k(i)=P(e_{k+1:T}\mid X_k=i),\quad b_T(i)=1,$$

$$b_k(i)=\sum_jP(j\mid i)P(e_{k+1}\mid j)b_{k+1}(j).$$

Smoothed marginal:

$$P(X_k=i\mid e_{1:T})=\alpha f_k(i)b_k(i).$$

For two umbrellas: $b_1(R)=.7(.9)+.3(.2)=.69$, $b_1(\neg R)=.3(.9)+.7(.2)=.41$. Multiply by $\langle.818,.182\rangle$ and normalize to $\langle.883,.117\rangle$: later evidence raises retrospective rain belief. Forward–backward costs $O(TN^2)$.

Viterbi:

$$\delta_t(i)=P(e_t\mid i)\max_j[\delta_{t-1}(j)P(i\mid j)],$$
$$\psi_t(i)=\arg\max_j[\delta_{t-1}(j)P(i\mid j)].$$

Choose best final state and follow backpointers, $O(TN^2)$ time and $O(TN)$ traceback memory. For `U,U,not-U`: $t_1=(.45,.10)$; $t_2=(.2835,.027)$; $t_3=(.019845,.06804)$, giving path Rain,Rain,Dry. Viterbi uses max; filtering/likelihood uses sum. Per-time marginal modes do not necessarily form the most probable joint path.

---

# Part X — Markov decision processes

## 40. MDP, policy, and return

Grid world: intended move .8, perpendicular slips .1 each, wall means stay. Fixed five-action intended outcome probability $.8^5=.32768$, so a fixed path is inadequate. A solution is a policy $\pi(s)$ for every encountered state.

An MDP is $\langle S,A,P,R,\gamma\rangle$: states, actions, $P(s'\mid s,a)$, reward, discount. It is fully observable/stochastic/Markovian. A POMDP is partially observable and normally uses belief state; the slides do not develop its algorithms.

$$G=\sum_{t=0}^\infty\gamma^tR(s_t),\qquad |G|\le\frac{R_{max}}{1-\gamma}\;(\gamma<1).$$

Reward is immediate; utility/value is expected cumulative return. Slide grid terminal rewards +1/-1, living reward -.04: 10 penalties then +1 gives .6; five gives .8. Severe negative living reward favors quick exit/risk; near zero favors caution; positive can encourage nontermination.

## 41. Bellman equations

Fixed policy:

$$U^\pi(s)=R(s)+\gamma\sum_{s'}P(s'\mid s,\pi(s))U^\pi(s').$$

Optimality:

$$U^*(s)=R(s)+\gamma\max_a\sum_{s'}P(s'\mid s,a)U^*(s').$$

$$\pi^*(s)=\arg\max_a\sum_{s'}P(s'\mid s,a)U^*(s').$$

Example backup with $R=-.04$, successor utilities `.8,.3,.5`, probabilities `.8,.1,.1`: $-.04+.8(.8)+.1(.3)+.1(.5)=.68$. Compare expected backup for every action; do not choose only the most likely successor.

## 42. Value and policy iteration

```python
def value_iteration(states, actions, transitions, reward, gamma, tol=1e-10):
    U={s:0.0 for s in states}
    while True:
        new={}; delta=0
        for s in states:
            if not actions(s): new[s]=reward(s)
            else:
                q=[sum(p*U[s2] for p,s2 in transitions(s,a))
                   for a in actions(s)]
                new[s]=reward(s)+gamma*max(q)
            delta=max(delta,abs(new[s]-U[s]))
        U=new
        if delta<tol: return U
```

For finite discounted $\gamma<1$, Bellman operator is a contraction and converges to unique $U^*$. Dense sweep $O(|S|^2|A|)$; sparse transitions help.

Policy iteration: initialize policy; evaluate its linear equations; improve each state greedily; stop when unchanged. Exact generic policy evaluation via Gaussian elimination costs $O(|S|^3)$ as slides note. Modified policy iteration uses a few evaluation sweeps because exact values may be unnecessary to identify improving actions. Value iteration improves values directly; policy iteration alternates evaluation/improvement.

---

# Part XI — Learning and decision trees

## 43. Learning concepts and hypothesis space

An agent learns when observations improve future performance. Online updates continuously; offline/batch learns from collected data. Supervised uses labeled pairs; unsupervised discovers structure; reinforcement learning uses reward/punishment. Classification has finite output; regression numeric output, often a conditional expectation/statistic.

Given $(x_i,y_i)$, search hypothesis space $H$ for $h$ that generalizes. Training fit is not generalization evidence; separate validation/test data. A problem is realizable relative to $H$ if the target belongs to $H$. Linearly separable labels are realizable by a linear classifier; nonlinear labels are not if $H$ is only linear.

Occam prefers simpler hypotheses under comparable evidence, but simplicity depends on representation/prior. MAP:

$$h_{MAP}=\arg\max_hP(h\mid D)=\arg\max_hP(D\mid h)P(h).$$

More expressive H increases fit possibilities and computational/sample difficulty. The slide's extreme all-Java-programs/Turing-machine space makes learning/evaluation potentially undecidable/nonterminating.

## 44. Decision-tree representation and entropy

Internal node tests attribute; branches outcomes; leaves predictions. A positive path is a conjunction and positive paths are ORed (DNF), so any Boolean function is representable, not necessarily compactly. With $n$ Boolean inputs, there are $2^{2^n}$ Boolean functions; majority can need large trees.

Restaurant attributes: Alternate, Bar, Fri/Sat, Hungry, Patrons, Price, Raining, Reservation, Type, WaitEstimate; target `WillWait`.

$$H(V)=-\sum_kP(v_k)\log_2P(v_k),$$

$$Gain(A)=H(E)-\sum_v\frac{|E_v|}{|E|}H(E_v).$$

Fair binary entropy is 1 bit; pure set 0. In the 12-example restaurant set, root has 6+/6− so entropy 1. `Patrons` has pure None/Some and Full with 2+/4−:

$$Remainder(Patrons)=\frac6{12}B(2/6)\approx.459,$$
$$Gain(Patrons)\approx.541.$$

`Type` is roughly balanced and near zero gain. Greedy max gain need not give globally smallest tree; minimum consistent tree is NP-hard.

## 45. Decision-tree algorithm and four base cases

1. all examples one class → leaf;
2. mixed+attributes → best split and recurse;
3. no examples at a child → parent plurality;
4. no attributes but conflicting labels → current plurality.

```python
from math import log2
from collections import Counter

def plurality(examples): return Counter(y for _,y in examples).most_common(1)[0][0]
def entropy(examples):
    c=Counter(y for _,y in examples); n=len(examples)
    return -sum((v/n)*log2(v/n) for v in c.values())
def gain(examples,a):
    groups={}
    for x,y in examples: groups.setdefault(x[a],[]).append((x,y))
    return entropy(examples)-sum(len(g)/len(examples)*entropy(g)
                                 for g in groups.values())
def learn_tree(examples,attrs,parent):
    if not examples: return ("leaf",plurality(parent))
    labels={y for _,y in examples}
    if len(labels)==1: return ("leaf",next(iter(labels)))
    if not attrs: return ("leaf",plurality(examples))
    a=max(attrs,key=lambda z:gain(examples,z)); children={}
    for v in {x[a] for x,_ in examples}:
        sub=[(x,y) for x,y in examples if x[a]==v]
        children[v]=learn_tree(sub,attrs-{a},examples)
    return ("test",a,children)
```

Production code must know unseen domain branches, deterministic ties, and candidate thresholds for continuous variables.

## 46. Overfitting, pruning, bias–variance

Overfitting = low train error but poor unseen generalization due to capacity/noise/small data/leakage. Pre-prune by depth/min-samples/gain; post-prune a subtree when validation performance does not worsen. Impute missing values from training statistics only; continuous features use learned thresholds.

For squared loss:

$$\mathbb E_{D,\epsilon}[(Y-\hat f_D(x))^2]=\sigma^2+
(\mathbb E_D[\hat f_D(x)]-f(x))^2+
\mathbb E_D[(\hat f_D(x)-\mathbb E_D\hat f_D(x))^2].$$

These are irreducible noise, squared bias, variance. Bias/variance are statistical components; underfitting/overfitting are observed behaviors. Underfitting is often associated with high bias and overfitting with high variance, but they are not definitions/synonyms. The standalone ML volume derives this fully.

---

# Part XII — Logic, applications, ethics

## 47. Formal logic — Standard-core supplement

Local slides mention logic/rules/semantic nets/theorem proving historically, not a full logic lecture.

- $KB\models\alpha$: every model satisfying KB satisfies $\alpha$ (semantic entailment);
- $KB\vdash_i\alpha$: procedure $i$ derives $\alpha$;
- sound: derives only entailed conclusions;
- complete: can derive every entailed conclusion in the target logic.

Material implication inside a sentence is not entailment between KB and conclusion. Useful equivalences: $P\to Q\equiv\neg P\lor Q$; De Morgan; remove biconditionals/implications, push negation, distribute OR over AND for CNF.

Resolution:

$$\frac{(P\lor C),(\neg P\lor D)}{C\lor D}.$$

To prove $KB\models\alpha$, add $\neg\alpha$ and derive empty clause. Propositional resolution is refutation-complete. Horn rules support forward chaining (data-driven) and backward chaining (goal-driven).

FOL adds objects, predicates, functions, quantifiers. Unification finds substitutions; occurs-check rejects $x=f(x)$. FOL resolution standardizes variables, Skolemizes existentials for refutation, converts to CNF, and unifies complementary literals. General FOL entailment is semidecidable.

## 48. Planning/applications/ethics

**Planning supplement:** actions have preconditions/effects; a plan achieves goal conditions. Search may find a plan. Local slides contrast early deliberative planning with reactive robotics but contain no full planning-algorithm unit.

Slide-grounded applications:

- NLP: synthesis vs recognition vs understanding; translation/retrieval; lexical, syntactic, contextual ambiguity and world knowledge;
- vision: recognition differs from scene understanding/action;
- robotics: sensing, state estimation, planning, reaction, and uncertain control work together;
- expert systems: narrow rule-based strength with knowledge-acquisition/maintenance/brittleness limits.

**Responsible-AI supplement:** identify affected stakeholders/harms; audit representation and subgroup errors; protect consent/privacy/provenance; test shift/robustness/misuse/calibration; provide oversight/appeal/logging/rollback; communicate limits; monitor deployment. Fairness metrics can conflict and context/law/harm determine appropriate constraints.

# Part XIII — Viva-first recall

## 49. One-minute answers

### What is AI?

AI studies computational agents that perceive an environment and choose actions to achieve goals or maximize expected performance. The rational-agent view is broader than human imitation.

### Rational versus always correct?

Rational means best expected action from available information/resources; uncertainty can still produce an unlucky outcome.

### State versus node?

State is a world configuration. Node is a search record with state, parent, action, cost, depth; multiple nodes can hold one state.

### BFS versus UCS?

BFS expands minimum depth and is optimal for equal costs. UCS expands minimum $g$ and is optimal for nonnegative costs with correct queue/duplicate assumptions.

### Why IDS despite repeated work?

Most exponential-tree nodes lie at deepest level, visited once; repeating sparse upper levels preserves $O(b^d)$ time while using $O(bd)$ memory.

### Greedy versus A*?

Greedy uses $h$ and ignores spent cost; A* uses $g+h$. A*'s optimality requires admissibility plus correct graph handling/cost assumptions.

### Admissible versus consistent?

Admissible: $h\le h^*$. Consistent: $h(n)\le c+h(n')$ per edge, making $f$ nondecreasing. Permanent-closing graph A* needs consistency; inconsistent admissible heuristics need reopening.

### A* with $h=0$?

It becomes UCS/Dijkstra ordering ($f=g$), remains optimal for nonnegative costs, and loses heuristic direction.

### Hill climb versus SA?

Hill climbing accepts improvements only and gets stuck locally. SA accepts some deterioration with temperature probability; a finite run has no global guarantee.

### Minimax and infinite depth?

Exact minimax realizes game value, so cannot make a game-theoretic mistake; if its position is theoretically lost it can still lose. Literal infinite tree generation cannot terminate, and real cutoff/evaluation errors are exploitable.

### Alpha–beta?

$\alpha$ is MAX's best guaranteed bound, $\beta$ MIN's; prune when $\alpha\ge\beta$. Same minimax answer; ideal ordering approaches $O(b^{m/2})$.

### MRV/degree/LCV?

Choose fewest legal values, tie by most unassigned-neighbor constraints, try value eliminating fewest options.

### Forward checking versus AC-3?

Forward checking propagates from the assigned variable only. AC-3 repeatedly enforces support on all directed arcs; arc-consistent does not mean solved.

### BN arrows causal?

Not automatically. A BN DAG encodes factorization/conditional dependence; causal interpretation needs causal assumptions.

### Filtering/smoothing/Viterbi?

Filtering estimates now from evidence so far; smoothing revises past using later evidence; Viterbi returns one most probable whole state path.

### MDP path versus policy?

A path is fixed action sequence; a policy maps every encountered state to an action and reacts to stochastic outcomes.

### Reward versus utility?

Reward is immediate; utility/value is expected cumulative discounted reward.

### Entropy/information gain?

Entropy measures uncertainty/impurity. Gain is entropy before minus weighted entropy after; greedy max gain is local, not global-tree optimality.

## 50. Invariants and complexities

| Algorithm | Essential invariant/answer condition | Time | Space |
|---|---|---:|---:|
| BFS | FIFO, mark discovery | $O(b^{d+1})$ | $O(b^{d+1})$ |
| UCS | priority $g$, best-g, goal on pop | $O(b^{1+\lfloor C^*/\epsilon\rfloor})$ common bound | same order |
| DFS | current path/LIFO | $O(b^m)$ | $O(bm)$ |
| DLS | cutoff distinct from failure | $O(b^\ell)$ | $O(b\ell)$ |
| IDS | DLS limits 0,1,... | $O(b^d)$ | $O(bd)$ |
| bidirectional BFS | correct reverse/intersection | $O(b^{d/2})$ | $O(b^{d/2})$ |
| A* | min $g+h$, reopen improvement if needed | exponential worst | exponential memory |
| minimax | alternate max/min terminal backup | $O(b^m)$ | $O(bm)$ |
| alpha–beta | maintain $\alpha,\beta$ | worst $O(b^m)$; ideal $O(b^{m/2})$ | $O(bm)$ |
| CSP backtracking | consistent partial assignment/restore domains | $O(d^n)$ worst | depth+domains |
| AC-3 | queue arcs whose support may change | $O(ed^3)$ | arcs+domains |
| HMM forward/backward | message after each evidence | $O(TN^2)$ | $O(N)$ rolling |
| Viterbi | max score+backpointer | $O(TN^2)$ | $O(TN)$ traceback |
| dense VI sweep | coherent Bellman backup | $O(|S|^2|A|)$ | $O(|S|)$ |
| policy evaluation | fixed-policy linear system | generic $O(|S|^3)$ | system storage |

## 51. Common wrong answers repaired

- "Rational means correct." → best expected action, not guaranteed outcome.
- "BFS finds cheapest." → only equal/unit costs.
- "UCS accepts generated goal." → accept when popped at minimum valid $g$.
- "Graph search never revisits." → cheaper path/reopening can be necessary.
- "Admissible equals consistent." → consistency is stronger edgewise triangle condition.
- "A* optimal with any h." → state heuristic/cost/graph assumptions.
- "$h=0$ makes BFS." → UCS; BFS only when equal costs.
- "SA accepts every bad move." → accepts with $e^{-\Delta/T}$ under minimization.
- "GA guarantees global optimum." → no ordinary finite-run guarantee.
- "Minimax predicts the human." → worst optimal response, not psychology.
- "Alpha–beta changes result." → only avoids irrelevant work.
- "Arc-consistent means solved." → local support can coexist with global failure.
- "BN edge proves cause." → not without causal model.
- "Conditioning removes dependence." → conditioning collider can create it.
- "Viterbi is filtering." → max path/backpointers versus sum marginals.
- "MDP solution is route." → state-action policy.
- "Entropy is error." → information/impurity, different metric.
- "Bias/variance equal under/overfit." → components versus behavioral patterns.

## 52. Board drills

1. Draw `S-G:10,S-A:1,A-G:2` to show BFS can be weighted-wrong and UCS cost 3.
2. Prove A*: frontier optimal-path node has $f\le C^*<f(suboptimal goal)$.
3. Test consistency on each edge $h(u)\le c+h(v)$.
4. Alpha–beta: after root $\alpha=3$, MIN seeing 2 prunes remaining leaves.
5. AC-3: delete unsupported values; when a domain shrinks enqueue incoming arcs.
6. Factor alarm joint in topological order.
7. HMM: predict, multiply emission, normalize; Viterbi replaces sum by max and stores argmax.
8. Bellman: immediate reward plus discounted expected successor utility, maximize across actions.
9. Gain: parent entropy minus weighted child entropy.
10. Bias–variance: noise + squared bias + variance, then distinguish from under/overfit.

## 53. Deep-recall appendix: details that image-heavy slides can hide

### History deck page-by-page concept index

The opening photographs of Frankenstein, the Mechanical Turk, Euphonia, and R.U.R. are not claims that those devices were intelligent. They show the long cultural/engineering desire to build artificial people, calculation, speech, and labor. R.U.R. also popularized "robot" from the Czech labor root. The later timeline connects logic and machinery to formal computation and stored programs.

The slides then ask how intelligence should be recognized. Turing replaces an inaccessible question about inner essence with an operational conversation test. Early chat programs can produce isolated plausible lines, but scripted surface behavior exposes the difference among word manipulation, grounded knowledge, and understanding. Searle's Chinese Room is a philosophical argument about whether correct symbol manipulation is sufficient for understanding; it does not prove that every AI system is impossible.

Three recurring limits explain the rise/fall cycles of optimism:

1. **scale:** branching multiplies and toy domains hide it;
2. **knowledge:** common sense humans use without noticing must be represented or learned;
3. **ambiguity/noise:** perception/language rarely provides one clean symbolic interpretation.

The knowledge-representation sequence moves through logic, semantic networks, experience/scripts, rules, and probabilistic confidence. Each representation privileges certain inference. Expert systems separate a knowledge base from an inference engine; hand entry makes expertise explicit but creates acquisition, validation, update, and brittleness costs. Machine learning shifts part of that burden to examples but introduces data/generalization problems.

The NLP pages distinguish:

- speech synthesis (produce waveform), speech recognition (waveform→words), and language understanding (words/context→meaning/action);
- lexical ambiguity (`bass`), structural ambiguity (prepositional-phrase attachment), and semantic/pragmatic ambiguity requiring world knowledge;
- translation as more than dictionary substitution; retrieval finds relevant text while extraction structures facts.

Robotics progresses from planned movement in carefully modeled worlds to perception-rich/reactive and hybrid systems. A robot needs mechanical actuation/control in addition to an AI planner. The final history pages deliberately raise emotion, creativity, consciousness, and understanding: capability evidence should be separated from philosophical attribution. A program producing a painting is evidence of generated output, not by itself a proof of subjective experience.

### Search implementation details

IDS driver must continue only on cutoff; ordinary failure means increasing the limit cannot reveal a deeper node in that finite branch formulation:

```python
from itertools import count

def iterative_deepening(start, is_goal, neighbors):
    for limit in count(0):
        result = dls(start, is_goal, neighbors, limit)
        if result is not CUTOFF:
            return result             # solution or definitive failure
```

Tie-breaking can change expansions but not the correctness theorem when its assumptions hold. Deterministic tie-breaking makes a trace reproducible. In graph search, storing only a Boolean visited flag is inadequate for UCS/A*: store cheapest $g$. With floating costs use a tolerance or immutable exact representation where appropriate rather than brittle direct equality.

A* contours contain nodes of increasing $f$. With $h=0$, contours resemble cost-distance circles; a useful heuristic stretches them toward the goal. A* necessarily expands all nodes with $f<C^*$ under its normal theorem and may expand some with $f=C^*$ depending on ties. "Optimally efficient" means no equally informed optimal algorithm can guarantee fewer expansions under the theorem's comparison conditions—not that A* has polynomial runtime.

### Local-search diagnostics

For 8-queens complete-state search, one queen per column gives $8^8$ assignments; objective can be number of attacking pairs. Moving a queen within its column changes conflicts. A state with one remaining conflict can still be a local minimum. Sideways moves traverse plateaus but must be bounded to avoid cycles.

SA parameters interact: proposal scale controls neighborhood distance; temperature controls willingness to accept deterioration; cooling controls how long exploration lasts; iterations per temperature control equilibration. Returning the final state can discard a better state visited earlier, hence code retains `best` separately.

In GA roulette selection, selection probability is $p_i=f_i/\sum_jf_j$ only for suitable nonnegative fitness. One-point crossover of `101|001` and `011|010` yields `101010` and `011001`; mutation flips a chosen bit. Elitism protects the best from accidental loss but too much elitism accelerates diversity collapse.

### Minimax implementation details

Terminal utility must be defined from a consistent player perspective. If a function returns utility for the player-to-move in some nodes and MAX in others, backup signs become wrong. An equivalent negamax implementation is possible in symmetric zero-sum games because $V_{player}(s)=-V_{opponent}(s)$.

Alpha cutoffs occur at MAX when value reaches/exceeds beta; beta cutoffs occur at MIN when value reaches/below alpha. A transposition table caches values for repeated game states; stored values may be exact, lower bounds, or upper bounds depending on cutoff, so table flags matter. Cyclic games additionally require repetition/draw rules.

Expected minimax needs actual chance probabilities. Replacing a chance node by MIN incorrectly assumes nature is adversarial; replacing MIN by average incorrectly assumes the opponent is random.

### CSP domain restoration and local repair

When forward checking/AC-3 is embedded in backtracking, every recursive choice must work on copied domains or record every deletion and undo it. Forgetting restoration can falsely delete valid solutions in sibling branches.

```python
def min_conflicts(state, variables, domains, conflicts, max_steps, rng):
    for _ in range(max_steps):
        bad=[x for x in variables if conflicts(state,x,state[x])>0]
        if not bad: return state
        x=rng.choice(bad)
        scores=[(conflicts(state,x,v),v) for v in domains[x]]
        best=min(score for score,_ in scores)
        state[x]=rng.choice([v for score,v in scores if score==best])
    return None
```

`AllDifferent(X1,...,Xn)` can propagate more strongly than treating every pair as `Xi != Xj`. A tree-structured CSP can be solved efficiently after directing edges and enforcing consistency; real scheduling may use continuous domains and nonlinear constraints, where simple finite-domain backtracking is not the whole solver.

### Bayesian-network inference details

Diagnostic inference goes effect→cause, e.g. $P(B\mid J,M)$; causal/predictive inference goes cause→effect, e.g. $P(J\mid B)$. Both are probabilistic queries even though arrows have one direction. Normalization constant is

$$\alpha=\frac1{\sum_x\tilde P(X=x,e)}.$$

VE order does not change the mathematical answer, only intermediate factor sizes/work. If eliminating Z, multiply **all and only** current factors mentioning Z before summing Z. Summing separately before multiplication can destroy dependencies and give the wrong answer.

Three d-separation motifs:

- chain $X\to Z\to Y$: observing Z blocks;
- fork $X\leftarrow Z\to Y$: observing Z blocks;
- collider $X\to Z\leftarrow Y$: unobserved Z blocks, but observing Z or a descendant opens.

### HMM dynamic-programming code

Viterbi must keep argmax predecessors, not only maximum scores:

```python
def viterbi(prior, transition, emissions):
    n=len(prior)
    score=[prior[i]*emissions[0][i] for i in range(n)]
    back=[]
    for emit in emissions[1:]:
        new=[0.0]*n; prev=[0]*n
        for i in range(n):
            candidates=[score[j]*transition[j][i] for j in range(n)]
            prev[i]=max(range(n), key=lambda j:candidates[j])
            new[i]=emit[i]*candidates[prev[i]]
        score=new; back.append(prev)
    last=max(range(n),key=lambda i:score[i]); path=[last]
    for prev in reversed(back):
        last=prev[last]; path.append(last)
    return list(reversed(path))
```

For long sequences multiply many probabilities underflows. Use scaling at each forward step or log probabilities; Viterbi becomes addition of log probabilities and `max`, with $\log0=-\infty$.

### MDP algorithm traps

A policy is stationary when $\pi(s)$ depends only on current state; finite-horizon optimal policies may depend on remaining time. Markov state must contain enough history to make the transition/reward prediction depend only on current state/action. If it does not, augment state.

Policy iteration pseudocode:

```text
choose arbitrary pi
repeat:
    evaluate U^pi from U(s)=R(s)+gamma sum_s' P(s'|s,pi(s))U(s')
    stable=true
    for each nonterminal s:
        a=argmax_a sum_s' P(s'|s,a)U(s')
        if a != pi(s): pi(s)=a; stable=false
until stable
```

Synchronous value iteration computes all new values from the previous vector. In-place/asynchronous updates can also converge under appropriate update coverage but give a different trace. Stopping by "utilities look unchanged" needs an explicit residual/tolerance.

### Decision-tree edge cases

Information gain can favor attributes with many distinct values; gain ratio or regularization can counter that (standard extension). A missing-value imputation mean applies to numeric attributes; categorical attributes need mode, a missing category, or probabilistic routing. Threshold candidates for sorted continuous values are often tested between adjacent values where labels change.

Training/test leakage includes choosing hyperparameters on the test set. Use training to fit, validation/cross-validation to choose, and test once for final estimate. Pruning should use validation evidence or a principled statistical/complexity criterion, not test-set tuning.

---

# Part XIV — Exact source coverage

## 53. MMI merged PDF: 521/521 pages

| Pages | Count | Covered topic |
|---:|---:|---|
| 1–105 | 105 | history, symbolic/subsymbolic, knowledge/expert systems, robotics, NLP/vision/applications |
| 106–145 | 40 | AI definitions, four views, Turing test, motivation |
| 146–177 | 32 | agents, PEAS, environments, architectures |
| 178–204 | 27 | problem formulation and examples |
| 205–243 | 39 | BFS/UCS/DFS/DLS/IDS/bidirectional/repeats |
| 244–289 | 46 | greedy/A*, admissibility/consistency, RBFS/SMA*, heuristics |
| 290–311 | 22 | second A* and memory-bounded recap |
| 312–343 | 32 | hill/beam/gradient/SA/GA |
| 344–385 | 42 | alternative-learning excerpt: Metropolis, proposals/schedules, neural/evolutionary optimization |
| 386–403 | 18 | GA selection/crossover/mutation/operator effects/partitioning |
| 404–446 | 43 | adversarial search, minimax, alpha–beta, evaluation, chance |
| 447–487 | 41 | second game lecture, ordering/non-quiescence/horizon/classification |
| 488–521 | 34 | CSP, backtracking heuristics, forward checking, AC-3, local repair |
| **Total** | **521** | **all pages accounted for** |

## 54. SB merged PDF: 214/214 pages

| Pages | Count | Covered topic |
|---:|---:|---|
| 1–27 | 27 | BN/CPT/alarm/independence/joint |
| 28–57 | 30 | enumeration, VE, factor ordering, irrelevant variables |
| 58–94 | 37 | temporal models/HMM/filtering/prediction/likelihood |
| 95–115 | 21 | smoothing/forward–backward/Viterbi |
| 116–155 | 40 | stochastic grid/MDP/Bellman/value-policy iteration |
| 156–174 | 19 | learning types/generalization/hypotheses/realizability/MAP |
| 175–214 | 40 | decision trees/entropy/gain/overfit/pruning/issues |
| **Total** | **214** | **all pages accounted for** |

## 55. Final self-test

- [ ] Four AI views; rationality; PEAS/environment.
- [ ] Problem formulation without state/node confusion.
- [ ] Trace all uninformed searches with conditions/complexities.
- [ ] Trace/prove A*, test consistency/reopening, explain $h=0$.
- [ ] RBFS/SMA*, hill, SA equation/schedule, GA operators, and the weight-vector/loss mapping for alternative neural training.
- [ ] Minimax/alpha–beta and exact infinite-depth-human answer.
- [ ] CSP with MRV/degree/LCV, forward checking, AC-3.
- [ ] BN factorization, alarm joint/posterior, VE steps.
- [ ] HMM filtering, smoothing, Viterbi backpointers.
- [ ] Bellman equations, value versus policy iteration.
- [ ] Entropy/gain, four tree base cases, pruning.
- [ ] Bias/variance equation versus under/overfitting.
- [ ] Mark logic/planning/ethics as standard-core supplements.

If a checkbox is uncertain, reconstruct it from the model, invariant, equation, and assumptions above rather than memorizing one sentence.
