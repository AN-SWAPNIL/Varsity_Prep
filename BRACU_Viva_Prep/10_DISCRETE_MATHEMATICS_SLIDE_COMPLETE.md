# Bismillah.

# CSE 103 Discrete Mathematics — Slide-Complete Viva Recall

This is a recall-and-explanation volume rebuilt against the current `103-DM/Discrete_merged.pdf` (**236/236 pages**), not a loose list of interview questions. The governing idea is: **define the object, state the exact conditions, work one tiny example, then say why it matters in computer science**.

The current merged source covers logic and proof, induction, sets/functions, counting, pigeonhole, sequences/recurrences/generating functions, graphs and coloring. Selected graph-theory/computer-mathematics notes were used only to reinforce graph/recurrence applications already routed here or to DSA; they are not treated as additional standalone viva courses.

## How to answer a mathematical viva question

Use this four-part pattern:

1. **Definition:** one exact sentence, including the domain and assumptions.
2. **Formal statement/formula:** write it with symbols.
3. **Witness, counterexample, or two-line derivation:** show that you understand it.
4. **Boundary:** say what it does *not* imply, or state the usual trap.

For a theorem, distinguish the **statement** from its **proof**. For an algorithm, give input, invariant/recurrence, output, and complexity. For a counting problem, explicitly name the objects being counted and explain why every object is counted exactly once.

## Core notation

| Symbol | Meaning |
|---|---|
| `¬p`, `~p` | not `p` |
| `p ∧ q` | `p` and `q` |
| `p ∨ q` | inclusive or: at least one is true |
| `p ⊕ q` | exclusive or: exactly one is true |
| `p → q` | if `p`, then `q` |
| `p ↔ q` | `p` iff `q` |
| `∀x` / `∃x` | for every `x` / there exists an `x` |
| `x ∈ A`, `A ⊆ B` | membership / subset |
| `|A|` | cardinality of a finite set |
| `P(A)` | power set of `A` |
| `⌈x⌉`, `⌊x⌋` | least integer at least `x`; greatest integer at most `x` |
| `[x^n]G(x)` | coefficient of `x^n` in `G(x)` |

---

# Lecture 01 — Statements, Propositional Logic, Truth Tables, and Equivalence

## 1. Why discrete mathematics belongs in computer science

Discrete mathematics supplies the language behind algorithms, data structures, digital logic, databases, networks, cryptography, AI, scheduling, and graph-based systems. The objects are often finite or countable—bits, strings, sets, program states, graph vertices, and steps of an algorithm—rather than continuously varying physical quantities.

The opening checker puzzle illustrates mathematical abstraction: strip away the picture, identify legal states and moves, guess a pattern for small levels, and seek an invariant or proof. The small answers `2, 4, 8, 20` do not justify extrapolating to `40`; level 5 is impossible. **Examples suggest a conjecture; they do not prove it.**

The Pythagorean rearrangement and the deceptive `65 = 64` picture make the same point. A diagram can motivate a proof, but an unnoticed gap/overlap invalidates an area argument. A rigorous proof begins with definitions/axioms and uses valid logical deductions.

## 2. Statement or proposition

A **statement** (proposition) is a declarative sentence that has exactly one truth value: true or false.

- `2 + 2 = 4` is a true statement.
- `3 × 3 = 8` is a false statement.
- “Every even integer greater than 2 is a sum of two primes” is a statement even though it is an unproved conjecture; it still has a truth value.
- `x + y > 0` is not yet a statement if the variables are free. It becomes one after values are assigned or variables are quantified.
- Questions, commands, and incomplete noun phrases are not statements.

An **atomic statement** is not built from smaller statements. A **compound/molecular statement** combines statements using logical operators.

Viva trap: “We do not know whether it is true” is different from “it has no truth value.”

## 3. Logical operators and complete truth table

| `p` | `q` | `¬p` | `p∧q` | `p∨q` | `p⊕q` | `p→q` | `p↔q` |
|---|---|---|---|---|---|---|---|
| T | T | F | T | T | F | T | T |
| T | F | F | F | T | T | F | F |
| F | T | T | F | T | T | T | F |
| F | F | T | F | F | F | T | T |

- `p ∨ q` is inclusive unless “exactly one” is stated.
- `p ⊕ q` means exactly one is true:

```text
p ⊕ q ≡ (p ∧ ¬q) ∨ (¬p ∧ q)
      ≡ (p ∨ q) ∧ ¬(p ∧ q)
```

For `n` propositional variables, a complete truth table has `2^n` rows. Evaluate inner subformulas first and keep one column per subformula; this makes a whiteboard derivation auditable.

## 4. Constructing a formula from a truth table

### Disjunctive normal form (DNF): use true rows

For each output-true row, create a **minterm**: use a variable if the row assigns T and its negation if the row assigns F; join them with `∧`. OR all minterms.

Example: output is true only on `(p,q)=(T,F)` and `(F,T)`:

```text
(p ∧ ¬q) ∨ (¬p ∧ q)
```

### Conjunctive normal form (CNF): use false rows

For each output-false row, form a clause that is false exactly on that row: negate a T input and leave an F input unnegated; join with `∨`. AND all clauses.

For XOR, false rows are `(T,T)` and `(F,F)`:

```text
(¬p ∨ ¬q) ∧ (p ∨ q)
```

This is the mathematical bridge from a truth-table specification to a Boolean formula/digital circuit. Canonical DNF/CNF may not be minimal; simplify afterward.

## 5. Logical equivalence and laws

Two formulas are **logically equivalent**, written `P ≡ Q`, when they have the same truth value for every assignment. A truth table proves equivalence exhaustively; algebraic rewriting proves it using known equivalences.

Essential laws:

```text
Identity:       p ∧ T ≡ p                 p ∨ F ≡ p
Domination:     p ∨ T ≡ T                 p ∧ F ≡ F
Idempotent:     p ∨ p ≡ p                 p ∧ p ≡ p
Double negation:¬¬p ≡ p
Complement:     p ∨ ¬p ≡ T                p ∧ ¬p ≡ F
Commutative:    p ∨ q ≡ q ∨ p             p ∧ q ≡ q ∧ p
Associative:    (p∨q)∨r ≡ p∨(q∨r)         (p∧q)∧r ≡ p∧(q∧r)
Distributive:   p∧(q∨r) ≡ (p∧q)∨(p∧r)
                p∨(q∧r) ≡ (p∨q)∧(p∨r)
Absorption:     p∨(p∧q) ≡ p               p∧(p∨q) ≡ p
De Morgan:      ¬(p∧q) ≡ ¬p∨¬q            ¬(p∨q) ≡ ¬p∧¬q
```

Example—negate “Jim is tall and thin.” First expose the hidden conjunction:

```text
¬(Tall(Jim) ∧ Thin(Jim))
≡ ¬Tall(Jim) ∨ ¬Thin(Jim)
```

“Jim is not tall and thin” is linguistically ambiguous and is not a safe formal negation.

## 6. Tautology, contradiction, satisfiability

- A **tautology** is true under every assignment, e.g. `p ∨ ¬p`.
- A **contradiction** is false under every assignment, e.g. `p ∧ ¬p`.
- A formula is **satisfiable** if at least one assignment makes it true.
- A formula is **contingent** if it is true on some assignments and false on others.

To classify a complex expression, simplify or construct its final truth-table column. For example,

```text
((p∧r) ∨ (q∧r)) ∧ (¬(p∨q) ∧ r)
```

is a contradiction: the left part requires `p` or `q`, while `¬(p∨q)` requires neither.

### L01 whiteboard drill

Given a three-input truth table: write canonical DNF from true rows, canonical CNF from false rows, simplify with laws, and state whether the result is satisfiable/tautological/contradictory.

### L01 common wrong answers

- Calling a command or an open sentence a proposition.
- Treating `or` as exclusive without saying so.
- Negating `p∧q` as `¬p∧¬q`.
- Claiming two formulas are equivalent because several sample rows match.
- Trusting a diagram without checking gaps, overlaps, and assumptions.

---

# Lecture 02 — Conditionals, Necessary/Sufficient Conditions, and Arguments

## 7. Implication

`p → q` means “if `p`, then `q`.” `p` is the **antecedent/hypothesis** and `q` the **consequent/conclusion**. It is false only when `p` is true and `q` is false.

```text
p → q ≡ ¬p ∨ q
¬(p → q) ≡ p ∧ ¬q
```

Why is a false hypothesis considered true? The conditional promises only that whenever `p` occurs, `q` occurs. If `p` did not occur, no violation was observed. This is **vacuous truth**, not evidence that `q` is true.

Example: “If GPA is 4.0, then the student receives a scholarship” is violated only by a student with GPA 4.0 who receives no scholarship.

Implication in mathematical logic does not require causality or relevance. `0=1 → 2+2=4` is true because its consequent is true; `0=1 → 7 is prime` is also true because its antecedent is false.

## 8. Converse, inverse, contrapositive

For `p → q`:

| Form | Formula | Equivalent to original? |
|---|---|---|
| converse | `q → p` | generally no |
| inverse | `¬p → ¬q` | generally no |
| contrapositive | `¬q → ¬p` | yes |

The converse and inverse are equivalent to each other because each is the contrapositive of the other.

Example:

```text
Original:      If n>2 is prime, then n is odd.        True
Converse:      If n>2 is odd, then n is prime.        False; n=9
Contrapositive:If n>2 is not odd, then n is not prime.True
```

## 9. Necessary and sufficient conditions

Translate the English direction before reasoning:

```text
“Q if P”       means P → Q.   P is sufficient for Q.
“P only if Q”  means P → Q.   Q is necessary for P.
“P iff Q”      means (P → Q) ∧ (Q → P).
```

Prime `>2` is sufficient for oddness; oddness is necessary, but not sufficient, for primality. The word immediately after **only if** is on the necessary/right side.

To prove `P ↔ Q`, prove both directions. It is often efficient to prove `P→Q` and the contrapositive of `Q→P`.

Worked example: for integer `n`, `n` is even iff `n²` is even.

- If `n=2k`, then `n²=4k²=2(2k²)`, even.
- For the reverse, prove the contrapositive: if `n=2k+1`, then `n²=4k²+4k+1=2(2k²+2k)+1`, odd.

Do not write `n=√(2k)` and declare it even; that expression need not be an integer multiple of 2.

## 10. Arguments and validity

An **argument form** is a sequence of premises followed by a conclusion. It is **valid** if there is no assignment in which every premise is true and the conclusion is false.

Validity is structural. It does not mean every premise or the conclusion is factually true. A **sound** argument is valid and has true premises; soundness then guarantees a true conclusion.

Core inference rules:

```text
Modus ponens:          p→q, p        therefore q
Modus tollens:         p→q, ¬q       therefore ¬p
Hypothetical syllogism:p→q, q→r      therefore p→r
Disjunctive syllogism: p∨q, ¬p       therefore q
Conjunction:           p, q          therefore p∧q
Simplification:        p∧q           therefore p
Addition:              p             therefore p∨q
Resolution:            p∨q, ¬p∨r     therefore q∨r
```

Two famous invalid forms:

```text
Affirming the consequent: p→q, q, therefore p       INVALID
Denying the antecedent:   p→q, ¬p, therefore ¬q     INVALID
```

Counterexample to the first: “If something is a fish, it drinks water; I drink water; therefore I am a fish.” The premises can be true while the conclusion is false.

## 11. Proving invalidity and deriving a conclusion

To disprove validity, find **one countervaluation** with all premises true and conclusion false. To prove validity by truth table, check only rows on which all premises are true.

Worked deduction from the slides:

```text
A. dining-table → saw-at-breakfast
B. living-room ∨ dining-room
C. living-room → coffee-table
D. ¬saw-at-breakfast
F. dining-room → dining-table
```

Then:

1. `¬dining-table` from A and D by modus tollens.
2. `¬dining-room` from F and step 1 by modus tollens.
3. `living-room` from B and step 2 by disjunctive syllogism.
4. `coffee-table` from C and step 3 by modus ponens.

## 12. Contradiction puzzles

For Knights and Knaves, encode “knights always tell truth; knaves always lie,” assume one type, propagate consequences, and reject a branch if it forces both a proposition and its negation. This is proof by cases plus contradiction.

The self-referential pair “The sentence below is false / The sentence above is true” warns that natural-language self-reference can produce semantic paradoxes; ordinary propositional truth assignments assume well-formed propositions whose truth conditions are already defined.

### L02 viva traps

- From `p→q` and `q`, nothing about `p` follows.
- From `p→q` and `¬p`, nothing about `q` follows.
- A valid argument can have a false conclusion when a premise is false.
- A true conclusion does not prove that its argument form is valid.
- `p→q`, `q→r`, `r→p` prove equivalence of truth values, not that all three are true; all three may be false.

---

# Lecture 03 — First-Order Logic and Quantifiers

## 13. Predicates, domains, and truth sets

A **predicate** is an open sentence containing variables, such as `P(x,y): x+2=y`. It becomes a proposition after values are substituted or its variables are quantified.

The **domain/universe of discourse** is the set of allowed substitutions. Domain is part of meaning:

```text
∀x, x² ≥ x
```

is true over positive integers but false over reals (`x=1/2` is a counterexample).

The **truth set** of `P(x)` over domain `D` is `{x∈D | P(x)}`.

## 14. Universal and existential quantifiers

```text
∀x∈D, P(x)   “P holds for every x in D.”
∃x∈D, P(x)   “P holds for at least one x in D.”
∃!x∈D, P(x)  “exactly one x in D satisfies P.”
```

How to prove/refute:

| Claim | To prove | To refute |
|---|---|---|
| `∀x P(x)` | general argument for arbitrary `x`; finite exhaustion if domain is finite | one counterexample |
| `∃x P(x)` | one valid witness | show `¬P(x)` for every `x` |

Examples:

- `∃m∈Z, m²=m` is proved by witness `m=0` or `m=1`.
- `∀x∈R, x²≥x` is refuted by `x=1/2`.

Natural language can hide quantification:

- “If a number is an integer, it is rational” means `∀x(x∈Z → x∈Q)`.
- “24 can be written as a sum of two even integers” means `∃m∃n(Even(m)∧Even(n)∧m+n=24)`.

## 15. Formal translations

Assume an integer domain unless written otherwise.

```text
All primes greater than 2 are odd:
∀x ((Prime(x) ∧ x>2) → Odd(x))

Goldbach's conjecture:
∀n ((Even(n) ∧ n>2) → ∃p∃q(Prime(p) ∧ Prime(q) ∧ n=p+q))

Fermat's Last Theorem:
∀n∈Z (n>2 → ¬∃a,b,c∈Z_nonzero (a^n+b^n=c^n))
```

Restrictions can be placed in the domain or written in an implication. For a universal statement, `∀x∈D Q(x)` is equivalent to `∀x(P(x)→Q(x))` when `D={x | P(x)}`.

## 16. Negating quantified statements

Quantifiers flip and the predicate is negated:

```text
¬∀x P(x) ≡ ∃x ¬P(x)
¬∃x P(x) ≡ ∀x ¬P(x)
```

For a universal implication:

```text
¬∀x(P(x)→Q(x))
≡ ∃x ¬(P(x)→Q(x))
≡ ∃x(P(x)∧¬Q(x))
```

Thus the negation of “every blond person has blue eyes” is “there exists a blond person without blue eyes,” not “no blond person has blue eyes.”

For nested quantifiers, push the negation inward one quantifier at a time:

```text
¬∀x∀y P(x,y) ≡ ∃x∃y ¬P(x,y)
¬∀x∃y P(x,y) ≡ ∃x∀y ¬P(x,y)
¬∃x∀y P(x,y) ≡ ∀x∃y ¬P(x,y)
¬∃x∃y P(x,y) ≡ ∀x∀y ¬P(x,y)
```

## 17. Order of quantifiers

Quantifiers of the same type commute; mixed quantifiers generally do not.

```text
∀virus v ∃program p Kills(p,v)
```

allows a different program for each virus. By contrast,

```text
∃program p ∀virus v Kills(p,v)
```

claims one universal antivirus and is stronger.

Concrete arithmetic example over integers:

- `∀x∃y(y>x)` is true: choose `y=x+1`.
- `∃y∀x(y>x)` is false: no largest integer exists.

When proving `∀x∃y`, begin with arbitrary `x` and construct a possibly `x`-dependent `y`. When proving `∃x∀y`, one single witness must work against every `y`.

## 18. Vacuous truth with predicates

`∀x(P(x)→Q(x))` is vacuously true if no domain element satisfies `P`. For an empty bowl, “every ball in the bowl is black” is true in classical logic because there is no nonblack ball in it. Its negation—“there exists a ball in the bowl that is not black”—is false.

Do not confuse “all members have property Q” with “there exists a member.” Universal statements do not assert existence.

## 19. Quantified inference rules and validity

- **Universal instantiation (UI):** from `∀x P(x)`, infer `P(c)` for a particular `c`.
- **Universal generalization (UG):** if `P(c)` is proved for an arbitrary `c` with no special assumptions, infer `∀xP(x)`.
- **Universal modus ponens:** `∀x(P(x)→Q(x)), P(a) ⟹ Q(a)`.
- **Universal modus tollens:** `∀x(P(x)→Q(x)), ¬Q(a) ⟹ ¬P(a)`.

Example: all humans are mortal; Zeus is not mortal; therefore Zeus is not human. This has valid form even if the names are fictional.

A quantified argument is valid if it works for every domain and interpretation of its predicates. To disprove validity, give a **countermodel**. For example,

```text
∀z(Q(z)∨P(z)) → (∀xQ(x) ∨ ∀yP(y))
```

is invalid. Let the domain be integers, `Q(z)=Even(z)`, and `P(z)=Odd(z)`. Every integer is even or odd, but not every integer is even and not every integer is odd.

By contrast,

```text
∀z(Q(z)∧P(z)) → (∀xQ(x) ∧ ∀yP(y))
```

is valid: instantiate an arbitrary element, simplify the conjunction, and generalize each property.

### L03 common wrong answers

- Omitting the domain.
- Negating `∀` without changing it to `∃`.
- Reversing `∀x∃y` and `∃y∀x`.
- Using one example to prove a universal statement.
- Generalizing from a specially chosen constant.
- Treating a universal statement as proof that its subject exists.

---

# Lecture 04 — Methods of Proof

## 20. Definitions used inside proofs

For integers:

```text
n is even ⇔ ∃k∈Z, n=2k
n is odd  ⇔ ∃k∈Z, n=2k+1
a divides b, written a|b, ⇔ ∃k∈Z, b=ak
```

An integer `p>1` is **prime** if its only positive divisors are `1` and `p`; an integer `>1` that is not prime is composite. `1` is neither prime nor composite.

A rational number has form `a/b`, where `a,b∈Z` and `b≠0`. Terminating decimals and repeating decimals are rational: if `x=0.121212…`, then `100x-x=12`, hence `x=12/99`.

## 21. Direct proof

To prove `P→Q`, assume `P`, unfold relevant definitions, and derive `Q`.

Example: if `x=2m+1` and `y=2n+1` are odd, then

```text
xy=(2m+1)(2n+1)=2(2mn+m+n)+1,
```

which is odd.

Divisibility templates:

1. If `a|b`, then `a|bc` for every integer `c`.
2. If `a|b` and `b|c`, then `a|c`.
3. If `a|b` and `a|c`, then `a|(sb+tc)` for all integers `s,t`.
4. For `c≠0`, `a|b` iff `ca|cb`.

Each proof replaces divisibility by an integer multiplier and factors `a`. Do not “cancel” in divisibility without stating the nonzero/integer condition.

## 22. Contrapositive proof

To prove `P→Q`, prove the equivalent `¬Q→¬P`. This is useful when the negated conclusion exposes a concrete algebraic form.

Claim: if `r` is irrational, then `√r` is irrational (where the real square root exists). Contrapositive: if `√r=a/b` is rational, then `r=a²/b²` is rational.

Contrapositive is a proof of the original implication; converse is not.

## 23. Biconditional proof

To prove `P↔Q`, prove `P→Q` and `Q→P`. You may prove either direction through its contrapositive. The even-square example in Lecture 02 is the model answer.

## 24. Proof by contradiction

To prove `P`, assume `¬P` and derive a contradiction such as `R∧¬R`, violation of a definition, or an impossible inequality. Then `¬P` is false, so `P` is true.

### `√2` is irrational

Assume `√2=m/n` in lowest terms, with positive integers `m,n`. Then

```text
m²=2n²,
```

so `m²` is even and therefore `m` is even; let `m=2k`. Substitution gives `n²=2k²`, so `n` is even. Then both share factor 2, contradicting lowest terms.

The subsidiary fact “if `m²` is even, then `m` is even” is proved by contrapositive: an odd integer has odd square.

### Infinitely many primes

Assume all primes are `p1,…,pk`. Let `N=p1p2…pk+1`. Every integer `N>1` has a prime divisor, but division by each listed `pi` leaves remainder 1. Thus `N` has a prime divisor not on the complete list—a contradiction.

Do not claim `N` itself must be prime; it need only possess an unlisted prime factor.

## 25. Proof by cases

Partition the domain into exhaustive, nonoverlapping cases and prove the claim in each. Example: for nonzero real `x`, either `x>0` or `x<0`, and in either case `x²>0`.

### Odd squares are `1 mod 8`

Let `n=2k+1`. Then

```text
n²=4k²+4k+1=4k(k+1)+1.
```

One of consecutive integers `k,k+1` is even, so `k(k+1)=2m`. Hence `n²=8m+1`.

### Nonconstructive existence by cases

There exist irrational `a,b` such that `a^b` is rational. Consider `x=(√2)^(√2)`:

- if `x` is rational, choose `a=b=√2`;
- if `x` is irrational, choose `a=x`, `b=√2`; then `a^b=(√2)^2=2`.

The proof establishes existence without identifying which case holds.

### L04 proof-writing checklist

- State arbitrary variables and their domains.
- Expand definitions (`even`, `divides`, `rational`) with new integer witnesses.
- Do not assume the desired conclusion.
- A counterexample refutes a universal claim; examples do not prove one.
- In contradiction, identify the exact contradiction.
- In cases, show the cases are exhaustive.
- End after the target statement has actually been reached.

---

# Lectures 05–06 — Induction, Strong Induction, Well Ordering, and Invariants

## 26. Principle of mathematical induction

Let `P(n)` be a proposition for integers `n≥n0`. If

```text
P(n0)                                            (base case)
∀k≥n0, P(k) → P(k+1)                            (induction step)
```

are true, then `P(n)` is true for every integer `n≥n0`.

The **induction hypothesis (IH)** is the temporary assumption `P(k)` inside the proof of `P(k+1)`. It is not an assumption that the theorem is globally true. The domino analogy works only after the first domino is actually knocked over and every domino is close enough to knock the next.

Whiteboard template:

```text
Claim: P(n) for all integers n≥n0.
Base: verify P(n0).
IH: assume P(k) for an arbitrary k≥n0.
Step: using the IH, derive P(k+1).
Conclusion: by induction, P(n) holds for every n≥n0.
```

The starting index matters. A proof of `P(k)→P(k+1)` without a base proves nothing. A base at `n=0` plus a forward step proves only nonnegative indices, not all integers.

## 27. Worked ordinary-induction proofs from L05

### Finite geometric sum

For `r≠1` and `n≥1`,

```text
1+r+⋯+r^n = (r^(n+1)-1)/(r-1).
```

Base `n=1`: both sides equal `1+r`. Assume the formula for `n`. Then

```text
1+r+⋯+r^n+r^(n+1)
= (r^(n+1)-1)/(r-1)+r^(n+1)
= (r^(n+2)-1)/(r-1).
```

### Divisibility of `2^(2n)-1`

For every `n≥1`, `3 | (2^(2n)-1)`.

Base: `2²-1=3`. If `3 | (2^(2k)-1)`, then

```text
2^(2(k+1))-1
=4·2^(2k)-1
=3·2^(2k)+(2^(2k)-1),
```

a sum of two multiples of 3.

### `6 | (n³-n)`

For every `n≥2`, `n³-n` is divisible by 6. Base: `2³-2=6`. Assume `6|(k³-k)`. Then

```text
(k+1)³-(k+1)
=(k³-k)+3(k²+k).
```

The first term is divisible by 6 by IH. `k²+k=k(k+1)` is even, so `3(k²+k)` is divisible by 6.

There is also a one-line factor proof: `n³-n=(n-1)n(n+1)`, a product of three consecutive integers; one is divisible by 3 and at least one is even.

### Exponential dominates linear

For `n≥3`, `2n+1<2^n`. Base: `7<8`. Assume `2k+1<2^k`. Then

```text
2(k+1)+1=2k+3 < 2^k+2 < 2^k+2^k=2^(k+1),
```

because `k≥3` implies `2<2^k`.

### Reciprocal-square-root lower bound

For `n≥2`,

```text
1/√1 + 1/√2 + ⋯ + 1/√n > √n.
```

The base is `1+1/√2>√2`. Assuming the claim for `n`,

```text
Σ_(i=1)^(n+1) 1/√i > √n+1/√(n+1)
                       = (√n√(n+1)+1)/√(n+1)
                       > (n+1)/√(n+1)=√(n+1),
```

where `√n√(n+1)>n`.

## 28. Strengthening the induction claim: deficient-board tiling

The original target “tile a `2^n × 2^n` board with an L-tromino when the missing square is in the middle” is too weak for the recursive step. Strengthen it:

> Every `2^n × 2^n` board with **any one square missing** can be tiled with L-shaped trominoes.

Base `n=0`: a `1×1` board whose one square is missing needs no tile. For the step, split the board into four equal quadrants. One quadrant contains the missing square. Place one L-tromino at the center so that it removes one central square from each of the other three quadrants. Now every quadrant is a smaller deficient board; apply the IH to each.

This is a general proof-design lesson: if the IH is not powerful enough to solve the subproblems, strengthen the claim while keeping it sufficient for the original goal.

## 29. The all-horses-same-color fallacy

The attempted induction says any `n` horses share a color, removes the first horse and the last horse to obtain two overlapping groups of size `n`, and uses an overlap to link their colors. The step fails from `n=1` to `n=2`: the two one-horse groups do not overlap. A base case at `n=0` or `n=1` cannot repair a false induction step.

## 30. Strong induction

Strong induction replaces the IH `P(k)` by all previous cases:

```text
P(n0), P(n0+1), …, P(k)  →  P(k+1).
```

It has the same logical power as ordinary induction but is more convenient when a problem splits into several smaller sizes not known in advance.

### Unstacking game

Starting with a stack of `n` boxes, split a stack of size `a+b` into positive sizes `a,b` and score `ab`; continue until singletons. Every strategy has total score

```text
S(n)=n(n-1)/2.
```

For a first split `n=a+b`, strong induction gives

```text
S(n)=ab+S(a)+S(b)
    =ab+a(a-1)/2+b(b-1)/2
    =(a+b)(a+b-1)/2.
```

The answer is independent of split order; `S(8)=28`, `S(16)=120`.

### Every integer greater than 1 is a product of primes

Assume the result for every integer from `2` through `n-1`. If `n` is prime, done. Otherwise `n=ab` with `1<a,b<n`; by the strong IH, both `a` and `b` are products of primes, hence so is `n`. This proves existence of a prime factorization, not uniqueness.

### Postage with 3-cent and 5-cent stamps

Every amount `n≥8` can be formed. Verify bases `8=3+5`, `9=3+3+3`, and `10=5+5`. For `n≥11`, form `n-3` by IH and add a 3-cent stamp.

With 5-cent and 7-cent stamps, every `n≥24` is possible. A convenient block of five bases is

```text
24=2·5+2·7, 25=5·5, 26=1·5+3·7,
27=4·5+1·7, 28=4·7.
```

Then add a 5-cent stamp to move from `n` to `n+5`.

Viva trap: the induction step must not invoke a smaller value below the proven base range.

## 31. Well-ordering principle (WOP)

Every nonempty subset of the nonnegative integers has a least element. This is false for nonnegative rationals—for example `{1,1/2,1/3,…}` has no least element. WOP and induction are equivalent foundational principles over the nonnegative integers.

Minimal-counterexample proof pattern:

1. Define `C={n∈N | ¬P(n)}`.
2. Assume `C` is nonempty.
3. By WOP, let `m` be its least element.
4. Use `m` to construct a smaller counterexample or otherwise contradict minimality.
5. Therefore `C=∅` and `P(n)` holds for all `n`.

The WOP version of the `√2` proof chooses a representation `√2=m/n` with the least positive denominator. The parity argument produces `√2=(m/2)/(n/2)`, a smaller positive denominator, contradiction.

### L06 “Non-Fermat” descent example

The deck contrasts the hard equation `a³+b³=c³` with the easier claim that there are no positive-integer solutions to

```text
4a³+2b³=c³.
```

Assume a solution and, by WOP, choose one with `|a|` minimum. A common factor could be divided out to produce a smaller solution, so choose a **primitive** solution with no common factor. But the equation makes `c³` even, hence `c` even; write `c=2c'`. Then

```text
4a³+2b³=8c'³  ⇒  b³=4c'³−2a³,
```

so `b³`, and therefore `b`, is even. Write `b=2b'`:

```text
8b'³=4c'³−2a³  ⇒  a³=2c'³−4b'³,
```

so `a` is even. Thus `a,b,c` have common factor 2, contradicting primitivity. The parity step uses the contrapositive of “an odd integer has an odd cube.” This is **infinite descent** expressed through WOP.

## 32. Invariants

An **invariant** is a property preserved by every legal move/iteration. To prove a target unreachable:

1. identify a property true initially;
2. prove each allowed move preserves it;
3. show the target lacks it.

### Diagonal chess move

A diagonally moving piece remains on the same square color: each diagonal move changes row and column parity together, preserving `(row+column) mod 2`. Therefore it cannot reach a square of the opposite color.

### Mutilated chessboard

Each domino covering two adjacent squares occupies one black and one white square. Removing two same-colored corner squares from an `8×8` board leaves unequal color counts, so 31 dominoes cannot tile it. Area alone (`62` squares for `31` dominoes) is necessary but not sufficient; the color invariant supplies the obstruction.

### Algorithmic connection

A loop invariant is the programming analogue. It must satisfy:

- **initialization:** true before the loop;
- **maintenance:** one iteration preserves it;
- **termination:** together with the exit condition, it implies correctness.

Induction proves the invariant over iteration count.

## 33. Induction errors and source cautions

- The visible L05 overview expression `n! ≥ n^n`, if read literally, is false for `n>1`; the universally true elementary inequality is `n!≤n^n`. Never induct on a false transcription.
- `P(0)` and `P(n)→P(n+1)` prove cases `n≥0`, not negative integers.
- Do not use `P(k+1)` while trying to prove it.
- Strong induction still requires base coverage.
- A recurrence/recursive program needs progress toward a base case.
- Induction verifies a proposed formula; it does not by itself discover the formula.

