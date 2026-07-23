# Bismillah.

# Machine Learning — Slide-Complete Viva Recall Book

This is a recall book, not a list of one-line answers. It reconstructs the concepts, equations, derivations, algorithms, calculations, code patterns, and likely follow-up questions in both local CSE 471 merged slide sets. Read the **viva answer** first; expand into the surrounding derivation only when the interviewer asks.

## How to answer an ML viva question

Use this order:

1. **Define it precisely.** State what object/process/error the term denotes.
2. **Give the governing equation or algorithm.** Define every symbol and expectation.
3. **Build intuition.** Explain why the equation or procedure behaves that way.
4. **Give one concrete example.** Prefer a two-line numerical calculation.
5. **State assumptions and failure modes.** This is what separates a strong answer from memorization.
6. **Connect related ideas without equating them.** For example, high bias often *causes the behavior called underfitting*, but bias and underfitting are not synonyms.

Notation used throughout:

- `x` is an input/feature vector; `y` is its target.
- `D={(x_i,y_i)}_{i=1}^n` is a training set sampled from a population.
- `h_D` or `f_θ` is the predictor learned from `D`.
- A **parameter** is learned from training data (`w`, neural-network weights). A **hyperparameter** is selected outside the fitting rule (depth, `k`, learning rate, regularization strength).
- An **epoch** is one pass through the training set; a **batch/mini-batch** is the subset used for one gradient update.

---

# Part I — Foundations, data, and evaluation

## 1. What is machine learning?

Tom Mitchell's operational definition is useful in a viva:

> A computer program learns from **experience E**, with respect to a class of **tasks T** and **performance measure P**, if its performance at tasks in T, as measured by P, improves with experience E.

Example: spam filtering. `T` = classify email, `E` = labeled historical emails, `P` = F1/precision-recall or cost-weighted error. The definition forces us to say what improvement means.

### AI, ML, and deep learning

- **Artificial intelligence** is the broad aim of making systems perform tasks associated with intelligent behavior.
- **Machine learning** learns behavior or predictive structure from experience/data instead of specifying every task rule.
- **Deep learning** is ML using multilayer representation-learning models. It is a subset of ML, not a synonym for AI.

### Learning settings

| Setting | Signal | Typical task | Example |
|---|---|---|---|
| Supervised | `(x,y)` labels | classification/regression | disease class, house price |
| Unsupervised | no task label | clustering/density/structure | customer segments |
| Semi-supervised | few labeled + many unlabeled | prediction | medical images with scarce labels |
| Self-supervised | targets constructed from the data | representation/pretraining | mask a token; predict next token |
| Reinforcement learning | reward after actions | sequential decision | game playing, control |

**Generative vs discriminative:** a generative model learns a joint/data mechanism such as `p(x,y)=p(y)p(x|y)` or `p(x)` and can often sample; a discriminative model directly learns `p(y|x)` or a decision boundary. Naive Bayes is generative; logistic regression is discriminative.

### Hypothesis space and inductive bias

A hypothesis space `H` is the set of functions the learner can choose from. Learning chooses `h∈H` that minimizes an empirical objective, often with regularization:

`θ̂ = argmin_θ [ (1/n) Σ_i L(y_i,f_θ(x_i)) + λΩ(θ) ]`.

An **inductive bias** is an assumption that lets the learner generalize beyond observed examples. A linear model assumes a linear boundary in its feature space; a CNN assumes locality and shared patterns; regularization prefers certain parameter values. “Bias” here is a broad preference and must not be confused automatically with the statistical bias in the bias–variance decomposition.

### Parametric and non-parametric models

- **Parametric:** fixed-form, finite parameter vector independent of training-set size, e.g. linear/logistic regression.
- **Non-parametric:** effective complexity may grow with data, e.g. k-NN, an unconstrained decision tree. It does not mean “has no parameters.”

## 2. End-to-end ML workflow

1. Define the prediction unit, population, target, inference-time information, metric, and error costs.
2. Collect and audit representative data; document how labels were produced.
3. Split by the **independence unit** before data-dependent preprocessing.
4. Fit preprocessing only on training data/fold.
5. Establish a simple baseline.
6. Train candidate models on train data; choose hyperparameters on validation data.
7. Freeze all decisions; evaluate once on the locked test set.
8. Perform error analysis, robustness/fairness checks, deployment monitoring, and retraining policy.

### Train, validation, and test

- **Training set:** estimates parameters.
- **Validation set:** chooses model, hyperparameters, threshold, features, and stopping time.
- **Test set:** estimates generalization after all choices are frozen.

If you repeatedly choose based on test results, the test set has become a validation set. With limited data, use `k`-fold cross-validation: divide into `k` folds, train on `k-1`, validate on the remaining fold, rotate, and average. For unbiased outer performance estimation while tuning, use **nested CV**. Stratification preserves class proportions; group/time-series splits preserve the real independence/deployment structure.

### Data leakage

Leakage means training or selection uses information that would be unavailable at real inference or improperly crosses data partitions. Examples:

- normalizing or imputing using the full dataset;
- using a post-outcome/future feature;
- oversampling before splitting;
- the same patient, user, recording, near-duplicate image, or graph template in train and test;
- target encoding without out-of-fold construction;
- choosing checkpoints repeatedly from test performance.

Fit preprocessing in a training-only pipeline, split by group/time, deduplicate, and lock the final test set.

## 3. Preprocessing and feature engineering

### Missing data

- Remove rows/columns only when justified; deletion can bias the sample.
- Numeric imputation: mean (sensitive to outliers), median (robust), model-based imputation.
- Categorical imputation: mode or an explicit “missing” category.
- Add a missingness indicator when absence itself may carry signal.
- Fit imputation statistics on training data only.

Missing completely at random, missing at random conditional on observed variables, and not missing at random lead to different statistical risks; imputation is not proof that bias vanished.

### Scaling

- Min–max: `x'=(x-x_min)/(x_max-x_min)` maps training range to `[0,1]`.
- Standardization: `z=(x-μ)/σ` gives training mean zero and standard deviation one.
- Robust scaling uses median and interquartile range.

Scale-sensitive models include k-NN, k-means, SVM, PCA, and gradient-based linear/neural models. Ordinary trees generally do not need scaling because order-preserving transforms do not change split order.

### Categorical encoding

- **Label/ordinal encoding:** integers; appropriate only when order is real or the model safely treats values categorically.
- **One-hot:** one indicator per category; avoids false numeric order but can be high-dimensional.
- **Target encoding:** category statistics derived from target; powerful but leakage-prone, so compute out-of-fold with smoothing.

### Feature engineering and EDA

Inspect distributions, duplicates, outliers, correlations, class imbalance, label consistency, subgroup coverage, and train/deployment mismatch. Transformations should be justified by domain and invariance, not applied mechanically.

## 4. Loss, risk, and model selection

The **empirical risk** is training loss:

`R̂_D(h)=(1/n)Σ_i L(y_i,h(x_i))`.

The **generalization risk** is population loss:

`R(h)=E_(X,Y)~P[L(Y,h(X))]`.

The generalization gap is `R(h)-R̂_D(h)` (estimated using unseen data). Sources of error discussed in the slides include noise, sampling variance, model unrealizability/misspecification, and optimization/computational limitations.

Regularized empirical risk minimization uses `R̂_D(h)+λΩ(h)`. Hyperparameter/model selection is different from parameter optimization: gradient descent may optimize weights for one model, while validation chooses depth, `λ`, learning rate, or architecture.

## 5. Classification metrics

For positive class `1`:

| | Predicted + | Predicted − |
|---|---:|---:|
| Actual + | TP | FN |
| Actual − | FP | TN |

`accuracy=(TP+TN)/(TP+TN+FP+FN)`

`precision=TP/(TP+FP)` — of predicted positives, how many were correct?

`recall/sensitivity/TPR=TP/(TP+FN)` — of actual positives, how many did we find?

`specificity/TNR=TN/(TN+FP)`

`FPR=FP/(FP+TN)=1-specificity`

`F1=2PR/(P+R)=2TP/(2TP+FP+FN)`

`balanced accuracy=(sensitivity+specificity)/2`

Matthews correlation coefficient:

`MCC=(TP·TN-FP·FN)/sqrt((TP+FP)(TP+FN)(TN+FP)(TN+FN))`.

MCC uses all four cells and remains informative under imbalance; it ranges from `-1` (opposite), through `0` (chance-like), to `1` (perfect), when denominators are defined.

**Worked example:** TP=40, FP=10, FN=20, TN=130. Accuracy=`170/200=.85`; precision=`40/50=.80`; recall=`40/60=.667`; F1=`80/(80+10+20)=.727`; specificity=`130/140=.929`. The example shows why accuracy alone hides missed positives.

### Multiclass averaging

- **Macro:** compute each class metric then average equally; highlights minority classes.
- **Micro:** pool all class decisions first; weights individual examples.
- **Weighted macro:** class metric weighted by support; can hide minority weakness.

### ROC, PR, threshold, and calibration

ROC plots TPR against FPR over thresholds; ROC-AUC measures ranking. PR plots precision against recall; PR-AUC is usually more revealing when positives are rare. Neither chooses the deployment threshold nor proves probabilities are calibrated.

A calibrated model's predictions near `0.8` should be correct about 80% of the time. Assess with reliability diagrams, Brier score, or log loss. Select thresholds from validation data using costs/constraints, not automatically `0.5`.

## 6. Regression metrics

- `MSE=(1/n)Σ(y-ŷ)^2`: penalizes large errors; differentiable.
- `RMSE=sqrt(MSE)`: same units as target.
- `MAE=(1/n)Σ|y-ŷ|`: more robust to outliers.
- `R²=1-Σ(y-ŷ)²/Σ(y-ȳ)²`: improvement over predicting the mean. Test `R²` can be negative.

Squared loss makes the population-optimal prediction `E[Y|X=x]`; absolute loss makes a conditional median optimal. A metric must reflect the real cost of errors.

---

# Part II — Bias, variance, fitting, and regularization

## 7. Bias–variance: the precise answer

### The viva answer

> Bias and variance are statistical components of expected predictive error. Underfitting and overfitting describe fitting/generalization behavior. High bias often manifests as underfitting, and high variance often manifests as overfitting, but the pairs are not definitions or exact synonyms.

### What is random, and which expectation is taken?

Assume squared-error regression:

`Y=f(x)+ε`, where `f(x)=E[Y|X=x]`, `E[ε|X=x]=0`, and `Var(ε|X=x)=σ²(x)`.

Draw a training dataset `D~P^n`; the learning algorithm produces `h_D`. At one fixed test input `x`, define:

- Mean learned prediction: `h̄(x)=E_D[h_D(x)]`.
- Bias: `Bias(x)=E_D[h_D(x)]-f(x)=h̄(x)-f(x)`.
- Squared bias: `Bias²(x)=(h̄(x)-f(x))²`.
- Variance: `Var(x)=E_D[(h_D(x)-h̄(x))²]`.
- Irreducible noise: `σ²(x)=Var(Y|X=x)=E_(Y|x)[(Y-f(x))²]`.

The expectation for bias and variance is over repeated training datasets. It may also include algorithm randomness such as initialization, shuffling, augmentation, and minibatch sampling. The target `Y` is a fresh outcome at the fixed `x`; its randomness is separate. To get overall risk, integrate the final expression over new inputs `X~P_X`.

### Decomposition and derivation

For a fresh target `Y` independent of training set `D` given fixed `x`:

`E_D E_(Y|x)[(Y-h_D(x))²]`

Add and subtract `f(x)` and `h̄(x)`:

`Y-h_D = (Y-f) + (f-h̄) + (h̄-h_D)`.

Square and take expectations. The cross terms are zero because:

- `E_(Y|x)[Y-f]=0`;
- `E_D[h̄-h_D]=0`;
- fresh label noise and training-set randomness are independent under the setup.

Therefore:

`E_D E_(Y|x)[(Y-h_D(x))²] = σ²(x) + Bias²(x) + Var(x)`.

And global expected test MSE is:

`E_X[σ²(X)+Bias²(X)+Var(X)]`.

This simple additive form is for squared-error regression. Bias–variance ideas extend more broadly, but do **not** quote this identical algebra as the exact decomposition for 0–1 classification error or every loss.

### Numerical example

At a fixed `x`, suppose the true conditional mean is `f(x)=10`, label-noise variance is `4`, and models trained on five independent datasets predict `[7,9,8,8,8]`.

- `h̄=(7+9+8+8+8)/5=8`.
- Bias=`8-10=-2`; bias²=`4`.
- Variance=`[(7-8)²+(9-8)²+0+0+0]/5=0.4`.
- Expected prediction MSE=`noise+bias²+variance=4+4+0.4=8.4`.

Bias is signed; the error contribution is squared bias. Variance is not “how noisy the labels are”—that is the irreducible-noise term.

### Why underfitting/overfitting are different

- **Underfitting:** the fitted model fails to capture useful structure, commonly producing high training and validation error. Excessive statistical bias, insufficient features/capacity, too much regularization, or failed optimization can all produce this behavior.
- **Overfitting:** the model fits training idiosyncrasies/noise so training performance is much better than unseen performance. High sampling variance is a common cause, but leakage, split shift, and validation over-tuning can create a similar observed gap.

Thus a train/validation plot is evidence, not a mathematical measurement of the decomposition. Bias and variance ideally concern repetition over many possible training sets, which we rarely observe directly.

### Diagnostic patterns and remedies

| Train behavior | Validation behavior | Common diagnosis | Check first | Typical remedies |
|---|---|---|---|---|
| poor | poor, small gap | underfitting/high-bias-like | optimization, features, labels | richer features/model, less regularization, train properly |
| excellent | much poorer, large gap | overfitting/high-variance-like | leakage/split mismatch | more independent data, regularization, augmentation, simpler model, early stopping, bagging |
| good | good | appropriate fit | subgroup/shift/calibration | preserve; validate robustness |
| poor | erratic/poor | not automatically “bias” | bad learning rate, bugs, noisy labels | debug optimization/data first |

Validation loss can be lower than training loss when training uses dropout, augmentation, label smoothing, or an explicit regularization term. Deep networks may exhibit **double descent**, so validation error need not always be the textbook single U-shaped curve.

### Complexity, regularization, and data

- Increasing capacity often reduces bias but may increase variance.
- Stronger regularization often increases bias but reduces variance.
- More representative independent data mainly reduces estimation variance; it cannot fix a fundamentally wrong target/feature space by itself.
- Bagging reduces variance by averaging unstable learners. If `M` model errors each have variance `s²` and pairwise correlation `ρ`, average variance is approximately `s²[ρ+(1-ρ)/M]`. Diversity matters; perfectly correlated models do not gain from averaging.
- Irreducible noise is irreducible only relative to the current features and label process. Better sensors/features/labels can change it.

### Real-world example

Suppose we predict house price from floor area alone. A straight line misses locality, age, and nonlinear effects: stable across samples but systematically wrong—high-bias-like underfitting. A depth-unlimited tree on 100 houses memorizes rare details: nearly zero train error but changes sharply when a few houses are replaced—high-variance-like overfitting. A regularized ensemble with more representative houses can balance both; unpredictable seller urgency remains noise unless new information captures it.

### Follow-up traps

- “Is bias an error?” — It is signed systematic deviation of the *mean learned predictor*; squared bias contributes to expected MSE.
- “Can a model have low bias and low variance?” — Yes, with appropriate representation, data, and signal; noise can still keep total error nonzero.
- “Does more data reduce bias?” — Usually it directly reduces variance; it may indirectly help if training/model selection changes, but it does not enlarge a misspecified hypothesis class.
- “Does high training error prove high bias?” — No. It could be optimization failure, corrupted labels, or an unsuitable metric.

## 8. Regularization

`L1: Ω(w)=||w||₁=Σ|w_j|` encourages exact zeros/sparsity but is nondifferentiable at zero; a subgradient or proximal method handles it.

