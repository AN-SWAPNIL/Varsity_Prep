# Bismillah.

# BRAC University Viva — Introduction, Teaching, and Industry Defense

This is the spoken-answer volume. The academic books explain *what you know*; this file helps you communicate it under pressure. Do not memorize every sentence. Memorize the structure, facts, and first two lines of each answer, then speak naturally.

---

# 1. Your positioning

Your clearest professional story is:

> **A strong fundamentals-first CSE graduate whose main teaching strength is DSA, supported by research in security/ML, practical AI/software experience, competitive programming, current university teaching, and genuine comfort with systems and hardware.**

Do not present DSA as your only subject. Say it is your strongest differentiator, then name OS, DBMS, OOP, networks/security, AI, architecture, DLD, microprocessors, ML, graphics, discrete mathematics, TOC, numerical methods, and SWE as subjects you can prepare and teach.

## 1.1 Thirty-second introduction

> “Assalamu alaikum. I am Ahmmad Nur Swapnil, a recent BUET CSE graduate with a CGPA of 3.94, and I am currently teaching in the CSE department at Presidency University. My strongest core area is data structures and algorithms, developed through coursework, ICPC participation, Codeforces Expert-level problem solving, and several years of mentoring. My research spans LLM-guided Matter-protocol security, visual reasoning about graph properties, low-cost EEG analysis, and Bangla speech benchmarks. I have also worked in agentic-AI and full-stack engineering roles. My long-term goal is to combine rigorous teaching, meaningful research, and practical engineering.”

## 1.2 Sixty-second introduction

Add only two things to the short version:

- you enjoy converting a difficult concept into a sequence students can reason about;
- your industry work taught you to validate systems rather than trust a successful demo.

Do not list every framework from the resume. A faculty panel cares more about depth, ownership, and judgment than a technology inventory.

## 1.3 If they say “Tell us something not in your CV”

> “One thing the CV does not show well is how much I enjoy diagnosing *why* someone is stuck. In mentoring and teaching, I often find that the visible coding error comes from an earlier conceptual gap—for example, treating a recursive call as magic or confusing an object reference with the object itself. I like finding that exact gap and designing the smallest example that repairs it.”

This answer is relevant, personal, and naturally opens a teaching discussion.

---

# 2. Why teaching?

## 2.1 Strong answer

> “I enjoy the point where a student moves from remembering a procedure to understanding why it works. My programming-instructor experience showed me that I like diagnosing misconceptions and designing examples; my current lecturer role has added lesson planning, labs, assessment, and responsibility for an entire class. Teaching also forces me to keep my own foundations precise. I want a career where teaching and research strengthen each other rather than treating either one as a side activity.”

## 2.2 Evidence behind the answer

Use evidence, not only emotion:

- freelance programming instruction since 2023;
- current lecturer role at Presidency University;
- preparation of lectures, labs, assignments, and assessments;
- mentoring in DSA, programming, ML, and web development;
- competitive-programming background that gives many examples and alternative solutions;
- research practice that helps you teach evidence, assumptions, and limitations.

## 2.3 Why BRAC University?

> “BRAC University offers the kind of environment I am looking for: strong CSE students, serious attention to teaching, and room to develop research alongside coursework. My fit is the combination of strong core-CS preparation—especially DSA—with research and engineering experience that can make lectures and projects more concrete. I would want to contribute as a dependable core-course teacher first, while gradually building collaborations and student research.”

Avoid generic flattery and never criticize your current institution. The answer should be about fit and contribution.

## 2.4 Future plan

> “In the near term, I want to become a dependable core-course teacher, improve my classroom and assessment practice, and turn my current research into rigorous publications. In the longer term, I want advanced study and a sustained research agenda while remaining closely involved in teaching and mentorship.”

If asked whether advanced study means leaving immediately, explain the actual plan honestly. Do not promise a timeline you cannot guarantee.

---

# 3. Which courses would you teach?

## 3.1 Primary answer

> “My first choice is Data Structures and Algorithms because it is where my academic preparation, competitive programming, and teaching experience overlap most strongly. I am also comfortable preparing OOP, DBMS, OS, computer networks and security, AI, SWE, and mathematical courses. I am not avoiding hardware: I am comfortable with DLD, architecture, and processor fundamentals; DSA is simply the area I would present as my strongest differentiator.”

## 3.2 If forced to choose among Architecture, OS, and Networks

Choose the subject you can defend most confidently that day. Then state one organizing idea:

- **Architecture:** the instruction path from ISA through datapath/control, memory hierarchy, and performance;
- **OS:** controlled sharing and abstraction of CPU, memory, storage, and devices;
- **Networks:** layered end-to-end communication under loss, delay, congestion, and heterogeneous links.