---

# Lecture 07 — Sets, Operations, Partitions, and Russell’s Paradox

## 34. Set fundamentals

A **set** is an unordered collection of distinct mathematical objects treated as one object. Order and repetition do not matter:

```text
{A,B,C}={C,B,A}={A,A,B,C,B}.
```

Sets may contain sets. In `S={a,{b},c}`, `{b}∈S` but `b∉S`. Likewise `{{b}}≠{b}`.

Ways to define a set:

- roster: `{1,2,4,8,…}`;
- set-builder: `{x∈Z | x is prime}`;
- truth set of a predicate.

## 35. Membership, subset, proper subset, equality

```text
x∈A       x is an element of A
A⊆B       ∀x(x∈A→x∈B)
A⊂B       A⊆B and A≠B       (when ⊂ is used for proper subset)
A=B       A⊆B and B⊆A
```

The empty set `∅` is a subset of every set because there is no element of `∅` that violates containment. It is not automatically an element of every set.

Membership and subset are different types of relation: `3∈{3,5,7}` while `{3}⊆{3,5,7}`.

## 36. Set operations

For universe `U`:

```text
A∪B = {x | x∈A or x∈B}
A∩B = {x | x∈A and x∈B}
A−B = {x | x∈A and x∉B}
A^c = U−A
A△B = (A−B)∪(B−A)      symmetric difference
```

Complement is undefined until a universe is specified.

With `A={1,3,6,8,10}` and `B={2,4,6,7,10}`:

```text
A∩B={6,10}
A∪B={1,2,3,4,6,7,8,10}
A−B={1,3,8}
```

## 37. Set identities and element proof

The logic laws have set analogues: identity, domination, idempotence, commutativity, associativity, distributivity, absorption, complements, and De Morgan:

```text
(A∪B)^c=A^c∩B^c
(A∩B)^c=A^c∪B^c
A∩(B∪C)=(A∩B)∪(A∩C)
A∪(B∩C)=(A∪B)∩(A∪C)
```

Formal proof technique: show mutual containment. For distributivity, for arbitrary `x`:

```text
x∈A∩(B∪C)
↔ x∈A ∧ (x∈B∨x∈C)
↔ (x∈A∧x∈B) ∨ (x∈A∧x∈C)
↔ x∈(A∩B)∪(A∩C).
```

## 38. Disjoint sets and partitions

Sets are **disjoint** if their intersection is empty. A collection `{A1,…,Ak}` partitions `A` iff:

1. every `Ai` is nonempty;
2. `Ai∩Aj=∅` whenever `i≠j`;
3. `A1∪⋯∪Ak=A`.

Modulo classes partition the integers. For modulus 3, every integer belongs to exactly one of `[0],[1],[2]`, determined by its remainder.

`a≡b (mod n)` means `n|(a-b)`, equivalently `a` and `b` leave the same remainder modulo positive `n`.

## 39. Power set

The **power set** `P(A)` is the set of every subset of `A`, including `∅` and `A`. If `|A|=n`, then

```text
|P(A)|=2^n.
```

Induction proof: remove an element `e`. The subsets split into two equal classes—those excluding `e`, in bijection with `P(A−{e})`, and those including `e`, obtained by adding `e` to each such subset. Thus `2^(n-1)+2^(n-1)=2^n`.

## 40. Cartesian product

```text
A×B={(a,b) | a∈A and b∈B}.
```

Ordered pairs matter: `(a,b)` need not equal `(b,a)`, and generally `A×B≠B×A`. If finite `|A|=m`, `|B|=n`, then `|A×B|=mn`. The rule extends to tuples: `|A1×⋯×Ak|=∏|Ai|`.

## 41. Russell’s and barber paradoxes

Naive unrestricted set formation creates Russell’s set

```text
R={x | x is a set and x∉x}.
```

If `R∈R`, its definition implies `R∉R`; if `R∉R`, its definition implies `R∈R`. The paradox shows that not every predicate can define a set inside a consistent naive theory; axiomatic set theories restrict comprehension.

Barber form: a barber shaves exactly those men who do not shave themselves. Asking whether the barber shaves himself produces the same self-reference contradiction.

### L07 common wrong answers

- Confusing `∅`, `{∅}`, and `{{∅}}`.
- Counting repeated roster entries more than once.
- Treating `∈` as `⊆`.
- Taking a complement without declaring the universe.
- Calling overlapping subsets a partition.

---

# Lecture 08 — Basic Counting, Inclusion–Exclusion, Permutations, and Binomial Identities

## 42. Sum and product rules

**Sum rule:** if `A` and `B` are disjoint finite sets,

```text
|A∪B|=|A|+|B|.
```

Operationally: if a task can be completed by one of mutually exclusive strategies with `n1,n2,…,nk` outcomes, total outcomes are `n1+⋯+nk`.

**Product rule:** if a procedure has successive choices with `n1,n2,…,nk` possibilities, and each complete outcome corresponds to exactly one choice tuple, then

```text
n1n2⋯nk
```

outcomes exist. The later number of choices may depend on earlier choices, but it must have the stated value for every relevant partial choice.

Examples:

- three ways from Palasi to Shahbag followed by five ways to Banani give `3·5=15` routes;
- one CR from 20 girls and one from 40 boys gives `20·40=800` pairs;
- length-`n` strings over an alphabet of size `m` give `m^n` strings.

## 43. Complement and partition techniques

“At least one” is often easiest by complement:

```text
# with at least one required feature = # all − # with none.
```

Password example: using 26 letters and 10 digits, length `n` with at least one digit:

```text
36^n−26^n.
```

For lengths 6, 7, or 8, sum this expression over those three lengths.

Case-sensitive passwords of length 6–8 that start with a letter use 52 choices first and 62 afterward:

```text
52·62^5 + 52·62^6 + 52·62^7 = 186,125,210,680,448.
```

The slide’s “four-digit numbers with at least one 7” calculation `10^4−9^4=3439` is correct for **four-character decimal strings with leading zero allowed**. For actual integers 1000–9999, the count is

```text
9000 − 8·9^3 = 3168,
```

because the first digit cannot be zero and, when avoiding 7, has 8 choices.

Serial-number example: a six-digit string with all digits distinct has

```text
10·9·8·7·6·5=151,200
```

possibilities out of `10^6`, so probability `0.1512`; a repeated-digit (“defective”) serial has probability `0.8488` under a uniform model.

## 44. Inclusion–exclusion

For two finite sets:

```text
|A∪B|=|A|+|B|−|A∩B|.
```

For three:

```text
|A∪B∪C|
=|A|+|B|+|C|
−|A∩B|−|A∩C|−|B∩C|
+|A∩B∩C|.
```

In general,

```text
|⋃_(i=1)^n Ai|
= Σ_(∅≠S⊆{1,…,n}) (−1)^(|S|+1) |⋂_(i∈S) Ai|.
```

The signs alternate because an element contained in exactly `r` sets is counted

```text
C(r,1)−C(r,2)+⋯+(−1)^(r+1)C(r,r)=1
```

time.

Worked examples:

- Multiples of 3 or 5 among `1,…,1000`: `⌊1000/3⌋+⌊1000/5⌋−⌊1000/15⌋=333+200−66=467`.
- Length-8 bit strings starting with 1 or ending in 00: `2^7+2^6−2^5=160`.
- Integers `1,…,1000` divisible by neither 3 nor 4: `1000−(333+250−83)=500`.
- In 50 students, 47 know at least one of Java/C++/C#; singles are `30,18,26`, pair intersections `9,16,8`. Thus all three `=47−30−18−26+9+16+8=6`, and none `=50−47=3`.

Viva trap: pairwise intersections include those in all three unless “exactly two” is explicitly stated.

## 45. Permutations and combinations

A **permutation** of an `n`-element set is an ordering of every element. There are `n!` permutations, where `0!=1`.

An ordered selection of `r` distinct items is

```text
P(n,r)=n(n−1)⋯(n−r+1)=n!/(n−r)!.
```

An unordered selection/subset of size `r` is

```text
C(n,r)=(n choose r)=n!/[r!(n−r)!].
```

Division by `r!` removes the `r!` orderings of each chosen subset. A length-`n` bit string containing exactly `r` ones is determined by their positions, so there are `C(n,r)`.

Useful identities:

```text
C(n,0)=C(n,n)=1
C(n,r)=C(n,n−r)
C(n+1,r)=C(n,r−1)+C(n,r)     Pascal
Σ_(r=0)^n C(n,r)=2^n
```

## 46. Poker worked examples

Total five-card hands:

```text
C(52,5)=2,598,960.
```

- Four of a kind: choose rank of four, then rank and suit of kicker:

```text
13·12·4=624.
```

- Full house: choose triple rank/suits, pair rank/suits:

```text
13·C(4,3)·12·C(4,2)=3744.
```

- Exactly two pairs: choose two pair ranks, their suits, then kicker rank/suit:

```text
C(13,2)·C(4,2)^2·11·4=123,552.
```

Equivalently the slide orders the two pair ranks and divides by 2. Forgetting this division double-counts each hand.

- At least one card of every suit: exactly one suit appears twice. Choose a value in each suit, the repeated suit, and a second distinct value there, then divide by 2 because the two cards of the repeated suit were ordered:

```text
13^4·4·12/2=685,464.
```

## 47. Binomial theorem

```text
(a+b)^n = Σ_(k=0)^n C(n,k)a^(n−k)b^k.
```

When multiplying `n` copies of `(a+b)`, a term `a^(n-k)b^k` results by choosing `b` from exactly `k` factors; there are `C(n,k)` choices.

Substitutions give:

```text
Σ C(n,k)=2^n                         set a=b=1
Σ (−1)^k C(n,k)=0 for n>0           set a=1,b=−1
Σ_(k even) C(n,k)=Σ_(k odd) C(n,k)=2^(n−1), n>0.
```

## 48. Combinatorial proof / double counting

A combinatorial proof defines one finite set and counts it two ways. It must explain why both expressions count the **same objects exactly once**.

### Symmetry

`C(n,k)=C(n,n-k)` because choosing the `k` included elements is in bijection with choosing the `n-k` excluded elements.

### Pascal’s identity

Count `k`-subsets of an `(n+1)`-element set according to whether a fixed element `x` is chosen:

```text
C(n+1,k)=C(n,k−1)+C(n,k).
```

### Vandermonde identities from the slides

Choose `n` balls from `n` red plus `n` blue balls, grouped by number `i` of red balls:

```text
Σ_(i=0)^n C(n,i)C(n,n−i)
=Σ_(i=0)^n C(n,i)^2
=C(2n,n).
```

Choose `n` cards from `n` red plus `2n` black cards, grouped by `r` red cards:

```text
Σ_(r=0)^n C(n,r)C(2n,n−r)=C(3n,n).
```

## 49. Counting decision checklist

1. Is the operation “OR” between disjoint cases? Use sum.
2. Is it a sequence of choices? Use product.
3. Do cases overlap? Partition more carefully or use inclusion–exclusion.
4. Is order relevant? Permutation if yes, combination if no.
5. Are objects repeated/identical? Expect division, stars-and-bars, or a generating function.
6. Is there an “at least one”? Try complement.
7. Can the same outcome be generated several ways? Identify and remove the exact multiplicity.

---

# Lecture 09 Part 1 — Functions and the Pigeonhole Principle

## 50. Function

A function `f:A→B` assigns **exactly one** element `f(x)∈B` to every input `x∈A`.

- `A` is the domain.
- `B` is the codomain.
- `f(A)={f(x)|x∈A}` is the image/range, which may be a proper subset of `B`.
- A many-to-one mapping is still a function; one input with two outputs is not.

Examples:

- `f(S)=|S|`, from finite sets to nonnegative integers, is a function.
- `length(s)` from strings to nonnegative integers is a function.
- `isPrime(n)` from positive integers to `{T,F}` is a function.
- “student name → student ID” may fail if the input really is only a nonunique name; “student record → unique ID” is a function.

## 51. Injection, surjection, bijection

```text
Injective (one-to-one): ∀x1,x2∈A, f(x1)=f(x2) → x1=x2.
Equivalent: x1≠x2 → f(x1)≠f(x2).

Surjective (onto):      ∀y∈B, ∃x∈A such that f(x)=y.

Bijective:              injective and surjective.
```

For finite sets:

- injection `A→B` implies `|A|≤|B|`;
- surjection implies `|A|≥|B|`;
- bijection implies `|A|=|B|`.

Cardinality equality alone does not make a particular function bijective; it only makes one possible. Infinite sets require more care: `n↦2n` is an injection from integers to integers whose image is only the even integers.

## 52. Fibers, inverse, and composition

The **inverse image/fiber** of `y∈B` is a set:

```text
f^(-1)({y})={x∈A | f(x)=y}.
```

This exists as a set for any function and may contain zero, one, or many inputs. An **inverse function** `f^(-1):B→A` exists iff `f` is bijective; then every fiber contains exactly one element.

For `f:X→Y` and `g:Y→Z`, composition is

```text
(g∘f)(x)=g(f(x)).
```

Composition is associative but generally not commutative. The codomain/type of the inner function must fit the domain of the outer one.

## 53. Ordinary pigeonhole principle — exact statement

### Object/box form

If more than `m` objects are placed in `m` boxes, some box contains at least two objects.

### Function form with quantifiers

For finite sets `A,B`:

```text
∀f:A→B, |A|>|B| → ∃x1,x2∈A
   (x1≠x2 ∧ f(x1)=f(x2)).
```

In words: a function from a larger finite set to a smaller finite set cannot be injective.

Proof by contradiction: if every box contained at most one object, then at most `m` objects could have been placed, contradicting that there were more than `m`.

## 54. Generalized pigeonhole principle

If `N` objects are distributed among `m≥1` boxes, then

```text
∃ a box containing at least ⌈N/m⌉ objects.
```

Fiber/quantifier form:

```text
∀f:A→B, |A|=N, |B|=m,
∃y∈B: |f^(-1)({y})| ≥ ⌈N/m⌉.
```

Equivalent threshold form:

```text
N>m(r−1)  ⇒  some box contains at least r objects.
```

The bound is tight: distribute objects as evenly as possible, so all box sizes are `⌊N/m⌋` or `⌈N/m⌉`. A dual averaging statement says some box contains at most `⌊N/m⌋` objects.

Proof: if every box had at most `⌈N/m⌉−1`, total objects would be at most `m(⌈N/m⌉−1)<N`, contradiction.

## 55. Pigeonhole recipe

Before calculating, say all four items aloud:

1. **Pigeons/objects:** what is being mapped?
2. **Holes/boxes:** what categories/images are possible?
3. **Mapping:** which box receives each object?
4. **Cardinality comparison:** why is the domain large enough?

The principle proves existence, not the identities of the colliding objects.

## 56. Worked pigeonhole examples from the slides

### Five selected integers contain a pair summing to 9

Partition `{1,…,8}` into four holes:

```text
{1,8}, {2,7}, {3,6}, {4,5}.
```

Five chosen numbers are five pigeons in four pair-boxes, so one box contributes both elements; they sum to 9.

### Equal handshake counts

In a party of `n` people, two have the same number of handshakes. A person can have degree `0,…,n−1`, but `0` and `n−1` cannot both occur: if someone met everyone, nobody met zero people. Therefore at most `n−1` degree values are realized by `n` people, forcing a repeated value.