`L2: Ω(w)=||w||₂²=Σw_j²` smoothly shrinks weights. For objective `L+λ||w||²`, gradient adds `2λw` (or `λw` if the penalty is `λ||w||²/2`). Correlated features may be distributed across L2 weights, while L1 may select one unstably.

Other regularizers include limited tree depth/pruning, dropout, early stopping, data augmentation, label smoothing, architectural constraints/weight sharing, and ensembling. `λ` is selected using validation, never the test set.

---

# Part III — Linear models and supervised learning

## 9. Linear regression

### Model and objective

Univariate: `ŷ=w₀+w₁x`. Multivariate with intercept column: `ŷ=Xw`.

Ordinary least squares minimizes

`J(w)=(1/2n)||Xw-y||²`.

Gradient:

`∇J(w)=(1/n)Xᵀ(Xw-y)`.

### Closed-form derivation

Set the gradient to zero:

`Xᵀ(Xw-y)=0 → XᵀXw=Xᵀy → ŵ=(XᵀX)⁻¹Xᵀy`, if `XᵀX` is invertible.

In practice use QR/SVD or pseudoinverse instead of explicitly forming an inverse; they are numerically safer and handle rank deficiency. With ridge regression:

`ŵ=(XᵀX+λI)⁻¹Xᵀy` (usually do not penalize the intercept).

For one feature:

`w₁=Σ(x_i-x̄)(y_i-ȳ)/Σ(x_i-x̄)² = Cov(x,y)/Var(x)`, and `w₀=ȳ-w₁x̄`.

### Gradient descent

```python
import numpy as np

def linear_regression_gd(X, y, lr=0.05, epochs=2000):
    X = np.c_[np.ones(len(X)), X]       # intercept
    w = np.zeros(X.shape[1])
    for _ in range(epochs):
        error = X @ w - y
        grad = X.T @ error / len(X)
        w -= lr * grad
    return w
```

Complexity per full-batch step is `O(nd)` for `n×d` data; storing `X` is `O(nd)`. Solving normal equations naïvely is roughly `O(nd²+d³)` and can be unsuitable for high dimension.

### Assumptions and traps

For prediction, a linear conditional-mean approximation may be useful without perfect classical assumptions. For unbiased/valid classical coefficient inference, discuss linear specification, independent zero-mean errors conditional on features, no perfect multicollinearity, and often homoscedasticity/normality for particular standard-error tests. Correlation or a fitted coefficient does not prove causation.

## 10. Perceptron

Binary labels `y∈{-1,+1}`; score `s=wᵀx+b`; predict `sign(s)`. For a misclassified example (`y(wᵀx+b)≤0`):

`w←w+ηyx`, `b←b+ηy`.

```python
def perceptron(X, y, lr=1.0, epochs=20):
    w = [0.0] * len(X[0]); b = 0.0
    for _ in range(epochs):
        for xi, yi in zip(X, y):
            if yi * (sum(a*z for a, z in zip(w, xi)) + b) <= 0:
                w = [a + lr*yi*z for a, z in zip(w, xi)]
                b += lr*yi
    return w, b
```

Perceptron convergence is guaranteed in finitely many mistakes if data are linearly separable with a positive margin under the theorem's assumptions. It does not output calibrated probabilities and may cycle on nonseparable data.

## 11. Logistic regression

`z=wᵀx+b`, `σ(z)=1/(1+e^{-z})`, `p(y=1|x)=σ(z)`.

Taking odds gives `p/(1-p)=e^z`; therefore log-odds `log[p/(1-p)]=wᵀx+b`. The decision boundary at threshold `0.5` is `wᵀx+b=0`.

Bernoulli likelihood is `Π_i p_i^{y_i}(1-p_i)^{1-y_i}`. Negative log-likelihood/binary cross-entropy:

`J=-Σ_i[y_i log p_i+(1-y_i)log(1-p_i)]`.

Because `dσ/dz=σ(1-σ)`, the derivative with respect to the logit simplifies to `p-y`; hence:

`∇_w J = Xᵀ(p-y)` (divide by `n` if using mean loss).

```python
import numpy as np

def sigmoid(z):
    z = np.clip(z, -40, 40)
    return 1 / (1 + np.exp(-z))

def logistic_regression_gd(X, y, lr=0.1, epochs=2000, l2=0.0):
    X = np.c_[np.ones(len(X)), X]
    w = np.zeros(X.shape[1])
    for _ in range(epochs):
        p = sigmoid(X @ w)
        reg = np.r_[0.0, w[1:]]       # no intercept penalty
        w -= lr * ((X.T @ (p-y))/len(X) + l2*reg)
    return w
```

Despite its name, it is a classification model. Its boundary is linear in the supplied features but nonlinear feature maps can create nonlinear boundaries. Choose the probability threshold based on validation costs; `0.5` is not sacred.

### Perceptron vs logistic regression

| Perceptron | Logistic regression |
|---|---|
| mistake-driven update | smooth likelihood/log-loss optimization |
| hard class score | probability model |
| separability convergence theorem | convex objective under standard setup |
| no calibrated probability | probabilities can be calibrated but must be checked |

## 12. Multiclass softmax and cross-entropy

For logits `z_k`,

`p_k=exp(z_k)/Σ_j exp(z_j)`.

For numerical stability compute `exp(z_k-max(z))`. With one-hot target `y`, categorical cross-entropy is `L=-Σ_k y_k log p_k=-log p_true`. The crucial derivative is:

`∂L/∂z_k=p_k-y_k`.

Softmax is invariant to adding the same constant to every logit. For mutually exclusive classes use one softmax; for independent multilabel targets use one sigmoid+BCE per label.

## 13. k-nearest neighbors

Store examples. For a query, compute distances, choose the `k` closest, then majority vote (classification) or average (regression). Training cost is essentially storage; naïve query cost is `O(nd)` plus neighbor selection (`O(n log k)` with a heap or `O(n)` selection). Scale features. Small `k` is flexible/high variance; large `k` smooths/high bias. High dimensions cause distance concentration; a meaningful metric and representation are essential.

## 14. Support vector machine

For separable data, choose the maximum-margin hyperplane. Soft-margin primal:

`min_(w,b,ξ) 1/2||w||² + CΣξ_i`

subject to `y_i(wᵀx_i+b)≥1-ξ_i`, `ξ_i≥0`.

Equivalent hinge loss is `max(0,1-yf(x))`. Only support vectors determine the boundary. A kernel computes `K(x,z)=φ(x)ᵀφ(z)` without explicitly constructing `φ`; RBF is `exp(-γ||x-z||²)`. `C` trades margin against violations; `γ` controls RBF locality. Scale inputs. Raw SVM scores are not calibrated probabilities.

---

# Part IV — Trees and ensembles

## 15. Decision trees

A tree recursively chooses a feature/test that most reduces impurity. It produces interpretable axis-aligned regions, captures nonlinear interactions, and needs little scaling; deep trees are unstable/high variance.

### Entropy and information gain

For class proportions `p_k`:

`H(S)=-Σ_k p_k log₂p_k`.

For Boolean proportion `q`, `B(q)=-qlog₂q-(1-q)log₂(1-q)`, with `0log0=0`. Entropy is `0` for a pure node and `1` for a 50/50 binary node.

For split `A` with children `S_v`:

`Remainder(A)=Σ_v |S_v|/|S| · H(S_v)`

`Gain(S,A)=H(S)-Remainder(A)`.

**Worked split:** parent has 6 positive, 4 negative: `H≈0.971`. A split gives left `(4+,0-)` of size 4 and right `(2+,4-)` of size 6. Weighted child entropy=`0.4·0+0.6·H(1/3,2/3)≈0.6·0.918=0.551`; gain=`0.420` bits.

Gini impurity is `1-Σp_k²`; CART commonly chooses binary splits using Gini for classification and squared-error reduction for regression.

### Continuous feature

Sort unique feature values; candidate thresholds lie between adjacent values (often only where labels change). Evaluate impurity decrease and choose the best. A straightforward scan after sorting is `O(n log n)` per feature; cumulative counts make threshold evaluation linear after sorting.

### Stopping and pruning

Stop by max depth, min samples, min impurity decrease, or purity. **Pre-pruning** stops early. **Post-pruning** first grows then removes branches whose validation/cost-complexity benefit is insufficient. Pruning trades a little training fit for lower variance/generalization.

```python
from math import log2

def entropy(labels):
    n = len(labels)
    counts = {c: labels.count(c) for c in set(labels)}
    return -sum((m/n)*log2(m/n) for m in counts.values())

def information_gain(parent, children):
    n = len(parent)
    return entropy(parent) - sum(len(c)/n * entropy(c) for c in children if c)
```

### ID3/C4.5/CART recall

- ID3: categorical splits, information gain.
- C4.5: gain ratio, continuous/missing handling, pruning.
- CART: binary tree; Gini classification or squared-error regression; cost-complexity pruning.

## 16. Bagging and random forest

**Bagging:** draw bootstrap samples, train learners independently, average/vote. Bootstrap means sampling `n` points with replacement; roughly `1-e^{-1}≈63.2%` unique examples appear in one sample. Out-of-bag examples can estimate error.

**Random forest:** bagged decision trees plus a random subset of features considered at each split. Feature randomness decorrelates trees, making averaging reduce variance more effectively. Trees can train in parallel. Classification votes; regression averages.

Viva contrast: bagging mainly stabilizes an unstable learner and reduces variance; it does not sequentially correct earlier learners.

## 17. AdaBoost

For binary labels `y_i∈{-1,+1}`:

1. Initialize sample weights `w_i=1/n`.
2. Train weak learner `h_t` using weights.
3. Weighted error `ε_t=Σ_i w_i [h_t(x_i)≠y_i]`.
4. Learner weight `α_t=1/2 ln((1-ε_t)/ε_t)`.
5. Update `w_i←w_i exp(-α_t y_i h_t(x_i))`; normalize.
6. Predict `sign(Σ_t α_t h_t(x))`.

Misclassified examples have `y_i h_t=-1`, so their weights multiply by `e^{α_t}`; correctly classified weights multiply by `e^{-α_t}`. If `ε_t=0.5`, `α_t=0` (no value); if error exceeds `0.5`, the learner is worse than random unless reversed. AdaBoost is sensitive to mislabeled/outlier points because their weights may grow.

```text
AdaBoost(D,T):
    w[i] = 1/n
    for t = 1..T:
        fit h_t using w
        err = sum_i w[i] * I(h_t(x_i) != y_i)
        alpha[t] = 0.5 * ln((1-err)/err)
        w[i] *= exp(-alpha[t] * y_i * h_t(x_i))
        normalize w
    return sign(sum_t alpha[t] h_t(x))
```

## 18. Gradient boosting

Gradient boosting builds an additive model `F_m(x)=F_(m-1)(x)+ηh_m(x)` by fitting each new weak learner to the **negative gradient** of the loss with respect to current predictions.

### Squared-error regression

Negative gradient is residual `r_i=y_i-F_(m-1)(x_i)`. Initialize with mean target. Fit a regression tree to residuals, then add its leaf outputs multiplied by learning rate.

Slide-style worked start: for targets whose mean is `71.2`, set every initial prediction to `71.2`. Residuals are `y_i-71.2`. A small tree groups similar residuals; if a sample's leaf predicts `18.8` and `η=.1`, new prediction is `71.2+.1(18.8)=73.08`. Repeat on new residuals.

### Binary log-loss classification

Initialize log-odds `F₀=log(p/(1-p))`, where `p` is positive fraction. Current probability is `p_i=σ(F(x_i))`. Pseudo-residual is `y_i-p_i`. Fit a tree; a Newton-style leaf value is approximately:

`γ_leaf = Σ_(i in leaf)(y_i-p_i) / Σ_(i in leaf)p_i(1-p_i)`.

Update logit `F←F+ηγ`, then convert with sigmoid. Do not average probabilities directly during additive logit boosting.

```python
# Conceptual squared-error gradient boosting
F = np.full(len(y), y.mean())
models = []
for _ in range(M):
    residual = y - F
    tree = SmallRegressionTree().fit(X, residual)
    F += learning_rate * tree.predict(X)
    models.append(tree)
```

Small learning rate usually needs more trees. Depth controls interactions. Early stopping and subsampling regularize. Unlike bagging, boosting is sequential and primarily reduces residual bias, though it can overfit/noise-chase.

## 19. Stacking

Train diverse base learners, then train a meta-learner on their predictions. To avoid leakage, the meta-learner must see **out-of-fold** base predictions for training examples. At inference, fit base models on all training data, obtain their predictions, and feed them to the meta-model. Simple voting/averaging has no learned meta-model.

---

# Part V — Neural networks and optimization

## 20. Neuron, MLP, and representation learning

A neuron computes `z=wᵀx+b`, then activation `a=φ(z)`. A feedforward network composes layers:

`a^(l)=φ(W^(l)a^(l-1)+b^(l))`.

Without nonlinear activations, stacked affine layers collapse into one affine transformation: `W₂(W₁x+b₁)+b₂=(W₂W₁)x+(W₂b₁+b₂)`. Depth becomes expressive because nonlinearities allow hierarchical representations.

### Activations

| Activation | Formula | Range | Strength / problem |
|---|---|---|---|
| sigmoid | `1/(1+e^-z)` | `(0,1)` | binary output; saturates, not zero-centered |
| tanh | `(e^z-e^-z)/(e^z+e^-z)` | `(-1,1)` | zero-centered; still saturates |
| ReLU | `max(0,z)` | `[0,∞)` | cheap, good gradient for `z>0`; dead neurons |
| Leaky ReLU | `max(αz,z)` | real | retains small negative gradient |
| GELU | `zΦ(z)` | real | smooth gating, common in Transformers |
| SiLU/Swish | `zσ(z)` | real | smooth, non-monotonic region |

Sigmoid derivative is `σ(z)(1-σ(z))`; tanh derivative is `1-tanh²(z)`; ReLU derivative is `1` for positive and `0` for negative input (choose a subgradient convention at zero).

The universal approximation theorem says a sufficiently wide network with a suitable nonlinearity can approximate broad classes of continuous functions on compact domains. It does not say training will find that approximation, it will generalize, or one hidden layer is efficient.

### Feedforward vs recurrent network

A feedforward network's graph is acyclic for one example. An RNN reuses parameters over sequence steps:

`h_t=φ(W_xh x_t + W_hh h_(t-1)+b_h)`, `y_t=g(W_hy h_t+b_y)`.

The hidden state summarizes past input; sharing lets variable-length sequences be processed. Training unrolls the graph and applies backpropagation through time (BPTT). Sequential recurrence limits parallelism and repeated Jacobians cause vanishing/exploding gradients. LSTM/GRU gates provide additive memory/update paths and learn when to retain/forget information. Transformers replace recurrent token processing with parallel attention during training, though autoregressive generation remains sequential.

## 21. Computation graph and backpropagation

Backpropagation is reverse-mode differentiation: it reuses intermediate derivatives to compute gradients of a scalar loss with respect to many parameters efficiently. It computes gradients; SGD/Adam are optimizers that use them.

### Worked scalar graph

Let `z=wx+b`, `a=ReLU(z)`, `ŷ=va+c`, `L=1/2(ŷ-y)²`.

Starting from `∂L/∂ŷ=ŷ-y`:

- `∂L/∂v=(ŷ-y)a`
- `∂L/∂c=ŷ-y`
- `∂L/∂a=(ŷ-y)v`
- `∂L/∂z=(ŷ-y)v·I[z>0]`
- `∂L/∂w=(ŷ-y)v·I[z>0]·x`
- `∂L/∂b=(ŷ-y)v·I[z>0]`

For a matrix layer `Z=XW+b`, upstream gradient `G=∂L/∂Z`:

`∂L/∂W=XᵀG`, `∂L/∂X=GWᵀ`, `∂L/∂b=Σ_rows G`.