The panel may immediately ask a basic calculation. Give the direct result first, then reasoning.

## 3.3 Hardware confidence answer

> “My CV emphasizes software and AI because those are my recent projects, but that does not mean I am weak in hardware. I am comfortable with Boolean logic, combinational and sequential circuits, counters, processor organization, pipelining, memory hierarchy, interrupts, and microprocessor/microcontroller fundamentals. I would prepare the specific course syllabus before teaching it, just as I would for any subject.”

Never claim that a course is “easy.” A basic course can still demand careful teaching.

---

# 4. How to answer technical questions at the board

Use this sequence:

1. Give the definition/result in one clean sentence.
2. State assumptions and notation.
3. Draw the smallest useful example.
4. Trace the mechanism or prove the claim.
5. State time/space cost or engineering consequence.
6. Name one boundary or common mistake.

If you need ten seconds, say: “Let me define the objects first.” That sounds disciplined, not evasive.

If you notice an error, correct it directly:

> “I need to correct that statement: high bias is commonly associated with underfitting, but bias and underfitting are not the same object. Bias is defined over repeated training sets.”

Do not defend a wrong first answer.

---

# 5. Teaching demonstration: motivate functions using sum from 1 to n

Assume students already know loops.

## 5.1 Start from a problem they can solve

Write:

```cpp
int n = 10;
int sum = 0;
for (int i = 1; i <= n; ++i) {
    sum += i;
}
cout << sum;
```

Ask: “What if the program needs the sum up to 10 here, up to 100 later, and up to a user-supplied value somewhere else?” Copying the loop creates duplication. A bug fix or input-rule change must then be repeated in every copy.

## 5.2 Extract the reusable behavior

```cpp
long long sumTo(int n) {
    long long sum = 0;
    for (int i = 1; i <= n; ++i) {
        sum += i;
    }
    return sum;
}

cout << sumTo(10) << '\n';
cout << sumTo(100) << '\n';
```

Explain the parts:

- `sumTo` is a meaningful name for one behavior;
- `n` is an input parameter;
- the body is the implementation;
- `return` sends one result to the caller;
- each call receives its own local `sum` and `i`.

## 5.3 State the motivation

> “A function packages a reusable computation behind a name and a clear input-output contract. It reduces duplication, improves readability, makes testing easier, and lets us change the implementation without changing every caller.”

Now show that abstraction is independent of implementation:

```cpp
long long sumTo(long long n) {
    if (n < 1) return 0;
    return n * (n + 1) / 2;
}
```

The callers do not change. The formula is not the motivation for functions; it demonstrates information hiding after the motivation is clear.

## 5.4 Check learning

Ask students:

- What are the input and output?
- Which variables are local?
- What should the contract say for `n<1`?
- How would we write `sumRange(a,b)` using `sumTo`?
- Why is printing inside the function less reusable than returning the value?

This closes the loop: motivation, construction, use, and assessment.

---

# 6. Teaching demonstration: recursion

## 6.1 Definition

Recursion solves a problem using one or more smaller instances of the same problem. A correct recursive design needs:

- a base case;
- a recursive case;
- progress toward the base case.

```cpp
long long factorial(int n) {
    if (n == 0) return 1;
    return n * factorial(n - 1);
}
```

Trace `factorial(4)` downward:

```text
factorial(4)
= 4 * factorial(3)
= 4 * 3 * factorial(2)
= 4 * 3 * 2 * factorial(1)
= 4 * 3 * 2 * 1 * factorial(0)
= 24
```

Draw one stack frame per call. Distinguish “making calls” from “returning values.” The proof mirrors induction: base case is correct; assuming the smaller result is correct, the recursive step constructs the larger result.

## 6.2 Recursion versus iteration

Neither is universally better.

| Criterion | Recursion | Iteration |
|---|---|---|
| Natural fit | trees, divide-and-conquer, backtracking, recursive definitions | simple repeated state updates |
| State | call stack holds pending work | variables/data structures hold state explicitly |
| Overhead | function calls and stack frames | usually lower |
| Failure risk | stack overflow if depth is large | infinite loop if progress fails |
| Clarity | often mirrors problem structure | often clearer for linear repetition |

Viva line:

> “Choose recursion when it exposes the recursive structure and the depth is safe; choose iteration when it is equally clear and avoids unnecessary call-stack cost.”

---

# 7. Teaching demonstration: motivate graphs

Start with three problems that look unrelated:

- roads between cities and shortest routes;
- people connected in a social network;
- courses connected by prerequisite rules.

Then reveal the common abstraction:

```text
G=(V,E)
```

- vertices represent entities;
- edges represent relationships;
- direction models asymmetric relationships;
- weights model distance, time, cost, or capacity.

Map each application:

| Application | Vertex | Edge | Type | First algorithmic question |
|---|---|---|---|---|
| Road map | location | road | weighted, often directed | shortest path |
| Friendship | person | relationship | usually undirected | connectivity/community |
| Prerequisites | course | “must precede” | directed | topological order/cycle |
| Web | page | hyperlink | directed | ranking/reachability |
| Network flow | router/state | link/transition | directed with capacity | maximum feasible flow |

> “Graphs matter because one mathematical representation lets us reuse traversal, shortest-path, ordering, matching, and flow algorithms across many domains.”

Check understanding by asking students to model a food-delivery system or dependency graph and decide whether edges need direction/weight.

---

# 8. Classroom judgment questions

## 8.1 Students have mixed backgrounds

> “I would define prerequisite knowledge explicitly, begin with a diagnostic low-stakes task, and provide a short bridge for missing essentials. Core class time should still reach the course outcomes, so stronger students get extensions while students who need support get worked examples, office hours, and targeted feedback.”

## 8.2 A student can code but cannot explain

Ask for the invariant, a small trace, and the complexity derivation. Then vary the input. Explanation is part of the learning outcome, especially in algorithms.

## 8.3 A student memorizes code

Change one assumption: duplicates, empty input, disconnected graph, negative edge, full queue, or a different indexing convention. Ask the student to predict behavior before editing code.

## 8.4 How would you assess DSA?

Use a mixture:

- concept/trace questions for mental models;
- implementation tasks for correctness and edge cases;
- complexity/proof questions for reasoning;
- design questions where several structures are compared;
- a small lab or viva where the student explains their own code.

Assessment should match course outcomes. A written exam alone cannot fully assess implementation and debugging.

## 8.5 How do you prevent plagiarism?

Use individualized inputs or variants, milestone submissions, short code vivas, version history, and questions about design decisions. Detection is secondary; assessment design should make understanding necessary.

## 8.6 A student challenges your answer

> “I would ask them to show the counterexample or source, work through it with the class, and correct myself openly if needed. Authority should not replace evidence. I would also keep the discussion focused and follow up after class if it needs a longer investigation.”

## 8.7 Teaching in English

Use short sentences, define symbols before formulas, pause after a new term, and ask a concrete check question. Technical precision matters more than an artificial accent. If a brief Bangla clarification is allowed, use it to unblock meaning, then restate the concept in English.

---

# 9. Industry experience: coherent story

## 9.1 Thirty-second version

> “At SysModeler I worked on agentic-AI workflows for model-based systems engineering, including natural-language-to-SysML generation and cyclic LangGraph validation of generated system models. At SocioFi I progressed from internship work to a researcher and AI-software role, building LangChain/LangGraph workflows, full-stack features, and integrations such as Azure Speech, Stripe, and Namecheap. These roles taught me that dependable software needs explicit validation, permissions, failure handling, observability, and maintainability—not only a successful demonstration.”

## 9.2 SysModeler AI & Systems Innovation Lab

Resume-grounded facts:

- role: Junior AI Engineer, remote, April–June 2026;
- domain: AI-assisted model-based systems engineering;
- task: generate SysML diagrams/models from natural language;
- architecture: cyclic graph workflows with LangGraph;
- purpose of the cycle: validate and repair generated models, especially for safety-critical use.

Concepts to defend:

- **SysML:** a modeling language for requirements, structure, behavior, constraints, and relationships in complex systems;
- **MBSE:** models are central engineering artifacts, not decorative diagrams after implementation;
- **agentic workflow:** multiple controlled steps choose tools/actions and consume observations;
- **cyclic graph:** a validator can return failed output to a repair step instead of accepting one pass;
- **formal validation boundary:** checking schema/consistency rules is not automatically a proof of all system safety properties;
- **reliability controls:** structured output, schema validation, bounded retries, timeout, tool permissions, logging, deterministic checks, and human approval for consequential output.

Prepare one exact personally owned workflow before the interview:

```text
input -> extraction -> model generation -> deterministic checks
      -> (failure) repair -> recheck -> human-reviewed output
```

Do not invent its metric or production status. State the real artifact, rule, failure, and result.

## 9.3 SocioFi Technology

Resume-grounded facts:

- internship/research/AI software work, May–October 2025;
- promoted after a three-month internship;
- LangChain/LangGraph AI workflows;
- full-stack work with Next.js and PERN/MERN stacks;
- third-party integrations: Azure Speech, Stripe, and Namecheap.

Likely follow-ups:

### Why LangGraph instead of one prompt?

A graph makes state, branches, retries, validation, and tool boundaries explicit. It helps inspect why a workflow failed. It does not automatically make the model reliable; deterministic guards and evaluation are still required.

### Stripe security