This is also a graph-theory degree argument. Saying merely “there are `n` values for `n` people” would not be enough.

### Cards and suits

Ten cards mapped to four suit boxes force at least

```text
⌈10/4⌉=3
```

cards of one suit.

### Birthday guarantee versus birthday probability

- Deterministic PHP: with 366 possible calendar birthdays, 367 people guarantee a shared birthday.
- Probability model (ignore leap day, assume uniform independent birthdays):

```text
P(no shared birthday among n)
=365·364·⋯·(365−n+1)/365^n,

P(at least one shared birthday)=1−that.
```

At `n=23`, the collision probability is about `0.507`; at `n=57`, about `0.990`. The 23-person result is not a direct pigeonhole guarantee.

### Equal subset sums

For 90 positive integers, each with at most 25 digits, there are `2^90` subsets. Every subset sum is a nonnegative integer below `90·10^25`, so there are fewer than about `9·10^26+1` possible sums. Since

```text
2^90 ≈ 1.238·10^27,
```

two distinct subsets have the same sum.

### Club or strangers: `R(3,3)=6`

Choose one person `x` among six. Of the other five, at least three are acquaintances of `x` or at least three are strangers to `x` (`⌈5/2⌉=3`).

- If three know `x`, either some pair among them know each other—forming a three-person club with `x`—or no pair do, forming three mutual strangers.
- The stranger case is symmetric.

Thus any six people contain three mutual acquaintances or three mutual strangers.

## 57. Strong real-world/computing applications

### Hash collisions — best one-minute viva answer

A hash function maps a huge key space into a finite set of hash values/buckets:

```text
h: Keys → {0,…,m−1}.
```

Because the possible keys outnumber the buckets, the pigeonhole principle guarantees two distinct keys with the same hash. A hash table must therefore resolve collisions using chaining or open addressing and still compare actual keys; a cryptographic hash cannot make collisions mathematically impossible, only computationally hard to find.

### Load/congestion lower bound

Assign `N` requests to `m` servers. Regardless of the load balancer, some server receives at least `⌈N/m⌉` requests. This supplies a hard lower bound on peak load; it does **not** say which server or that a poor algorithm cannot do worse.

### Lossless compression impossibility

There are `2^n` binary strings of length `n`, but only

```text
1+2+⋯+2^(n−1)=2^n−1
```

binary strings shorter than `n`. Therefore no injective lossless compressor can shorten **every** `n`-bit input. Some inputs must remain at least `n` bits.

### Remainder collision

Among `n+1` integers, two have the same remainder modulo `n`; subtracting them gives a multiple of `n`. Pigeons are integers, holes are remainders `0,…,n−1`.

### What was weak about “resources and programs”?

It did not define objects, boxes, or a forced conclusion. A solid answer is: “Map `N` jobs to `m` CPU workers. PHP guarantees one worker receives at least `⌈N/m⌉` jobs.” The exact mapping and bound make it a proof rather than an analogy.

## 58. Pigeonhole traps

- `N=m` does not force a collision.
- Use ceiling for a guaranteed maximum load, not floor.
- The birthday paradox is probabilistic; the 367-person statement is deterministic.
- Categories must cover every object and the mapping must be well-defined.
- A hash collision means equal hash values, not equal keys.
- PHP does not produce the pair; it proves at least one exists.

---

# Lecture 09 Parts 2–3 — Counting by Mapping

## 59. Bijection rule

If `f:A→B` is a bijection, then `|A|=|B|`. To count a complicated set `A`, map it bijectively to an easier set `B`, then prove:

- injection: different `A`-objects yield different encodings;
- surjection: every valid `B`-encoding decodes to an `A`-object.

### Power set ↔ bit strings

For `S={s1,…,sn}`, map subset `T` to bit string `b1…bn`, where `bi=1` iff `si∈T`. The inverse reads selected positions, so it is a bijection and `|P(S)|=2^n`.

```text
POWER-SET(S):
    for mask = 0 to 2^|S| − 1:
        T = empty set
        for i = 0 to |S|−1:
            if bit i of mask is 1: add S[i] to T
        output T
```

Time is `Θ(n2^n)` if each subset is explicitly materialized; output size already makes exponential work unavoidable.

### Three distinct chess pieces in different rows/columns

Encode pawn, knight, bishop by their row/column coordinates. Choose three ordered distinct rows and three ordered distinct columns:

```text
(8·7·6)^2=112,896.
```

## 60. Stars and bars

Choosing 12 doughnuts from 5 types corresponds to 12 zeros (items) and 4 ones (separators), so

```text
C(12+5−1,5−1)=C(16,4)=1820.
```

General forms:

```text
x1+⋯+xk=n, xi≥0:   C(n+k−1,k−1)
x1+⋯+xk=n, xi≥1:   C(n−1,k−1)
x1+⋯+xk≤n, xi≥0:   C(n+k,k)       (add slack variable)
```

For lower bounds `xi≥li`, set `yi=xi−li≥0` and reduce the target by `Σli`.

Examples from the slides:

```text
x1+x2+x3+x4=10, xi≥0: C(13,3)=286.
x1+x2+x3+x4=14, xi≥1: C(13,3)=286.
x1+x2+x3+x4≤10, xi≥0: C(14,4)=1001.
```

## 61. Choosing nonadjacent objects

Choose `r` nonadjacent positions from a row of `N`. If chosen indices are

```text
1≤a1<a2<⋯<ar≤N, with a_(i+1)≥ai+2,
```

set `bi=ai−(i−1)`. Then `1≤b1<⋯<br≤N−r+1`, a bijection to ordinary `r`-subsets. Therefore

```text
C(N−r+1,r).
```

For 6 nonadjacent books among 20: `C(15,6)=5005`.

## 62. Counting a nested loop by mapping

The slide loop is

```c
for (int i = 1; i <= n; i++)
    for (int j = 1; j <= i; j++)
        for (int k = 1; k <= j; k++)
            printf("hello world\n");
```

Iterations correspond to triples `1≤k≤j≤i≤n`, or multisets of size 3 chosen from `n` values. Thus

```text
C(n+3−1,3)=C(n+2,3)=n(n+1)(n+2)/6.
```

The exact count is `Θ(n³)`. Do not multiply `n·n·n` as if every loop always ran `n` times; bounds depend on outer indices.

## 63. Division rule / constant-size fibers

If `f:A→B` is onto and every `b∈B` has exactly `k` preimages, then

```text
|A|=k|B|, so |B|=|A|/k.
```

Examples:

- Two identical nonattacking rooks: ordered placements number `8²·7²=3136`; swapping rook labels gives the same placement, so divide by 2: `1568`.
- `n` distinct people around a round table, rotations equivalent: each circular arrangement has `n` linear representations, so `n!/n=(n−1)!`.
- Size-4 subsets of a 13-set: mapping permutations to their first four as a set has fiber size `4!9!`, giving `13!/(4!9!)=C(13,4)`.

Division works only when every final object is overcounted by the same factor.

## 64. Repeated objects and multinomial counting

If a word has `n` letters with multiplicities `n1,…,nk`, distinct rearrangements number

```text
n!/(n1!n2!⋯nk!).
```

`MISSISSIPPI` contains 11 letters: `M^1 I^4 S^4 P^2`, hence

```text
11!/(4!4!2!)=34,650.
```

The source slide displays `13!/(4!4!2!)`; that is a typo because the word has 11 letters.

A 20-mile walk with five moves each N/E/S/W has

```text
20!/(5!5!5!5!)
```

distinct direction sequences.

## 65. Catalan bijections

The following sets have the same cardinality:

- valid strings of `n` pairs of parentheses;
- monotone paths from `(0,0)` to `(n,n)` that never cross the diagonal;
- mountain paths with `n` upstrokes and `n` downstrokes that never go below the baseline.

Map `(` to right/upstroke and `)` to up/downstroke. Prefix validity—opens at least closes—becomes the geometric noncrossing condition.

Their common count is the Catalan number

```text
C_n = 1/(n+1) C(2n,n) = C(2n,n)−C(2n,n+1).
```

First values: `1,1,2,5,14,42,…` for `n=0,1,2,…`.

### Counting-by-mapping viva test

Never stop after saying “there is a mapping.” State its encoding, inverse/decoding, and why it is one-to-one and onto—or state the exact constant fiber size if using division.

# Lecture 10 — Number Sequences, Sums, Annuities, Harmonic Growth, and Factorials

## 66. Sequence: explicit and recursive descriptions

A **sequence** is an ordered list `a1,a2,...` (or `a0,a1,...`). It is formally a function whose domain is an initial part of the integers or all nonnegative/positive integers. Order and index matter: `{1,2,3}` is a set, while `<1,2,3>` is a sequence.

An **explicit formula** gives a term directly from its index. Slide examples include

```text
ai = i             -> 1,2,3,4,...
ai = i^2           -> 1,4,9,16,...
ai = 2^i           -> 2,4,8,16,...
ai = (-1)^i        -> -1,1,-1,1,...
ai = i/(i+1)       -> 1/2,2/3,3/4,...
```

Other pattern exercises are

```text
1/4,2/9,3/16,4/25,...       ai=i/(i+1)^2
1/3,2/9,3/27,4/81,...       ai=i/3^i
0,1,-2,3,-4,5,...           ai=(i-1)(-1)^i
1,-1/4,1/9,-1/16,...        ai=(-1)^(i+1)/i^2
```

A **recursive definition** supplies base value(s) and defines later values using earlier ones:

```text
a1=1, ai=ai-1+2             -> 1,3,5,7,...
a1=1, ai=2ai-1              -> 1,2,4,8,...
a1=a2=1, ai=ai-1+ai-2       -> Fibonacci 1,1,2,3,5,...
```

Both parts are essential. A recurrence without enough base cases does not determine a unique sequence.

### Repeated-squaring example

Given `a1=3` and `ai=(ai-1)^2`, the first terms are `3,9,81,6561,...`. The exact formula is

```text
ai = 3^(2^(i-1)).
```

Induction: it holds for `i=1`. If `ai=3^(2^(i-1))`, then

```text
ai+1=(ai)^2=(3^(2^(i-1)))^2=3^(2^i).
```

This example is a reminder that looking at initial values suggests a claim; it does not prove it.

## 67. Summation notation and legal index manipulation

```text
sum(i=m..n) ai = am + am+1 + ... + an.
```

Linearity:

```text
sum(c ai + d bi) = c sum(ai) + d sum(bi).
```

Splitting a range:

```text
sum(i=m..n) ai = sum(i=m..k) ai + sum(i=k+1..n) ai.
```

Change of variable must preserve the same terms. For example, with `j=i+1`,

```text
sum(i=1..n) 1/(i+1) = sum(j=2..n+1) 1/j.
```

Common viva error: changing `i` to `i+1` inside the summand but forgetting to change both limits.

## 68. Telescoping sums

Partial fractions expose cancellation:

```text
1/[i(i+1)] = 1/i - 1/(i+1).
```

Therefore

```text
sum(i=1..n) 1/[i(i+1)]
= (1-1/2)+(1/2-1/3)+...+(1/n-1/(n+1))
= 1-1/(n+1)
= n/(n+1).
```

A series **telescopes** when most adjacent terms cancel after rewriting. Whiteboard method: derive the partial fraction, expand three terms, show cancellation, keep the boundary terms.

## 69. Arithmetic sequences and sums

An arithmetic sequence has constant difference `d`:

```text
ai+1=ai+d,
an=a1+(n-1)d.
```

Its first-`n` sum is

```text
Sn = n(a1+an)/2
   = n[2a1+(n-1)d]/2.
```

Proof by pairing: write the sum forward and backward. Every column adds to `a1+an`; there are `n` columns, so `2Sn=n(a1+an)`.

Slide example: `89,102,...,466` has 30 terms and common difference 13. Fifteen pairs each sum to `555`, so the total is `8325`.

Special cases worth instant recall:

```text
1+2+...+n = n(n+1)/2
1+3+...+(2n-1) = n^2
2+4+...+2n = n(n+1).
```

## 70. Geometric sequences and finite/infinite series

A geometric sequence has constant ratio `r`:

```text
ai+1=r ai,
an=a1 r^(n-1).
```

For `r != 1`, subtracting `rSn` from `Sn` gives

```text
1+r+r^2+...+r^n = (1-r^(n+1))/(1-r)
                 = (r^(n+1)-1)/(r-1).
```

More generally,

```text
a1+a1r+...+a1r^(n-1) = a1(1-r^n)/(1-r).
```

If `|r|<1`, then `r^(n+1)->0`, so

```text
sum(i=0..infinity) r^i = 1/(1-r).
```

The condition `|r|<1` is not optional. At `r=1` the partial sums grow; for `r=-1` they oscillate; for `|r|>1` the terms do not even approach zero.

## 71. Geometric-factorization proof: a Mersenne necessary condition

Claim: if `2^n-1` is prime, then `n` is prime.

Prove the contrapositive. If `n=pq` with `p,q>1`, put `x=2^q`. Then

```text
2^n-1 = 2^(pq)-1
      = x^p-1
      = (x-1)(1+x+x^2+...+x^(p-1))
      = (2^q-1)(1+2^q+2^(2q)+...+2^((p-1)q)).
```

Both factors exceed 1, so `2^n-1` is composite. Thus the contrapositive, and hence the original implication, is true.

The converse is false: prime `n` does not guarantee a Mersenne prime; `n=11` gives `2^11-1=2047=23*89`.

## 72. Present value and annuities

Let the annual **bank factor** be `b=1+i`, where `i` is the interest rate, and let the discount factor be `r=1/b`. Money `P` received `k` years from now has present value

```text
PV = P/b^k = P r^k.
```

For equal end-of-year payments `P` for `N` years,

```text
PV = P(r+r^2+...+r^N)
   = Pr(1-r^N)/(1-r).
```

If payments begin immediately instead, include the `r^0` term:

```text
PV_due = P(1+r+...+r^(N-1)).
```

This timing distinction is a frequent error. The slide's `$100` paid at each year-end for 10 years with `b=1.03` has

```text
PV=100r(1-r^10)/(1-r) approximately $853.02.
```

For a perpetuity beginning now,

```text
P+Pr+Pr^2+... = P/(1-r),   |r|<1.
```

For payments growing linearly—`m,2m,3m,...` at successive year ends—differentiate the geometric series:

```text
sum(i=1..infinity) i x^i = x/(1-x)^2, |x|<1,
PV = m r/(1-r)^2.
```

Why can an infinite stream have finite value? Discounting is exponential, and exponential decay dominates linear payment growth.

## 73. Harmonic numbers and growth

The `n`th harmonic number is

```text
Hn = 1 + 1/2 + 1/3 + ... + 1/n.
```

It diverges, but very slowly. Group denominators by powers of two:

```text
1 | 1/2 | 1/3+1/4 | 1/5+...+1/8 | ...
```

Each full block after the first has sum between `1/2` and `1`, so with about `log2 n` blocks,

```text
Hn = Theta(log n).
```

The integral comparison gives tighter bounds because `1/x` decreases:

```text
integral(1..n+1) dx/x <= Hn <= 1 + integral(1..n) dx/x,
ln(n+1) <= Hn <= 1+ln n.
```

More precisely, `Hn=ln n+gamma+o(1)`, where `gamma` is Euler's constant, but the slides' essential result is logarithmic growth.

## 74. Guessing the sum of squares

