# Bismillah.

# Thesis, Research, and Industry Viva Defense

> **Evidence boundary (résumé refreshed September 2026).** Personal facts were checked against `My_Resume/main.tex`. The existing public-paper/Matter explanations below retain their cited source/version boundaries. The private Matter and visual-certificate manuscripts were not supplied as sources for this chapter: undisclosed findings, exact VPG formula, eight property names, model versions, splits and personal task allocation are **not guessed**. Confirm them from your manuscripts. A résumé assertion is not independent verification of a research result.

Public references used for facts that are not in the résumé:

- [NEUROSKY-EPI / Affordable EEG preprint](https://arxiv.org/abs/2511.01879)
- [Bengali-Loop preprint](https://arxiv.org/abs/2602.14291)
- [Official Matter SDK repository](https://github.com/project-chip/connectedhomeip)
- [Official chip-tool guide](https://project-chip.github.io/connectedhomeip-doc/development_controllers/chip-tool/chip_tool_guide.html)
- [Official Matter access-control guide](https://project-chip.github.io/connectedhomeip-doc/guides/access-control-guide.html)
- [BUET 2026 undergraduate-research listing](https://cse.buet.ac.bd/academics/undergraduate_research/2026)

---

# 1. The research answer that never sounds vague

For any thesis or paper, answer in this order:

1. **Problem:** what precise gap exists?
2. **Why it matters:** who or what is affected?
3. **Research question:** what did you test or investigate?
4. **Method:** data, representation, algorithm, baselines, and validation.
5. **Result:** the most important measured finding, with the correct unit.
6. **Your contribution:** concrete verbs and artifacts—not “I helped.”
7. **Limitation:** one real threat to validity.
8. **Next step:** the experiment that addresses that limitation.

## 1.1 Three useful answer lengths

**One sentence**

> “I studied **problem** because **motivation**, using **method**, and found **result**.”

**Thirty seconds**

> “The existing situation has **gap**. We asked **question**. We built or evaluated **method** against **baseline**, measured it with **metric**, and observed **result**. My main contribution was **specific artifact or experiment**.”

**Ninety seconds**

Add threat model/data design, one ablation or validation step, one limitation, and future work. Stop there and invite the panel to choose a detail.

## 1.2 Contribution language

Use verbs that a panel can investigate:

- designed the state representation;
- implemented the extraction or evaluation pipeline;
- generated and validated a subset of the dataset;
- ran the baseline and ablation experiments;
- wrote the SDK test harness;
- analyzed errors and categorized findings;
- wrote or revised particular manuscript sections.

Do not claim the whole team’s work. “We” describes the paper; “I” describes only your work.

## 1.3 The result-versus-claim distinction

- **Observation:** what happened in the experiment.
- **Result:** an observation summarized by a metric and uncertainty.
- **Conclusion:** an interpretation supported by the result.
- **Claim:** the scope in which that conclusion is asserted.

Example: “Context improved clustering on this dataset” is narrower and safer than “context solves epilepsy diagnosis.”

---

# Part I — Primary thesis: LLM-guided security analysis of Matter

# 2. A defensible thesis story

## 2.1 One sentence

> “My thesis studies whether a structured, section-wise LLM workflow—combining security-property extraction, protocol state-machine modeling, GraphRAG retrieval, and Matter SDK experiments—can help analysts find specification-level security inconsistencies in the large, stateful Matter protocol.”

## 2.2 Thirty seconds

> “Matter is a cross-vendor smart-home standard. Its security requirements are distributed across commissioning, credentials, fabrics, access control, and operational messaging, so a dangerous interaction may span distant specification sections. We built a section-wise LLM-guided workflow that extracts security properties, models relevant states and transitions, reconnects cross-section evidence through GraphRAG, and treats LLM outputs only as hypotheses. Candidates are manually checked and, where possible, tested with the Matter SDK and chip-tool. The résumé reports 17 specification-level findings, including 8 major findings. That number must be defended with the private manuscript’s exact taxonomy and evidence.”

## 2.3 Why this domain?

> “Smart-home software affects physical spaces, and a standards-level ambiguity may propagate across multiple vendors. The problem combines networking, security, protocol state reasoning, formal modeling, and modern language models. I was interested in using LLMs as evidence-retrieval and hypothesis-generation assistants without treating fluent output as proof.”

## 2.4 What makes it research, not a chatbot demo?

A scientific contribution requires:

- a precise security question or property;
- a reproducible corpus/version of the specification;
- a defined extraction and state-modeling procedure;
- baselines, such as plain prompting or vector-only retrieval;
- controlled comparisons or ablations;
- traceable evidence for every candidate;
- independent/manual review criteria;
- executable validation where the claim is testable;
- false-positive analysis and threats to validity.

If the study did not perform one of these, say so. Never invent an experiment during a viva.

---

# 3. Matter fundamentals you should be able to draw

Matter is an IP-based application-layer connectivity standard and ecosystem. Do not say that Matter *is* Thread. Thread and Wi-Fi can provide IP connectivity; Bluetooth Low Energy is commonly used during discovery/commissioning.

## 3.1 Core vocabulary

- **Node:** an addressable Matter logical device.
- **Endpoint:** a logical device/function inside a node.
- **Cluster:** a standardized feature interface, containing attributes, commands, and events.
- **Attribute:** persistent or reportable state.
- **Command:** requested action.
- **Event:** occurrence reported by a server.
- **Fabric:** a logical trust domain containing a controller and commissioned nodes.
- **Fabric ID:** identifies a fabric; operational identity is fabric scoped.
- **Commissioner:** brings a device into a fabric.
- **Commissionee:** device being commissioned.
- **Fabric Administrator:** authority that manages fabric membership/credentials.
- **DAC/PAI/PAA:** device attestation certificate, product attestation intermediate, and trusted product attestation authority.
- **NOC:** node operational certificate, used for operational identity.
- **ACL:** access-control list governing subjects, privileges, targets, and fabric scope.

## 3.2 Simplified commissioning flow

```text
uncommissioned device
    -> discovery and setup-code information
    -> PASE secure commissioning session
    -> device attestation and product checks
    -> network provisioning when required
    -> operational credentials / fabric installation
    -> initial access-control configuration
    -> CASE operational sessions
    -> normal cluster interaction
```

This is a conceptual flow. Exact ordering and optional steps depend on the commissioning method and Matter version.

## 3.3 PASE versus CASE

| PASE | CASE |
|---|---|
| Password-authenticated session establishment | Certificate-authenticated session establishment |
| Used while establishing trust during commissioning | Used after operational credentials exist |
| Based on setup secret/password information | Based on fabric-scoped operational certificates |
| Solves initial secure-channel bootstrapping | Solves authenticated operational communication |

Never describe the setup code as a long-term operational key.

## 3.4 Attestation versus operational identity

- **Device attestation:** “Is this device associated with a trusted product/manufacturer chain and expected product information?”
- **Operational authentication:** “Is this node a legitimate member of this fabric?”

Passing attestation does not itself grant arbitrary operational access. Authorization is a separate decision.

## 3.5 Authentication versus authorization

- Authentication establishes identity or possession of credentials.
- Authorization decides whether that authenticated subject may perform a requested action.

For a command such as unlocking a door:

```text
secure session valid?
    -> authenticated fabric/subject?
        -> ACL privilege and target match?
            -> command semantics/state permit action?
```

Encryption alone does not supply authorization.

## 3.6 Why IPv6?

IPv6 provides a common network layer across links such as Thread and Wi-Fi, supports a very large address space, and fits modern IP service discovery and routing. Matter is at the application layer; the transport/link choices beneath it are distinct architectural decisions.

---

# 4. Threat model and security-property extraction

## 4.1 Start every security claim with a threat model

State:

- assets: keys, credentials, fabric membership, ACLs, device state, privacy-sensitive events;
- adversary position: local radio, local IP network, remote application path, malicious commissioned node, compromised commissioner, or physical access;
- capabilities: eavesdrop, replay, inject, delay, reorder, open a commissioning window, invoke commands, or alter storage;
- trusted components: roots, secure storage, commissioner, crypto implementation, transport assumptions;
- out of scope: side channels, invasive physical attacks, compromised root authorities, or denial of service—only if the study explicitly excludes them.

Changing the attacker changes whether something is a vulnerability.

## 4.2 Turn prose into checkable properties

A useful representation is:

```text
Property = (precondition, actor, action/message, protected object,
            required authorization/state, expected postcondition,
            source citation)
```

Example pattern—not a thesis finding:

```text
If node X is not a member of fabric F,
then X must not obtain fabric-scoped operational data for F,
unless a specification-defined commissioning transition authorizes it.
```

Security-property families:

- confidentiality and data minimization;
- integrity and origin authentication;
- freshness, replay resistance, and uniqueness;
- authorization and least privilege;
- state-transition validity;
- credential binding and lifecycle;
- cross-fabric isolation;
- secure failure and recovery;
- availability/resource exhaustion;
- auditability and revocation.

## 4.3 Specification flaw versus implementation flaw

- **Specification flaw:** compliant implementations may still exhibit unsafe behavior because the normative requirements are missing, inconsistent, ambiguous, or compose unsafely.
- **Implementation flaw:** the code violates an adequate specification or implements it incorrectly.

An SDK experiment demonstrates behavior in that implementation/version. To call it specification-level, tie the behavior to normative text and explain why a compliant implementation is allowed or driven to behave that way.

---

# 5. Why section-wise analysis, state machines, and GraphRAG

## 5.1 Why not one giant prompt?

Large-spec prompting creates:

- context-window pressure and omitted evidence;
- poor traceability;
- attention dilution;
- inconsistent terminology across distant sections;
- non-reproducible free-form judgments.

Section-wise processing improves coverage and provenance, but risks losing cross-section dependencies. That is why retrieval and explicit relationships are needed.

## 5.2 Protocol state machine

A state machine is a tuple such as

$$
M=(S,\Sigma,\delta,s_0,F)
$$

where `S` is the set of states, `Σ` the events/messages, `δ` the transition relation, `s0` the initial state, and `F` any terminal/accepting states when relevant.

For security analysis, enrich transitions:

```text
(source state, actor, event, guard/precondition,
 action, destination state, security assertions, evidence)
```

State modeling finds bugs that sentence-level analysis misses: a message valid in one state may be unsafe before authentication, after revocation, during recommissioning, or under interleaving.

## 5.3 Safety and liveness

- **Safety:** “something bad never happens,” such as an unauthorized subject never gains a privilege.
- **Liveness:** “something good eventually happens,” such as a valid commissioning exchange eventually completes under stated network assumptions.

Temporal wording matters: `always`, `eventually`, `until`, `before`, `after`, and `only if` carry different requirements.

## 5.4 Why a graph-backed retrieval layer?

Plain vector retrieval ranks semantic similarity. A graph can explicitly represent:

- section references;
- entity aliases;
- credential ownership;
- state/transition dependencies;
- normative requirement conflicts;
- actor-resource-permission links;
- evidence-to-candidate provenance.

GraphRAG should not be described as magic. It is retrieval augmented by graph structure. It can still fail due to bad extraction, missing edges, stale versions, poor entity resolution, or an incomplete query.

## 5.5 Hallucination controls

- require source section/paragraph for every extracted rule;
- distinguish normative “shall” from explanatory prose;
- retrieve both supporting and contradicting evidence;
- use schema-constrained output;
- reject candidates without evidence;
- separate model generation from human adjudication;
- reproduce testable claims in a pinned SDK version;
- record prompt/model/settings and random seeds;
- measure confirmed-candidate precision rather than announcing raw generations as vulnerabilities.

An LLM proposes. Evidence and experiments decide.

---

# 6. SDK and chip-tool validation

`chip-tool` is a Matter controller/testing command-line tool. Conceptually it can commission a device, establish sessions, read/write attributes, invoke commands, subscribe to changes, and exercise access-control behavior.

## 6.1 A good validation record

For each candidate keep:

1. candidate ID and claimed violated property;
2. exact normative source and Matter version;
3. attacker and initial state;
4. SDK commit/build configuration/device or example app;
5. commissioning/fabric/credential setup;
6. precise command/message sequence;
7. expected behavior;
8. observed output, logs, packet trace, and device state;
9. repetitions and controls;
10. interpretation: confirmed, rejected, ambiguous, or implementation-only.

## 6.2 Positive and negative controls

- **Positive control:** an authorized operation that should succeed.
- **Negative control:** a clearly unauthorized operation that should fail.
- **Candidate case:** differs only in the condition under study.

Without controls, failure may be a setup mistake and success may be ordinary authorized behavior.

## 6.3 False positives and false negatives

- False positive: workflow flags a safe/irrelevant behavior.
- False negative: workflow misses a real issue.

If there is no complete labeled universe of vulnerabilities, full recall cannot be measured. You can still report candidate confirmation rate, known-case recovery, reviewer agreement, ablation results, and reproducibility.

## 6.4 Defending “17 findings, 8 major”

Do not recite only the count. For the private manuscript, be ready with:

- the taxonomy used to group duplicates/root causes;
- exact criterion for “major”;
- at least two representative findings permitted for disclosure;
- requirement citations and affected states;
- SDK reproduction steps;
- whether each is spec-level, implementation-level, or composition-level;
- disclosure/patch/version status;
- false-positive adjudication;
- your exact role in discovering and validating each example.

If disclosure is restricted, say: “I can explain the methodology and a sanitized example, but not an undisclosed exploit detail.”

---

# 7. Matter thesis rapid questions

**Why an LLM?** To scale extraction and cross-reference hypothesis generation over a large natural-language specification; not to replace validation.

**Why not only keyword search?** Keywords miss aliases, semantic relations, state dependencies, and interactions expressed differently across sections.

**Why not only embeddings?** Similarity does not encode all explicit actor, state, credential, and authorization relations; graph edges make some dependencies traversable and auditable.

**Is GraphRAG formal verification?** No. Retrieval and generation are probabilistic. Formal verification proves properties of a faithful formal model under assumptions; this workflow can help build/check candidates but is not automatically a proof.

**Can testing prove absence of vulnerabilities?** No. Testing samples executions. It can reproduce a behavior or refute a particular hypothesis under a configuration, not prove universal security.

**Biggest validity threats?** Specification/SDK version drift, incomplete extraction, state-model omissions, model nondeterminism, ambiguous normative text, reviewer subjectivity, and limited implementation coverage.

**Best next step?** Convert high-value properties and state fragments into machine-checkable models, evaluate on multiple versions/implementations, expand independent review, and track disclosure/patch outcomes.

---

# Part II — Recognizing graph properties through visual certificates

# 8. Central story

## 8.1 Thirty seconds

> “Recognizing a graph property from an image is harder than running an algorithm on an adjacency list: the model must first recover visual structure and then reason in a layout-invariant way. We constructed a 24,000-image benchmark over eight graph properties, including YES examples, same-layout negatives, and explicit counter-certificates. We evaluated zero-shot and fine-tuned multimodal language models and supervised vision models, and introduced Visual Proof Gain to quantify the value of proof-like visual evidence. The exact eight properties, VPG definition, splits, models, and my contribution must be stated exactly as in the private manuscript.”

## 8.2 Graph property

A graph property is invariant under graph isomorphism. If `G ≅ H`, then either both satisfy the property or neither does. Planarity, connectedness, bipartiteness, and existence of a Hamiltonian cycle are examples; a vertex being drawn on the left is not.

This makes layout controls essential. A vision model should not infer the label from color, location, density, renderer artifacts, or drawing style.

## 8.3 Certificate and counter-certificate

For a decision problem:

- a **certificate** is a witness that can be checked more easily than rediscovering the answer;
- a **counter-certificate** is a checkable witness against a claim or for the complementary class, when such a witness is defined.

Examples from general graph theory—not necessarily the paper’s eight tasks:

- path between two vertices as a reachability witness;
- a two-coloring as a bipartiteness witness;
- an odd cycle as a non-bipartiteness witness;
- a listed cycle visiting all vertices once as a Hamiltonian-cycle witness;
- a cut and matching flow value as part of a maximum-flow optimality certificate.

A highlighted shape is useful only if a verifier can map it to graph elements and check the logical condition.

## 8.4 Why same-layout negatives?

Suppose a positive and negative image use unrelated layouts. The model may learn visual density, crossing frequency, or renderer style instead of the property. A same-layout or matched-layout negative holds nuisance visual features as constant as possible while changing the underlying label. It is a causal control against shortcut learning.

## 8.5 Dataset design

For each generated sample preserve:

```text
graph identity
property and label
generation seed
layout algorithm and coordinates
rendering style
certificate/counter-certificate identity
source graph pair or transformation
split assignment
```

The split must prevent near-duplicate leakage. If the same graph appears with multiple layouts/certificate overlays, all variants should normally remain in one split when testing generalization to unseen graphs.

## 8.6 What can leak?

- graph duplicates or isomorphic variants across splits;
- the same coordinates with only cosmetic changes;
- class-specific colors, markers, line widths, or file metadata;
- graph-size imbalance by class;
- property-specific generators;
- certificate presence that directly reveals the label;
- prompt wording or filename cues.

Use matched generation, graph-level grouping, style randomization, metadata stripping, and adversarial shortcut probes.

## 8.7 Why not OCR plus a classical graph algorithm?

That is a valid baseline. It decomposes the task into vertex/edge extraction followed by exact symbolic reasoning. Its weaknesses are crossings, occlusion, anti-aliasing, labels, curved edges, and uncertain topology. A strong evaluation compares end-to-end visual models with this modular baseline and reports where perception versus reasoning fails.

## 8.8 Visual Proof Gain

The phrase implies a contrast between matched conditions with and without valid visual evidence, but the **exact formula, direction, aggregation, and range are manuscript-specific**. Do not substitute a guessed accuracy difference.

Be able to state:

1. the exact mathematical definition;
2. numerator/denominator or paired difference;
3. what “proof” condition means;
4. whether higher is always better;
5. how invalid/counter evidence is handled;
6. confidence interval/significance procedure;
7. why ordinary accuracy does not answer the same question.

## 8.9 Likely viva questions

**Why 24,000 images?** Give the exact product/factorization arithmetic from the manuscript: properties × labels × evidence conditions × layouts/sizes/seeds. A round number alone is not justification. “Factorial” would mean an expression such as `n!`, which is not what this multiplication is.

**Why eight properties?** Explain coverage across local/global structure, computational difficulty, certificate availability, and visual ambiguity using the actual property list.

**Can a model memorize layout?** Yes; matched layouts, grouped splits, unseen layouts, style perturbations, and shortcut baselines test this risk.

**Does a correct label prove reasoning?** No. Test certificate localization/verification, counterfactual evidence, explanations tied to vertices/edges, and adversarial changes.

**Zero-shot versus fine-tuning?** Zero-shot tests transferred capability; fine-tuning tests task adaptation but increases overfitting/leakage risk and needs clean validation.

**Main limitation?** Synthetic imagery may not represent hand-drawn/noisy diagrams; property and graph-size coverage may be narrow; success may reflect visual cues rather than algorithmic generalization.

---

# Part III — NEUROSKY-EPI

# 9. Central story and public facts

The public preprint describes the first open single-channel consumer-grade epilepsy EEG dataset collected in a South Asian clinical setting, with contextual metadata. It proposes **EmbedCluster**, transferring representations from EEGNet models trained on clinical data, enriching them with contextual autoencoder embeddings, and clustering patients.

Your résumé states that this work was accepted as a poster at the **NeurIPS 2025 Workshop on Learning from Time Series for Health (TS4H)**. Say “NeurIPS workshop poster,” not “main-track NeurIPS paper.”

## 9.1 Thirty seconds

> “Clinical multichannel EEG is expensive and difficult to access in many low-resource settings. NEUROSKY-EPI investigates whether low-cost single-channel EEG, combined with contextual metadata, can support meaningful patient stratification. The pipeline transfers EEGNet representations, learns context embeddings through an autoencoder, and clusters patients. This is a feasibility and dataset contribution, not a diagnostic-device claim.”

## 9.2 Public arXiv-v1 dataset and result card

Use the version qualifier **“the public arXiv v1 reports”** because later manuscript versions may change preprocessing, cohorts, or evaluation.

### Cohort and data

- 25 epilepsy patients from one South Asian hospital: 13 female and 12 male;
- two controlled conditions per participant: about one minute resting/eyes closed and one minute awake/eyes open;
- 2,032 labeled approximately one-second NEUROSKY-EPI windows;
- patient annotation: recent seizure-frequency change, `Yes=15`, `No=10`;
- a consumer NeuroSky MindWave Mobile 2 using a single frontal Fp1 electrode/reference setup;
- ten per-window band/consumer features, including delta through gamma bands plus proprietary Attention and Meditation indices;
- de-identified demographic, clinical, medication, and self-reported context fields, with categorical/binning measures described for privacy.

The transfer source was CHB-MIT: the paper reports 24 pediatric patients and 12,009 labeled eight-second segments after restricting to Fp1/the nearest frontal channel and transforming inputs to match the consumer-feature pathway. It states that NEUROSKY-EPI was not used to train that supervised seizure/non-seizure source model.

### Embeddings and reported clustering results

The public pipeline aggregates window embeddings at patient level using mean and standard deviation, then evaluates four clustering algorithms: K-means, agglomerative, Gaussian mixture model, and spectral clustering.

- **EEGNet-transfer embeddings:** arXiv v1 reports `62.50%` clustering accuracy for all four algorithms and cluster sizes of about 12–13 patients.
- **Contextual autoencoder:** the paper describes a three-layer feed-forward autoencoder with code dimension 4 and reports that appending four rest/active context summaries yields a 16-dimensional window embedding, then mean-plus-standard-deviation aggregation yields a 32-dimensional patient representation. It reports `58.33%` for K-means, agglomerative, and spectral, and `62.50%` for GMM. It also reports examples of a 21/4 agglomerative split and a 15/10 K-means split. Treat the stated `16D -> 32D` shapes as version-reported facts, not arithmetic you can presently derive: if all four context summaries were scalar, `4+4` would be 8 rather than 16. Verify whether each summary is multi-dimensional or whether another component is omitted from the public prose.

### Evaluation-arithmetic warning for the viva

Do **not** turn `62.50%` into an invented “number of correct patients.” A single hard-label score over all 25 patients changes in increments of `1/25=4%`, so `62.5%` is not directly reconstructible as `correct/25`. Likewise, unsupervised cluster IDs have no intrinsic class meaning: clustering accuracy normally requires choosing the best label permutation (for more classes, often via Hungarian matching).

The public v1 text reports the percentages but does not state enough in the displayed evaluation description to reconstruct the exact scoring denominator, split/repetition aggregation, or label-permutation procedure. Before the viva, verify these items from the authors' evaluation code/current manuscript:

1. exact unit scored—patients, folds, repetitions, or some held-out subset;
2. whether results are one run or an average and how uncertainty was computed;
3. how cluster IDs were aligned to `Yes/No` labels;
4. whether any label information influenced model choice or only final evaluation;
5. why the reported percentages have those denominators;
6. the exact tensors concatenated to obtain the reported 16-dimensional window and 32-dimensional patient representations.

Until verified, the defensible sentence is: **“arXiv v1 reports 62.50% for EEGNet embeddings and 58.33–62.50% for the contextual autoencoder; I would check the precise evaluation denominator and cluster-label mapping before converting those percentages to subject counts.”** The paper itself characterizes 62.50% as only moderately above 50% chance and not sufficient for clinical decision-making. With 25 patients from one hospital and a single electrode, treat the work as an early feasibility study.

## 9.3 Core signal concepts

- EEG measures voltage differences arising from aggregate neural activity, contaminated by eye, muscle, movement, line, and electrode artifacts.
- Sampling frequency `fs` gives Nyquist frequency `fs/2`; frequencies above it alias unless filtered before sampling.
- A single Fp1 electrode has limited spatial information and is especially exposed to ocular artifacts.
- Filtering changes the signal; report bandpass/notch choices and avoid leakage from noncausal filtering in deployment claims.
- Windowing produces correlated samples. Two windows from one patient are not independent patients.

## 9.4 EEGNet intuition

EEGNet is a compact convolutional architecture for EEG. Temporal convolutions learn frequency-sensitive filters; depthwise/separable operations reduce parameters and can learn channel/filter-specific structure. A single-channel adaptation loses much of the multichannel spatial-filter advantage, so exact input shape and transfer procedure matter.

## 9.5 Context autoencoder

An autoencoder learns

$$
z=f_\theta(c), \qquad \hat c=g_\phi(z)
$$

by minimizing reconstruction loss such as

$$
\mathcal L=\frac1n\sum_i\lVert c_i-\hat c_i\rVert_2^2.
$$

The latent vector `z` is a compressed context representation. Normalize continuous features, encode categorical variables deliberately, handle missingness, and prevent target leakage. Reconstruction quality alone does not prove clinical usefulness.

## 9.6 Patient stratification versus diagnosis

- **Stratification:** group patients by learned similarities for analysis or hypothesis generation.
- **Classification:** assign known labels.
- **Diagnosis:** clinical determination requiring validated clinical evidence and workflow.

Unsupervised clusters are not automatically disease subtypes. Clinical interpretation needs external validation.

## 9.7 K-means recall

K-means minimizes within-cluster squared distance:

$$
J=\sum_{i=1}^{n}\lVert x_i-\mu_{c_i}\rVert_2^2.
$$

Algorithm:

1. initialize `k` centroids, preferably k-means++;
2. assign each point to the nearest centroid;
3. recompute each centroid as its cluster mean;
4. repeat until assignments or objective stabilize.

It assumes roughly compact, scale-comparable clusters; standardize features and use multiple initializations. Choose/evaluate `k` with domain knowledge and metrics such as silhouette score, adjusted Rand index when reference labels exist, stability, and clinically interpretable separation.

## 9.8 Leakage and evaluation

Patient-correlated windows can cause severe leakage if randomly split by window. For claims about unseen patients, use patient-level separation. Fit preprocessing, feature selection, autoencoders, and normalization on training data only.

Report:

- number of patients and windows separately;
- class/patient distribution;
- split unit and seed;
- window overlap;
- transfer source and frozen/fine-tuned layers;
- context variables;
- baseline signal-only versus signal+context;
- patient-level uncertainty;
- ethics/consent/privacy process stated in the paper.

## 9.9 Responsible claims

- Small patient count limits external validity even if window count is large.
- Consumer-grade single-channel EEG cannot replace clinical multichannel EEG.
- Demographic/context features can encode social bias.
- Medical data requires consent, de-identification, access control, and cautious release.
- Report association/stratification, not diagnosis or treatment efficacy.

---

# Part IV — Bengali-Loop

# 10. Central story and public facts

The public preprint reports two realistic long-form Bangla speech benchmarks:

- ASR: 191 recordings, 158.6 hours, about 792,000 words from 11 YouTube channels;
- diarization: 24 recordings, 22 hours, 5,744 manually annotated speaker segments;
- reported baselines: Tugstugi at 34.07% WER and pyannote.audio at 40.08% DER.

## 10.1 Thirty seconds

> “Short clean speech datasets do not capture long Bangla media with music, noise, speaker changes, overlap, dialect variation, and long-context errors. Bengali-Loop provides reproducible long-form ASR and speaker-diarization benchmarks, standardized data and annotation formats, and baseline WER/CER/DER evaluation. It is a community-scale benchmark, so I should distinguish the paper’s contribution from my documented personal contribution.”

## 10.2 Public arXiv-v1 protocol and result card

### Long-form ASR

The full corpus contains 191 recordings, but the public-v1 baseline table is explicitly evaluated on **37 test recordings**:

| Model | WER | CER |
|---|---:|---:|
| Tugstugi | 34.07% | 16.44% |
| Hishab TITU-BN | 50.67% | 21.99% |

Lower is better. The scoring protocol reports Unicode NFC normalization, punctuation removal, consistent whitespace, digit-to-Bangla-word conversion, and explicit code-mixed token handling. For limited-context models, the paper describes chunked inference such as overlapping 30-second windows followed by overlap-aware hypothesis stitching. In a viva, distinguish the **191-recording collection total** from the **37-recording baseline test set**.

### Speaker diarization

The 24-recording, 22-hour, 5,744-segment corpus is split as follows:

| Split | Recordings | Hours | Segments | Average speakers/recording |
|---|---:|---:|---:|---:|
| train | 10 | 9.5 | 2,612 | 17.1 |
| test | 14 | 12.5 | 3,132 | 15.4 |
| total | 24 | 22.0 | 5,744 | 16.1 |

The v1 annotation policy assigns an overlapped interval to the speaker who began first, producing a single-label reference. Its DER protocol specifies a boundary collar of about `0.25 s`, optimal system/reference speaker-ID assignment via the Hungarian algorithm, and scoring consistent with that single-label overlap policy. Verify the released scoring script before asserting an exact collar if a newer version changes the “e.g., 0.25 s” wording.

| Diarization system on the 14-recording test set | DER |
|---|---:|
| pyannote.audio pretrained pipeline | 40.08% |
| Silero VAD + ECAPA + agglomerative clustering | 61.50% |
| WebRTC VAD + ECAPA + agglomerative clustering | 73.71% |

Again, lower is better. Hungarian mapping is necessary because predicted speaker IDs are arbitrary; it does not repair missed speech, false-alarm speech, or incorrect turn boundaries.

## 10.3 ASR metrics

Word error rate:

$$
WER=\frac{S+D+I}{N},
$$

where substitutions `S`, deletions `D`, and insertions `I` transform the reference into the hypothesis, and `N` is reference word count.

Character error rate uses the same edit-distance structure at character level:

$$
CER=\frac{S_c+D_c+I_c}{N_c}.
$$

WER can exceed 100% when insertions are large. Bangla normalization and tokenization choices materially change WER/CER, so the evaluation pipeline must be standardized.

## 10.4 Diarization

Speaker diarization asks **who spoke when**, not what they said.

A common pipeline:

```text
audio
 -> speech activity detection
 -> segmentation
 -> speaker embeddings
 -> similarity/scoring
 -> clustering
 -> resegmentation/overlap handling
 -> speaker-labelled timeline
```

Diarization error rate is commonly

$$
DER=\frac{FA+MISS+CONF}{TOTAL},
$$

where `FA` is false-alarm speech, `MISS` is missed speech, and `CONF` is speaker confusion time. Collar and overlap-scoring conventions must be stated because they affect the value.

## 10.5 Long-form difficulties

- context-window limits and chunk-boundary deletion/repetition;
- music, reverberation, noise, and code switching;
- speaker overlap and rapid turns;
- dialect and pronunciation variation;
- subtitle timing/transcript errors;
- inconsistent punctuation and orthography;
- identity permutation in diarization;
- domain and channel shift.

## 10.6 Personal contribution precision

The public paper lists you as a co-author. Its acknowledgment also associates you with recorded voiceovers for hidden test cases. State any further collection, verification, annotation, code, baseline, analysis, or writing contribution only if you personally performed it and it is documented. Never imply that you built all 158.6 hours or all benchmark components alone.

---

# Part V — Research methods across all works

# 11. Baselines, ablations, and uncertainty

## 11.1 Baseline

A baseline is a meaningful comparison, not necessarily a weak model. Examples:

- Matter: plain prompting, keyword search, vector-only RAG, human-only review;
- visual graphs: majority/random, image classifier, MLLM zero-shot, OCR+parser+algorithm;
- EEG: raw/statistical features, signal-only embedding, context-only, no transfer;
- speech: published ASR/diarization pipeline under the same normalization and scoring.

## 11.2 Ablation

Remove or replace one component while holding other conditions fixed:

- no graph retrieval;
- no state model;
- no certificate overlay;
- random rather than matched negative;
- no context vector;
- no transfer learning;
- alternate VAD/chunking/clustering.

An ablation supports a component-contribution claim; it does not establish causality if multiple factors change.

## 11.3 Confidence and significance

Report the experimental unit. Thousands of windows/images are not thousands of independent patients/graphs if grouped by an underlying entity.

Useful practices:

- bootstrap at graph/patient/recording level;
- confidence intervals, not only point estimates;
- paired tests for matched samples;
- multiple seeds and initialization variance;
- effect size alongside p-value;
- correction when many hypotheses are tested.

## 11.4 Validity taxonomy

- **Internal validity:** did the method cause the measured difference, or did leakage/confounding do it?
- **Construct validity:** does the metric represent the intended concept?
- **External validity:** does the result generalize to new devices, drawings, patients, languages/domains, or versions?
- **Conclusion validity:** is the statistical/data support strong enough?

---

# Part VI — Industry experience and compact project defense

# 12. Industry experience

## 12.1 Presidency University — Lecturer (June 2026–present)

> “I teach theory and sessional courses, prepare lectures/labs/assignments/assessments aligned with learning outcomes, guide implementation, and evaluate students. The experience strengthened my ability to turn a concept into a sequence of motivation, model, example, practice, and feedback.”

Evidence to give when asked: one course, one difficult concept, how you diagnosed misunderstanding, and how assessment changed afterward.

## 12.2 SysModeler AI & Systems Innovation Lab — Junior AI Engineer (April–June 2026)

> “I worked on agentic-AI support for model-based systems engineering: generating SysML-style system models from natural language and using cyclic LangGraph workflows to validate and revise generated models. The key engineering issue was not generation alone, but maintaining typed structure, traceability, termination criteria, and validation for safety-critical use.”

Be ready to distinguish:

- a DAG pipeline from a cyclic workflow;
- generation from validation;
- syntactic from semantic model correctness;
- deterministic checks from LLM review;
- maximum-iteration/stop conditions from accidental infinite loops;
- traceability from ungrounded prose.

## 12.3 SocioFi Technology — Researcher and AI software developer intern (May–October 2025)

> “I progressed from internship to a researcher role while building AI-enabled web workflows with LangChain/LangGraph and production integrations such as Azure Speech, Stripe, Namecheap, and full-stack deployments. The strongest lesson was that an AI feature is also a systems problem: authentication, retries, idempotency, observability, latency, cost, and failure handling matter.”

Likely probes:

- Stripe webhook authenticity and idempotency;
- OAuth versus JWT;
- secret storage and rotation;
- API timeout/retry/backoff;
- durable workflow state;
- hallucination/evaluation;
- CI/CD rollback and monitoring.

## 12.4 Programming instructor

> “I mentor students in DSA, ML, web development, and programming assignments. I first expose their current mental model with a trace or prediction question, explain one invariant, let them work a small case, and then increase complexity.”

This supports “Why teaching?” better than saying only that you enjoy teaching.

---

## 12.5 Seniors' interview checklist — defend evidence, not just terminology

**Source:** Industry Prep D27/D29/D31 and BRAC Ques Bank C29/C47/C49.

For each current résumé item rehearse: what problem, why important, what you
personally did, evidence/results, strongest limitation, and what you would test
next. Describe the Matter and visual-certificate manuscripts as **submitted and
under review according to the résumé**, not accepted. Describe NEUROSKY-EPI as
a NeurIPS 2025 TS4H **workshop poster**, not a main-track acceptance.

Practise a 60–90 second research explanation for non-specialists: problem →
small example → method → measured outcome → limitation. If asked a precise
equation such as VPG, use the actual manuscript; do not invent one from its name.
Do not claim an LLM's critique is formal verification without stating a formal
property, model, verification procedure and its guarantee.

For industry answers, show one concrete failure path on the board, e.g. API
request → timeout → safe retry with idempotency key → reconciliation. State
which behavior you implemented versus which improvement you now propose.
For coding interviews/written tests, write runnable core logic on paper, explain
the invariant aloud in English, test empty/singleton/adversarial examples and
justify the optimization. A link to a large problem bank is a practice resource,
not evidence that every linked problem has been covered here.

# 13. Compact project answers

Projects should be brief unless the panel chooses one. Use: problem → architecture → your role → hardest decision → security/test → limitation.

## 13.1 SecureHerAI

Mobile client with Spring Boot/PostgreSQL backend and cloud deployment, supporting SOS, incident reporting, trusted contacts, map tracking, and safety heatmaps. Discuss JWT/OAuth trust boundaries, authorization beyond login, location-data minimization, notification failure, CI/CD, and abuse-resistant reporting.

## 13.2 DomainBuddy

PERN/Supabase platform integrating Gemini-assisted discovery, Stripe payment, and Namecheap registration. The crucial distributed-systems point is that payment success and domain registration are separate external operations: use verified webhooks, idempotency keys, durable states, reconciliation, and compensation/refund logic.

## 13.3 Weather Agent

MERN conversational assistant integrating Gemini, Azure speech, and weather data. Distinguish model-generated text from authoritative weather fields; validate tool arguments, preserve conversational state deliberately, bound cost/latency, and handle speech/API failure.

## 13.4 BookBreeze

Node/Express/Oracle library system with role-specific behavior, lending, employee/admin functions, and analytics. Be able to defend normalized schema, PK/FK constraints, transaction around borrow/return, prevention of duplicate active loans, indexes, authentication middleware, and SQL injection prevention.

## 13.5 Travel BD

Flutter/Firebase travel and community app. Explain why both GetX and Provider were used if that is still in the résumé, Firebase security rules, authentication, location permission, offline/error state, and separation of UI state from persistent/domain state.

## 13.6 NodiWatch

Hackathon prototype using Next.js/FastAPI and Earth Engine with Sentinel-2 optical and Sentinel-1 SAR signals for river monitoring. Know the exact three layers, ground truth, temporal comparison, thresholds, cloud handling, and personal role. Explain that a spectral index is an analytical feature—not automatically a validated pollution detector.

---

# 14. Final manuscript-only recall card

The following facts cannot be recovered from the supplied workspace. Read them directly from the private manuscripts and write them on one personal page before the viva:

- Matter: exact 17-finding taxonomy, exact 8 major criteria/examples, specification/SDK versions, baselines, model/prompt settings, adjudication, false-positive counts, and your personal contribution.
- Visual certificates: exact eight properties, 24,000-image arithmetic, exact VPG equation, split unit, generators/layouts, model versions, best results, ablations, error analysis, and your personal contribution.
- NEUROSKY-EPI: current-version preprocessing/input shape, exact evaluation denominator/split/repetitions, cluster-label permutation mapping, uncertainty, ethics details, and your contribution. Public arXiv-v1 cohort/window/result counts are summarized in Section 9.2; verify whether the current manuscript changes them.
- Bengali-Loop: exact contribution beyond the publicly documented hidden-test voiceovers, normalization rules, baseline configuration, scoring conventions, and any analysis/writing role.

This is not an invitation to improvise. If a number is not remembered, say what the metric measured and offer to verify the exact value rather than fabricating it.

---

# 15. Research mock viva

1. What is your thesis question in one sentence?
2. Why is Matter analysis stateful?
3. Why does section-wise analysis both help and hurt?
4. What does GraphRAG add over vector retrieval?
5. What is the difference between an LLM candidate and a confirmed vulnerability?
6. How do you distinguish specification and implementation flaws?
7. Show one positive and one negative control for an SDK test.
8. Can testing prove a protocol secure?
9. What is the denominator behind “17 findings”?
10. What exactly made a finding “major”?
11. Define a graph property and a certificate.
12. Why are same-layout negatives important?
13. State the exact VPG equation and explain each term.
14. What is the split unit, and how did you prevent graph leakage?
15. Could an OCR-plus-algorithm baseline outperform a vision model?
16. Why is 2,000 EEG windows not equivalent to 2,000 patients?
17. What is EmbedCluster?
18. Why is an autoencoder embedding not automatically clinically meaningful?
19. What is the difference between stratification and diagnosis?
20. Derive WER and DER and explain their scoring conventions.
21. What makes long-form Bangla speech hard?
22. What did you personally contribute to each paper?
23. Which result are you least confident will generalize, and why?
24. What experiment would most strongly challenge your conclusion?
25. What did industry work teach you that changed your research practice?
