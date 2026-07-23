# Bismillah.

# Theory of Computation — Core-Complete Viva Recall

> **Source boundary:** no local TOC slide folder exists in this workspace. This is a standard-core supplement, not a claim of slide-by-slide alignment. It emphasizes definitions, constructions, proof techniques, algorithms, and the distinctions most often tested in a viva.

The subject asks three increasingly deep questions:

1. What can a machine with a fixed finite amount of memory recognize?
2. What changes when we add a stack or an unbounded tape?
3. Among decidable problems, which ones can be solved efficiently?

---

# 1. Alphabets, strings, and languages

- An **alphabet** `Sigma` is a finite nonempty set of symbols.
- A **string** over `Sigma` is a finite sequence of symbols.
- `epsilon` is the empty string and has length `0`.
- `Sigma*` is every finite string over `Sigma`, including `epsilon`.
- `Sigma+ = Sigma* - {epsilon}`.
- A **language** over `Sigma` is any subset of `Sigma*`.

For string `x,y`, concatenation is `xy`; `|xy|=|x|+|y|`. Concatenation is associative but not generally commutative. `x^0=epsilon`.

For languages `A,B`:

```text
A union B       = {w | w in A or w in B}
AB              = {xy | x in A and y in B}
A^0             = {epsilon}
A*              = union_(i>=0) A^i
A+              = union_(i>=1) A^i
reverse(A)      = {reverse(w) | w in A}
```

A language may be described by a machine that accepts it, a grammar that generates it, or a declarative property of its strings.

---

# 2. Deterministic finite automata

## 2.1 Definition

A DFA is a five-tuple

```text
M=(Q, Sigma, delta, q0, F)
```

where `Q` is a finite state set, `Sigma` the input alphabet, `delta:Q x Sigma -> Q` a total transition function, `q0` the start state, and `F subseteq Q` the accepting states.

The extended transition function processes a whole string:

```text
delta*(q, epsilon)=q
delta*(q, xa)=delta(delta*(q,x),a)
```

The accepted language is

```text
L(M)={w in Sigma* | delta*(q0,w) in F}.
```

Every state represents the finite information about the processed prefix that is relevant to future acceptance.

## 2.2 Example: even number of `1`s

Use states `E` and `O`; start/accept at `E`. Reading `1` toggles; reading `0` stays.

```text
        0      1
E       E      O
O       O      E
```

Invariant: after reading any prefix, the state records whether the prefix contains an even or odd number of ones. This invariant is the correctness proof.

## 2.3 Product construction

To recognize intersection of DFA languages `L1,L2`, build states `(q1,q2)`, advance both components on each symbol, and accept when both are accepting. Choose final pairs differently for union, difference, or symmetric difference.

If the DFAs have `m,n` states, the product has at most `mn` states before unreachable-state removal.

## 2.4 Complement

For a **complete** DFA, swap accepting and nonaccepting states. If transitions are missing, first add a dead state. Complementing an NFA’s final-state set directly is not valid because NFA acceptance is existential over paths.

---

# 3. NFA and epsilon-NFA

## 3.1 Definition

An NFA may have zero, one, or many transitions for a state/symbol. Formally `delta:Q x Sigma -> P(Q)`. It accepts if **at least one** complete path consumes the whole string and reaches a final state.

An epsilon-NFA also moves without consuming input. `epsilon-closure(S)` is every state reachable from set `S` using only epsilon transitions, including `S` itself.

NFAs are not more expressive than DFAs; both recognize exactly the regular languages. NFAs can be exponentially more concise.

## 3.2 Subset construction

Each DFA state represents a set of possible NFA states.

```text
start = epsilon_closure({nfa_start})
queue = [start]
seen  = {start}

while queue not empty:
    S = pop(queue)
    for each symbol a:
        T = epsilon_closure(union of delta(q,a) for q in S)
        dfa_transition[S,a] = T
        if T not in seen:
            add T to seen and queue

accepting DFA sets = {S | S intersects NFA_accepting}
```

An `n`-state NFA yields at most `2^n` subset states, although many may be unreachable.

## 3.3 Epsilon-closure algorithm

Run DFS/BFS starting from all states in `S`, following only epsilon edges. With adjacency lists, one closure is `O(V+E_epsilon)` worst case.