The integral of `x^2` suggests cubic growth, so guess a cubic polynomial

```text
sum(i=1..n) i^2 = an^3+bn^2+cn+d.
```

Substituting four small `n` values determines `a=1/3`, `b=1/2`, `c=1/6`, `d=0`, yielding

```text
1^2+2^2+...+n^2 = n(n+1)(2n+1)/6.
```

After guessing, prove it by induction. Never present interpolation from a few points as the proof.

## 75. Products, factorial, logarithms, and Stirling's formula

Product notation:

```text
product(i=m..n) ai = am am+1 ... an.
```

Factorial is

```text
n! = product(i=1..n) i,  and 0!=1.
```

Taking logs converts a product to a sum:

```text
ln(n!) = sum(i=1..n) ln i.
```

Integral comparison gives the main scale

```text
integral(1..n) ln x dx = n ln n - n + 1,
ln(n!) = Theta(n ln n).
```

Exponentiating shows `n!` is roughly of order `(n/e)^n` times a subexponential factor. Stirling's approximation sharpens it:

```text
n! ~ sqrt(2*pi*n) (n/e)^n.
```

Here `f(n)~g(n)` means `f(n)/g(n)->1`, stronger than merely `Theta(g(n))`.

### L10 recall and coding drill

```text
sequence -> explicit or recurrence + base cases
sum      -> linearity / pairing / telescoping / geometric formula
growth   -> grouping or integral comparison
product  -> take logarithms
```

An iterative generator for the recurrence `a1=3, ai=ai-1^2` uses constant extra space:

```text
a = 3
for i = 2 to n:
    a = a*a
return a
```

It performs `n-1` multiplications, hence `Theta(n)` arithmetic operations, although bit complexity grows much faster because the number itself doubles in bit-length at every squaring.

# Lecture 11 — Ordinary Generating Functions

## 76. What a generating function is

For a sequence `<g0,g1,g2,...>`, its **ordinary generating function (OGF)** is

```text
G(x) = g0 + g1 x + g2 x^2 + ... = sum(n>=0) gn x^n.
```

The coefficient-extraction notation is

```text
[x^n]G(x)=gn.
```

A generating function encodes the entire sequence in the coefficients of one algebraic object. In counting, `x` is usually a **formal variable**: the point is coefficient algebra, not numerical convergence. Analytic convergence becomes relevant only when we substitute a numerical value.

Basic correspondences:

```text
<1,0,0,0,...>             <-> 1
<0,1,0,0,...>             <-> x
<1,1,1,1,...>             <-> 1/(1-x)
<1,r,r^2,r^3,...>         <-> 1/(1-rx)
<1,-1,1,-1,...>           <-> 1/(1+x)
<0,1,2,3,...>             <-> x/(1-x)^2
<1,2,3,4,...>             <-> 1/(1-x)^2
```

## 77. Operations on generating functions

Suppose `A(x)=sum an x^n` and `B(x)=sum bn x^n`.

### Scaling and addition

```text
cA(x)             <-> <ca0,ca1,...>
A(x)+B(x)         <-> <a0+b0,a1+b1,...>.
```

### Right shift

Multiplying by `x^k` inserts `k` zeros at the front:

```text
x^k A(x) = sum(n>=0) an x^(n+k)
          <-> <0,...,0,a0,a1,...>.
```

### Differentiation

```text
A'(x)=a1+2a2 x+3a3 x^2+...
```

Starting with `1/(1-x)=sum(n>=0)x^n`:

```text
d/dx [1/(1-x)] = 1/(1-x)^2
                = sum(n>=0)(n+1)x^n.
```

To generate positive squares, note

```text
sum(n>=1) n x^n = x/(1-x)^2.
```

Differentiate and multiply by `x`:

```text
sum(n>=1) n^2 x^n = x(1+x)/(1-x)^3.
```

Equivalently, `<1,4,9,16,...>` has OGF `(1+x)/(1-x)^3` when index 0 contains `1^2`.

### Product / convolution

```text
C(x)=A(x)B(x),
cn=[x^n]C(x)=sum(i=0..n) ai b(n-i).
```

This is the **Cauchy product** or convolution. The exponent `n` can be split as `i+(n-i)`, so the coefficient sums all compatible choices from the two factors.

## 78. Taylor and the negative-binomial identity

Taylor's formula at zero is

```text
f(x)=sum(n>=0) f^(n)(0)/n! * x^n.
```

Applied to `(1-x)^(-k)` for a positive integer `k`, it gives

```text
(1-x)^(-k) = sum(n>=0) C(n+k-1,k-1)x^n
            = sum(n>=0) C(n+k-1,n)x^n.
```

This is the GF form of stars and bars. For `k=2`,

```text
1/(1-x)^2 = sum(n>=0)(n+1)x^n.
```

## 79. Counting distinct and unlimited selections

For one distinct object, the choices are “take zero” or “take one,” so its factor is `1+x`. For `k` distinct objects,

```text
(1+x)^k,
[x^n](1+x)^k=C(k,n).
```

For one type with unlimited identical copies, the choices are `0,1,2,...`, so its factor is

```text
1+x+x^2+...=1/(1-x).
```

For `k` varieties and `n` total items,

```text
[x^n](1-x)^(-k)=C(n+k-1,k-1).
```

This is exactly the number of nonnegative integer solutions of `x1+...+xk=n`.

## 80. Translating restrictions into factors

For each independent category, write one polynomial/series whose allowed exponents are its allowed quantities; multiply the factors; extract the coefficient for the required total.

```text
exactly r copies       -> x^r
at most r copies       -> 1+x+...+x^r
at least r copies      -> x^r/(1-x)
even number            -> 1+x^2+x^4+...=1/(1-x^2)
multiple of q          -> 1+x^q+x^(2q)+...=1/(1-x^q)
zero or one            -> 1+x
unlimited              -> 1/(1-x).
```

### Fruit problem from the slides

The requirements are: apples even, bananas a multiple of 5, at most four oranges, and at most one pear. Therefore

```text
A(x)=1/(1-x^2)
B(x)=1/(1-x^5)
O(x)=1+x+x^2+x^3+x^4=(1-x^5)/(1-x)
P(x)=1+x=(1-x^2)/(1-x).
```

Multiplying causes complete cancellation:

```text
F(x)=A(x)B(x)O(x)P(x)=1/(1-x)^2.
```

Hence the number of bags containing `n` fruits is

```text
[x^n]F(x)=n+1.
```

For `n=6`, this gives 7, matching the slide's enumeration.

## 81. Fibonacci by generating functions

Let `r0=0`, `r1=1`, and `rn=rn-1+rn-2` for `n>=2`. Define

```text
R(x)=r0+r1x+r2x^2+...
```

Align the recurrence by shifting:

```text
R(x)             = r0+r1x+r2x^2+r3x^3+...
-xR(x)           =    -r0x-r1x^2-r2x^3-...
-x^2R(x)         =          -r0x^2-r1x^3-...
```

Every coefficient of degree at least 2 vanishes, leaving

```text
(1-x-x^2)R(x)=x,
R(x)=x/(1-x-x^2).
```

Factor the denominator using

```text
phi=(1+sqrt(5))/2, psi=(1-sqrt(5))/2,
1-x-x^2=(1-phi*x)(1-psi*x).
```

Partial fractions and `1/(1-cx)=sum c^n x^n` then give Binet's formula:

```text
rn=(phi^n-psi^n)/sqrt(5).
```

The derivation pattern matters more than memorizing the last formula: define the OGF, multiply by shifts matching the recurrence, isolate initial terms, solve algebraically, and extract coefficients.

## 82. Tower of Hanoi by generating functions

For `s0=0` and `sn=2sn-1+1`, define `S(x)=sum(n>=0)sn x^n`. Since the constant sequence beginning at degree 1 has GF `x/(1-x)`,

```text
S(x)-2xS(x)-x/(1-x)=0.
```

Thus

```text
S(x)=x/[(1-x)(1-2x)]
    = -1/(1-x)+1/(1-2x).
```

The coefficient of `x^n` is `-1+2^n`, so

```text
sn=2^n-1.
```

## 83. Slide exercises, fully worked

### Coefficient of `x^17` in `(1+x^5+x^7)^20`

Only `17=5+5+7` is possible. Choose two of the 20 factors to supply `x^5`, then one of the remaining 18 to supply `x^7`:

```text
C(20,2)C(18,1)=190*18=3420.
```

This also models 20 bags, each offering no coin, one distinguishable `$5` coin, or one distinguishable `$7` coin, with at most one coin selected per bag.

### Select 6 of 60 students

Each student contributes `1+x`, so

```text
[x^6](1+x)^60=C(60,6).
```

### Bounded integer solutions

For `a+b+c=6`, `-1<=a<=2`, and `1<=b,c<=4`, use

```text
(x^-1+1+x+x^2)(x+x^2+x^3+x^4)^2.
```

The coefficient of `x^6` is 12. Direct verification by `a` gives `2+3+4+3=12` solutions for `a=-1,0,1,2` respectively.

### An odd coefficient that vanishes

```text
1/[(1-x)^2(1+x)^2] = 1/(1-x^2)^2.
```

Only even powers occur, so

```text
[x^2005] 1/[(1-x)^2(1+x)^2] = 0.
```

### Logarithm generating function

Starting from `1/(1+x)=1-x+x^2-x^3+...` and integrating term by term,

```text
ln(1+x)=x-x^2/2+x^3/3-x^4/4+...
```

Thus `<0,1,-1/2,1/3,-1/4,...>` has OGF `ln(1+x)`.

### Distributing 30 identical souvenirs to 50 trainees

Each trainee receives any nonnegative number:

```text
G(x)=(1+x+x^2+...)^50=(1-x)^(-50).
```

Therefore

```text
[x^30]G(x)=C(30+50-1,30)=C(79,30)=C(79,49).
```

## 84. Coefficient-computation algorithms

Generating functions do not require symbolic algebra when only coefficients through degree `N` are needed. Truncate after every multiplication.

```text
multiplyTruncated(a[0..N], b[0..N], N):
    c[0..N] = all zeros
    for i = 0 to N:
        for j = 0 to N-i:
            c[i+j] += a[i] * b[j]
    return c
```

This direct convolution costs `Theta(N^2)` time and `Theta(N)` extra space. Repeating it for `k` category factors costs `O(kN^2)` in the simple implementation.

For unlimited copies of `k` item sizes, coefficient DP is faster:

```text
ways[0]=1; ways[1..N]=0
for each size s:
    for total = s to N:
        ways[total] += ways[total-s]
```

This computes coefficients of `product_s 1/(1-x^s)` in `O(kN)` time and `O(N)` space. The increasing inner loop is what permits repeated use of the current size.

### L11 viva traps

- The exponent records the total size; the coefficient records the number of ways.
- Multiplication represents combining independent/disjoint choices; addition represents disjoint alternatives.
- Check whether objects are distinct and whether repetition is permitted before choosing a factor.
- State indexing. `x/(1-x)^2` generates `<0,1,2,...>` from index 0, while `1/(1-x)^2` generates `<1,2,3,...>`.
- Simplify before expanding; parity or cancellation may make the answer immediate.

# Lecture 12 — Recursion, Recurrence Modeling, Recursive Programs, and Closed Forms

## 85. Recursion and recurrence relations

**Recursion** solves or defines an object in terms of smaller instances of the same kind. A recursive program needs:

1. a base case that returns without another recursive call;
2. a recursive case that reduces the problem;
3. a progress argument—a well-founded measure such as `n` strictly decreases, so the base case must eventually be reached.

A **recurrence relation** is an equation defining sequence terms from earlier terms. Its order is the number of previous positions needed. Initial values are part of the specification.

Slide examples, with consistent indexing, are

```text
arithmetic: a0=a, an=an-1+d                 -> an=a+nd
geometric:  a0=a, an=r an-1                 -> an=a r^n
harmonic:   a1=1, an+1=n an/(n+1), n>=1     -> an=1/n.
```

The source's harmonic line writes `a0=1` beside an `i/(i+1)` update; read literally at `i=0`, that would produce zero. The intended indexing is the corrected one above.

The rabbit-population motivation uses `wn` for newborn pairs and `rn` for reproducing pairs. Starting from `w0=1,r0=0`, newborns mature after one month and reproducing pairs remain reproducing:

```text
w(n)=r(n-1),
r(n)=r(n-1)+w(n-1),
therefore r(n)=r(n-1)+r(n-2).
```

This is how a story becomes a recurrence: name the state variables, state the timing assumptions, and eliminate the auxiliary variable.

## 86. How to derive a counting recurrence

Use this repeatable proof structure:

1. Define `rn` precisely.
2. Choose a structural feature that every size-`n` object has—often its first/last symbol or a distinguished element.
3. Partition all valid objects into disjoint, exhaustive cases.
4. Remove/fix that feature and map each case to smaller valid objects.
5. Apply product rule inside a case and sum rule across cases.
6. Give every required base value.

You must justify both **no omission** and **no double counting**. Guessing Fibonacci from the first few values is not a derivation.

## 87. Power-set recurrence

Let `rn=|P(Sn)|` for `Sn={a1,...,an}`. Every subset either excludes `an` or includes it:

```text
exclude an: any subset of S(n-1)             -> r(n-1)
include an:  add an to any subset of S(n-1)  -> r(n-1)
```

The two cases are disjoint and exhaustive, so

```text
r0=1,
rn=2r(n-1),
rn=2^n.
```

## 88. Bit strings avoiding `11`

Let `rn` count binary strings of length `n` that contain no consecutive `11`.

- If the string starts with `0`, append any valid length-`n-1` string: `r(n-1)` choices.
- If it starts with `1`, the next bit must be `0`; append any valid length-`n-2` string: `r(n-2)` choices.

Thus

```text
r0=1, r1=2,
rn=r(n-1)+r(n-2), n>=2.
```

Values are `1,2,3,5,8,...`, so `rn=F(n+2)` under `F0=0,F1=1`.

For strings avoiding `111`, partition by first valid terminating prefix `0`, `10`, or `110`:

```text
r0=1, r1=2, r2=4,
rn=r(n-1)+r(n-2)+r(n-3), n>=3.
```

### Memoized and bottom-up code

```text
countNo11(n):
    if n == 0: return 1
    if n == 1: return 2
    if memo[n] exists: return memo[n]
    memo[n] = countNo11(n-1) + countNo11(n-2)
    return memo[n]
```

Memoization uses `Theta(n)` time and `Theta(n)` memo/stack space. The direct un-memoized recursion is exponential because it recomputes the same states.

```text
countNo11Iterative(n):
    if n == 0: return 1
    prev2 = 1; prev1 = 2
    for length = 2 to n:
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current
    return prev1
```

The iterative version is `Theta(n)` time and `Theta(1)` auxiliary space.

## 89. Domino tilings of a `2 x n` board

Let `rn` be the number of tilings with `2 x 1` dominoes.

- A vertical first domino leaves a `2 x (n-1)` board: `r(n-1)`.
- If the first domino is horizontal, another horizontal domino is forced underneath it; they leave a `2 x (n-2)` board: `r(n-2)`.

Therefore

```text
r0=1, r1=1,
rn=r(n-1)+r(n-2).
```

Why `r0=1`? There is one empty tiling; it makes the recurrence work at `n=2`. Values are `1,1,2,3,5,...`, hence `rn=F(n+1)`.

## 90. Catalan recurrence from valid parentheses