### Minimal PyTorch MLP

```python
import torch
from torch import nn

model = nn.Sequential(
    nn.Linear(d_in, 128),
    nn.ReLU(),
    nn.Dropout(0.2),
    nn.Linear(128, n_classes)
)

optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.CrossEntropyLoss()  # expects raw logits and integer labels

for xb, yb in loader:
    optimizer.zero_grad()
    logits = model(xb)
    loss = criterion(logits, yb)
    loss.backward()
    optimizer.step()
```

Do not apply softmax before `CrossEntropyLoss`; it internally combines log-softmax and negative log-likelihood stably.

## 22. Vanishing/exploding gradients and initialization

Backprop multiplies many Jacobians. Products of factors mostly below one vanish; above one explode. Saturating sigmoid/tanh, long recurrent chains, and poor initialization worsen the problem.

Remedies: ReLU-like activations, Xavier/He initialization, normalization, residual/skip connections, gating, gradient clipping (controls explosions, especially RNNs), and suitable depth/learning rate.

### Xavier/Glorot derivation recall

For `z_j=Σ_i w_ij x_i`, independent zero-mean terms give approximately

`Var(z)=n_in Var(w) Var(x)`.

Preserving forward variance suggests `Var(w)≈1/n_in`; preserving backward variance suggests `1/n_out`. Xavier compromises:

`Var(w)=2/(n_in+n_out)`.

- Xavier normal standard deviation: `sqrt(2/(n_in+n_out))`.
- Xavier uniform: `w~U[-sqrt(6/(n_in+n_out)), +sqrt(6/(n_in+n_out))]`.

For ReLU, roughly half the activations are zero, motivating He initialization `Var(w)=2/n_in`; normal std `sqrt(2/n_in)`.

## 23. Batch normalization, layer normalization, and dropout

### Batch normalization

For a mini-batch feature/channel:

`μ_B=(1/m)Σ_i x_i`, `σ_B²=(1/m)Σ_i(x_i-μ_B)²`

`x̂_i=(x_i-μ_B)/sqrt(σ_B²+ε)`, `y_i=γx̂_i+β`.

`γ,β` are learned. During training use mini-batch statistics; at inference use running estimates accumulated during training—not a newly computed “entire test-dataset mean.” In CNNs BN normally computes each channel's statistics across batch and spatial positions. Batch composition affects it, especially with tiny/correlated batches.

### Layer normalization

LN performs the same standardize-then-affine idea across features of each individual observation/token. It does not depend on other batch members and uses the same rule at train and inference, making it suitable for variable batches and Transformers.

### Slide mini-batch calculation

For rows `[7,2,3]`, `[2,-4,-1]`, `[-5,2,2]`, `[3,3,-3]`:

- BN per-feature means are `[1.75, 0.75, 0.25]`.
- Population variances are `[18.6875, 7.6875, 5.6875]`.
- Each BN value is `(x_j-mean_j)/sqrt(var_j+ε)` before learned `γ,β`.

LN works row-by-row:

- `[7,2,3]`: mean `4`, variance `14/3`.
- `[2,-4,-1]`: mean `-1`, variance `6`.
- `[-5,2,2]`: mean `-1/3`, variance `98/9≈10.889`.
- `[3,3,-3]`: mean `1`, variance `8`.

Then standardize the three values in each row. BN and LN are not interchangeable just because both normalize.

### Dropout

With drop probability `p`, **inverted dropout** during training is

`h'=0` with probability `p`, otherwise `h'=h/(1-p)`.

Therefore `E[h']=h`; inference uses the full activation with no random mask. Dropout discourages fragile co-adaptation and acts as stochastic regularization. It is not normally active during deterministic inference.

## 24. Optimization algorithms

Let `g_t=∇_θL_t(θ_t)`.

### Batch, stochastic, and mini-batch gradient descent

- Batch GD uses all examples per step: accurate/stable but costly.
- SGD uses one example: cheap, noisy, may escape shallow traps but has high variance.
- Mini-batch uses a vectorized subset: standard compromise and GPU-friendly.

Shuffle ordinary IID training data each epoch; do not violate temporal/group structure when it matters. Learning rate too high diverges/oscillates; too low is slow. Batch size changes gradient noise and effective optimization, so learning-rate retuning may be necessary.

### Momentum and Nesterov

One convention:

`v_t=βv_(t-1)+g_t`, `θ_(t+1)=θ_t-ηv_t`.

Momentum smooths noisy gradients and accelerates persistent directions. Nesterov computes the gradient after a look-ahead step, approximately `g(θ_t-ηβv_(t-1))`, allowing earlier correction.

### AdaGrad

`r_t=r_(t-1)+g_t⊙g_t`

`θ←θ-η g_t/(sqrt(r_t)+ε)`.

Rarely updated features get larger effective steps, useful for sparse data; the accumulator only grows, so learning may stop too early.

### RMSProp and AdaDelta

RMSProp uses an exponential moving average:

`r_t=ρr_(t-1)+(1-ρ)g_t²`, `θ←θ-ηg_t/(sqrt(r_t)+ε)`.

AdaDelta also tracks a moving average of squared updates, reducing dependence on a manually chosen global learning-rate scale.

### Adam

`m_t=β₁m_(t-1)+(1-β₁)g_t`

`v_t=β₂v_(t-1)+(1-β₂)g_t²`

Bias correction: `m̂_t=m_t/(1-β₁^t)`, `v̂_t=v_t/(1-β₂^t)`.

`θ←θ-η m̂_t/(sqrt(v̂_t)+ε)`.

Adam combines momentum-like first moment and RMSProp-like second moment. AdaMax uses the infinity norm; Nadam adds Nesterov-style momentum. AdamW decouples weight decay from Adam's adaptive gradient update and is usually the intended neural-network weight decay.

### Practical training controls

- Learning-rate schedules: step, cosine decay, warmup, reduce-on-plateau.
- Early stopping: monitor validation metric, keep best checkpoint, use patience.
- Gradient clipping: clip norm/value to prevent explosion; it does not solve all vanishing-gradient causes.
- Curriculum learning orders easy-to-hard examples; it encodes a training assumption and is not always beneficial.
- Adding gradient noise can regularize/explore but needs tuning.

### Distributed SGD ideas from the slides

- **Hogwild!:** workers asynchronously update shared parameters without locks; fast for sparse conflicts, but stale/racing updates.
- **Downpour SGD:** distributed workers compute/update parameter servers asynchronously; tolerates slow workers but gradients may be stale.
- **Synchronous data parallelism:** all-reduce/aggregate gradients then perform the same update; consistent but waits for stragglers.
- **Elastic Averaging SGD:** local workers explore while an elastic penalty pulls them toward a center parameter vector.

## 25. Online learning

Online learning updates as data arrive instead of repeatedly fitting a fixed batch. It suits streams and distribution change but requires drift monitoring, stable update rates, and protection against catastrophic changes. An online mistake/regret guarantee is different from an IID generalization guarantee.

---

# Part VI — Convolutional neural networks and computer vision

## 26. Why CNN instead of flattening an image?

An image is a tensor, usually `(batch,channels,height,width)` in PyTorch. Flattening `224×224×3` gives 150,528 numbers and destroys explicit neighborhood layout. A dense layer then needs separate weights for the same edge at every position.

CNN inductive biases:

- **local connectivity:** early filters see nearby pixels;
- **weight sharing:** one detector scans all locations;
- **translation equivariance:** shifting input shifts the feature map;
- pooling/global aggregation can give approximate **translation invariance** in the final decision;
- deeper layers combine edges/textures into parts and objects with a larger receptive field.

Do not say convolution itself is strictly translation invariant; it is primarily equivariant, with boundary/stride caveats.

## 27. Convolution/cross-correlation

Deep-learning libraries usually compute cross-correlation without flipping the learned kernel:

`Y[i,j]=b+Σ_aΣ_b X[i+a,j+b]K[a,b]`.

Because the kernel is learned, calling it convolution is conventional.

Slide calculation using input

```text
0 1 2
3 4 5
6 7 8
```

and kernel

```text
0 1
2 3
```

produces `[[19,25],[37,43]]`, e.g. `0·0+1·1+3·2+4·3=19`.

```python
import torch

def conv2d_valid(X, K):
    kh, kw = K.shape
    Y = torch.zeros(X.shape[0]-kh+1, X.shape[1]-kw+1)
    for i in range(Y.shape[0]):
        for j in range(Y.shape[1]):
            Y[i, j] = (X[i:i+kh, j:j+kw] * K).sum()
    return Y
```

### Output shape

For one dimension with input `n`, padding on each side `p`, kernel `k`, dilation `d`, stride `s`:

`out=floor((n+2p-d(k-1)-1)/s)+1`.

If `d=1`, this becomes `floor((n+2p-k)/s)+1`. “Same” stride-1 odd-k padding uses `p=(k-1)/2`; “valid” uses `p=0`.

### Channels and parameter count

Kernel tensor shape is `(C_out,C_in,K_h,K_w)`. Each output filter spans every input channel; one filter yields one output channel.

Parameters=`C_out(C_in K_h K_w + 1)` with one bias per output channel. It is independent of input image height/width. Doubling both input and output channels of an internal conv approximately **quadruples**, not doubles, kernel weights.

Compute (multiply-add scale) is approximately `H_out W_out C_out C_in K_h K_w` per example.

### Backpropagation through convolution

For upstream `G[i,j]=∂L/∂Y[i,j]`:

`∂L/∂K[a,b]=Σ_iΣ_j G[i,j]X[i+a,j+b]`

`∂L/∂X[u,v]=Σ_(i,j,a,b: u=i+a,v=j+b) G[i,j]K[a,b]`

`∂L/∂b=Σ_iΣ_jG[i,j]`.

Input gradients accumulate wherever sliding windows overlap. Autograd performs these operations, but the chain-rule meaning remains important.

## 28. Padding, stride, pooling, and receptive field

- Padding controls edge utilization and output size; zero/reflect/replicate padding encode different boundary assumptions.
- Stride skips positions and downsamples; aliasing can occur if high frequencies are not controlled.
- Max pooling chooses local maximum; average pooling averages. Pooling has no learned kernel weights.
- Pooling reduces spatial cost and sensitivity to small shifts but loses precise location.

Receptive field recursion: let jump `j₀=1`, receptive field `r₀=1`. For layer `l` with stride `s_l`, dilation `d_l`, kernel `k_l`:

`j_l=j_(l-1)s_l`

`r_l=r_(l-1)+(k_l-1)d_l j_(l-1)`.

Thus deeper units see larger effective input regions.

## 29. LeNet worked shape and parameter calculation

For `1×28×28` input:

1. Conv `1→6`, `5×5`, padding 2: output `6×28×28`; params `6(1·25+1)=156`.
2. Average pool `2×2`, stride 2: `6×14×14`; no parameters.
3. Conv `6→16`, `5×5`, no padding: `16×10×10`; params `16(6·25+1)=2,416`.
4. Pool `2×2`: `16×5×5`.
5. Flatten: `400`.
6. FC `400→120`: `400·120+120=48,120`.
7. FC `120→84`: `120·84+84=10,164`.
8. FC `84→10`: `84·10+10=850`.

Total including biases=`61,706`. If a handwritten calculation excludes some/all biases, state that convention explicitly; the architecture and bias-inclusive count above are internally consistent.

```python
class LeNet(nn.Module):
    def __init__(self, n_classes=10):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(1, 6, 5, padding=2), nn.Sigmoid(),
            nn.AvgPool2d(2, 2),
            nn.Conv2d(6, 16, 5), nn.Sigmoid(),
            nn.AvgPool2d(2, 2), nn.Flatten(),
            nn.Linear(400, 120), nn.Sigmoid(),
            nn.Linear(120, 84), nn.Sigmoid(),
            nn.Linear(84, n_classes)
        )
    def forward(self, x): return self.net(x)
```

## 30. Architecture evolution

### AlexNet

Modern breakthrough on ImageNet: deeper/larger than LeNet, ReLU, max pooling, dropout, data augmentation, GPU training. The missing historical ingredients were sufficiently large labeled data (ImageNet) and compute (GPUs). It demonstrated learned features beating hand-engineered pipelines.

### VGG

Uses repeated small `3×3` convolutions and periodic pooling in a simple uniform stack. Two `3×3` layers have a `5×5` receptive field with more nonlinearities and often fewer parameters than one dense `5×5` mapping. Weakness: very high compute/parameter cost, especially original fully connected heads.

### Network in Network (NiN)

Uses `1×1` convolutions as learned channel mixing at each location and global average pooling instead of huge FC heads. A `1×1` conv is a shared per-pixel fully connected transformation across channels.

```python
def nin_block(cin, cout, kernel, stride, padding):
    return nn.Sequential(
        nn.Conv2d(cin, cout, kernel, stride, padding), nn.ReLU(),
        nn.Conv2d(cout, cout, 1), nn.ReLU(),
        nn.Conv2d(cout, cout, 1), nn.ReLU()
    )
```

### Inception/GoogLeNet

Parallel branches use `1×1`, `3×3`, `5×5`, and pooling to capture multiple scales, then concatenate channels. `1×1` bottlenecks reduce channels before expensive kernels. GoogLeNet stacks Inception blocks and reduces reliance on massive FC layers.

### ResNet

A residual block computes `y=F(x)+x`. Instead of learning desired mapping `H(x)` directly, residual branch learns `F(x)=H(x)-x`; identity is easy when `F≈0`. The skip path gives a direct gradient route and makes very deep optimization easier. If shape changes, a projection `1×1` convolution (possibly strided) maps `x` to the required dimensions. A skip connection helps gradients but is not literally “no transformation anywhere.”

### DenseNet

Layer `l` receives concatenation `[x₀,x₁,...,x_(l-1)]`, promoting feature reuse and gradient flow. Unlike ResNet's addition, DenseNet concatenates, so channels grow by a **growth rate**; transition layers compress/downsample. Cost is memory/concatenation overhead.

## 31. Augmentation and transfer learning

Augmentation creates label-preserving variants: crop, flip, color jitter, small rotation, noise, mixup/cutmix when appropriate. It expands effective support and encodes invariance. A transformation is harmful if it changes the label (mirroring text, laterality, direction-sensitive diagrams).

Fine-tuning procedure:

1. Load a model pretrained on a source dataset.
2. Replace final head for target classes.
3. Optionally freeze backbone and train head.
4. Unfreeze some/all backbone; use a smaller learning rate.
5. Preserve required input normalization and validate domain shift.

```python
from torchvision.models import resnet18, ResNet18_Weights
net = resnet18(weights=ResNet18_Weights.DEFAULT)
net.fc = nn.Linear(net.fc.in_features, num_classes)
```

Fine-tuning is transfer learning; training only a frozen head is feature extraction. A large source–target domain gap can limit or reverse transfer benefit.

## 32. Semantic segmentation and transposed convolution

Semantic segmentation assigns a class to every pixel. Output logits often have shape `(B,C,H,W)`. Summing/averaging cross-entropy across pixels is a valid loss, with class weighting/IoU-aware losses useful under imbalance.

A fully convolutional network replaces dense classification heads with spatial convolutional prediction and upsamples coarse feature maps. U-Net uses an encoder–decoder plus same-scale skip **concatenations** so the decoder recovers fine localization while retaining semantic context.

### Transposed convolution

A normal convolution can be represented as matrix multiplication `y=Kx`. A transposed convolution applies `Kᵀ` to its input; this explains the name. It is a learned upsampling operator, not generally the mathematical inverse of convolution and not guaranteed to reconstruct the original values.

Output size:

`out=(n-1)s-2p+d(k-1)+output_padding+1`.

Stride greater than one expands spatial positions (conceptually inserts gaps/zeros before filtering); padding removes/crops boundary contribution according to the formula. Uneven overlap can create checkerboard artifacts; resize-then-convolve is an alternative.