---

# 4. Regular expressions and equivalence

Regular expressions are built from:

- `emptyset`, denoting no strings;
- `epsilon`, denoting `{epsilon}`;
- each symbol `a`, denoting `{a}`;
- union `R|S`;
- concatenation `RS`;
- star `R*`.

Precedence is normally star, concatenation, then union. Parenthesize in a viva.

Kleene’s theorem: regular expressions, DFAs, NFAs, epsilon-NFAs, and regular grammars describe exactly the regular languages.

## 4.1 Regex to automaton

Thompson construction recursively builds an epsilon-NFA:

- symbol: one labeled edge;
- union: new start/final with epsilon branches;
- concatenation: epsilon-connect first final to second start;
- star: new start/final with epsilon skip and loop edges.

Then apply subset construction if a DFA is needed.

## 4.2 Automaton to regex

State elimination labels edges with regular expressions. When eliminating state `k`, update every remaining edge `i->j`:

```text
R_ij <- R_ij | R_ik (R_kk)* R_kj.
```

Introduce one start with no incoming edges and one accept with no outgoing edges. Elimination order affects expression size, not the recognized language.

---

# 5. DFA minimization and Myhill-Nerode

## 5.1 Distinguishable states

States `p,q` are distinguishable if some suffix `z` makes exactly one of `delta*(p,z)`, `delta*(q,z)` accepting. Otherwise they are equivalent and can be merged.

## 5.2 Partition refinement

1. Remove unreachable states.
2. Start with partition `{F, Q-F}`.
3. Split a block whenever two states transition on some symbol into different current blocks.
4. Repeat until stable.
5. Each final block becomes one minimal-DFA state.

Correctness idea: final/nonfinal states are distinguished by `epsilon`; each refinement discovers a longer distinguishing suffix. Stable states accept the same future language.

## 5.3 Table-filling alternative

Mark every accepting/nonaccepting pair. Repeatedly mark pair `(p,q)` if some symbol sends it to an already marked pair. Unmarked pairs are equivalent.

## 5.4 Myhill-Nerode theorem

Define `x ~_L y` iff for every suffix `z`, `xz in L` exactly when `yz in L`. A language is regular iff this relation has finitely many equivalence classes. The number of classes equals the number of states in the minimal complete DFA.

To prove nonregularity, it is enough to exhibit infinitely many prefixes pairwise distinguishable by suffixes. For `L={0^n1^n}`, prefixes `epsilon,0,00,...` are pairwise distinguishable: for `i<j`, suffix `1^i` accepts after `0^i` but not after `0^j`.

---

# 6. Closure and decision properties of regular languages

Regular languages are closed under union, intersection, complement, difference, symmetric difference, concatenation, star, reversal, homomorphism, inverse homomorphism, and intersection with another regular language.

Important decision problems are decidable:

- membership: simulate DFA in `O(|w|)`;
- emptiness: graph-search for a reachable final state;
- finiteness: check whether a reachable cycle can still reach a final state;
- equivalence: test emptiness of symmetric difference using a product DFA;
- inclusion `L1 subseteq L2`: test emptiness of `L1 intersection complement(L2)`.

---

# 7. Pumping lemma for regular languages

If `L` is regular, there exists pumping length `p` such that every `w in L` with `|w|>=p` can be written `w=xyz` with:

```text
|xy|<=p,
|y|>0,
and x y^i z in L for every i>=0.
```

The quantifiers matter:

```text
exists p, for every long w in L,
exists a valid split xyz,
for every i>=0, the pumped string remains in L.
```

To disprove regularity, reverse the game:

1. Assume `L` regular and receive arbitrary `p`.
2. Choose a strategic `w in L` depending on `p`.
3. Consider **every** split meeting the length conditions.
4. Choose an `i` that makes the string leave `L`.
5. Contradict the lemma.

### Board proof: `{0^n1^n | n>=0}` is not regular

Choose `w=0^p1^p`. Since `|xy|<=p` and `|y|>0`, `y` contains only zeros. Pump down with `i=0`; the result has fewer zeros than ones and is outside the language. This works for every valid split.

The pumping lemma is necessary, not sufficient: satisfying a pumping-like property is not the normal way to prove a language regular.

---

# 8. Context-free grammars