Let `Cn` count valid strings containing `n` pairs of parentheses, with `C0=1`. Match the first `(` with its unique closing `)`. If there are `i` pairs inside it, there are `n-1-i` pairs after it:

```text
( valid-i-pair-string ) valid-(n-1-i)-pair-string.
```

For fixed `i`, product rule gives `Ci C(n-1-i)`. The matching position determines one disjoint case, so

```text
C0=1,
Cn=sum(i=0..n-1) Ci C(n-1-i).
```

This yields `1,1,2,5,14,42,...` and has closed form

```text
Cn = C(2n,n)/(n+1).
```

The slide's staircase-rectangle problem has the same recurrence: choose the rectangle covering the bottom-right corner. If it contains diagonal position `i`, it splits the remaining region into independent `(i-1)`- and `(n-i)`-stairs. Summing `C(i-1)C(n-i)` over `i=1..n` produces the same Catalan number.

### Dynamic program for Catalan numbers

```text
catalan(n):
    C[0] = 1
    for size = 1 to n:
        C[size] = 0
        for left = 0 to size-1:
            C[size] += C[left] * C[size-1-left]
    return C[n]
```

This direct recurrence DP takes `Theta(n^2)` arithmetic operations and `Theta(n)` space. The closed formula can be evaluated faster, but large-integer arithmetic and overflow must be considered.

## 91. Partitions into nonempty groups: Stirling numbers

Let `S(n,r)` be the number of ways to partition `n` labeled elements into `r` nonempty unlabeled groups—the Stirling number of the second kind. Focus on element `n`:

- It forms a singleton group. Partition the other `n-1` elements into `r-1` groups: `S(n-1,r-1)`.
- It does not form a singleton. Partition the other elements into `r` groups, then choose one of those `r` groups to receive it: `rS(n-1,r)`.

Thus

```text
S(n,r)=S(n-1,r-1)+rS(n-1,r).
```

Boundary conditions:

```text
S(0,0)=1;
S(n,0)=0 for n>0;
S(0,r)=0 for r>0;
S(n,n)=1; S(n,1)=1 for n>=1.
```

The deck checks `S(4,2)=7`, `S(4,3)=6`, and `S(4,4)=1`.

```text
stirlingSecond(n, r):
    create S[0..n][0..r], initially 0
    S[0][0] = 1
    for i = 1 to n:
        for j = 1 to min(i,r):
            S[i][j] = S[i-1][j-1] + j*S[i-1][j]
    return S[n][r]
```

Time is `O(nr)` and space is `O(nr)`, reducible to `O(r)` with two rows or a carefully descending one-dimensional update.

## 92. Tower of Hanoi recurrence and code

To move `n` disks from origin `o` to destination `d` using buffer `b`:

1. move the top `n-1` disks from `o` to `b`;
2. move disk `n` from `o` to `d`;
3. move the `n-1` disks from `b` to `d`.

Correct pseudocode—the slide mixes parameter names `number` and `n`, so keep one name consistently:

```text
Hanoi(o, d, b, n):
    if n == 0:
        return
    Hanoi(o, b, d, n-1)
    print "move disk", n, "from", o, "to", d
    Hanoi(b, d, o, n-1)
```

Move count:

```text
T(0)=0,
T(n)=2T(n-1)+1,
T(n)=2^n-1.
```

Time is `Theta(2^n)` because that many moves must be printed; maximum recursion depth and stack space are `Theta(n)`.

## 93. Merge sort recurrence, algorithm, and complexity

Merge sort recursively sorts two halves, then merges the sorted halves.

```text
mergeSort(A, left, right):
    if left >= right: return
    mid = left + floor((right-left)/2)
    mergeSort(A, left, mid)
    mergeSort(A, mid+1, right)
    merge(A, left, mid, right)

merge(A, left, mid, right):
    i=left; j=mid+1; temp=[]
    while i<=mid and j<=right:
        if A[i] <= A[j]: append A[i]; i++
        else:             append A[j]; j++
    append all remaining A[i..mid]
    append all remaining A[j..right]
    copy temp back to A[left..right]
```

Merging `n` total elements takes `Theta(n)` time and at most `n-1` key comparisons. For powers of two,

```text
T(n)=2T(n/2)+Theta(n).
```

The recursion tree has `log2 n` merge levels. Each level processes `n` elements altogether, so

```text
T(n)=Theta(n log n).
```

The usual array implementation uses `Theta(n)` temporary storage and a `Theta(log n)` call stack. Merge sort is stable when equal elements are taken from the left half first. Its worst-case time is `Theta(n log n)`, unlike elementary bubble/selection-style sorting at `Theta(n^2)`.

## 94. Reading recursive code and the call stack

The slide's “Hello World” routine is best written as `void`, because it prints rather than computes a returned integer:

```c
void hello(int n) {
    if (n == 0) return;
    printf("Hello World %d\n", n);
    hello(n - 1);
}
```

`hello(10)` prints `10,9,...,1`. If the recursive call comes before `printf`, stack frames first descend to zero and then print while unwinding, giving `1,2,...,10`.

`hello(-1)` never reaches the equality test `n==0`; `n` keeps decreasing until language-level integer overflow/undefined behavior or stack exhaustion. A robust precondition is `n>=0`, or use `if (n<=0) return` where that matches the specification.

Call-stack trace for the post-order version:

```text
hello(3)
  hello(2)
    hello(1)
      hello(0) returns
    print 1
  print 2
print 3
```

This explains why statement placement before or after the recursive call changes the output order.

## 95. Recursive sum of `1..n`

```c
long long AP(int n) {
    if (n == 0) return 0;
    return n + AP(n - 1);
}
```

Correctness mirrors induction: the base sum is zero; assuming `AP(n-1)` returns `1+...+(n-1)`, adding `n` gives the desired sum. It takes `n+1` calls, `Theta(n)` time, and `Theta(n)` stack space. The formula `n(n+1)/2` takes `Theta(1)` arithmetic operations, subject to integer-overflow considerations.

For teaching functions on a whiteboard, this is also a good motivation: put the repeated computation in a reusable unit `sumTo(n)`, give it an input contract, return one result, and test it independently.

## 96. Duplicate recursive work: exponential versus linear

The deck contrasts these two ways to compute `2^n`:

```c
long long exSlow(int n) {
    if (n == 0) return 1;
    return exSlow(n-1) + exSlow(n-1);
}

long long exLinear(int n) {
    if (n == 0) return 1;
    return 2 * exLinear(n-1);
}
```

For the first version, including the current call and both branches,

```text
C(0)=1,
C(n)=2C(n-1)+1,
C(n)=2^(n+1)-1.
```

So it is `Theta(2^n)` time and `Theta(n)` maximum stack depth. The second makes only one recursive call per level: `n+1` calls including the base call, `Theta(n)` time, and `Theta(n)` stack.

The key lesson is not “recursion is slow.” **Repeated subproblems** are slow. Memoization, algebraic simplification, or an iterative formulation removes them.

For general exponentiation `a^n`, exponentiation by squaring is even better:

```text
power(a,n):
    if n==0: return 1
    half=power(a,floor(n/2))
    if n is even: return half*half
    else:         return a*half*half
```

It uses `Theta(log n)` recursive calls and multiplications.

## 97. Recursion versus iteration

Neither is universally better.

| Criterion | Recursion | Iteration |
|---|---|---|
| Natural fit | Trees, divide-and-conquer, backtracking, recursive definitions | Linear repetition and state updates |
| State | Implicit call frames | Explicit variables/data structures |
| Extra space | Usually one frame per depth | Often constant for simple loops |
| Risks | Stack overflow; duplicate subproblems | More manual bookkeeping |
| Clarity | Often mirrors the proof/problem structure | Often direct for simple sequences |

Strong viva answer: “Choose the representation that matches the problem. A tree traversal or merge sort is naturally recursive; summing `1..n` is normally simpler and more space-efficient iteratively or by formula. Compare actual time and maximum depth, not the keywords.” Tail-call optimization is language/compiler dependent; Java and ordinary C implementations should not be assumed to eliminate the stack.

## 98. Solving recurrences by expansion, guess, and induction

For

```text
a0=1, ak=ak-1+2,
```

expansion gives `a1=3`, `a2=5`, and suggests `ak=1+2k`. Prove it by induction:

```text
ak=ak-1+2=[1+2(k-1)]+2=1+2k.
```

For Hanoi, `a0=0, ak=2ak-1+1`, repeated expansion gives

```text
ak=2^k a0+(2^k-1)=2^k-1.
```

Workflow: compute small terms, expand symbolically until a pattern appears, state the conjecture with its domain, then prove it. A correct-looking pattern without proof is incomplete.

## 99. Recursion-tree solution for merge sort

For `T(n)<=2T(n/2)+n`, assume `n=2^h` for a clean derivation.

- Level `i` contains `2^i` subproblems of size `n/2^i`.
- Work per node outside recursion is proportional to `n/2^i`.
- Total work at level `i` is `2^i * n/2^i = n`.
- There are `log2 n` internal levels, plus linear total leaf work.

Therefore `T(n)=O(n log n)`; a matching lower bound for the same recurrence gives `Theta(n log n)`. The deck's induction checks the upper-bound guess:

```text
T(2k) <= 2T(k)+2k
       <= 2k log2 k + 2k
       = 2k log2(2k).
```

## 100. Second-order homogeneous linear recurrences

Consider

```text
ak=A ak-1+B ak-2,    B!=0.
```

Try a geometric solution `ak=t^k`. Dividing by `t^(k-2)` gives the **characteristic equation**

```text
t^2-A t-B=0.
```

Why linear combinations work: if `rk` and `sk` each satisfy the recurrence, then for constants `C,D`,

```text
A(Cr(k-1)+Ds(k-1))+B(Cr(k-2)+Ds(k-2))
=C[Ar(k-1)+Br(k-2)]+D[As(k-1)+Bs(k-2)]
=Crk+Dsk.
```

So `Crk+Dsk` is also a solution.

## 101. Distinct-root theorem

If the characteristic equation has distinct roots `r` and `s`, then every solution has form

```text
an=C r^n+D s^n.
```

Use `a0` and `a1` to solve the two equations

```text
C+D=a0,
Cr+Ds=a1.
```

Example from the slides:

```text
ak=ak-1+2ak-2
```

has characteristic equation `t^2-t-2=(t-2)(t+1)=0`, so

```text
an=C 2^n+D(-1)^n.
```

For the displayed sequence `2,1,5,7,17,...`, `C+D=2` and `2C-D=1`; hence `C=D=1` and

```text
an=2^n+(-1)^n.
```

### Why the theorem is valid

Choose `C,D` so the formula agrees at `n=0,1`; distinct roots make that 2-by-2 system uniquely solvable. Both the claimed formula and original sequence obey the same order-2 recurrence. Strong induction then shows equality at every later index because equality at `k-1` and `k-2` forces equality at `k`.

## 102. Fibonacci closed form

For `F0=0`, `F1=1`, `Fn=Fn-1+Fn-2`, the characteristic equation is

```text
t^2-t-1=0,
phi=(1+sqrt(5))/2,
psi=(1-sqrt(5))/2.
```

Thus `Fn=C phi^n+D psi^n`. The initial values yield `C=1/sqrt(5)` and `D=-1/sqrt(5)`:

```text
Fn=(phi^n-psi^n)/sqrt(5).
```

Because `|psi|<1`, `Fn` is the nearest integer to `phi^n/sqrt(5)` for `n>=0`. This formula explains the exponential growth, but a simple iterative algorithm is usually preferable for exact computation; floating-point Binet values can round incorrectly for large `n`.

The expansion pattern on slides 61–62 is the Fibonacci addition identity

```text
Fn = F(n-k)F(k+1) + F(n-k-1)Fk,   0<=k<n,
```

equivalently

```text
F(m+n)=F(m-1)Fn+Fm F(n+1),   m>=1.
```

It follows by induction on either index using the Fibonacci recurrence. It can relate distant terms—for example `F7=F5F3+F4F2=5*2+3*1=13`—but by itself is not a constant-time way to compute `Fn` unless paired with fast-doubling identities.

## 103. Repeated-root theorem

If the characteristic equation has a repeated root `r`, the two independent solutions are `r^n` and `n r^n`, so

```text
an=(C+Dn)r^n.
```

The reason `nr^n` works: a repeated root means the quadratic is `(t-r)^2`, hence `A=2r` and `B=-r^2`. Substituting `an=nr^n` into

```text
an=2r an-1-r^2 an-2
```

gives

```text
2r(n-1)r^(n-1)-r^2(n-2)r^(n-2)
=[2(n-1)-(n-2)]r^n
=nr^n.
```

Slide exercise:

```text
a0=1, a1=3, ak=4ak-1-4ak-2.
```

The characteristic polynomial is `(t-2)^2`, so `an=(C+Dn)2^n`. From `a0=1`, `C=1`; from `a1=3`, `2(C+D)=3`, so `D=1/2`. Therefore

```text
an=2^n+n2^(n-1).
```

## 104. Recurrence-solving decision guide

```text
constant first difference       -> arithmetic expansion
multiply then add constant      -> unroll / shift equilibrium
divide into equal subproblems   -> recursion tree (or Master theorem if allowed)
order-2 homogeneous linear      -> characteristic roots
counting structure              -> disjoint/exhaustive cases first
overlapping recursive calls     -> memoization or bottom-up DP
```

### L12 common wrong answers

- A base case alone is insufficient; the recursive branch must move toward it.
- `rn=rn-1+rn-2` is not meaningful until `r0,r1` are specified.
- Two cases may be individually valid but still overlap; then adding their counts double-counts.
- Total calls and maximum recursion depth are different. `exSlow` has exponential calls but only linear depth.
- `T(n)=2T(n/2)+n` is not `Theta(n)`; every one of `Theta(log n)` levels contributes `Theta(n)`.
- Distinct-root and repeated-root formulas are different; using only `Cr^n` in the repeated case cannot fit arbitrary two initial values.

# Lecture 13 — Graphs, Trees, Euler Tours, Directed Graphs, and Hamiltonian Cycles

## 105. Why graphs model problems

A graph keeps **objects and relationships** while discarding irrelevant physical detail. In the Seven Bridges of Konigsberg problem, land regions become vertices and bridges become edges. The geographical drawing is irrelevant; the question becomes: is there a walk using each edge exactly once?

Typical models:

- routers/computers as vertices and links as edges;
- people as vertices and friendships as edges;
- cities as vertices and roads as weighted edges;
- tasks as vertices and dependencies as directed arcs;
- states as vertices and legal transitions as arcs.

## 106. Graph definitions and types

A finite undirected graph is `G=(V,E)`, where `V` is the vertex set and each edge joins two vertices.

- In a **simple graph**, an edge is an unordered pair `{u,v}` with `u!=v`; there are no loops or parallel edges.
- A **multigraph** may have multiple edges between the same endpoints; depending on convention it may also allow loops.
- A **directed graph** or digraph is `G=(V,A)`, where an arc `(u,v)` has tail `u` and head `v`.
- A **weighted graph** associates a cost, distance, capacity, or other value with edges.

Vertices `u,v` are **adjacent** if `uv` is an edge. An edge is **incident** with each of its endpoints. The open neighborhood is

```text
N(v)={u in V : uv in E}.
```

For a simple graph, `deg(v)=|N(v)|`. With parallel edges, degree counts incidences, not distinct neighbors. A loop contributes 2 to undirected degree.

Maximum and minimum degree are

```text
Delta(G)=max_v deg(v),
delta(G)=min_v deg(v).
```