```python
up = nn.ConvTranspose2d(
    in_channels=64, out_channels=32,
    kernel_size=4, stride=2, padding=1
)  # doubles H,W
```

### CNN viva traps from the class test

- Conv parameter count independent of input height/width: **true**.
- Doubling every channel always doubles parameters: **false**; internal kernel products often scale about fourfold.
- ResNet skip gives a direct gradient route: **true**, with projection caveat when shapes differ.
- Sum/mean pixelwise cross-entropy is valid for segmentation: **true**.

---

# Part VII — Probability, Bayesian learning, clustering, and EM

## 33. Probability essentials

- Joint: `P(A,B)=P(A∩B)`.
- Conditional: `P(A|B)=P(A,B)/P(B)` when `P(B)>0`.
- Product rule: `P(A,B)=P(A|B)P(B)=P(B|A)P(A)`.
- Marginalization: `P(A)=Σ_b P(A,b)` for discrete `B` (integrate for continuous).
- Total probability: if `{B_i}` partitions the space, `P(A)=Σ_iP(A|B_i)P(B_i)`.
- Bayes rule: `P(B|A)=P(A|B)P(B)/P(A)`.

Independence `A⊥B` means `P(A,B)=P(A)P(B)`. Conditional independence `A⊥B|C` means `P(A,B|C)=P(A|C)P(B|C)`; variables can be dependent marginally but independent after conditioning, or the reverse (collider effect).

For densities, a density value may exceed 1; probabilities are integrals/areas and remain at most 1.

### Bayes numerical example

Suppose disease prevalence is 1%, sensitivity 90%, and specificity 95%. For a positive test:

`P(D|+) = .90·.01 / [.90·.01 + .05·.99] = .009/.0585 ≈ .154`.

Even a decent test yields only about 15.4% posterior probability because false positives come from the much larger healthy population. This demonstrates the base-rate effect.

## 34. Maximum likelihood, MAP, and Bayesian learning

For parameters `θ` and data `D`:

- Likelihood: `p(D|θ)` viewed as a function of `θ`.
- MLE: `θ_ML=argmax_θ p(D|θ)=argmax log p(D|θ)`.
- Posterior: `p(θ|D)∝p(D|θ)p(θ)`.
- MAP: `θ_MAP=argmax[log p(D|θ)+log p(θ)]`.
- Full Bayesian prediction integrates uncertainty: `p(y*|x*,D)=∫p(y*|x*,θ)p(θ|D)dθ`.

MLE is MAP under a uniform prior (where meaningful). A Gaussian prior on weights corresponds to an L2-style penalty; a Laplace prior corresponds to L1. MAP returns a point estimate, not the whole posterior.

### Bernoulli MLE

For `N` coin flips, `c` heads:

`L(θ)=θ^c(1-θ)^(N-c)`.

`ℓ=c logθ+(N-c)log(1-θ)`; set derivative `c/θ-(N-c)/(1-θ)=0`, giving `θ̂_ML=c/N`.

### Gaussian MLE

For IID scalar data, MLE mean is `μ̂=(1/N)Σx_i`; MLE variance is `σ̂²=(1/N)Σ(x_i-μ̂)²`. The unbiased sample variance uses `1/(N-1)` and serves a different objective.

### Beta–Bernoulli conjugacy

Prior `θ~Beta(a,b)` has density proportional to `θ^(a-1)(1-θ)^(b-1)`. After `c` successes and `N-c` failures:

`θ|D~Beta(a+c,b+N-c)`.

Posterior mean=`(a+c)/(a+b+N)`; MAP, when both posterior shape parameters exceed 1, is `(a+c-1)/(a+b+N-2)`. `a,b` act like prior pseudo-counts, but their interpretation should match the prior construction.

## 35. Bayesian networks

A Bayesian network is a directed acyclic graph whose nodes are random variables and whose edges encode a factorization:

`P(x₁,...,x_n)=Π_i P(x_i | Parents(X_i))`.

The local Markov property says a node is conditionally independent of its non-descendants given its parents. A node's **Markov blanket**—parents, children, and its children's other parents—makes it conditionally independent of every other node.

In the classic burglary–earthquake–alarm network with alarm causing two calls, a complete assignment probability is the product of the five relevant conditional-table entries. The slide example multiplies `0.90·0.70·0.01·0.999·0.998≈0.00628`.

### d-separation intuition

- Chain `A→B→C`: conditioning on `B` blocks the path.
- Fork `A←B→C`: conditioning on common cause `B` blocks it.
- Collider `A→B←C`: path is blocked without conditioning; conditioning on `B` or a descendant can open it (“explaining away”).

Exact inference by enumeration/variable elimination can be exponential in graph structure/treewidth; a compact factorization is not automatically cheap inference.

## 36. Naive Bayes

Assume features are conditionally independent given class:

`P(y|x₁,...,x_d) ∝ P(y)Π_jP(x_j|y)`.

Predict the class with largest log score:

`logP(y)+Σ_jlogP(x_j|y)`.

Use logs to avoid underflow. Variants:

- Gaussian NB for continuous conditionally Gaussian features;
- Multinomial NB for counts such as word frequency;
- Bernoulli NB for binary feature presence.

Laplace/add-`α` smoothing prevents unseen categories from making the entire product zero: `(count+α)/(total+αK)`. Conditional independence is often false, yet decision boundaries can still work because accurate joint probability estimation is not necessary for correct class ranking.

## 37. Gaussian mixture model

A `K`-component GMM density is

`p(x)=Σ_(k=1)^K π_k N(x|μ_k,Σ_k)`, with `π_k≥0`, `Σπ_k=1`.

It is soft/probabilistic clustering. A latent one-hot component `z` chooses a Gaussian. Covariance choice controls shape: spherical, diagonal, tied, or full. Full covariance is expressive but parameter-heavy and may become singular.

## 38. Expectation–maximization for GMM

Direct likelihood contains `log Σ_k`, making component assignments coupled. EM alternates:

### E-step: responsibilities

`r_ik=P(z_i=k|x_i)=π_k N(x_i|μ_k,Σ_k) / Σ_j π_jN(x_i|μ_j,Σ_j)`.

### M-step

`N_k=Σ_i r_ik`

`μ_k=(1/N_k)Σ_i r_ik x_i`

`Σ_k=(1/N_k)Σ_i r_ik(x_i-μ_k)(x_i-μ_k)ᵀ`

`π_k=N_k/N`.

```python
# conceptual GMM-EM
for _ in range(max_iter):
    weighted = [pi[k] * gaussian_pdf(X, mu[k], cov[k]) for k in range(K)]
    R = np.stack(weighted, axis=1)
    R /= R.sum(axis=1, keepdims=True)             # E-step
    Nk = R.sum(axis=0)
    pi = Nk / len(X)
    mu = (R.T @ X) / Nk[:, None]
    for k in range(K):
        D = X - mu[k]
        cov[k] = (D.T * R[:, k]) @ D / Nk[k] + 1e-6*np.eye(X.shape[1])
```

EM alternates computing the expected complete-data log likelihood and maximizing it. Observed-data likelihood does not decrease, but EM can reach a local optimum/saddle and is initialization-sensitive. Regularize covariance, use multiple starts, and monitor log likelihood.

### Slide coin-mixture EM calculation

Five length-10 sequences have head fractions `(0.4,0.9,0.8,0.3,0.7)`. A hidden variable says whether coin A or B generated each sequence; unknown parameters are head biases `θ_A,θ_B`. Begin `θ_A=.60`, `θ_B=.82`.

For the fifth sequence (7 heads, 3 tails), likelihoods (the common binomial coefficient cancels during normalization) are:

- A: `.60^7·.40^3≈.00179`;
- B: `.82^7·.18^3≈.00145`.

Normalize to responsibilities about `(0.55,0.45)`. Across all five sequences, the slide E-step obtains A-responsibilities `[.97,.12,.29,.99,.55]` and B-responsibilities `[.03,.88,.71,.01,.45]`. M-step uses expected heads divided by expected flips:

`θ_A=(.97·.4+.12·.9+.29·.8+.99·.3+.55·.7)/(.97+.12+.29+.99+.55)≈.483`

`θ_B=(.03·.4+.88·.9+.71·.8+.01·.3+.45·.7)/(.03+.88+.71+.01+.45)≈.813`.

Here fractions can be used because every sequence has the same 10 flips; the factor 10 cancels. Iterate E/M until stable.

### General EM pattern

When latent variables `Z` make complete data easier:

1. E-step: `Q(θ|θ_old)=E_(Z|X,θ_old)[log p(X,Z|θ)]`.
2. M-step: `θ_new=argmax_θ Q(θ|θ_old)`.

## 39. K-means and Lloyd's algorithm

Objective:

`J=Σ_i ||x_i-μ_(c_i)||²`.

Algorithm:

1. initialize `K` centroids;
2. assign each point to nearest centroid;
3. replace each centroid by mean of assigned points;
4. repeat until assignments/objective stabilize.

Why the mean? For one cluster, differentiating `Σ_i||x_i-μ||²` with respect to `μ` gives `2Σ(μ-x_i)=0`, so `μ` is the sample mean.

Why Lloyd converges: assignment chooses the best centroid for fixed means, so objective cannot increase; mean update minimizes squared error for fixed assignments, so it cannot increase. There are finitely many assignments, so it reaches a fixed point, but only a local optimum.

```python
import numpy as np

def kmeans(X, K, iters=100, seed=0):
    rng = np.random.default_rng(seed)
    C = X[rng.choice(len(X), K, replace=False)].copy()
    for _ in range(iters):
        labels = ((X[:, None, :] - C[None, :, :])**2).sum(2).argmin(1)
        newC = np.array([X[labels == k].mean(0) if np.any(labels == k)
                         else X[rng.integers(len(X))] for k in range(K)])
        if np.allclose(C, newC): break
        C = newC
    return C, labels
```

Each iteration costs `O(NKd)`; memory can be `O(NK)` if all distances are stored or lower if streamed. K-means favors spherical, similarly scaled clusters; it is sensitive to scale, outliers, chosen `K`, empty clusters, and initialization.

### k-means++

Choose the first centroid randomly. Choose each next point with probability proportional to squared distance from its nearest chosen centroid. It spreads initial centers and gives a known expected approximation guarantee; multiple restarts remain useful.

### Soft k-means

Replace hard assignments with weights, e.g.

`r_ik = exp(-β||x_i-μ_k||²)/Σ_j exp(-β||x_i-μ_j||²)`,

then `μ_k=Σ_i r_ikx_i/Σ_i r_ik`. Large `β` approaches hard assignment. A spherical equal-covariance GMM has a closely related responsibility rule, but it is a probabilistic density model with mixture weights/variance.

The MDSR slide also motivates responsibility as normalized gravitational pull: for distance `d_ki`, `r_ki=(1/(d_ki²+ε))/Σ_l(1/(d_li²+ε))`. This is an illustrative soft-assignment rule; the exponential/Gaussian rule comes from a different modeling choice. In either case the M-step is the responsibility-weighted center.

### K-means vs GMM

| K-means | GMM |
|---|---|
| hard cluster | posterior soft responsibility |
| squared-distance objective | likelihood objective |
| effectively spherical/equal scale | covariance models elliptical shapes |
| Lloyd updates | EM updates |

## 40. Dimensionality reduction recall

### PCA

Center data matrix `X`. Covariance is `S=XᵀX/(n-1)`. The first principal direction maximizes projected variance:

`v₁=argmax_(||v||=1) vᵀSv`, so it is the top eigenvector. Further directions are orthogonal eigenvectors. Equivalently use SVD `X=UΣVᵀ`; columns of `V` are directions and squared singular values determine explained variance.

PCA is linear, unsupervised, scale-sensitive, and high variance need not be label-relevant. Standardize when unit differences are arbitrary. It is used for compression, denoising, visualization, and decorrelation.

### UMAP and HDBSCAN in the text-clustering slides

UMAP constructs a neighborhood graph and optimizes a low-dimensional embedding that preserves local structure approximately; it is nonlinear and stochastic, so global distances/visual clusters must not be overinterpreted. HDBSCAN finds density-stable clusters, can infer cluster count, and marks low-density points as noise; results depend on density parameters and embedding quality.

---

# Part VIII — Markov decision processes and reinforcement learning

## 41. MDP definition

An MDP is `(S,A,P,R,γ)`:

- states `s∈S`;
- actions `a∈A`;
- transition `P(s'|s,a)`;
- reward, e.g. `R(s,a,s')`;
- discount `0≤γ<1` (or a finite episodic horizon).

The Markov property says the next-state distribution depends on the present state/action, not the full past, assuming the state representation is sufficient.

Return from time `t`:

`G_t=R_(t+1)+γR_(t+2)+γ²R_(t+3)+...=Σ_(k=0)^∞γ^kR_(t+k+1)`.

A policy `π(a|s)` chooses actions. `γ` trades immediate versus delayed reward and makes infinite sums/contractions well-behaved under bounded rewards.

## 42. Value functions and Bellman equations

`V^π(s)=E_π[G_t|S_t=s]`.

`Q^π(s,a)=E_π[G_t|S_t=s,A_t=a]`.

Policy Bellman expectation equation:

`V^π(s)=Σ_aπ(a|s)Σ_s'P(s'|s,a)[R(s,a,s')+γV^π(s')]`.

Optimality equations:

`V*(s)=max_a Σ_s'P(s'|s,a)[R+γV*(s')]`

`Q*(s,a)=Σ_s'P(s'|s,a)[R+γmax_a'Q*(s',a')]`

`π*(s)=argmax_a Q*(s,a)`.

## 43. Dynamic programming: value and policy iteration

### Value iteration

Initialize `V`. Repeatedly apply Bellman optimality backup:

`V_new(s)=max_aΣ_s'P(s'|s,a)[R+γV(s')]`.

Stop when changes are sufficiently small, then extract greedy policy. With finite discounted MDP, Bellman optimality operator is a contraction and converges to `V*`.

### Policy iteration

1. Policy evaluation: solve/iterate Bellman equations for current `π`.
2. Policy improvement: `π_new(s)=argmax_aΣ_s'P[R+γV^π(s')]`.
3. Repeat until unchanged.

Policy iteration makes fewer outer improvements but evaluation can be costly; modified policy iteration uses partial evaluation.

## 44. Passive learning, ADP, TD, and active learning

- **Passive RL:** fixed policy; learn its utility/model.
- **Direct utility estimation:** average observed returns for states; unbiased with enough samples but wastes Bellman structure and has high variance.
- **Adaptive dynamic programming (ADP):** estimate transition/reward model, then solve the induced MDP; sample-efficient but model errors matter.
- **Temporal difference (TD):** model-free bootstrapping:

`V(s)←V(s)+α[R+γV(s')-V(s)]`.

The bracket is TD error. TD updates before an episode ends and combines sampling with bootstrapping.

Active RL must explore while exploiting. Greedy-only behavior can miss better actions. `ε`-greedy takes a random action with probability `ε`; decay carefully so exploration does not disappear too early. Other approaches include optimistic initialization and upper-confidence/softmax action selection.

## 45. Q-learning

Off-policy TD control update:

`Q(s,a)←Q(s,a)+α[R+γmax_a'Q(s',a')-Q(s,a)]`.

```python
from collections import defaultdict
import random

Q = defaultdict(lambda: [0.0] * n_actions)
for episode in range(num_episodes):
    s = env.reset()
    done = False
    while not done:
        a = random.randrange(n_actions) if random.random() < epsilon \
            else max(range(n_actions), key=lambda j: Q[s][j])
        s2, r, done = env.step(a)
        target = r if done else r + gamma * max(Q[s2])
        Q[s][a] += alpha * (target - Q[s][a])
        s = s2
```

Q-learning is **off-policy** because its target uses the greedy `max` action even when behavior explores. SARSA uses the actually chosen next action and is on-policy:

`Q(s,a)←Q(s,a)+α[R+γQ(s',a')-Q(s,a)]`.

Tabular Q-learning convergence requires finite states/actions, sufficient visitation, suitable decaying step sizes, and stationary Markov dynamics. With function approximation, bootstrapping, and off-policy data—the “deadly triad”—divergence is possible. DQN adds replay and target networks to improve stability but does not make all guarantees automatic.

---

# Part IX — Language representation and tokenization

## 46. Bag-of-words to contextual embeddings

### Bag-of-words

Build a vocabulary, then represent a document by word counts (or TF-IDF). It is sparse, high-dimensional, and mostly ignores order/context: “dog bites man” and “man bites dog” have the same unigram counts. It remains a strong, interpretable baseline for many text tasks.

Traditional TF-IDF weight:

`tfidf(t,d)=tf(t,d)·log(N/df(t))` (variants smooth/normalize).

### Static embeddings

Word2vec/GloVe map each vocabulary item to a dense vector. Similar distributional contexts create nearby vectors, enabling semantic similarity and analogical structure. A static embedding assigns one vector to “bank,” so it cannot distinguish river bank from financial bank without contextual machinery.

### Contextual embeddings

A language model transforms raw token embeddings using surrounding tokens; the final vector for “bank” changes with context. Token embeddings represent individual contextualized positions; a sentence/document embedding aggregates or learns a vector for the whole text. Pooling choices include `[CLS]`, mean pooling with attention-mask handling, or a specifically trained sentence encoder.

Cosine similarity:

`cos(u,v)=uᵀv/(||u||||v||)`.

It measures angle, not magnitude. Normalize when dot product should equal cosine.

## 47. Word2vec

### CBOW and skip-gram

- **CBOW:** predict a target word from surrounding context words.
- **Skip-gram:** predict surrounding context words from one center word.

Sliding a context window over raw text constructs supervision, so it is self-supervised.

### Negative sampling

For positive center-context pair `(w,c)` and negative contexts `n_j`, maximize

`log σ(v_cᵀv_w) + Σ_(j=1)^K log σ(-v_(n_j)ᵀv_w)`.

This turns an expensive full-vocabulary softmax into binary discrimination between observed and sampled pairs. Negatives are commonly sampled from a smoothed unigram distribution; frequent-word subsampling improves efficiency/quality. The two embedding tables (input/center and output/context) are learned by SGD; one or a combination is retained.

## 48. Why tokenization is difficult

Whitespace splitting fails on punctuation, contractions, `Mr.`, `O'Neill`, languages without spaces, code indentation, and morphology. Word tokenization has a huge vocabulary and unknown words. Replacing rare/unseen words with `<UNK>` bounds the vocabulary but destroys information; `<UNK>` is used during training so the model learns an embedding it can use at test time.

Character tokenization nearly eliminates unknowns and has a tiny vocabulary, but produces much longer sequences. With dense self-attention, sequence computation/memory grows quadratically, and semantic units require more layers to compose.

Subword tokenization balances vocabulary and sequence length: common words/fragments remain whole; rare words decompose.

## 49. Byte-pair encoding (BPE)

Training algorithm:

1. Represent each word as base symbols (characters or bytes), retaining word frequency.
2. Count frequencies of adjacent symbol pairs, weighted by word frequency.
3. Merge the most frequent pair into a new symbol; add it to vocabulary.
4. Retokenize occurrences and repeat until desired vocabulary/merge count.

Slide example starts with weighted words `hug:10`, `pug:5`, `pun:12`, `bun:4`, `hugs:5`. Initial symbols are `b,g,h,n,p,s,u`. Pair `ug` appears `10+5+5=20`, so it is first merged. Repeating yields vocabulary including `ug`, `un`, and `hug`.

### Class-test BPE simulation

Corpus: `ATCG CGAT ACGTTC ACGCG TCAG`; target vocabulary size 7.

Start with four characters `{A,T,C,G}`. The annotated slide solution's tie-breaking path is:

1. Most frequent pair `CG` → add `CG` (size 5).
2. Recount; merge `A+CG` → add `ACG` (size 6).
3. Recount; merge `T+C` → add `TC` (size 7).

Final vocabulary under that valid tie-breaking: `{A,T,C,G,CG,ACG,TC}`. With frequency ties, another deterministic tie-breaking policy can yield a different but valid merge sequence; state the rule.

```python
from collections import Counter

def learn_bpe(words_with_freq, target_vocab_size):
    corpus = [(tuple(word), freq) for word, freq in words_with_freq]
    vocab = set(ch for symbols, _ in corpus for ch in symbols)
    merges = []
    while len(vocab) < target_vocab_size:
        counts = Counter()
        for symbols, freq in corpus:
            for pair in zip(symbols, symbols[1:]):
                counts[pair] += freq
        pair = max(counts, key=lambda p: (counts[p], p))
        merged = ''.join(pair)
        vocab.add(merged); merges.append(pair)
        updated = []
        for symbols, freq in corpus:
            out = []; i = 0
            while i < len(symbols):
                if i+1 < len(symbols) and (symbols[i], symbols[i+1]) == pair:
                    out.append(merged); i += 2
                else:
                    out.append(symbols[i]); i += 1
            updated.append((tuple(out), freq))
        corpus = updated
    return vocab, merges
```

### BPE variants and other tokenizers

- GPT-2-style byte-level BPE begins with 256 byte values, avoiding an enormous full Unicode base vocabulary and almost eliminating unknown inputs.
- **WordPiece** selects merges based on a likelihood/score rather than raw pair frequency; used by BERT families.
- **Unigram LM** begins with many candidate pieces and removes pieces while minimizing likelihood loss.
- **SentencePiece** trains directly on raw text without mandatory whitespace pretokenization, useful across languages; it can implement BPE or unigram.

Subwords still struggle with agglutinative/non-concatenative morphology and language-specific pretokenization. Tokenizer choice affects context length, cost, multilingual fairness, code/number handling, and downstream behavior.

### Byte/character-level models

ByT5 operates on bytes, greatly reducing vocabulary embedding parameters and improving robustness to noisy text, but sequences and generation can be much longer/slower (the slide notes up to about 7× slower generation than mT5 in its setting). Charformer learns soft blocks/segmentations so the model can aggregate characters into latent subwords. There is no free lunch: vocabulary size, sequence length, compute, and linguistic bias trade off.

## 50. Special tokens and tokenizer–model contract

Common special tokens:

- `[CLS]`: sequence representation/classification in BERT-style models;
- `[SEP]`: sequence boundary/separator;
- `[MASK]`: masked-language-model target;
- BOS/EOS: beginning/end;
- PAD: batch padding, ignored by an attention/loss mask;
- chat role/control tokens and fill-in-the-middle tokens.

Token IDs are model-specific. The tokenizer and model vocabulary/embedding table must match. Decode a sequence of IDs jointly when byte/subword boundaries interact; decoding every ID separately can display different whitespace fragments.

---

# Part X — Transformers and pretrained language models

## 51. Autoregressive language modeling

An autoregressive model factorizes a sequence:

`p(x₁,...,x_T)=Π_(t=1)^T p(x_t|x_<t)`.

During self-supervised next-token training, a text sequence supplies many shifted `(prefix,next token)` examples. Teacher forcing presents ground-truth previous tokens in parallel with a causal mask. At generation, append one sampled token and repeat; decoding is sequential even though training positions are processed in parallel.

Cross-entropy for a target token is `-log p(target|prefix)`. Perplexity is `exp(average token NLL)`; lower is better only when tokenization/data are comparable.

## 52. Transformer overview

Input token IDs index an embedding table. Add/encode position. A stack of Transformer blocks repeatedly applies attention and position-wise feedforward networks with residual connections and normalization. A language-model head maps final hidden states to vocabulary logits; weights may be tied to the input embedding table.

The slide analogy: CNNs chop a signal into patches and process patches with shared operations. Transformers also process tokens identically/in parallel, but each token can depend on all other permitted tokens through attention.

## 53. Scaled dot-product self-attention

For input `X∈R^(n×d_model)`:

`Q=XW_Q`, `K=XW_K`, `V=XW_V`, where `Q,K∈R^(n×d_k)` and `V∈R^(n×d_v)`.

`Attention(Q,K,V)=softmax(QKᵀ/sqrt(d_k)+M)V`.

`M` contains `0` for allowed positions and a very negative value for masked positions. Softmax is row-wise, so every query's attention weights sum to one.

### Dictionary intuition

Query asks “what information am I looking for?”, keys describe what each token offers, dot products score compatibility, softmax turns scores into a soft lookup distribution, and values carry the retrieved information. The output for query `i` is `Σ_j a_ijv_j`.

### Why divide by `sqrt(d_k)`?

If query/key components have independent mean 0, variance 1, their dot product sums `d_k` products and has variance about `d_k`. Large logits make softmax saturate and gradients tiny. Scaling gives variance near one.

### Causal, bidirectional, and cross-attention

- Encoder self-attention can see all non-padding tokens.
- Decoder causal self-attention masks future keys (`j>i`).
- Cross-attention uses queries from one sequence/modality and keys/values from another, e.g. decoder attends to encoder output or text attends to image features.

Dense attention constructs an `n×n` score matrix: time roughly `O(n²d+n d²)` and attention memory `O(n²)` per layer (implementation details change constants). This motivates sparse/linear attention and state-space alternatives.

## 54. Multi-head, multi-query, and grouped-query attention

For each head `h`, project independent `Q_h,K_h,V_h`, compute attention, concatenate, then output-project:

`MHA(X)=Concat(head₁,...,head_H)W_O`.

Heads can learn different relation/position subspaces. They are computed in parallel, though “each head learns a human-interpretable relation” is not guaranteed.

- **MHA:** every query head has its own K/V head; best flexibility, largest KV cache.
- **MQA:** many query heads share one K and one V head; smallest KV cache/faster decoding, possible quality loss.
- **GQA:** groups of query heads share K/V heads; compromise used in modern LLMs.

## 55. Positional information and RoPE

Attention without positions is permutation-equivariant: permuting tokens permutes outputs but supplies no sequence order. Solutions include learned absolute embeddings, sinusoidal embeddings, relative position biases, and rotary position embeddings (RoPE).

RoPE rotates pairs of query/key coordinates by an angle determined by token position/frequency. The dot product between rotated `q_i` and `k_j` depends on relative offset `i-j`; RoPE is applied to Q/K before attention scoring, not merely added once to raw token embeddings.

## 56. Transformer block details

A modern pre-normalized decoder block is approximately:

`u=x+Attention(LN(x))`

`y=u+FFN(LN(u))`.

FFN acts independently at every token with shared weights, commonly `W₂ φ(W₁x)` or gated variants such as SwiGLU. Residual connections preserve an identity path; LayerNorm stabilizes feature scales. Original Transformer often used post-norm; pre-norm generally improves deep optimization.

## 57. KV cache

At autoregressive step `t`, old tokens' keys and values at each layer are unchanged. Cache them, compute only the new token's Q/K/V, and attend its query to cached/new K/V. This avoids recomputing previous token states and does **not** change the intended mathematical output aside from floating-point/kernel details.

Why not QV or QKV cache?

- Past **queries** are not reused to generate the current token in ordinary decoding.
- Keys are required to compute current attention scores; QV without K is insufficient.
- QKV adds memory with negligible normal benefit because old Q is unused.

KV caching reduces repeated compute but cache memory grows roughly with layers × sequence length × KV heads × head dimension. It does not remove the current token's need to score against the context.

## 58. Encoder-only, decoder-only, and encoder–decoder models

| Architecture | Visibility/objective | Strength | Example |
|---|---|---|---|
| encoder-only | bidirectional; masked-token/representation | classification, embeddings | BERT |
| decoder-only | causal next-token | open-ended generation | GPT/Llama |
| encoder–decoder | encoder bidirectional, decoder causal + cross-attention | conditioned sequence-to-sequence | original Transformer, T5 |

BERT masks some input tokens and predicts them, learning contextual representations. GPT removes encoder/cross-attention and predicts the next token. T5 expresses tasks as text-to-text instructions. “LLM” is a moving, informal size/capability label; both generative and representation models may be called language models.

### RNN encoder–decoder to attention

An early seq2seq RNN compressed a whole source sequence into one context vector, creating a long-sequence bottleneck. Attention let the decoder form a weighted combination of all encoder states at every output step. The Transformer removed recurrence, making token training more parallel while retaining context-dependent interaction.

## 59. Sampling and decoding

Given logits `z`, temperature `T>0` uses `softmax(z/T)`. Lower `T` sharpens/determinizes; higher `T` flattens/diversifies. `T=0` is implemented as greedy selection, not literal division by zero.

- Greedy: choose argmax each step; deterministic but myopic/repetitive.
- Beam search: retain top sequence hypotheses; useful in constrained generation/translation but can prefer bland/high-likelihood text.
- Top-k: sample among `k` highest-probability tokens.
- Top-p/nucleus: use smallest set whose cumulative probability reaches `p`.

Always picking the most probable token is not generally best global sequence quality. Sampling changes output distribution, not learned weights. Set maximum new tokens and stop tokens; distinguish total context window from number of generated tokens.

## 60. Mamba/selective state-space recall

The Fahim source mentions Mamba as a promising non-Transformer architecture. A careful viva answer:

> Mamba is a selective state-space sequence model. It updates a compressed recurrent state in linear sequence time, and input-dependent selection lets the model choose what information to retain or forget. Unlike full self-attention it does not explicitly materialize all token-pair scores, which can improve long-sequence efficiency. I understand the high-level distinction; I would not claim hands-on work unless I performed it.

Do not claim it has “infinite memory” or that linear asymptotics automatically make every implementation faster at every length.

---

# Part XI — Using pretrained models, prompting, and multimodality

## 61. Text classification with pretrained models

Three slide pipelines:

### Task-specific representation model

Use a pretrained encoder already fine-tuned for the task. Tokenizer creates IDs/masks; model outputs class logits; evaluate on held-out data. Verify label mapping and domain/language match. A model-card leaderboard result is not proof it works on your population.

### Frozen embeddings plus classifier

Encode each document into a vector, then train logistic regression or another simple classifier. This is compute-efficient and gives a strong baseline:

```python
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression

encoder = SentenceTransformer("all-MiniLM-L6-v2")
X_train = encoder.encode(train_texts, normalize_embeddings=True)
X_test = encoder.encode(test_texts, normalize_embeddings=True)
clf = LogisticRegression(max_iter=2000).fit(X_train, y_train)
pred = clf.predict(X_test)
```

The encoder is frozen; only classifier parameters learn. Fine-tuning the encoder can improve task fit but needs compute/data and stronger overfitting controls.

### Zero-shot classification

Embed a document and natural-language label descriptions, then choose maximum cosine similarity; or use an NLI/generative model prompted with candidate labels. Label wording strongly influences results. Zero-shot means no labeled examples used for that task, not “the model has never seen related information.”

### Generative classification

Prompt a text-to-text/chat model to output one allowed label. Constrain/parse output, validate prompt/model changes, and measure the same test metrics. Generative classification is flexible but slower and can produce invalid/explanatory text unless constrained.

## 62. Text clustering and BERTopic pipeline

Slide pipeline:

1. Embed documents with a semantic sentence/document encoder.
2. Optionally reduce dimension with UMAP for clustering efficiency/manifold structure.
3. Cluster with HDBSCAN; it can mark outliers rather than force every document into a cluster.
4. Inspect documents/clusters.
5. Produce topic representations with class-based TF-IDF (c-TF-IDF).

For c-TF-IDF, concatenate documents in each cluster into one meta-document. A common BERTopic form weights term `t` in class `c` approximately as

`w_(t,c)=tf_(t,c) · log(1 + A/f_t)`,

where `A` is average words per class and `f_t` is total frequency across class-documents. It identifies words frequent in one topic but less globally common.