A CFG is `G=(V,Sigma,R,S)` where `V` is a finite nonterminal set, `Sigma` terminals, `R` productions `A->alpha`, and `S` the start symbol.

- A derivation applies productions.
- A leftmost/rightmost derivation chooses which nonterminal to replace.
- A parse tree records hierarchical production use; its leaf yield is the string.
- `L(G)` is the set of terminal strings derivable from `S`.

Example for balanced parentheses:

```text
S -> SS | (S) | epsilon
```

## 8.1 Ambiguity

A grammar is ambiguous if some string has two distinct parse trees/equivalently two distinct leftmost derivations. Ambiguity belongs to the grammar; a language is inherently ambiguous only if every CFG for it is ambiguous.

The expression grammar

```text
E -> E+E | E*E | id
```

is ambiguous. Encode precedence and associativity:

```text
E -> E+T | T
T -> T*F | F
F -> (E) | id
```

## 8.2 Left recursion removal

For immediate left recursion

```text
A -> A alpha_1 | ... | A alpha_m | beta_1 | ... | beta_n
```

where no `beta` begins with `A`, transform to

```text
A  -> beta_1 A' | ... | beta_n A'
A' -> alpha_1 A' | ... | alpha_m A' | epsilon
```

This helps predictive top-down parsing; it does not by itself remove all ambiguity.

## 8.3 Simplification and Chomsky Normal Form

Remove non-generating and unreachable symbols; eliminate epsilon and unit productions under the transformation’s rules. In CNF, productions are:

```text
A -> BC
A -> a
```

plus a controlled start-to-epsilon rule if `epsilon` belongs to the language. CNF supports proofs and CYK; it is not meant to be readable source grammar.

---

# 9. Pushdown automata

A PDA is a finite automaton with a stack. A transition can depend on the state, next input/epsilon, and stack top, then change state and replace/pop/push stack symbols.

Nondeterministic PDAs recognize exactly the context-free languages. Unlike finite automata, deterministic and nondeterministic PDAs do not recognize the same class: deterministic CFLs form a proper subset of CFLs.

### PDA intuition for `0^n1^n`

- push one marker per `0`;
- nondeterministically/structurally switch at the first `1`;
- pop one marker per `1`;
- reject incorrect order, missing/excess symbols;
- accept when input and required stack content finish.

The stack supplies unbounded nested/counting memory in LIFO form, but one stack cannot in general compare three independent counts such as `a^n b^n c^n`.

Acceptance by empty stack and final state are equivalent for nondeterministic PDAs after standard transformations, but the machine definitions differ.

---

# 10. CFL closure and pumping

CFLs are closed under union, concatenation, star, reversal, homomorphism, inverse homomorphism, and intersection with a regular language. They are not closed under general intersection, complement, or difference.

The intersection-with-regular property is powerful: assume a language CFL, intersect it with a carefully chosen regular language, and obtain a known non-CFL.

## 10.1 CFL pumping lemma

For every CFL `L`, sufficiently long `w` can be written

```text
w = u v x y z
|vxy| <= p
|vy| > 0
u v^i x y^i z in L for every i>=0.
```

Two regions `v` and `y` pump together. To disprove CFL status, cover every placement of the short window `vxy`. Some non-CFLs resist this lemma; Ogden’s lemma lets the prover mark positions and is stronger.

## 10.2 Why `{a^n b^n c^n}` is not context-free

Choose `a^p b^p c^p`. Since `|vxy|<=p`, the pumped regions cannot cover all three symbol blocks. Pumping changes at most two blocks while the third count remains `p`, breaking equality for a suitable `i`.

State the case split carefully: `v,y` may lie in one block or cross one boundary; the length bound prevents spanning both boundaries.

---

# 11. CYK parsing

For a grammar in CNF and input `w_1...w_n`, let `T[i,l]` contain nonterminals deriving the substring beginning at `i` of length `l`.

```text
for i=1..n:
    T[i,1] = {A | A -> w_i}

for length=2..n:
    for start=1..n-length+1:
        for split=1..length-1:
            for each production A -> BC:
                if B in T[start,split]
                   and C in T[start+split,length-split]:
                    add A to T[start,length]

accept iff S in T[1,n]
```