Do not trust price or payment success sent by the client. Create payment intent/session on the server, verify signed webhooks, make webhook processing idempotent, store minimum sensitive data, protect secrets, and reconcile the provider event with the local order state.

### Azure Speech failure handling

Handle authentication expiry, network timeout, unsupported/audio format, partial recognition, silence/noise, quota/rate limits, and user consent/privacy. Expose a retry or text fallback rather than silently losing input.

### Third-party API design

Use timeouts, bounded retries with backoff for transient failures, idempotency where actions can repeat, circuit breaking when appropriate, input/output validation, secret isolation, structured logs, and graceful degradation.

## 9.4 Freelance programming instructor

> “Since 2023 I have mentored undergraduates in programming, DSA, ML, and web development. The main skill I developed is locating the prerequisite misconception rather than only fixing the final code. I use small traces, ask students to predict the next state, and then vary the input so they must transfer the idea.”

Prepare one true student-misconception story using situation → diagnosis → teaching intervention → evidence of understanding.

---

# 10. Industry answer framework

For any experience question use **STAR-L**:

- **Situation:** relevant context only;
- **Task:** what *you* owned;
- **Action:** design, implementation, and reasoning;
- **Result:** verified outcome, with a number only if documented;
- **Learning:** what you would retain or change.

Every role needs five facts written privately before the viva:

1. one component you personally owned;
2. one design choice and rejected alternative;
3. one failure/bug and how evidence isolated it;
4. one security/reliability control;
5. one verified result.

If a fact is not in your memory or records, do not manufacture it. A precise modest answer is stronger than an impressive claim that collapses under follow-up.

---

# 11. Compact project defense

Projects are lower priority than thesis/research, but every resume item needs a defensible core.

| Project | Problem and core stack | Defensible technical focus |
|---|---|---|
| SecureHerAI | safety-assistance prototype; React Native/Expo, Spring Boot, PostgreSQL, Azure | authentication, trusted contacts, alert/report flow, deployment boundary |
| DomainBuddy | domain discovery/purchase; PERN, Supabase, Stripe, Gemini, Namecheap | server-side price/payment control, provider API consistency |
| Weather Agent | conversational weather; MERN, Gemini, Azure Speech, OpenWeatherMap | tool/API orchestration, voice fallback, hallucination boundary |
| BookBreeze | library management; Node, Oracle, React | normalized schema, roles, transactions, lending constraints |
| Travel BD | travel discovery/community; Flutter, Firebase | state management, authentication, data access rules |
| NodiWatch | river monitoring prototype; Next.js, FastAPI, Earth Engine, Sentinel-1/2 | MNDWI/spectral/SAR signals, ground-truth and threshold limitations |

For each, prepare only:

- architecture in one diagram;
- your exact contribution;
- hardest technical issue;
- one security/failure case;
- one limitation or unimplemented feature.

Never describe a prototype as a guaranteed emergency, medical, financial, or environmental decision system.

---

# 12. Communication under pressure

## 12.1 If you do not know

> “I have not worked with that method directly. My current understanding is … . I would verify the exact detail before teaching or implementing it.”

Then give only what you know. This is better than guessing.

## 12.2 If you partially remember an equation

Define the random variables/terms first and derive it if possible. For example, bias–variance becomes easier after writing `Y=f(x)+epsilon` and adding/subtracting the mean predictor.

## 12.3 If the question is ambiguous

State the interpretation:

> “By successor, do you mean the next node in inorder sequence? Under that definition …”

Do not ask for clarification when a conventional interpretation is safe; state it and proceed.

## 12.4 If interrupted

Stop immediately, answer the new question directly, and return only if invited. A viva tests interaction, not delivery of a memorized lecture.

## 12.5 If the interviewer gives a contradictory expected answer

Separate conventions from facts. Example: a chain of four toggle flip-flops driven at 32 kHz gives `Q1=16`, `Q2=8`, `Q3=4`, `Q4=2 kHz` under the usual stage naming. If someone reports 4 kHz, they may be counting the third divided output as the “fourth” point. Explain the convention respectfully.

---

# 13. Final spoken checklist

Before entering, be able to say without notes:

- thirty-second self-introduction;
- why teaching, why BRAC University, and future plan;
- why DSA is your first choice without sounding one-dimensional;
- the complete function teaching demonstration;
- one recursion trace and recursion-versus-iteration comparison;
- the graph motivation using map/social/prerequisite examples;
- one true teaching misconception story;
- one owned SysModeler workflow and validation failure;
- one owned SocioFi feature and reliability/security issue;
- one compact architecture/contribution/limitation answer for each resume project;
- the exact boundaries between what you built, what the team built, and what remains planned.

The goal is not to sound rehearsed. The goal is to make the first sentence correct, the example concrete, and the limitation honest.