Topic representations can be refined with:

- KeyBERT-style semantic similarity between topic/document embeddings and candidate phrases;
- **maximal marginal relevance (MMR)**, balancing query/topic relevance with diversity:

`argmax_(d∈R\S)[λSim(d,q)-(1-λ)max_(s∈S)Sim(d,s)]`;

- generative models that label a topic from representative keywords/documents.

Clustering output is exploratory: UMAP distortion, embedding bias, HDBSCAN parameters, and random seeds can change apparent topics. Read representative documents; do not equate a colorful 2D plot with ground truth.

## 63. Prompt engineering

A prompt can include role/persona, instruction, context, input data, examples, constraints, output schema, and abstention rule. The model remains probabilistic and prompt-sensitive; prompt iteration must be evaluated on a representative set, not one attractive example.

### Zero-, one-, and few-shot

- Zero-shot: instruction only.
- One-shot: one demonstration.
- Few-shot/in-context learning: multiple input–output demonstrations in context; no weight update.

Choose examples that cover task variation and use consistent formatting. Order/label balance can matter.

### Prompt chaining

Break a complex job into stages such as product description → name → slogan → pitch. Chaining makes interfaces inspectable and allows validation between steps, but errors can propagate and latency/cost rise.

### Reasoning-oriented prompting

- **Chain-of-thought (CoT):** provide/request intermediate steps for multi-step problems.
- **Zero-shot CoT:** a reasoning cue without a demonstration.
- **Self-consistency:** sample multiple reasoning paths and majority-vote/final-answer aggregate; often improves reliability at `N` times inference cost.
- **Tree-of-thought:** generate, score, expand, and prune several intermediate candidates; useful for search-like creative/planning tasks but expensive and evaluator-dependent.

Explanations can be plausible yet wrong and are not guaranteed faithful access to internal computation. Verify final results with tools/rules/tests when possible.

### Output validation

Ask for structured JSON/schema, enumerate permitted labels, parse strictly, retry/repair invalid output, or use constrained decoding/grammar so illegal tokens cannot be sampled. Schema validity does not guarantee factual correctness. Hallucination mitigation includes grounded context/retrieval, explicit uncertainty/abstention, citations that are checked, and external verification—not merely “please do not hallucinate.”

## 64. Vision Transformer (ViT)

For image `H×W×C`, patch size `P×P`, number of patches `N=(H/P)(W/P)`. Flatten each patch (`P²C` values) and linearly project to `d_model`. Prepend an optional learnable class token, add positional embeddings, then process with Transformer encoder blocks. Use the class token or pooled representation for classification.

Example: `224×224` image, `P=16` gives `14×14=196` patch tokens (plus class token). Patch projection parameters are `P²C·d_model` plus bias.

Compared with CNNs, ViT has weaker built-in locality/translation bias and global token interaction from early layers; it often benefits from large-scale pretraining and augmentation. It is not “CNN with attention,” though patch projection can be implemented as a strided convolution. Smaller patches improve detail but increase attention cost quadratically in patch count.

## 65. CLIP

CLIP has an image encoder and text encoder producing normalized embeddings in one space. For a batch of matching image–caption pairs, construct similarity logits

`s_ij = exp(τ) · image_iᵀ text_j`,

where `τ` is a learned logit scale. Optimize cross-entropy so each image selects its paired text and each text selects its paired image (symmetric contrastive loss). Other batch pairs are negatives.

Applications:

- text-to-image/image-to-text retrieval;
- zero-shot image classification by comparing an image with prompted class descriptions;
- multimodal clustering/search.

Cosine score has no universal “high” threshold; interpret relative to candidates/validation. Performance inherits dataset/caption biases and prompt wording.

## 66. BLIP-2 and the Q-Former

BLIP-2 connects a frozen image encoder to a frozen LLM using a trainable Querying Transformer (Q-Former). Learnable query tokens cross-attend to image features and compress them into a small set of visual representations. Training first aligns vision/language using tasks such as image–text contrastive learning, image–text matching, and image-grounded text generation. A projection then turns Q-Former output into soft visual prompts in the LLM's embedding space.

Benefit: reuse strong frozen components and train the bridge rather than both giant models. Use cases include captioning, visual question answering, and image-conditioned chat. Limitations include visual hallucination, weak counting/spatial reasoning, training-data gaps, and conversational “memory” that is just supplied prior text unless external state is added.

### Any modality as tokens

The general Transformer recipe is: divide input into chunks/patches, project each to `R^d`, add position/type information, and apply self/cross-attention. Images, audio frames, video patches, graphs, and multimodal streams can all be tokenized, but the tokenization/projection encodes domain-specific assumptions.

---

# Part XII — Pretraining, post-training, preference optimization, and test-time scaling

## 67. Building a modern language model

The slide lifecycle is:

1. **Pretraining:** next-token prediction over huge diverse text/code; creates a base model.
2. **Mid-training/continued pretraining:** smaller final stage with upsampled high-quality/in-domain, synthetic, instruction, or newly available sources.
3. **Supervised fine-tuning (SFT):** train on prompt–completion/instruction demonstrations.
4. **Preference tuning:** use ranked responses to shape helpfulness/style/safety.
5. **RL with verifiable rewards (RLVR):** optimize on tasks with objectively checkable final answers/constraints.
6. **Inference/test-time scaling:** allocate extra sampling/search/reasoning computation at use time.

Data, model, algorithm, training infrastructure, evaluation, licensing, decontamination, and transparency all matter. “Open weights” is not necessarily fully open: a reproducible ecosystem also releases data, code, training recipe, checkpoints, and evaluation details. OLMo is presented as a fully open base-model effort; Tülu as an open post-training recipe.

## 68. Pretraining and mid-training schedule

The OLMo slides show warmup to a peak learning rate, long cosine decay across trillions of pretraining tokens, then a short mid-training stage (roughly 1% of total budget in the example) with learning rate decayed linearly to zero. Pretraining consumes broad, plentiful data; mid-training upsamples scarce high-quality/domain/instruction/synthetic data near the final model.

Decontaminate evaluation examples from training data. More tokens are not automatically better: duplicates, low-quality text, personally identifying data, copyright/licensing constraints, and domain imbalance affect behavior.

## 69. Supervised fine-tuning and data curation

SFT minimizes token cross-entropy on desired completions conditioned on prompts. It teaches instruction format/behavior and targeted skills rather than erasing all pretraining knowledge.

Data sources may be human-written, real interactions, public instruction sets, or synthetic Self-Instruct/persona-generated tasks. The slide recipe emphasizes:

- curate against targeted evaluations/capabilities;
- mix chat, knowledge, reasoning, code, math, multilingual, precise instruction following, and safety data;
- filter licensing and contamination;
- use diversity and difficult examples, not volume alone;
- real user interactions with strong models can help broadly;
- safety data may be relatively orthogonal, but must still be checked for capability trade-offs.

### Reasoning/CoT data

Step-by-step traces can help multi-step tasks and make errors easier to inspect, but expert human annotation is costly and hard to scale. Alternatives in the slides:

- human GSM8K-style traces: high quality, limited scale/diversity;
- program-aided traces: execution verifies coded problems but covers only expressible tasks;
- self-generated traces: scalable but quality depends on the generator;
- persona-driven synthetic math/code/instruction data;
- self-consistency/majority voting to keep examples with agreement and remove those with no majority.

The reported lesson is that carefully selected smaller data can match or beat an unfiltered larger set. A visible rationale is not guaranteed faithful, so correctness filtering matters.

## 70. Preference data, RLHF, and RLAIF

For prompt `x`, collect responses `y_w` (preferred/winner) and `y_l` (rejected/loser), ranked by humans (RLHF pipeline) or AI judges (RLAIF). Preferences express nuance that a single reference answer cannot, but judge bias, order/length bias, annotator disagreement, and domain mismatch must be audited.

### Reward-model route

Train reward model `r_φ(x,y)` so preferred responses score higher, often with Bradley–Terry loss:

`L_RM=-E log σ(r_φ(x,y_w)-r_φ(x,y_l))`.

Then optimize policy while constraining departure from reference/base policy:

`max_θ E_(x,y~πθ)[r_φ(x,y)] - β D_KL(π_θ(y|x) || π_ref(y|x))`.

The reward term captures modeled preference; KL reduces destructive drift/reward exploitation. PPO implements an on-policy clipped policy-gradient version and needs policy, reference/reward/value components and fresh generations, making it complex and memory-intensive.

### Direct preference optimization (DPO)

DPO directly trains the policy on preference pairs without an explicit reward-model-and-RL loop:

`L_DPO = -E log σ( β log[π_θ(y_w|x)/π_ref(y_w|x)] - β log[π_θ(y_l|x)/π_ref(y_l|x)] )`.

It increases the preferred response's relative log-likelihood advantage over the rejected response, measured against the reference. It is simpler/cheaper but still depends on preference quality and reference behavior. The slides report PPO tending to outperform DPO slightly in their experiments, while DPO's practicality often wins during development; this is an empirical result, not a universal theorem.

Variants noted:

- length-normalized DPO normalizes preferred/rejected sequence log-likelihood by length;
- SimPO uses a length-normalized preference margin without a reference model.

High-quality preference data was the largest observed factor; scaling a reward model alone did not reliably improve downstream policy. On-policy/in-domain prompts can help.

## 71. Reward hacking and over-optimization

Optimizing too strongly against an imperfect neural reward model can raise predicted reward while true/human quality eventually declines. The policy discovers artifacts, verbosity, formatting, or adversarial patterns that exploit the proxy. This is Goodhart's law in action.

Mitigate with KL constraints, held-out human evaluation, diverse/judge ensembles, on-policy data refresh, conservative optimization/early stopping, adversarial tests, and verifiable rewards where possible. A higher reward-model score is not itself proof of better output.

## 72. RL with verifiable rewards (RLVR)

For math, code tests, or exact instruction constraints, use a verification function, e.g. reward `1` for correct final answer and `0` otherwise. The slides' Tülu recipe starts from SFT/DPO, chooses a targeted dataset plus verifier, and trains with PPO. Ground-truth final answers are required, but intermediate reasoning traces need not be supplied.

Advantages: cheap objective feedback and less subjective neural reward hacking. Risks: sparse reward, gaming the verifier/parser, incorrect/ambiguous gold labels, narrow task over-specialization, and unobserved bad reasoning that happens to reach the right answer. Base-model competence/CoT knowledge makes sparse-reward learning more tractable.

## 73. Test-time scaling and budget forcing

Test-time scaling spends extra inference compute rather than changing weights:

- **Parallel:** sample many independent candidates, then vote/rerank/rejection-sample.
- **Sequential:** allow one trajectory more reasoning tokens/steps, possibly with control prompts.

The `s1` slides describe filtering 59K questions by quality, difficulty, and diversity to 1K (`s1K`), distilling reasoning traces, fine-tuning a reasoning model, then **budget forcing**—encouraging it to continue reasoning by adding a cue such as “Wait” and controlling the token budget. Reported gains are empirical and benchmark-dependent.

More thinking tokens can help difficult tasks but eventually waste compute or amplify wrong paths. Parallel scaling offers diversity; sequential scaling offers depth. Verifier quality, latency, cost, and diminishing returns determine the choice.

---

# Part XIII — Deep generative models

## 74. Generative modeling goal

A generative model approximates a data distribution so it can assign likelihood/density (for some model families), learn latent structure, reconstruct, or draw new samples. Typical applications in the slides include image generation/editing, representation learning, anomaly/outlier detection, data augmentation, and studying/debiasing latent factors.

## 75. Autoencoder

Encoder maps `z=f_φ(x)`; decoder reconstructs `x̂=g_θ(z)`. Train with reconstruction loss, e.g. MSE for a Gaussian-like continuous observation model or BCE for appropriate Bernoulli-scaled pixels:

`min_(φ,θ) Σ_i ||x_i-g_θ(f_φ(x_i))||²`.

A bottleneck/regularization prevents trivial identity copying and encourages compressed features. An undercomplete AE has latent dimension smaller than input; sparse/denoising AEs impose other constraints. Low reconstruction error does not automatically mean a semantically meaningful or smooth latent space, and arbitrary latent samples may decode poorly because an ordinary AE does not match `z` to a known prior.

For anomaly detection, train on normal data and flag high reconstruction error—but powerful AEs may reconstruct anomalies too, and thresholds require held-out validation.

## 76. Variational autoencoder

VAE defines prior `p(z)` (usually `N(0,I)`), decoder likelihood `p_θ(x|z)`, and approximate posterior `q_φ(z|x)`, often diagonal Gaussian with encoder outputs `μ(x),logσ²(x)`.

### ELBO

The evidence lower bound is

`log p_θ(x) ≥ E_(qφ(z|x))[log p_θ(x|z)] - D_KL(q_φ(z|x)||p(z)) = ELBO`.

Train by minimizing negative ELBO:

`L_VAE = -E_q[log p_θ(x|z)] + D_KL(q_φ(z|x)||p(z))`.

The first term is reconstruction/negative log-likelihood; the KL term makes encodings resemble a sampleable prior and regularizes latent space.

For `q=N(μ,diag(σ²))`, `p=N(0,I)`:

`D_KL(q||p)=1/2 Σ_j(μ_j²+σ_j²-1-logσ_j²)`.

### Reparameterization trick

Sampling directly from `N(μ,σ²)` appears to block ordinary backprop. Rewrite:

`ε~N(0,I)`, `z=μ+σ⊙ε`.

Randomness is isolated in `ε`; `z` remains differentiable in `μ,σ`.

```python
def vae_loss(x, recon_logits, mu, logvar):
    recon = torch.nn.functional.binary_cross_entropy_with_logits(
        recon_logits, x, reduction="sum")
    kl = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
    return recon + kl

std = torch.exp(0.5 * logvar)
z = mu + std * torch.randn_like(std)
```

`β`-VAE uses `reconstruction + β·KL`. Larger `β` can encourage factorized/disentangled latents but often sacrifices reconstruction and does not guarantee human-interpretable factors without assumptions/inductive bias. **Posterior collapse** occurs when decoder ignores `z` and `q(z|x)≈p(z)`; KL warmup, architecture balance, or free-bits-style controls can help.

## 77. Generative adversarial network

Generator maps noise `z~p(z)` to fake sample `G(z)`. Discriminator outputs `D(x)`, probability/score that input is real. Canonical minimax game:

`min_G max_D [ E_(x~p_data) logD(x) + E_(z~p_z) log(1-D(G(z))) ]`.

Discriminator maximizes correct real/fake classification. The original minimax generator minimizes `log(1-D(G(z)))`, but when discriminator confidently rejects fakes its gradient can saturate. Common **non-saturating** generator loss is

`L_G=-E_z logD(G(z))`.

```python
# one conceptual GAN update
z = torch.randn(batch, latent_dim, device=device)
fake = G(z)

loss_D = bce(D(real), torch.ones(batch, 1, device=device)) + \
         bce(D(fake.detach()), torch.zeros(batch, 1, device=device))
opt_D.zero_grad(); loss_D.backward(); opt_D.step()

loss_G = bce(D(fake), torch.ones(batch, 1, device=device))
opt_G.zero_grad(); loss_G.backward(); opt_G.step()
```

Under ideal infinite-capacity optimization, optimal discriminator is `D*(x)=p_data(x)/(p_data(x)+p_g(x))`; the game relates to Jensen–Shannon divergence and equilibrium `p_g=p_data`, `D=1/2`. Real neural training is a nonstationary minimax problem and may oscillate.

Failure modes: mode collapse (little diversity), vanishing/unstable gradients, discriminator overpowering generator, sensitivity to architecture/hyperparameters. Remedies include balanced update schedules, normalization, spectral normalization, Wasserstein/hinge objectives, gradient penalty, data augmentation, and careful monitoring of both quality and diversity. Loss curves alone may not track sample quality.

### GAN variants in the slides