## 107. Handshaking lemma and degree sequences

Every undirected edge has two endpoints, so double-counting vertex-edge incidences gives

```text
sum(v in V) deg(v)=2|E|.
```

Consequences:

1. the degree sum is even;
2. the number of odd-degree vertices is even.

Example: `(2,2,1)` and `(2,2,2,2,1)` cannot be degree sequences of any undirected graph because their sums are odd.

An even sum is necessary but not sufficient for a **simple** graph. The slide's `(3,3,3,1)` has even sum 10 but is impossible on four vertices: if three vertices have degree 3, each connects to every other vertex, forcing the fourth vertex to have degree at least 3, not 1.

### Havel-Hakimi test for a simple degree sequence

```text
isGraphical(degrees):
    repeatedly:
        remove all zeros
        if list is empty: return true
        sort nonincreasing
        remove first value d
        if d < 0 or d > remaining list length: return false
        subtract 1 from the next d values
        if any becomes negative: return false
```

The transformation preserves graphicality: a highest-degree vertex can be connected to vertices of the next-highest degrees without losing the existence of a realization. Straight sorting every round is polynomial (a simple implementation is `O(n^2 log n)`). For a viva, distinguish the handshaking necessary test from this actual decision algorithm.

## 108. Graph representations

An **adjacency matrix** uses an `|V| x |V|` matrix. It needs `Theta(V^2)` space, tests adjacency in `Theta(1)`, and is convenient for dense graphs.

An **adjacency list** stores each vertex's neighbors. It needs `Theta(V+E)` space for an undirected simple graph, and iterating over neighbors costs `Theta(deg(v))`; it is usually preferable for sparse graphs.

In an undirected adjacency list each edge appears twice. Remember that when counting storage or processing edge entries.

## 109. Graph isomorphism

Graphs `G1=(V1,E1)` and `G2=(V2,E2)` are **isomorphic** if a bijection `f:V1->V2` preserves adjacency:

```text
{u,v} in E1  iff  {f(u),f(v)} in E2.
```

The `iff` preserves both edges and nonedges. Isomorphism means the graphs have the same structure after relabeling, not necessarily the same drawing or names.

To prove isomorphism: give the complete vertex mapping, show it is bijective, and verify adjacency/nonadjacency. To prove non-isomorphism: exhibit an invariant that differs.

Useful isomorphism invariants include

- number of vertices and edges;
- sorted degree sequence;
- number of connected components;
- presence/number of triangles or cycles of a given length;
- distances, cut vertices, and degree patterns among neighbors.

Matching invariants are generally **not sufficient**. Two non-isomorphic graphs can have the same degree sequence.

A baseline algorithm tries all `n!` bijections and checks all vertex pairs in `O(n^2)` per mapping, for `O(n! n^2)` time. In a viva, do not convert the slide's “not easy” remark into the false claim that no better method exists; its intended lesson is that no simple invariant such as degree sequence completely decides general isomorphism.

## 110. Walks, trails, paths, and cycles

Terminology varies, so state your convention:

- A **walk** is a vertex sequence where consecutive vertices are adjacent; vertices and edges may repeat.
- A **trail** is a walk with no repeated edge.
- A **path** is a walk with no repeated vertex.
- A **closed walk** starts and ends at the same vertex.
- A **cycle** is a closed path with no repeated vertex except first=last.

The deck informally calls any adjacent vertex sequence a “path” and then says **simple path** when vertices are distinct. If an examiner follows that convention, clarify rather than argue terminology.

A shortest unweighted `u-v` walk is simple: if it repeats a vertex, the segment between repetitions is a cycle; removing it produces a shorter walk.

## 111. Connectedness and components

Vertices `u,v` are connected when a path joins them. An undirected graph is **connected** if every vertex pair is connected. A **connected component** is a maximal connected subgraph. A graph is connected iff it has exactly one component.

Breadth-first search marks exactly the vertices in the start vertex's component:

```text
BFS(G,s):
    mark s; Q.enqueue(s)
    while Q not empty:
        u=Q.dequeue()
        for each v in Adj[u]:
            if v unmarked:
                mark v
                parent[v]=u
                distance[v]=distance[u]+1
                Q.enqueue(v)
```

With adjacency lists, BFS is `Theta(V+E)` time and `Theta(V)` auxiliary space. It also finds shortest path lengths in an **unweighted** graph. Running BFS/DFS from every still-unmarked vertex counts and labels all components in the same `Theta(V+E)` total time.

## 112. Trees and forests

A **forest** is an acyclic undirected graph. A **tree** is a connected acyclic undirected graph. A vertex of degree 1 is a **leaf**; a one-vertex tree is a special case whose only vertex has degree 0.

For a finite undirected graph `T` with `n` vertices, the following are equivalent:

1. `T` is connected and acyclic.
2. Every pair of vertices has exactly one simple path between them.
3. `T` is connected and has `n-1` edges.
4. `T` is acyclic and has `n-1` edges.
5. Removing any edge disconnects `T`—it is minimally connected.
6. Adding any missing edge creates exactly one cycle—it is maximally acyclic.

These are characterizations, not six unrelated facts.

## 113. Core tree proofs from the slides

### Unique path

Connectivity gives at least one `u-v` path. If there were two distinct simple paths, follow them from `u` to their first divergence and then to their next common vertex; the two internally different subpaths form a cycle, contradicting acyclicity.

### Adding or removing an edge

In a tree there is a unique path between `u` and `v`; adding edge `uv` closes exactly that path into a cycle. Conversely, removing a tree edge `uv` destroys the unique `u-v` path and disconnects the graph.

### At least two leaves

In a tree with at least two vertices, take a longest simple path `v1,...,vk`. If `v1` had a neighbor other than `v2`, that neighbor either lies on the path—creating a cycle—or lies outside—extending the path. Both are impossible, so `v1` is a leaf; symmetrically `vk` is another leaf.

### A tree has `n-1` edges

Induct on `n`. A one-vertex tree has 0 edges. For `n>1`, remove a leaf and its incident edge. The remaining graph is still connected and acyclic, hence a tree with `n-1` vertices and, by induction, `n-2` edges. Restoring the leaf restores one edge, giving `n-1`.

### Useful converses

If a connected graph on `n` vertices had fewer than `n-1` edges, it could not connect all vertices; if it has exactly `n-1`, it cannot contain a cycle, because removing a cycle edge would leave a connected graph with too few edges. Dually, an acyclic graph with `n-1` edges must be connected.

Any subgraph of an acyclic graph is acyclic, because a cycle in the subgraph would also be a cycle in the original graph. Consequently, every **connected** subgraph of a tree is itself a tree; connectedness cannot be omitted.

## 114. Euler trail and Euler circuit

An **Euler trail/path** uses every edge exactly once. An **Euler circuit/cycle** is an Euler trail that returns to its starting vertex. Vertices may repeat; edges may not.

For an undirected graph after ignoring isolated vertices:

```text
Euler circuit <=> all active vertices lie in one connected component
                  and every vertex has even degree.

open Euler trail <=> all active vertices lie in one connected component
                     and exactly two vertices have odd degree.
```

Combining them: an Euler trail exists iff the active part is connected and the number of odd-degree vertices is 0 or 2. With two odd vertices, the trail must start at one and end at the other. Because odd vertices occur in even number, “at most two” is equivalent to “zero or two.”

### Necessity

Whenever a trail visits an intermediate vertex, an unused arrival edge is paired with a later departure edge; hence its used degree is even. In an open trail only the start and end can have one unpaired incident edge and therefore odd degree. A trail using all edges also makes every non-isolated edge reachable from the trail, giving connectivity of the active part.

This immediately proves the Seven Bridges graph impossible: all four land vertices have odd degree, but an Euler trail permits only two odd endpoints.

### Sufficiency idea from the slides

If every degree is even, begin at any active vertex and follow unused edges. One cannot get stuck at a different vertex: every arrival consumes one incident edge, while even degree ensures departures can be paired until returning to the start. This gives a cycle. Remove its edges; all remaining degrees stay even. Inductively decompose the remaining edges into cycles, then splice each new cycle into the current closed trail at a shared vertex. Connectivity guarantees a shared point until all edges are included. This is the idea behind Hierholzer's algorithm.

For exactly two odd vertices `s,t`, temporarily add edge `st`; every degree becomes even. Find an Euler circuit and remove the added edge, breaking it into an Euler trail from `s` to `t`.

## 115. Hierholzer's algorithm and complexity

Use edge IDs so parallel edges are distinguishable:

```text
EulerUndirected(G):
    verify active vertices are connected
    verify odd-degree count is 0 or 2
    start = an odd vertex if two exist, else any active vertex
    stack = [start]; output = []
    while stack not empty:
        v = stack.last
        if v has an unused incident edge e=(v,u):
            mark edge-ID e used
            stack.push(u)
        else:
            output.append(stack.pop())
    reverse(output)
    return output
```

With adjacency lists and a cursor that skips already-used edge IDs, each edge is processed a constant number of times. Connectivity checking and construction therefore take `O(V+E)` time and `O(V+E)` storage. The returned vertex list has `E+1` entries.

## 116. Directed graphs

For arc `(u,v)`, `u` is the tail and `v` the head. It contributes 1 to `outdeg(u)` and 1 to `indeg(v)`, so

```text
sum_v outdeg(v)=|A|=sum_v indeg(v).
```

A directed path must follow arrow direction. A directed cycle begins and ends at the same vertex and otherwise has no repeated vertex.

Directed Euler conditions, together with the appropriate connectivity of all nonzero-degree vertices, are:

```text
Euler circuit:
    indeg(v)=outdeg(v) for every v.

open Euler trail from s to t:
    outdeg(s)=indeg(s)+1,
    indeg(t)=outdeg(t)+1,
    indeg(v)=outdeg(v) for every other v.
```

The slide states the same imbalance using the opposite viewpoint: one node has `indeg=outdeg+1` (the end) and another has `indeg=outdeg-1` (the start).

Degree balance alone is not enough if the arcs lie in disconnected pieces. For a circuit, the active vertices should be mutually reachable in the directed sense (equivalently, in this balanced setting, verify the standard active-component condition). For an open path, adding the temporary arc `t->s` reduces the test to the circuit case.

Hierholzer's stack algorithm works for directed graphs too; consume an unused outgoing arc instead of an undirected edge.

## 117. Euler versus Hamilton

An Euler problem visits every **edge** once; a Hamilton problem visits every **vertex** once. This difference is the first sentence of a strong viva answer.

| Feature | Euler | Hamilton |
|---|---|---|
| Must use once | Every edge | Every vertex |
| Repetition allowed | Vertices may repeat | No vertex repeats, except start=end for a cycle |
| Simple characterization | Connectivity plus degree parity/balance | No comparable simple degree criterion in general |
| Standard construction | Hierholzer, `O(V+E)` | Search/DP; general problem is computationally hard |

A vertex having degree less than 2 rules out a Hamiltonian cycle in a nontrivial graph, but degree at least 2 does not guarantee one.

## 118. Complete graphs and counting Hamiltonian cycles

The complete graph `Kn` has an edge between every distinct vertex pair:

```text
|E(Kn)|=C(n,2)=n(n-1)/2,
deg(v)=n-1.
```

To count undirected Hamiltonian cycles, arrange the `n` labeled vertices in a sequence: `n!`. Each geometric cycle is represented `n` times by choice of starting point and twice by direction, so

```text
# Hamiltonian cycles in Kn = n!/(2n)=(n-1)!/2, n>=3.
```

For `K5`, the answer is `4!/2=12`; for `K8`, it is `7!/2=2520`. In a directed complete graph where reverse orientations are distinct, fixing only the starting point gives `(n-1)!` directed cycles.

## 119. Traveling salesperson problem (TSP)

Given weighted city-to-city edges, TSP asks for a minimum-total-weight Hamiltonian cycle. A naive undirected complete-graph search evaluates `(n-1)!/2` tours, factorial time.

The subset dynamic program fixes a start `s` and defines

```text
DP[S][v] = minimum cost of a path that starts at s,
           visits exactly the vertices in S, and ends at v.

DP[{s}][s]=0
DP[S][v]=min over u in S-{v} (DP[S-{v}][u]+w(u,v)).
```

Finally return `min_v DP[V][v]+w(v,s)`. This Held-Karp method takes `O(n^2 2^n)` time and `O(n2^n)` space—much better than factorial but still exponential.

### L13 whiteboard decision checklist

```text
relationship model?       -> graph/digraph and what V,E mean
all edges exactly once?   -> Euler; check connectivity + parity/balance
all vertices exactly once?-> Hamilton; do not use Euler's criterion
connected components?     -> BFS/DFS
tree claim?               -> use unique path / n-1 edges / leaf induction
same structure?           -> isomorphism mapping or differing invariant
```

### L13 common wrong answers

- Degree is not always the number of distinct neighbors in a multigraph.
- Even degree sum does not make a simple degree sequence graphical.
- Equal degree sequences do not prove two graphs isomorphic.
- A walk, trail, and simple path impose different repetition restrictions.
- “Zero odd vertices” is the circuit case; “two odd vertices” is the open-trail case.
- Connectivity in Euler's theorem concerns vertices incident with edges; isolated vertices are harmless under the standard active-vertex convention.
- Euler's theorem says nothing about Hamiltonian cycles.

# Lecture 14 — Graph Coloring, Bipartite Graphs, Greedy Ordering, and Interval Graphs

## 120. Proper vertex coloring and chromatic number

A **proper vertex coloring** assigns a color to every vertex so adjacent vertices receive different colors. A graph is **`k`-colorable** if some proper coloring uses at most `k` colors. Its **chromatic number** is

```text
chi(G)=minimum number of colors in a proper coloring of G.
```

Each color class is an **independent set**—a set containing no adjacent pair. Conversely, partitioning `V` into `k` independent sets is exactly a `k`-coloring.

For a nonempty edgeless graph, `chi(G)=1`. If a graph has at least one edge, at least two colors are necessary. “The coloring I found uses `k` colors” proves only `chi(G)<=k`; optimality also needs a lower bound.

Useful bounds are

```text
omega(G) <= chi(G) <= Delta(G)+1,
```

where `omega(G)` is the size of a largest clique. Every clique vertex must have a different color.

## 121. Chromatic numbers of standard graphs

### Paths, cycles, and complete graphs

```text
chi(Pn)=1 for n=1, otherwise 2.

chi(Cn)=2 if n is even;
chi(Cn)=3 if n is odd.

chi(Kn)=n.
```

Why an odd cycle needs 3: alternating two colors around the cycle returns to the starting edge with both endpoints forced to the same color. Three colors suffice by alternating around all but one vertex and using a third color there.

### Wheels and the naming convention

Under the deck's convention, wheel `Wn` has `n` total vertices: a rim `C(n-1)` plus one universal hub. The hub needs a color different from every rim color, hence

```text
chi(Wn)=4 when n is even  (rim C(n-1) is odd),
chi(Wn)=3 when n is odd   (rim C(n-1) is even).
```

Thus the displayed `W6` needs 4 colors. Some books define `Wn` as a rim `Cn` plus a hub—`n+1` vertices—which reverses the parity wording. State the convention before answering.

## 122. Trees are bipartite

Pick any root. Color a vertex red if its distance from the root is even and green if odd. Every tree edge joins levels whose distances differ by one; if an edge joined equal parity levels, the two root paths plus that edge would create a cycle. Therefore every nontrivial tree is 2-colorable.