With a straightforward indexed grammar, time is `O(n^3 |G|)` and table space `O(n^2 |V|)`/bitset equivalent. Store backpointers to reconstruct a parse tree.

---

# 12. Turing machines

A deterministic single-tape TM has finite control, a conceptually unbounded tape, a read/write head, and transition function that reads a symbol, writes a symbol, moves left/right (sometimes stay), and changes state.

A typical formal tuple contains states, input alphabet, tape alphabet, blank symbol, transition function, start state, and accept/reject states.

The exact tuple convention matters less than the model:

- input begins on tape;
- computation may use unbounded cells over time;
- accept/reject are halting outcomes;
- a machine may loop unless it is a decider.

Multitape, nondeterministic, two-way-infinite tape, and other standard variants have the same computability power, though simulation time can differ.

## 12.1 Recognizer versus decider

- A **recognizer** accepts every member; on a nonmember it may reject or loop.
- A **decider** halts on every input and accepts exactly the members.
- Recognizable languages are also called recursively enumerable/Turing-recognizable.
- Decidable languages are recursive.

Every decidable language is recognizable. A language is decidable iff both it and its complement are recognizable: dovetail the two recognizers until one accepts.

## 12.2 Enumerator equivalence

A language is recognizable iff some TM enumerator prints exactly its strings. To recognize from an enumerator, run until the target appears. To enumerate from a recognizer, dovetail simulations across all strings and time steps so one nonhalting input cannot block the rest.

## 12.3 Church-Turing thesis

The thesis says every effectively computable procedure is computable by a Turing-equivalent model. It is a foundational thesis, not an ordinary theorem, because “effectively computable” was an informal concept; many independently developed models converge to the same class.

---

# 13. Decidability and reductions

## 13.1 Mapping reduction

`A <=m B` means there is a total computable function `f` such that

```text
x in A iff f(x) in B.
```

Consequences:

- if `A <=m B` and `B` is decidable, then `A` is decidable;
- if `A` is undecidable and `A <=m B`, then `B` is undecidable;
- if `A <=m B` and `B` is recognizable, then `A` is recognizable: compute `f(x)` and run the recognizer for `B`;
- contrapositively, if `A` is not recognizable and `A <=m B`, then `B` is not recognizable.

Direction trap: to prove target `B` hard, reduce a known hard `A` **to** `B`, not `B` to `A`.

## 13.2 Halting problem

```text
HALT_TM={<M,w> | M halts on w}
```

is undecidable. It is recognizable: simulate `M(w)` and accept if it halts.

A contradiction proof assumes a total decider `H(M,w)`, then constructs a machine that on encoding `x` does the opposite/loops when `H(x,x)` predicts halting. Running it on its own encoding contradicts the prediction.

## 13.3 Acceptance problem

```text
A_TM={<M,w> | M accepts w}
```

is recognizable but undecidable. `HALT` and `A_TM` are related but not identical: a machine may halt and reject.

## 13.4 Rice’s theorem

Every nontrivial semantic property of the partial function/language recognized by a TM is undecidable. “Does `M` accept any string?”, “Is `L(M)` regular?”, and “Does `M` accept all strings?” are semantic and nontrivial.

Rice does not apply directly to syntactic properties such as “Does the machine description contain ten states?”

## 13.5 Post Correspondence Problem

Given top/bottom string tiles, PCP asks whether a nonempty sequence of tile indices makes the concatenated top and bottom strings equal. PCP is recognizable but undecidable and is a common source for grammar/automata undecidability reductions.

---

# 14. Complexity classes

Complexity normally studies decision problems under a reasonable machine model.

- **P:** decidable in deterministic polynomial time.
- **NP:** yes-instances have polynomial-size certificates verifiable in polynomial time; equivalently nondeterministic polynomial time.
- **co-NP:** complements of NP languages.
- **NP-hard:** every NP problem polynomial-time reduces to it; it need not be a decision problem, in NP, or decidable.
- **NP-complete:** both in NP and NP-hard.

Known: `P subseteq NP`; unknown: `P=NP`. NP does **not** mean “non-polynomial.”

## 14.1 Showing membership in NP

State:

- certificate;
- polynomial bound on certificate length;
- verifier;
- verifier running time;
- why a yes-instance has a certificate and a no-instance has none accepted.