- **Progressive GAN:** grow generator/discriminator from low to high resolution, stabilizing high-resolution training.
- **StyleGAN:** map input noise through a mapping network to style vectors; inject styles at layers controlling coarse-to-fine features and separate stochastic noise for local detail.
- **Conditional GAN:** condition both G/D on a class/text/input image.
- **pix2pix:** paired image-to-image translation; adversarial loss plus reconstruction (often L1) to match paired target.
- **CycleGAN:** unpaired domains with two generators and discriminators; cycle consistency `F(G(x))≈x`, `G(F(y))≈y` plus adversarial losses. Cycle consistency does not guarantee semantically correct one-to-one translation.

## 78. Diffusion models: forward and reverse processes

A DDPM gradually corrupts data with a fixed Gaussian forward process, then learns a reverse denoiser.

Choose schedule `0<β_t<1`; define `α_t=1-β_t` and `ᾱ_t=Π_(s=1)^t α_s`.

Forward Markov step:

`q(x_t|x_(t-1))=N(x_t; sqrt(α_t)x_(t-1), β_tI)`.

The crucial closed form (“nice property”) samples any timestep directly:

`q(x_t|x_0)=N(x_t; sqrt(ᾱ_t)x_0, (1-ᾱ_t)I)`

so

`x_t=sqrt(ᾱ_t)x_0 + sqrt(1-ᾱ_t)ε`, `ε~N(0,I)`.

The learned reverse model is Gaussian:

`p_θ(x_(t-1)|x_t)=N(x_(t-1); μ_θ(x_t,t), Σ_θ(x_t,t))`.

Original DDPM fixes/chooses variance and trains a network `ε_θ(x_t,t)` to predict added noise. Mean reparameterization:

`μ_θ(x_t,t)=1/sqrt(α_t)[x_t - β_t/sqrt(1-ᾱ_t) · ε_θ(x_t,t)]`.

Simplified training loss:

`L_simple=E_(x0,t,ε)||ε-ε_θ(sqrt(ᾱ_t)x_0+sqrt(1-ᾱ_t)ε,t)||²`.

This arises from a variational bound whose timestep KL terms are Gaussian; the simplified noise-prediction MSE works well.

## 79. DDPM training algorithm and code

1. Sample real batch `x₀`.
2. Sample timestep `t` uniformly for every example.
3. Sample Gaussian noise `ε`.
4. Construct `x_t` directly using `ᾱ_t`.
5. Predict noise from `(x_t,t)`.
6. Minimize MSE/L1/Huber between true and predicted noise.

```python
def extract(a, t, x_shape):
    out = a.to(t.device).gather(0, t)
    return out.reshape(t.shape[0], *((1,) * (len(x_shape)-1)))

def q_sample(x0, t, noise=None):
    noise = torch.randn_like(x0) if noise is None else noise
    return (extract(sqrt_alpha_bar, t, x0.shape) * x0 +
            extract(sqrt_one_minus_alpha_bar, t, x0.shape) * noise)

def diffusion_loss(model, x0, t):
    eps = torch.randn_like(x0)
    xt = q_sample(x0, t, eps)
    eps_hat = model(xt, t)
    return torch.nn.functional.mse_loss(eps_hat, eps)

for x0 in loader:
    x0 = x0.to(device)                    # typically scaled to [-1,1]
    t = torch.randint(0, T, (len(x0),), device=device)
    loss = diffusion_loss(unet, x0, t)
    optimizer.zero_grad(); loss.backward(); optimizer.step()
```

### Schedules

The slide code includes linear (`β` from `10^-4` to `0.02`), quadratic, sigmoid, and cosine schedules. Schedule controls signal-to-noise progression; improved DDPM work found cosine schedules useful. Precompute `α`, cumulative `ᾱ`, `sqrt(ᾱ)`, `sqrt(1-ᾱ)`, reciprocal terms, and posterior variance.

## 80. Diffusion U-Net

The noise predictor takes `(B,C,H,W)` noisy images plus timestep `(B,)` and returns noise of the same image shape. Slide implementation components:

- initial convolution;
- sinusoidal timestep embedding, followed by an MLP;
- down stages with time-conditioned ResNet blocks, group normalization, attention, residual paths, and downsampling;
- middle ResNet–attention–ResNet;
- up stages with concatenated U-Net skip features, ResNet blocks, attention, and upsampling;
- final residual block and `1×1` output convolution.

Time embedding tells the shared network the current noise level. The code uses weight-standardized convolution with GroupNorm, SiLU, full attention in the bottleneck, and linear-attention variants elsewhere.

Core residual/time-conditioned block pattern:

```python
class TimeResBlock(nn.Module):
    def __init__(self, cin, cout, time_dim):
        super().__init__()
        self.time = nn.Sequential(nn.SiLU(), nn.Linear(time_dim, 2*cout))
        self.conv1 = nn.Conv2d(cin, cout, 3, padding=1)
        self.norm1 = nn.GroupNorm(8, cout)
        self.conv2 = nn.Conv2d(cout, cout, 3, padding=1)
        self.norm2 = nn.GroupNorm(8, cout)
        self.skip = nn.Conv2d(cin, cout, 1) if cin != cout else nn.Identity()

    def forward(self, x, temb):
        scale, shift = self.time(temb)[:, :, None, None].chunk(2, dim=1)
        h = self.norm1(self.conv1(x))
        h = torch.nn.functional.silu(h * (1 + scale) + shift)
        h = torch.nn.functional.silu(self.norm2(self.conv2(h)))
        return h + self.skip(x)
```

## 81. DDPM sampling

Start `x_T~N(0,I)`. For `t=T-1,...,0`, compute model mean; if `t>0`, add posterior Gaussian noise, while final step returns mean:

```python
@torch.no_grad()
def p_sample(model, x, t, t_index):
    beta_t = extract(betas, t, x.shape)
    mean = extract(sqrt_recip_alpha, t, x.shape) * (
        x - beta_t * model(x, t) /
        extract(sqrt_one_minus_alpha_bar, t, x.shape)
    )
    if t_index == 0:
        return mean
    var = extract(posterior_variance, t, x.shape)
    return mean + torch.sqrt(var) * torch.randn_like(x)

@torch.no_grad()
def sample_loop(model, shape):
    x = torch.randn(shape, device=next(model.parameters()).device)
    for i in reversed(range(T)):
        t = torch.full((shape[0],), i, device=x.device, dtype=torch.long)
        x = p_sample(model, x, t, i)
    return x
```

Diffusion generally offers stable coverage/high quality compared with classic GAN training, but iterative denoising is slow. Later work learns variance, uses cascades, classifier/classifier-free guidance, latent diffusion, and faster samplers/distillation. Classifier-free guidance combines conditional and unconditional noise predictions, often increasing prompt adherence at a diversity/over-saturation trade-off.

## 82. AE vs VAE vs GAN vs diffusion

| Model | Training signal | Sampling | Main strength | Common weakness |
|---|---|---|---|---|
| AE | reconstruction | no principled prior by default | compression/features | latent holes, blurry MSE reconstructions |
| VAE | reconstruction likelihood + KL | sample prior then decode | smooth probabilistic latent | blur/posterior collapse |
| GAN | adversarial game | one generator pass | sharp fast samples | instability/mode collapse, no direct likelihood |
| DDPM | predict noise/score across timesteps | iterative denoising | quality/coverage/stable objective | slow multi-step generation |

---

# Part XIV — Developing and evaluating trustworthy ML systems

## 83. Baselines, experiments, and ablations

Begin with a trivial baseline (majority/mean), then a strong simple baseline (linear model, tree, bag-of-words, frozen embeddings). A sophisticated model is useful only if it improves the metric under the same split and cost constraints.

An **ablation** removes or changes one component to estimate its contribution: no augmentation, no attention, different loss, frozen vs fine-tuned encoder. Keep other conditions controlled and report variability across seeds/folds. An association in an ablation is strongest when experimental conditions are comparable; interactions mean individual gains need not add linearly.

Document:

- data version, inclusion/exclusion, label policy, split identifiers;
- code/environment/random seeds/checkpoint-selection rule;
- hyperparameter search space and budget;
- primary metric chosen before seeing test results;
- confidence intervals or fold/seed distribution, not only best run;
- compute, latency, memory, and failure cases.

## 84. Error analysis

Inspect false positives/negatives and stratify by class, source, subgroup, difficulty, time, device, and data quality. Look for label errors, ambiguous cases, duplicated templates, spurious shortcuts, and consistent failure modes. Do not change the test set to make a model look better; if labels are corrected, version the dataset and explain the audit.

### Class imbalance

Options include class-weighted loss, resampling training data, threshold tuning, focal loss for abundant easy negatives, and obtaining more minority examples. Apply oversampling only inside training folds. Evaluate per-class recall/precision, macro metrics, PR curves, calibration, and real error costs.

## 85. Distribution shift

- **Covariate shift:** `p(x)` changes while conditional relation is assumed stable.
- **Label/prior shift:** `p(y)` changes.
- **Concept/conditional shift:** `p(y|x)` changes; usually hardest.

Random IID test performance does not guarantee performance after time, geography, sensor, user, policy, or adversarial change. Monitor input statistics, missingness, prediction/uncertainty distributions, delayed labels, subgroup performance, and operational outcomes. Define alerts, rollback, and retraining triggers.

## 86. Fairness, privacy, robustness, and interpretability

- Dataset bias can be inherited/amplified; evaluate relevant subgroups and intersectional groups.
- Fairness metrics (demographic parity, equalized odds, calibration) can conflict under different base rates; choose based on context, law, and harm—not a universal scalar.
- Remove/minimize sensitive data, enforce access control, consider privacy-preserving training where needed, and test memorization/leakage.
- Test perturbations, out-of-distribution inputs, corruptions, adversarial cases, and abstention/fallback.
- Feature importance, saliency, attention maps, or SHAP describe model behavior under assumptions; none automatically proves causal reasoning. Validate explanation stability and usefulness.

For high-stakes decisions, human review is not magic: define reviewer information, authority, workload, escalation, and how disagreement/automation bias is handled.

## 87. Deployment and monitoring

Validate the full pipeline, not just a notebook model: schema checks → preprocessing → model → calibration/threshold → business rule → logging. Avoid train/serve skew by sharing versioned transformations. Measure latency percentiles, throughput, memory, uptime, and cost alongside predictive metrics.

Deploy with shadow/canary/A-B stages where appropriate, maintain a rollback model, log model/data versions, and protect sensitive logs. Feedback loops can alter future training data—for example, a recommender changes what users see—so post-deployment data are not passively IID.

## 88. Responsible LLM evaluation

Automatic benchmarks can be contaminated, narrow, or prompt-sensitive. Combine task metrics, robust parsing, adversarial cases, human pairwise evaluation, latency/cost, and safety/privacy checks. Human preference evaluation needs randomized order, clear rubrics, multiple annotators, agreement analysis, and representative prompts. An LLM-as-judge is scalable but may prefer verbosity/style/self-family; calibrate against humans.

---

# Part XV — Whiteboard teaching scripts and viva drills

## 89. Whiteboard: explain bias–variance in 90 seconds

Draw one fixed `x` and several fitted curves from different training samples.

1. “The target is random: `Y=f(x)+ε`; `f(x)=E[Y|x]`.”
2. “Training data are also random; training on dataset `D` gives `h_D(x)`.”
3. Write `h̄(x)=E_Dh_D(x)`.
4. Write bias `h̄-f`, variance `E_D(h_D-h̄)²`, noise `Var(Y|x)`.
5. Write `E_D E_(Y|x)(Y-h_D)²=noise+bias²+variance`.
6. Say: “Underfitting/overfitting are behaviors. High bias often underfits; high variance often overfits. They are related, not identical.”
7. Give the numeric example: true 10, mean prediction 8, noise 4, bias² 4, prediction variance .4, expected MSE 8.4.

Likely follow-up: “Expectation over what?” Answer: label randomness conditional on fixed `x` for noise; repeated training datasets and algorithm randomness for bias/variance; then optionally average over deployment `X`.

## 90. Whiteboard: decision-tree split

1. Draw parent with 6 positive, 4 negative.
2. `H(parent)=-(.6log₂.6+.4log₂.4)=.971`.
3. Candidate split: left 4+/0−, right 2+/4−.
4. `Remainder=.4·0+.6·.918=.551`.
5. `Gain=.971-.551=.420`.
6. Explain recursion, stopping, and pruning.

Follow-up: information gain can favor many-valued attributes; gain ratio compensates by split information.

## 91. Whiteboard: logistic regression derivative

1. `z=wᵀx`, `p=σ(z)`.
2. `L=-[ylogp+(1-y)log(1-p)]`.
3. Chain rule gives `dL/dz=p-y`.
4. Therefore `∇_wL=(p-y)x`; for a batch `Xᵀ(p-y)/n`.
5. Update `w←w-η∇L`.

Follow-up: the linear quantity is log-odds/boundary; probability is nonlinear sigmoid.

## 92. Whiteboard: one convolution

Use the `3×3` input and `2×2` kernel in §27. Calculate top-left `19`; slide to get `25,37,43`. Then write:

`out=floor((n+2p-k)/s)+1`, parameters=`C_out(C_in k²+1)`.

Follow-up: convolution is translation-equivariant; global pooling/classification creates approximate invariance.

## 93. Whiteboard: BN vs LN

Draw a matrix whose rows are examples/tokens and columns are features.

- BN: normalize each column (and spatial locations per CNN channel) using batch statistics; running stats at inference.
- LN: normalize across columns within each row; no batch dependency.
- Both learn `γ,β`.

Use the slide mini-batch means/variances in §23 if asked to calculate.

## 94. Whiteboard: attention

1. `Q=XW_Q`, `K=XW_K`, `V=XW_V`.
2. `S=QKᵀ/sqrt(d_k)`; apply causal/padding mask.
3. `A=softmax_rows(S)`; each row sums to 1.
4. `O=AV`.
5. Explain dictionary query–key–value analogy.
6. Multi-head: repeat with separate projections, concatenate, output-project.

Follow-up: cache K/V because past K/V are reused; old Q is not.

## 95. Whiteboard: K-means vs EM

K-means: hard nearest-center assignment → arithmetic mean update. Each step lowers within-cluster SSE.

GMM EM: posterior soft responsibility → weighted mean/covariance/mixture update. Each step does not decrease likelihood. Both can reach local optima and need initialization/multiple starts.

## 96. Whiteboard: Bellman and Q-learning

Write

`V*(s)=max_aΣ_s'P(s'|s,a)[R+γV*(s')]`.

Then remove need for known `P` by writing sample update:

`Q(s,a)←Q(s,a)+α[r+γmax_a'Q(s',a')-Q(s,a)]`.

Explain exploration and off-policy target.

## 97. Whiteboard: BPE

Write words as character sequences with frequencies. Count adjacent pairs, circle the most frequent, replace all occurrences with merged token, recount, repeat. State tie-breaking. Use the class-test result `{A,T,C,G,CG,ACG,TC}` if given that corpus/tie path.

## 98. Whiteboard: VAE and diffusion

VAE: `x→(μ,logσ²)`, sample `z=μ+σ⊙ε`, decode `x̂`; loss=`reconstruction+KL`.

Diffusion: choose random `t`, create `x_t=sqrt(ᾱ_t)x₀+sqrt(1-ᾱ_t)ε`, train U-Net to predict `ε`; generation begins from Gaussian noise and applies learned reverse steps.

## 99. High-frequency viva questions

### “What is the difference between loss, cost, and metric?”

Loss is usually per-example optimization penalty; cost/objective aggregates loss plus possible regularization; metric is evaluation measure and may be nondifferentiable. Terminology varies, so define your use.

### “Why not train on the test set?”

It destroys independent generalization estimation. Any decision influenced by it optimistically biases reported performance.

### “What is overfitting?”