For a forest, apply the same argument independently to every component. An edgeless forest has chromatic number 1; a forest containing an edge has chromatic number 2.

## 123. Bipartite graphs and equivalent characterizations

A graph is **bipartite** if

```text
V=L union R, L intersection R=empty,
```

and every edge has one endpoint in `L` and the other in `R`. Equivalently:

```text
G is bipartite
<=> G is 2-colorable
<=> G contains no odd cycle.
```

Proof directions:

- A bipartition gives a 2-coloring by coloring `L` and `R` differently.
- A 2-coloring gives a bipartition into its two color classes.
- A bipartite cycle alternates between sides, so it has even length.
- If there is no odd cycle, choose a root in each component and separate vertices by even/odd distance. An edge joining equal parity levels, together with suitable paths back toward the root, would produce an odd cycle; hence all edges cross the partition.

## 124. BFS test for bipartiteness

```text
isBipartite(G):
    color[v]=UNCOLORED for every v
    for each vertex s:
        if color[s] is UNCOLORED:
            color[s]=0; enqueue(s)
            while queue not empty:
                u=dequeue()
                for v in Adj[u]:
                    if color[v] is UNCOLORED:
                        color[v]=1-color[u]
                        parent[v]=u
                        enqueue(v)
                    else if color[v]==color[u]:
                        return false
    return true
```

With adjacency lists this is `O(V+E)` time and `O(V)` extra space. Starting BFS in every uncolored component matters; testing only one start can miss an odd cycle elsewhere. On a conflict edge whose endpoints have the same color, parent paths can be used to recover an explicit odd-cycle certificate.

## 125. Modeling resource conflicts as coloring

The standard recipe from the slides is

```text
object   -> vertex
conflict -> edge
resource -> color
minimum resources -> chromatic number.
```

The correspondence must be proved in both directions:

- A valid assignment of `k` resources colors each object by its resource; conflicting objects use different resources, so the coloring is proper.
- A proper `k`-coloring assigns the resource represented by each color; no conflicting pair shares it.

### Flight gates

Each vertex is a flight interval; overlap produces an edge; each color is a gate. Minimum gates equal the chromatic number of the interval-overlap graph.

### Exam scheduling

Each vertex is a course; put an edge between two courses if at least one student takes both; a color is an exam time slot. A `k`-coloring exists iff the exams fit in `k` slots.

### Register allocation

Each vertex is a program variable/live range. Two variables are adjacent when their live ranges overlap, meaning storing them in one register could overwrite a still-needed value. Colors represent registers. Real compilers may spill some variables to memory when available registers are fewer than required.

## 126. Greedy coloring and the maximum-degree bound

Given an order `v1,...,vn`, greedy coloring assigns each vertex the smallest color absent from its already-colored neighbors:

```text
greedyColor(G, order):
    color[v]=UNCOLORED
    for v in order:
        forbidden = empty set
        for u in Adj[v]:
            if color[u] is assigned:
                forbidden.add(color[u])
        color[v] = smallest positive color not in forbidden
    return color
```

A vertex has at most `Delta(G)` neighbors, so at most that many colors can be forbidden. One of `Delta(G)+1` colors is always available:

```text
chi(G)<=Delta(G)+1.
```

With adjacency lists and reusable marking arrays, greedy coloring runs in `O(V+E)` time after the order is known. It always returns a valid coloring, but not necessarily an optimal one; different orders can use very different numbers of colors.

## 127. Good orderings and degeneracy

If vertices can be ordered so that each vertex has at most `d` neighbors appearing earlier, greedy coloring in that order uses at most `d+1` colors.

A graph is **`d`-degenerate** if every nonempty subgraph has a vertex of degree at most `d`. Construct the order by repeatedly removing a current vertex of degree at most `d` and pushing it onto a stack; coloring in reverse removal order exposes at most `d` already-colored neighbors.

```text
degeneracyOrder(G):
    maintain current degrees and buckets keyed by degree
    repeatedly remove a minimum-degree remaining vertex v
    push v on stack
    decrement each remaining neighbor's degree
    return reverse(stack)
```

With degree buckets this can be implemented in `O(V+E)` time; a naive scan for a low-degree vertex can cost `O(V^2)`. Trees are 1-degenerate because every nontrivial subtree has a leaf, so this method yields two colors.

## 128. Interval graphs and clique number

An **interval graph** represents each vertex by an interval on a line; two vertices are adjacent iff their intervals overlap. A **clique** is a set of pairwise adjacent vertices, and `omega(G)` is the maximum clique size.

For any graph, `chi(G)>=omega(G)`. For interval graphs the lower bound is exact:

```text
chi(G)=omega(G).
```

This makes interval-conflict gate allocation optimally solvable, unlike arbitrary graph coloring.

## 129. Earliest-finish lemma and proof of optimal coloring

Let `v` be an interval whose right endpoint is earliest. Every neighbor interval intersects `v`; because no interval ends before `v`, such a neighbor contains `v`'s right endpoint (under the closed-interval convention). Hence `v` and all its neighbors pairwise intersect at that common point and form a clique. If `omega(G)=k`, then

```text
deg(v)+1 <= k,
deg(v) <= k-1.
```

The deck's narrative briefly says “degree `k-1`”; the justified statement is **at most** `k-1`.

Remove `v`. The remaining graph is again an interval graph and has clique number at most `k`. By induction it can be colored with `k` colors. Since `v` has at most `k-1` neighbors, at least one of those `k` colors is free for `v`. Therefore `chi(G)<=k`; combined with `chi(G)>=k`, this proves equality.

Algorithmically, repeatedly remove the earliest-finishing interval, then greedily color in reverse removal order. Sorting endpoints costs `O(n log n)`; appropriate heaps/sets allow efficient color assignment.

An equivalent scheduling sweep sorts intervals by start time and reuses the resource whose interval finishes earliest:

```text
sort intervals by start time
active = min-heap by finish time, storing resource IDs
free_ids = stack/queue/set of released resource IDs
next_id = 0
for interval I:
    while active is nonempty and active.min.finish does not conflict with I.start:
        (finish, id) = pop active
        insert id into free_ids
    if free_ids is nonempty:
        remove one id from free_ids
    else:
        id = next_id
        next_id++
    assign I to id
    push (I.finish, id) into active
```

The separate `free_ids` pool matters: several resources may finish before the next interval starts, and discarding all but one released ID could later create unnecessary resources. The algorithm creates a new ID only when every existing resource is active, so that instant gives a clique/lower bound of the new resource count. It therefore uses exactly the maximum number of simultaneously active intervals, which is `omega(G)`, and runs in `O(n log n)` time.

Endpoint convention matters. If a flight ending at time `t` and one beginning at `t` may share a gate, use half-open intervals `[start,end)` and release when `finish<=start`. If touching endpoints count as conflict, use closed intervals and release only when `finish<start`.

## 130. Additional coloring recall

- The famous four-color theorem says every planar graph can be vertex-colored with at most four colors; the deck mentions it as motivation but does not develop the proof.
- A clique gives a lower-bound certificate; an explicit coloring gives an upper-bound certificate. When the bounds meet, optimality is proved.
- `Delta+1` is sufficient, not usually necessary: a star can have huge maximum degree but needs only two colors.
- Greedy is an algorithm; “chromatic number” is the optimum. Never equate the number used by one greedy order with `chi(G)` without a matching lower bound.

### L14 whiteboard drill

If asked to model a new scheduling problem, say: “I make one vertex per job, connect jobs that cannot share a slot, and use one color per slot. I prove assignment-to-coloring and coloring-to-assignment. A clique of `k` mutually conflicting jobs proves at least `k` slots; then I try to construct a `k`-coloring.”

# Rapid Recall Appendix

## 131. One-page formula spine

### Logic and quantifiers

```text
p->q                 == !p or q
!(p->q)              == p and !q
p->q                 == !q -> !p
!(forall x P(x))     == exists x !P(x)
!(exists x P(x))     == forall x !P(x)
!(p and q)           == !p or !q
!(p or q)            == !p and !q
```

### Sets and counting

```text
|P(A)|                         = 2^|A|
|A x B|                       = |A||B|
|A union B|                   = |A|+|B|-|A intersection B|
P(n,r)                        = n!/(n-r)!
C(n,r)                        = n!/[r!(n-r)!]
(x+y)^n                       = sum(k=0..n) C(n,k)x^(n-k)y^k
nonnegative x1+...+xk=n       = C(n+k-1,k-1)
positive x1+...+xk=n          = C(n-1,k-1)
r nonadjacent among N         = C(N-r+1,r)
multiset permutations         = n!/(n1!...nk!)
Catalan Cn                    = C(2n,n)/(n+1)
```

### Pigeonhole

```text
N objects, m boxes -> some box has at least ceil(N/m).
To force at least r in one box, require N > m(r-1).
```

### Sequences and generating functions

```text
arithmetic an                 = a1+(n-1)d
arithmetic sum                = n(a1+an)/2
sum(i=0..n) r^i               = (1-r^(n+1))/(1-r), r!=1
sum(i>=0) r^i                 = 1/(1-r), |r|<1
Hn                            = Theta(log n)
sum(i=1..n) i^2               = n(n+1)(2n+1)/6
n!                            ~ sqrt(2*pi*n)(n/e)^n
sum(n>=0)x^n                  = 1/(1-x)
sum(n>=1)n x^n                = x/(1-x)^2
(1-x)^(-k)                    = sum(n>=0)C(n+k-1,n)x^n
[x^n]A(x)B(x)                 = sum(i=0..n)ai b(n-i)
```

### Recurrences and graphs

```text
no-11 strings                 rn=r(n-1)+r(n-2), r0=1,r1=2
2xn dominoes                  rn=r(n-1)+r(n-2), r0=r1=1
Catalan                       Cn=sum(i=0..n-1)Ci C(n-1-i)
Stirling second kind          S(n,r)=S(n-1,r-1)+rS(n-1,r)
Hanoi                         T(n)=2T(n-1)+1=2^n-1
merge sort                    T(n)=2T(n/2)+Theta(n)=Theta(n log n)
order-2 roots r,s distinct    an=C r^n+D s^n
repeated root r               an=(C+Dn)r^n
sum degrees                   =2|E|
tree                          |E|=|V|-1
Euler circuit                 active connected + 0 odd vertices
Euler open trail              active connected + exactly 2 odd vertices
# Hamilton cycles in Kn       =(n-1)!/2
omega(G) <= chi(G)            <= Delta(G)+1
interval graph                chi(G)=omega(G)
```

## 132. High-yield whiteboard/viva drills

### Drill A — Pigeonhole with a real use case

Say, without vague analogies:

> “The generalized pigeonhole principle says that mapping `N` objects to `m` boxes forces a box with at least `ceil(N/m)` objects. For example, a hash function maps a larger key space to `m` hash values, so distinct keys must collide. Therefore a hash table needs collision handling; the theorem proves existence, not which keys collide.”

Follow-ups to be ready for: Why ceiling? When is the bound tight? Does a cryptographic hash avoid collisions? What are objects and boxes?

### Drill B — Prove an implication

Write the domain first. Choose direct proof when the hypothesis unfolds cleanly; contrapositive when the negated conclusion gives a usable form; contradiction when assuming the negation creates incompatible facts. Never prove a converse by accident.

### Drill C — Derive rather than recognize a recurrence

For no-`11` strings, say: “Every valid string begins with exactly one of `0` or `10`. Removing that prefix leaves an arbitrary valid shorter string, so the cases contribute `r(n-1)` and `r(n-2)`. They are disjoint and exhaustive.” Then give bases.

### Drill D — Graph question triage

Ask whether the requirement concerns edges or vertices. For every edge once, use Euler parity plus active connectivity and construct with Hierholzer. For every vertex once, it is Hamiltonian; do not offer the Euler test. For shortest unweighted paths, use BFS.

### Drill E — Prove a coloring is optimal

Give both directions of the bound: a `k`-clique proves `chi>=k`; an explicit `k`-coloring proves `chi<=k`. Only together do they prove `chi=k`.

## 133. Source corrections and notation cautions

The following are deliberate corrections/clarifications, not omissions:

| Source location | What appears or can be misread | Safe, correct viva version |
|---|---|---|
| L01 graphical puzzles | A drawing seems to prove an area/count identity | Check hidden gaps/overlaps; a diagram motivates but does not replace proof. |
| L05 slide 3 | `n! >= n^n` | False for `n>1`; the elementary bound is `n! <= n^n`. |
| L05/L06 rendered exponents | `2n x 2n` can appear after extraction | The deficient-board theorem is for `2^n x 2^n`. |
| L08 slides 23–24 | “4-digit numbers” counted as `10^4-9^4=3439` | That counts zero-padded four-character strings. Actual integers `1000..9999`: `9000-8*9^3=3168`. |
| L09 mapping, MISSISSIPPI | `13!/(4!4!2!)` | The word has 11 letters: `11!/(4!4!2!)=34650`. |
| L12 slide 3 | harmonic recurrence starts at `a0=1` | Use `a1=1`, `a(n+1)=n an/(n+1)` for `n>=1`. |
| L12 slides 47–54 | print routine returns `int`; Hanoi tests `n` although parameter is `number` | Use `void` for print-only code and one consistent parameter name. |
| L12 exponential calls | formatting looks like `2n+1-1`; optimized version says `n` calls | Slow call count including base is `2^(n+1)-1`; one-branch version makes `n+1` calls including the initial/base calls. |
| L13 simple cycle wording | “every vertex is degree 2” | Every vertex has degree 2 **within the cycle subgraph**; it may have other incident edges in the ambient graph. |
| L13 Euler statement | says the graph is connected | Standard condition may ignore isolated vertices; all nonzero-degree vertices must lie in one component. |
| L13 isomorphism comment | may sound like only checking every permutation is known | Use brute force only as the baseline; say the general problem is nontrivial, not that no improved method exists. |
| L14 wheel notation | `W_even`/`W_odd` parity | The deck counts total vertices; state whether `Wn` means `n` total vertices or rim `Cn` plus hub. |
| L14 slide 33 | says the earliest-finishing interval has degree `k-1` | The proof establishes degree **at most** `k-1`. |

# Current Source Coverage Audit

## 134. Current merged source

| Current source | Pages | Material represented in this volume |
|---|---:|---|
| `Discrete_merged.pdf` | 236 | propositions/logic, predicates/quantifiers, proof, induction, sets, counting, functions, pigeonhole, sequences, generating functions, recursion/recurrences, graphs and coloring |
| selected Computer Mathematics / Graph Theory pages | cross-reference only | recurrence, graph and scheduling reinforcement already routed to Discrete/DSA; no separate low-priority viva volume |

The full 236-page merged PDF was re-read. Text-bearing pages were extracted directly; formulas, graph drawings and worked examples were checked in their page context. Repeated explanations are consolidated, but every viva-relevant definition, theorem, proof pattern, formula, recurrence, algorithm, complexity consequence and correction is retained.

## 135. How to rehearse this volume

Hide the explanation, answer each heading aloud, reproduce the formula/proof/code on paper, then compare. Recognition while reading is easier than retrieval in a viva; whiteboard reconstruction is the test.

Final source-specific checks:

- state the pigeonhole objects, boxes and forced lower bound;
- distinguish converse/inverse/contrapositive and necessary/sufficient conditions;
- give bases, hypothesis and inductive step without circularity;
- justify a recurrence from disjoint exhaustive cases;
- distinguish Euler (edges) from Hamilton (vertices);
- prove a chromatic number with both a lower bound and a matching coloring.