For Hamiltonian cycle, certificate is an ordered vertex list; verify every vertex appears once, consecutive edges exist, and last connects to first in polynomial time.

## 14.2 NP-completeness proof template

To prove target `X` NP-complete:

1. Show `X in NP`.
2. Choose known NP-complete `Y`.
3. Construct polynomial transformation `Y <=p X`.
4. Prove `y` is YES iff transformed instance is YES.
5. Bound transformation time and output size.

Do not reduce `X` to known hard `Y`; that only shows `X` is no harder than `Y`.

## 14.3 Optimization versus decision

“Find the shortest tour” is an optimization problem. Its decision version asks whether a tour of cost at most `K` exists. Decision TSP is NP-complete; optimization TSP is NP-hard. A polynomial optimization algorithm would solve the decision version.

## 14.4 Polynomial reductions and consequences

If an NP-complete problem is in P, then `P=NP`. If `A` is NP-hard and `A <=p B`, then `B` is NP-hard. If `A <=p B` and `B in P`, then `A in P`.

Weak versus strong NP-hardness matters for numeric problems: a pseudo-polynomial algorithm can still exist for weakly NP-hard problems such as ordinary knapsack formulations.

## 14.5 Space classes

- `L`: deterministic logarithmic space;
- `NL`: nondeterministic logarithmic space;
- `PSPACE`: deterministic polynomial space.

Standard containments include

```text
L subseteq NL subseteq P subseteq NP subseteq PSPACE.
```

Savitch’s theorem gives `NSPACE(s(n)) subseteq DSPACE(s(n)^2)` for suitable `s`, so `NPSPACE=PSPACE`. These classes are supplements unless present in the course syllabus.

---

# 15. Chomsky hierarchy

| Language class | Grammar restriction | Machine intuition |
|---|---|---|
| Regular | right/left-linear | finite automaton |
| Context-free | one nonterminal on LHS | nondeterministic PDA |
| Context-sensitive | noncontracting/context rules | linear-bounded automaton |
| Recursively enumerable | unrestricted | TM recognizer |

Containments are proper under the standard definitions. A grammar’s syntactic class determines an upper bound on language complexity; the same language may have grammars in a more powerful class too.

---

# 16. High-probability viva traps

1. **Can a DFA omit a transition?** A formal DFA transition is total; add a dead state.
2. **Can an NFA accept if one branch rejects?** Yes, if some complete branch accepts.
3. **Are NFAs faster?** They are mathematical models; implementation/simulation and state size determine cost.
4. **Can a finite automaton count?** It can count modulo a fixed constant, not arbitrary unbounded equality.
5. **Does pumping prove regularity?** No.
6. **Is every CFG unambiguous?** No; some languages are inherently ambiguous.
7. **Does one stack recognize `a^n b^n c^n`?** No; that language is not context-free.
8. **Are CFLs closed under intersection?** Not general intersection, but intersection with a regular language is CFL.
9. **Does a recognizer halt on nonmembers?** Not necessarily.
10. **Is every undecidable problem NP-hard?** Complexity/reduction definitions must be specified; undecidability and NP-completeness are different notions.
11. **Does NP mean hard to verify?** No, NP emphasizes polynomial-time verification of yes certificates.
12. **Does `A <=p B` mean A is harder?** No; `B` is at least as hard as `A` under that reduction.

---

# 17. Board-ready proof/construction checklist

- [ ] Design a DFA by defining the information each state remembers.
- [ ] Convert an epsilon-NFA to a DFA using closure/subsets.
- [ ] Minimize a DFA with partition refinement and a distinguishing suffix.
- [ ] Prove `{0^n1^n}` nonregular with correct pumping quantifiers.
- [ ] Remove immediate left recursion and explain why it helps parsing.
- [ ] Convert a small CFG to CNF and run one CYK table.
- [ ] Sketch a PDA for balanced parentheses or `0^n1^n`.
- [ ] Prove `{a^n b^n c^n}` non-CFL with all pumping-window cases.
- [ ] Distinguish TM recognizer, decider, enumerator, and dovetailing.
- [ ] State a mapping reduction in the correct direction.
- [ ] Explain HALT undecidability and Rice’s theorem boundaries.
- [ ] Prove a problem NP-complete using membership, reduction, iff correctness, and polynomial cost.