Learning training-specific noise/idiosyncrasy such that train performance is much better than unseen performance. It is commonly associated with high variance, not identical to variance.

### “Why cross-entropy instead of accuracy?”

Accuracy is piecewise constant/non-differentiable in model scores and ignores probability confidence. Cross-entropy is differentiable and a proper likelihood-based objective that strongly penalizes confident wrong predictions.

### “Why can accuracy be misleading?”

With 1% positives, predicting all negatives gives 99% accuracy but zero positive recall. Use the confusion matrix and cost-relevant metrics.

### “Does normalization regularize?”

BN's batch noise can have a regularizing side effect, but its central function is to stabilize/condition training. LN is deterministic per example and should not be sold as the same stochastic regularizer.

### “Why residual connections?”

They provide an identity information/gradient route and let blocks learn residual corrections, improving optimization of deep networks.

### “Why is self-attention quadratic?”

Every one of `n` queries scores `n` keys, producing an `n×n` matrix. Projection/FFN also cost `O(nd²)`, so the dominant term depends on `n` versus model width and implementation.

### “Is KV cache exact?”

It reuses values that would otherwise be recomputed, so intended math is unchanged. Quantization/finite-precision kernels can produce tiny implementation differences.

### “What does EM guarantee?”

Each exact iteration does not decrease observed-data likelihood; it does not guarantee the global maximum.

### “What is the difference between bagging and boosting?”

Bagging trains independent bootstrapped learners and averages mainly to reduce variance. Boosting trains sequentially on errors/negative gradients mainly to reduce residual bias; it is more sensitive to noise.

### “Why is a transposed convolution transposed?”

Its linear operator is the transpose of the matrix representing ordinary convolution. It is not generally an inverse.

### “Can an LLM reason?”

It can produce outputs that solve multi-step tasks and can improve with reasoning-oriented training/inference. Whether that is called reasoning is a conceptual claim; explanations may be unfaithful, so evaluate behavior and verify results rather than infer internal cognition from fluent text.

### “What is hallucination?”

Fluent content unsupported by reliable evidence/context. Reduce with grounding, retrieval, abstention, constrained outputs, and external verification; prompting alone cannot guarantee elimination.

### “Proprietary vs open model interface?”

Proprietary models are usually accessed through hosted API/SDK: low deployment burden but rate limits, usage cost, privacy/governance concerns, limited weight/architecture control, and service dependence. Open-weight models can run locally/on your server and allow quantization/fine-tuning/deeper integration, but you supply hardware, serving, security, licensing compliance, and optimization. “Open-weight” alone may not mean training data/code are open.

### “Two uses of Papers with Code?”

Use it to compare benchmark/task leaderboards and to connect papers with implementations, datasets, and reproducibility resources. Leaderboard rank still requires checking data, metric, compute, and evaluation comparability.

## 100. Complexity recall table

Let `n` examples, `d` features, `K` clusters/classes/trees as context indicates, sequence length `L`, hidden width `d_m`.

| Algorithm/operation | Typical time | Important qualifier |
|---|---|---|
| linear/logistic GD step | `O(nd)` | full batch |
| normal equation | about `O(nd²+d³)` | QR/SVD preferred; shape matters |
| k-NN training/query | store / `O(nd)` | naïve query |
| tree training | often `O(d n log n)` | implementation/depth dependent |
| tree inference | `O(depth)` | per sample |
| random forest | about trees × tree cost | parallelizable |
| Ada/gradient boosting | learners × learner cost | sequential |
| k-means iteration | `O(nKd)` | Lloyd |
| full-covariance GMM EM | roughly `O(nKd²)` | diagonal is `O(nKd)` |
| dense layer | `O(d_in d_out)` | per example |
| 2D convolution | `O(H_oW_oC_oC_iK_hK_w)` | per example |
| dense attention | `O(L²d_m + Ld_m²)` | memory `O(L²)` for scores |
| value-iteration sweep | `O(|S|²|A|)` dense | sparse transitions cheaper |
| tabular Q update | `O(|A|)` | due to max; one transition |
| DDPM sampling | `T` network passes | accelerated samplers reduce steps |

Big-O is not a benchmark: vectorization, sparsity, cache, GPU kernels, batch size, and constants matter.

---

# Part XVI — Compact equation sheet

## 101. Core supervised equations

```text
OLS:                  w_hat = (X^T X)^(-1) X^T y
OLS gradient:         X^T(Xw-y)/n
Sigmoid:              1/(1+exp(-z))
Logistic gradient:    X^T(p-y)/n
Softmax:              exp(z_k-max z)/sum_j exp(z_j-max z)
Softmax+CE gradient:  p-y
Entropy:              -sum_k p_k log2 p_k
Information gain:     H(parent)-sum_v |S_v|/|S| H(S_v)
AdaBoost alpha:       0.5 ln((1-error)/error)
L1 / L2:              sum |w_j| / sum w_j^2
```

## 102. Neural and vision equations

```text
Affine layer:         z = Wx+b
BN/LN core:           gamma (x-mu)/sqrt(var+eps) + beta
Xavier variance:      2/(fan_in+fan_out)
He variance:          2/fan_in
Conv output:          floor((n+2p-d(k-1)-1)/s)+1
Conv parameters:      C_out(C_in K_h K_w+1)
Transposed output:    (n-1)s-2p+d(k-1)+output_padding+1
Attention:            softmax(QK^T/sqrt(d_k)+mask)V
```

## 103. Probabilistic, clustering, and RL equations

```text
Bayes:                P(h|d)=P(d|h)P(h)/P(d)
MAP:                  argmax_theta [log p(D|theta)+log p(theta)]
GMM responsibility:  pi_k N(x_i|mu_k,Sigma_k) / sum_j pi_j N(...)
K-means objective:    sum_i ||x_i-mu_(c_i)||^2
Bellman optimality:   V*(s)=max_a sum_s' P(s'|s,a)[R+gamma V*(s')]
TD:                   V <- V + alpha[R+gamma V'-V]
Q-learning:           Q <- Q + alpha[R+gamma max Q'-Q]
```

## 104. Bias–variance and generative equations

```text
Expected squared error = noise + bias^2 + variance
Bias(x)                 = E_D[h_D(x)] - f(x)
Variance(x)             = E_D[(h_D(x)-E_D h_D(x))^2]
VAE negative ELBO       = -E_q log p(x|z) + KL(q(z|x)||p(z))
GAN minimax             = min_G max_D E log D(x)+E log(1-D(G(z)))
DDPM q sample           = sqrt(alpha_bar_t)x0 + sqrt(1-alpha_bar_t)epsilon
DDPM simple loss        = E ||epsilon-epsilon_theta(x_t,t)||^2
```

---

# Part XVII — Source/page coverage audit

## 105. Sources processed

| Local source | Pages | Extraction | Visual inspection |
|---|---:|---|---|
| `ML/471/Fahim_sir_Merged(ML).pdf` | 674 | page-delimited text read and topic-indexed | low/zero-text, diagrams, handwritten calculations, exams, equations, and code pages rendered and inspected |
| `ML/471/MDSR_merged(ML).pdf.pdf` | 512 | page-delimited text read and topic-indexed | handwritten derivations and image-heavy NN, Bayesian, clustering, RL, and generative-model blocks rendered and inspected |
| **Total** | **1,186** | **complete page range accounted for** | **visual fallback used where extraction was insufficient** |

Decorative covers, acknowledgments, references, URL-only pages, and blank dividers were inspected/accounted for but were not expanded into fake technical content. Unreadable equations were checked against their rendered page; no technical claim was invented from a blank extraction.

## 106. Fahim merged PDF coverage matrix (674/674)

| PDF pages | Slide/source block | Concepts retained here |
|---:|---|---|
| 1–44 | CNN introduction and handwritten calculations | image tensors, flattening failure, locality/equivariance, convolution calculation/code/backprop, padding/stride/output shape, channels, pooling/receptive field, LeNet shapes/parameters/code |
| 45–74 | Modern CNN architectures | hand-crafted vs learned features, AlexNet, VGG, NiN/`1×1`, Inception/GoogLeNet, function classes, ResNet projection/identity, DenseNet |
| 75–93 | Normalization | motivation, BN equations/train-inference behavior, CNN BN, LN, BN-vs-LN examples |
| 94–114 | CV techniques | augmentation, transfer/fine-tuning code, segmentation, transposed convolution, FCN, U-Net |
| 115–120 | Class test and handwritten solution | CNN true/false traps, BN/LN calculation procedure, channel conversion, up-conv stride, fine-tuning |
| 121–144 | Hands-On LLM front matter/TOC/dividers | chapter scope identified; publishing/front-matter content not treated as ML theory |
| 145–177 | LLM Chapter 1 | BoW, embeddings/history, RNN encoder–decoder, attention/Transformer, BERT/GPT, pretraining/fine-tuning, open vs proprietary interface, responsible use |
| 178 | visual divider | accounted for |
| 179–213 | LLM Chapter 2 | tokenizers/special tokens, token/context/document embeddings, word2vec/negative sampling, recommendation embeddings |
| 214 | visual divider | accounted for |
| 215–249 | LLM Chapter 3 | autoregressive forward pass, LM head/decoding, context, KV cache, attention Q/K/V, MHA/MQA/GQA, Transformer block, RoPE |
| 250–275 | LLM Chapter 4 | text classification with task-specific models, frozen embeddings+logistic regression, zero-shot labels, T5/generative classification, metrics |
| 276–305 | LLM Chapter 5 | text clustering, UMAP, HDBSCAN, c-TF-IDF/BERTopic, KeyBERT, MMR, generative topic labeling |
| 306–337 | LLM Chapter 6 | generation controls, prompt components, hallucination/persona, few-shot, chaining, CoT/self-consistency/tree-of-thought, structured/constrained output |
| 338–365 | LLM Chapter 9 | ViT patching, shared multimodal embedding, CLIP training/code/use, BLIP-2/Q-Former, preprocessing/caption/VQA/chat |
| 366–450 | MIT Transformer lecture | CNN-to-token principles, self-supervision, autoregression, embeddings, query-key-value dictionary intuition, full matrix attention derivation, multi-head parallelism, mask/LN/residual/position, cross-modal attention, success/failure modes |
| 451–478 | Tokenization lecture | word boundaries/unknowns, character/subword trade-off, complete BPE procedure/example, byte BPE, WordPiece/SentencePiece, multilingual limits, ByT5, Charformer |
| 479–482 | Class test, handwritten BPE answer, blank continuation | contextual vs static embedding, autoregression, model interfaces, decoding, KV/QV/QKV cache, word2vec, worked corpus BPE |
| 483–520 | Open LM lecture: setup and SFT | OLMo openness/reproducibility, modern LM stages, Tülu recipe, evaluation/license/decontamination, SFT, data sources/mixing |
| 521–541 | Reasoning-data curation | capability mixes, CoT value/cost, persona synthetic data, self-consistency filtering, human/program/self-generated traces |
| 542–571 | Preference tuning | human/AI preference data, reward model, RLHF/PPO objective, DPO equation, SimPO/length normalization, empirical data/algorithm lessons |
| 572–604 | RLVR and over-optimization | reward hacking, rule-based verifier, Tülu RLVR setup, training curves/scaling, fully open base/post-training relation |
| 605–624 | Test-time scaling | s1K collection/filtering/distillation, budget forcing, sequential vs parallel inference, ablations/results |
| 625–637 | Open pre/mid-training and evaluation | warmup/cosine/linear schedule stages, pretraining vs mid-training data, improvement/evaluation, open research needs |
| 638–674 | Annotated diffusion | DDPM forward/reverse math, ELBO/noise objective, U-Net/time/residual/attention/groupnorm code, schedules/q-sampling/loss/data transforms, reverse sampler/training loop/follow-ups |

Explicit Fahim visual-review targets included pages `2,22,38,40–42,45,48,50–52,64,75,94,96,98–99,102–103,115–120,142–144,178,214,275,305,371,376,387–388,416–450,473–482,484–495,502,541,548,555–558,573–576,589–591,600–603,606–621,631–634`, plus the diffusion code/equation sequence `638–674`.

## 107. MDSR merged PDF coverage matrix (512/512)

| PDF pages | Slide/source block | Concepts retained here |
|---:|---|---|
| 1–18 | Handwritten linear classification/regression | univariate OLS derivation, perceptron/logistic setup and gradients |
| 19–43 | ML introduction and basic supervised learning | T/E/P, learning types, splits, hypothesis space, decision-tree entropy/gain, learning curves, metrics, preprocessing |
| 44–97 | Linear models, ensembles, exams | multivariate GD/normal equation, bagging/RF/stacking/AdaBoost, L1/L2, perceptron/logistic, worked metric/model questions |
| 98–148 | AIMA learning chapter and ML systems | supervised/hypothesis spaces, bias vs variance vs fitting, trees/pruning, validation/loss/regularization/tuning, linear classifiers, ensembles/online learning, data/feature/EDA/trust/deployment |
| 149–206 | Neural-network lecture | FNN/MLP/CNN/RNN, activations, computation graph/backprop, softmax/CE, BN/LN/dropout, vanishing gradients, Xavier derivation/exercises |
| 207–220 | AIMA deep-learning chapter | deep vs shallow/feedforward/recurrent, universal approximation caveats, auto-diff, encodings/output/loss, hidden representations/CNN/pooling/tensors |
| 221–252 | Optimization lecture/article | batch/SGD/minibatch, momentum/NAG, AdaGrad/AdaDelta/RMSProp/Adam/AdaMax/Nadam, Hogwild/Downpour/delay/distributed systems/EASGD, shuffle/curriculum/BN/early stop/noise |
| 253–309 | Trees and gradient boosting | classification/regression trees, continuous splits/pruning, gradient-boosted regression and logistic classification with residual/Newton leaf calculations |
| 310–359 | Probability and Bayesian learning | probability/Bayes, Bayesian networks/Markov blanket, ML/MAP/Bayesian prediction, Naive Bayes, generative vs discriminative, Beta conjugacy, GMM/EM |
| 360–384 | Clustering | k-means objective/Lloyd proof/init/k-means++, limitations, soft k-means, coin/GMM-style EM intuition |
| 385–417 | MDP and RL | returns, Bellman/value/policy iteration, passive utility/ADP/TD, active exploration, Q-learning |
| 418–508 | Image-heavy deep generative lecture | generative motivation, anomaly/debias uses, AE/VAE, ELBO/KL/reparameterization/β-VAE, GAN intuition/training, progressive/StyleGAN, conditional/pix2pix/CycleGAN/speech transformation |
| 509–512 | Explicit GAN objective slides | minimax discriminator/generator losses and final GAN comparison |

Visual inspection was performed across the MDSR handwritten/image-heavy ranges `1–18`, `25–43`, `44–97`, `149–206`, `285–309`, `310–359`, `360–384`, `385–417`, and continuously across the generative-model pages `418–512`.

## 108. Final self-audit checklist

- [x] Begins exactly with `# Bismillah.`
- [x] Both local PDFs accounted for: 674 + 512 = 1,186 pages.
- [x] Bias and variance defined as statistical quantities, with expectation domains and squared-error derivation.
- [x] Bias/variance explicitly distinguished from underfitting/overfitting.
- [x] Worked numeric bias–variance example and learning-pattern remedies included.
- [x] Slide equations, handwritten calculations, algorithms, assumptions, complexity, and traps retained.
- [x] Executable/minimal code included for core linear, tree, ensemble, NN, convolution, clustering, RL, tokenization, VAE/GAN, and diffusion procedures.
- [x] CNN, Transformer/tokenization, multimodality, post-training, RLVR, and diffusion slide sets covered.
- [x] MDSR classical ML, optimization, Bayesian/EM, clustering, RL, and generative blocks covered.

Use this book for recall, then practice aloud: define → equation → intuition → example → limitation. That sequence is the most reliable defense against another “I knew the topic but could not state it precisely” moment.
