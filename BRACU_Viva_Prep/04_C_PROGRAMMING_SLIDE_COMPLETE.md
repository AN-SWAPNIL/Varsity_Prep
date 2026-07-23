# Bismillah.

# C Programming — Slide-and-Code Complete Viva Recall

> **Source basis:** all 13 PDFs in `Discrete and C/CSE 101/Mahfuj Islam Sir` were read: 12 individual lecture PDFs totaling 147 pages and the 147-page merged compilation, for 294 inspected PDF pages. The merged file substantially repeats the individual lectures, so page totals are coverage totals, not 294 unique lectures. All 35 non-metadata `.c` files and the accompanying READMEs in `Rayhan Rashed Sir` were also audited. Modern corrections are marked explicitly because several teaching examples use obsolete or unsafe C idioms.

---

# 1. Source coverage matrix

| Source | Pages | Main content |
|---|---:|---|
| Lecture 1 Writing C Program | 17 | program structure, formatted I/O, algorithm-to-code workflow |
| Lecture 2 Programming Language C | 11 | character set, tokens, identifiers, types, scope |
| Lecture 3 Operator | 14 | unary/binary/ternary operators, conversion, precedence |
| Lecture 4 Library Functions and Header Files | 15 | prototypes, headers, math/string/I/O functions, formatting |
| Lecture 5 Control Structure | 15 | statements, selection, loops |
| Lecture 6 Function | 6 | prototype/call/definition, arguments, return, variadic example |
| Lecture 7 Recursive Function — General | 6 | factorial, Fibonacci, Euclid GCD, recurrence |
| Lecture 7A Recursive Function — Tower of Hanoi | 9 | recursive design and trace |
| Lecture 7B Recursive Function — BST | 5 | iterative/recursive binary search and array BST ideas |
| Lecture 8A — 1D Array | 17 | traversal, sort, search, insert/delete, passing arrays |
| Lecture 8A — 2D Array | 12 | matrices, addition, multiplication, transpose |
| Lecture 9 Pointer | 20 | addresses, dereference, pointer parameters and arrays |
| Mahfuz_Sir_C_Merged | 147 | merged repetition/sequence of the above material |
| Rayhan string programs | 10 files | representation, input, library/manual operations, substring search |
| Rayhan structure programs | 7 files | nested structures, typedef, arrays, contact application |
| Rayhan file programs | 14 files | text/binary I/O, seeking, redirection, persistence |
| Rayhan bitwise programs | 4 files | masks, shifts, fields, reversal, next bit pattern |

Exact code audit appears in §19.

---

# 2. From problem to executable program

## 2.1 Problem-solving sequence

1. specify input and output;
2. identify constraints and exceptional cases;
3. write an algorithm/pseudocode;
4. choose data representation and functions;
5. implement;
6. compile with warnings;
7. test normal, boundary, and invalid cases;
8. debug and document assumptions.

An **algorithm** is a finite, unambiguous sequence of effective steps that terminates and produces the required output for valid input. A program is an implementation in a programming language.

## 2.2 Minimal conforming hosted C program

```c
#include <stdio.h>

int main(void) {
    puts("Hello, world!");
    return 0;
}
```

- `#include` is a preprocessing directive.
- `<stdio.h>` declares standard I/O functions.
- `int main(void)` says the hosted entry function returns status and takes no arguments.
- braces delimit a compound statement/block.
- `;` terminates most statements.
- returning `0` communicates successful termination; reaching the closing brace of `main` is also successful in modern C.

**Correction:** `void main()` is not a portable standard hosted signature. Use `int main(void)` or `int main(int argc, char **argv)`.

## 2.3 Translation pipeline

```text
source .c
 -> preprocessing (#include, #define, conditional compilation)
 -> compilation (C to assembly/object representation)
 -> assembly (object file)
 -> linking (objects + libraries -> executable)
 -> loading/execution
```

- A declaration tells the compiler a name and type.
- A definition allocates an object or supplies a function body.
- A prototype enables argument/return-type checking at a call site.
- The linker resolves external symbols across translation units.

Useful command:

```text
gcc -std=c17 -Wall -Wextra -Wpedantic -Wconversion program.c -o program
```

Warnings are evidence to inspect, not cosmetic text to suppress blindly.

---

# 3. Lexical elements, identifiers, and types

## 3.1 Tokens

C source is decomposed into tokens:

- keywords: `int`, `if`, `return`, `struct`, `sizeof`;
- identifiers: programmer-defined names;
- constants/literals: `42`, `3.5`, `'A'`, `"hello"`;
- string literals;
- operators: `+`, `==`, `&&`, `&`, `<<`;
- punctuators: `; , ( ) [ ] { }`.

Identifiers are case-sensitive, start with a letter or underscore, and continue with letters, digits, or underscores. Reserved identifiers and keywords must not be repurposed.

## 3.2 Character representation correction

The slides discuss ASCII and state that C does not support Unicode. The accurate answer is subtler:

- C defines execution/source character sets and numeric character types;
- `char` stores one byte, not inherently an ASCII or Unicode character;
- an implementation may use ASCII-compatible encodings, UTF-8, or another encoding;
- wide/multibyte facilities exist, but Unicode processing depends on encoding and libraries;
- a UTF-8 code point may occupy multiple `char` bytes, so `strlen` counts bytes, not user-perceived characters.

## 3.3 Fundamental types

- integer: `char`, `short`, `int`, `long`, `long long`, signed/unsigned variants;
- floating: `float`, `double`, `long double`;
- Boolean: `_Bool`, commonly `bool` through `<stdbool.h>` in C17;
- `void`: no value/incomplete object type;
- derived: pointers, arrays, functions;
- user-defined compositions: `struct`, `union`, `enum`, `typedef` aliases.

The standard gives minimum ranges/order relationships, not universal byte sizes. Use `sizeof`, `<limits.h>`, and `<stdint.h>` when exact-width types such as `uint32_t` exist and are required.

## 3.4 Signed versus unsigned

- Unsigned arithmetic is modulo `2^w` for width `w`.
- Signed overflow is undefined behavior.
- Mixing signed and unsigned can convert a negative signed value to a huge unsigned value.
- Use `size_t` for object sizes/array indexes where appropriate, and compare compatible types.

## 3.5 Floating point

Binary floating point cannot exactly represent most decimal fractions. Therefore:

```c
double a = 0.1 + 0.2;
/* a == 0.3 may be false */
```

Use a domain-appropriate tolerance, considering absolute and relative scale. Floating-point division by zero and exceptional values follow implementation/IEC 60559 behavior where supported; integer division by zero is undefined.

## 3.6 Scope, storage duration, and linkage

- **Block scope:** name declared inside a block.
- **File scope:** name declared outside functions.
- **Automatic storage duration:** ordinary local object exists during block activation.
- **Static storage duration:** file-scope objects and `static` locals exist for the entire program and are zero-initialized if not explicitly initialized.
- **Allocated storage duration:** dynamic allocation until `free`.
- **Linkage:** whether declarations in different scopes/translation units denote the same entity.

```c
static int next_id(void) {
    static int id;   /* initialized once; retains value */
    return ++id;
}
```

`static` at file scope gives internal linkage; `extern` declares an externally defined object/function; neither means “stored on the stack.”

---

# 4. Input, output, format strings, and headers

## 4.1 `printf`

```c
int age = 23;
double cgpa = 3.94;
printf("age=%d cgpa=%.2f\n", age, cgpa);
```

Common conversions:

| Value | `printf` conversion |
|---|---|
| `int` | `%d` or `%i` |
| `unsigned int` | `%u` |
| hexadecimal unsigned | `%x`/`%X` |
| `long` | `%ld` |
| `size_t` | `%zu` |
| `double` | `%f`, `%e`, `%g` |
| character | `%c` |
| null-terminated string | `%s` |
| pointer | `%p` with `(void *)p` |

Because variadic arguments are not type-safe beyond format checking, a mismatched specifier can cause undefined behavior. `printf` returns the number of characters written or a negative value on error.

## 4.2 `scanf`

```c
int n;
if (scanf("%d", &n) != 1) {
    /* invalid or unavailable input */
}
```

`scanf` needs addresses so it can modify caller objects. An array expression such as `name` usually converts to a pointer to its first element, so `scanf("%19s", name)` uses no extra `&`. Always bound `%s` to leave space for `\0`.

```c
char name[20];
if (scanf("%19s", name) == 1) { /* one whitespace-delimited word */ }
```

For lines, prefer `fgets`:

```c
char line[100];
if (fgets(line, sizeof line, stdin)) {
    line[strcspn(line, "\n")] = '\0';
}
```

**Correction:** `gets` was removed from the C standard because it cannot prevent buffer overflow. Several supplied examples use it only as historical teaching material; never use it in new code.

## 4.3 Headers and prototypes

Headers expose declarations/macros/types. Examples:

- `<stdio.h>`: streams and formatted I/O;
- `<stdlib.h>`: allocation, conversions, `exit`, sorting/searching;
- `<string.h>`: byte-string/memory operations;
- `<math.h>`: mathematical functions, often link with `-lm` on Unix-like toolchains;
- `<ctype.h>`: character classification/conversion;
- `<stdint.h>`, `<limits.h>`, `<float.h>`: numeric properties;
- `<errno.h>`: error indicator used by some library calls.

Do not manually invent a library prototype. Include its standard header.

---

# 5. Operators, conversion, precedence, and side effects

## 5.1 Major groups

- arithmetic: `+ - * / %`;
- comparison: `< <= > >= == !=`;
- logical: `! && ||`;
- bitwise: `~ & | ^ << >>`;
- assignment: `= += -= *= /= %= ...`;
- increment/decrement: `++ --`;
- conditional: `cond ? a : b`;
- address/dereference: `& *`;
- member access: `.` and `->`;
- indexing/call: `[]`, `()`;
- `sizeof`, cast, comma.

**Correction:** bitwise and logical operators are different. `&`/`|` operate bit-by-bit and evaluate both operands; `&&`/`||` produce logical truth and short-circuit.

## 5.2 Integer division and remainder

```c
7 / 2     /* 3 */
7.0 / 2   /* 3.5 */
7 % 2     /* 1 */
```

Integer division truncates toward zero. `%` is for integer operands. For negative values, quotient/remainder follow the language rule `a == (a/b)*b + a%b` when division is defined.

## 5.3 Prefix and postfix

```c
int i = 5;
int a = ++i;   /* i=6, a=6 */
int b = i++;   /* b=6, then i=7 */
```

Avoid clever expressions that modify and read an object without sequencing. For example, `i = i++ + 1` has undefined behavior in C. Split side effects into separate statements.

## 5.4 Short-circuiting

```c
if (p != NULL && p->value > 0) { ... }
```

The right operand is evaluated only if needed. This is useful for safety checks. A single `&` would evaluate both and is not a substitute.

## 5.5 Precedence is not evaluation order

Precedence determines grouping, not which operand is evaluated first. Function-argument evaluation order is generally unspecified. Parenthesize for clarity, but do not use parentheses as if they establish all sequencing.

## 5.6 Conversions

Usual arithmetic conversions find a common type for operands. Explicit cast:

```c
double mean = (double)sum / count;
```

A cast can suppress a warning but does not make an invalid conversion safe. Check range before narrowing.

---

# 6. Control structures

## 6.1 Selection

```c
if (x < 0) {
    puts("negative");
} else if (x == 0) {
    puts("zero");
} else {
    puts("positive");
}
```

Zero is false; nonzero is true. Assignment inside a condition is legal but error-prone: `if (x = 5)` assigns and is true. Use `==` for comparison.

## 6.2 `switch`

```c
switch (choice) {
case 1:
    add();
    break;
case 2:
    remove_item();
    break;
default:
    puts("invalid choice");
}
```

Cases require integral constant expressions. Without `break`, execution falls through to later cases; use it intentionally and document intentional fallthrough.

## 6.3 Loops

```c
for (int i = 0; i < n; ++i) { ... }

while (condition) { ... }

do { ... } while (condition);  /* body executes at least once */
```

Loop correctness:

- initialization establishes an invariant;
- condition and invariant imply safe useful work;
- update makes progress;
- a variant/bound proves termination;
- on exit, invariant plus negated condition gives the result.

`break` exits the nearest loop/switch. `continue` skips to the next iteration. `return` exits the function. Avoid `goto` except narrow cleanup/state-machine cases where it improves correctness.

## 6.4 Sentinel loop

```c
long sum = 0;
int x;
while (scanf("%d", &x) == 1 && x != 0) {
    sum += x;
}
```

Check input success and sentinel separately. Otherwise invalid input may leave a stale variable and create an infinite loop.

---

# 7. Functions, parameters, and modular design

## 7.1 Prototype, call, definition

```c
int add(int x, int y);        /* declaration/prototype */

int main(void) {
    int result = add(2, 3);   /* call */
    printf("%d\n", result);
}

int add(int x, int y) {      /* definition */
    return x + y;
}
```

- Arguments are expressions at the call.
- Parameters are local objects in the called function.
- C passes arguments **by value**.
- To let a function modify a caller object, pass its address by value.

```c
void swap(int *a, int *b) {
    int t = *a;
    *a = *b;
    *b = t;
}
```

## 7.2 Function contract

State preconditions, postconditions, side effects, and errors:

```c
/* Pre: a points to at least n ints.
   Post: returns their sum; does not modify a.
   Caveat: signed overflow must not occur. */
long long sum_array(const int *a, size_t n);
```

`const int *a` means the function does not modify integers through `a`; it is documentation plus compiler checking, not deep immutability of the whole program.

## 7.3 Return values

Do not return the address of an automatic local object:

```c
int *bad(void) {
    int x = 4;
    return &x;      /* dangling after return */
}
```

Return by value, let the caller provide storage, use allocated storage with clear ownership, or use static storage only when its lifetime/shared-state tradeoff is appropriate.

## 7.4 Variadic functions

The slides show `<stdarg.h>`. Variadic arguments lose ordinary type/count information, so the function needs a convention such as a count or format string.

```c
double average(size_t n, ...) {
    va_list ap;
    va_start(ap, n);
    double sum = 0;
    for (size_t i = 0; i < n; ++i)
        sum += va_arg(ap, double);
    va_end(ap);
    return n ? sum / n : 0.0;
}
```

Passing an unexpected type and reading it as another is undefined behavior.

---

# 8. Recursion

## 8.1 Necessary parts

- base/termination case;
- reduction to a smaller valid instance;
- recursive hypothesis/contract;
- combination of subresult;
- proof that reduction reaches the base.

## 8.2 Factorial

```c
unsigned long long factorial(unsigned n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}
```

`T(n)=T(n-1)+Θ(1)=Θ(n)` time and `Θ(n)` call stack. Numeric overflow occurs quickly even though recursion is logically correct.

## 8.3 Fibonacci

```c
unsigned long long fib(unsigned n) {
    if (n < 2) return n;
    return fib(n - 1) + fib(n - 2);
}
```

Naive recursion recomputes subproblems: exponential time, `Θ(n)` maximum stack. Iteration or memoization gives `Θ(n)` time; fast doubling can give `O(log n)` arithmetic steps.

## 8.4 Euclid’s GCD

```c
int gcd(int a, int b) {
    if (b == 0) return a < 0 ? -a : a;
    return gcd(b, a % b);
}
```

Invariant: common divisors of `(a,b)` equal common divisors of `(b,a mod b)`. Time is logarithmic in the magnitude of the smaller operand in the standard analysis.

## 8.5 Tower of Hanoi

To move `n` disks from source `S` to destination `D` using auxiliary `A`:

1. move `n-1` from `S` to `A`;
2. move largest from `S` to `D`;
3. move `n-1` from `A` to `D`.

```c
void hanoi(unsigned n, char src, char aux, char dst) {
    if (n == 0) return;
    hanoi(n - 1, src, dst, aux);
    printf("move %u: %c -> %c\n", n, src, dst);
    hanoi(n - 1, aux, src, dst);
}
```

$$
T(n)=2T(n-1)+1=2^n-1.
$$

This is both the algorithm’s move count and the minimum possible: the largest disk requires all `n-1` disks moved away and later restored above it.

## 8.6 Recursive binary search

```c
int binary_search(const int a[], int low, int high, int x) {
    if (low > high) return -1;
    int mid = low + (high - low) / 2;
    if (a[mid] == x) return mid;
    if (x < a[mid]) return binary_search(a, low, mid - 1, x);
    return binary_search(a, mid + 1, high, x);
}
```

Precondition: ascending sorted array and valid bounds. Time `O(log n)`, recursive stack `O(log n)`; iterative form uses `O(1)` auxiliary space.

---

# 9. One-dimensional arrays and algorithms

## 9.1 Representation

```c
int a[5] = {10, 20, 30, 40, 50};
```

Elements are contiguous and indexed `0..4`. `a[i]` is defined as `*(a+i)` when valid. Access outside the array is undefined behavior; C performs no automatic bounds checking.

`sizeof a / sizeof a[0]` gives element count only where `a` is still an actual array. In a function parameter `int a[]`, it is adjusted to `int *a`, so pass the length separately.

## 9.2 Traversal and sum

```c
long long sum(const int a[], size_t n) {
    long long s = 0;
    for (size_t i = 0; i < n; ++i) s += a[i];
    return s;
}
```

Time `Θ(n)`, auxiliary space `Θ(1)`.

## 9.3 Linear search

```c
int linear_search(const int a[], size_t n, int x) {
    for (size_t i = 0; i < n; ++i)
        if (a[i] == x) return (int)i;
    return -1;
}
```

Best `Θ(1)`, worst/average `Θ(n)`. Works whether sorted or not.

## 9.4 Selection-style sorting from the slides

```c
void selection_sort(int a[], size_t n) {
    for (size_t i = 0; i < n; ++i) {
        size_t min = i;
        for (size_t j = i + 1; j < n; ++j)
            if (a[j] < a[min]) min = j;
        int t = a[i]; a[i] = a[min]; a[min] = t;
    }
}
```

Invariant: before iteration `i`, `a[0..i-1]` contains the `i` smallest values in sorted order. `Θ(n²)` comparisons, `O(n)` swaps, `O(1)` extra space, normally unstable.

## 9.5 Insertion into an array

Insert `x` at index `pos`, with capacity available:

```c
int insert_at(int a[], size_t *n, size_t capacity,
              size_t pos, int x) {
    if (pos > *n || *n == capacity) return 0;
    for (size_t i = *n; i > pos; --i) a[i] = a[i - 1];
    a[pos] = x;
    ++*n;
    return 1;
}
```

Worst `Θ(n)` due to shifting. In sorted insertion, first find position (binary search can reduce comparisons) but shifting still costs `Θ(n)`.

## 9.6 Deletion

```c
int delete_at(int a[], size_t *n, size_t pos) {
    if (pos >= *n) return 0;
    for (size_t i = pos; i + 1 < *n; ++i) a[i] = a[i + 1];
    --*n;
    return 1;
}
```

Order-preserving deletion costs `Θ(n)` worst case. If order does not matter, replace with the last element and decrement length in `O(1)`.

---

# 10. Two-dimensional arrays and matrices

```c
int a[3][4];
```

C stores this as three contiguous rows of four `int`s in row-major order. `a[i][j]` is equivalent to `*(*(a+i)+j)`.

When passing it, all dimensions except the first must be known:

```c
void print_matrix(size_t rows, size_t cols, int a[rows][cols]);
```

## 10.1 Addition

Defined only for equal dimensions:

```c
for (size_t i = 0; i < r; ++i)
    for (size_t j = 0; j < c; ++j)
        out[i][j] = a[i][j] + b[i][j];
```

Time `Θ(rc)`.

## 10.2 Multiplication

If `A` is `m×n` and `B` is `n×p`, then `C` is `m×p`:

$$
C_{ij}=\sum_{k=0}^{n-1} A_{ik}B_{kj}.
$$

```c
for (size_t i = 0; i < m; ++i)
    for (size_t j = 0; j < p; ++j) {
        c[i][j] = 0;
        for (size_t k = 0; k < n; ++k)
            c[i][j] += a[i][k] * b[k][j];
    }
```

Classical time `Θ(mnp)`; result storage `Θ(mp)`. Verify inner dimensions and overflow.

## 10.3 Transpose

`B[j][i]=A[i][j]`. Out-of-place time `Θ(rc)` and space `Θ(rc)`. A square matrix can transpose in place by swapping only above/below diagonal:

```c
for (size_t i = 0; i < n; ++i)
    for (size_t j = i + 1; j < n; ++j) {
        int t = a[i][j]; a[i][j] = a[j][i]; a[j][i] = t;
    }
```

---

# 11. Pointers

## 11.1 Address and dereference

```c
int x = 10;
int *p = &x;
*p = 20;        /* modifies x */
```

- `&x`: address of `x`;
- `int *p`: pointer intended to point to `int`;
- `*p`: referenced object, only valid if `p` points to a live suitable object;
- `NULL`: null pointer constant/conventional invalid “no object” state;
- uninitialized/dangling/out-of-bounds pointers must not be dereferenced.

## 11.2 Pointer arithmetic

If `p=&a[i]`, then `p+1` points to `a[i+1]`, scaled by element size. Pointer arithmetic is defined only within the same array object or one-past its end; one-past may be compared/subtracted but not dereferenced.

```c
for (int *p = a; p != a + n; ++p)
    printf("%d\n", *p);
```

## 11.3 Arrays are not pointers

An array is an object containing elements. In most expressions its name converts to a pointer to the first element, but differences remain:

- `sizeof array` is whole array size; `sizeof pointer` is pointer size;
- array assignment is not permitted;
- `&array` has pointer-to-array type;
- string arrays own writable storage, pointer-to-literal variables do not.

## 11.4 Pointer parameters

```c
int divide(int num, int den, int *q, int *r) {
    if (den == 0 || q == NULL || r == NULL) return 0;
    *q = num / den;
    *r = num % den;
    return 1;
}
```

C is still pass-by-value: copies of the pointer values are passed, and those copies refer to caller objects.

## 11.5 `const` placements

- `const int *p`: cannot modify `*p` through `p`; `p` may change.
- `int *const p`: fixed pointer; pointed value may change.
- `const int *const p`: neither through this name.

## 11.6 Aliasing and lifetime

A pointer does not own or extend lifetime automatically. Common bugs:

- returning address of local;
- using a pointer after `free`;
- double `free`;
- storing pointer into a buffer later reallocated;
- violating bounds/alignment/effective-type rules;
- assuming two pointer parameters never alias.

---

# 12. Strings and the ten supplied string programs

## 12.1 Representation

A C string is a sequence of `char` terminated by `\0` within accessible storage.

```c
char a[] = "hello";       /* six bytes, writable array */
const char *p = "hello";  /* points to string literal; do not modify */
```

An array `{'h','e','l','l','o'}` without `\0` is not a valid C string. Printing it with `%s` reads beyond bounds and is undefined—the supplied `string1.c` intentionally exposes this distinction, but some of its prints are unsafe.

## 12.2 Manual core operations

```c
size_t my_strlen(const char *s) {
    const char *p = s;
    while (*p) ++p;
    return (size_t)(p - s);
}

char *my_strcpy(char *dst, const char *src) {
    char *ret = dst;
    while ((*dst++ = *src++) != '\0') { }
    return ret;
}

int my_strcmp(const char *a, const char *b) {
    while (*a && (unsigned char)*a == (unsigned char)*b) {
        ++a; ++b;
    }
    return (unsigned char)*a - (unsigned char)*b;
}
```

`strcpy`/`strcat` do not know destination capacity. The caller must prove enough room. Use length checks or size-aware designs; `strncpy` is not a universal safe replacement because it may omit termination and pads unnecessarily.

## 12.3 Comparison

`a == b` for character arrays/pointers compares addresses after array conversion, not string content. `strcmp(a,b)` returns negative, zero, or positive; do not assume it returns exactly `-1` or `1`.

## 12.4 Substring search

The supplied `string10.c` shows naive matching. Correct straightforward version:

```c
const char *find_substring(const char *text, const char *pat) {
    if (*pat == '\0') return text;
    for (const char *s = text; *s; ++s) {
        const char *a = s, *b = pat;
        while (*a && *b && *a == *b) { ++a; ++b; }
        if (*b == '\0') return s;
    }
    return NULL;
}
```

Worst-case naive time `O(nm)`. Algorithms such as KMP preprocess pattern to avoid rechecking and run in `O(n+m)`, covered in DSA rather than these C slides.

## 12.5 Conversions

`atoi` gives no reliable error reporting. Prefer `strtol`/`strtoul`, checking end pointer, `errno`, and range.

---

# 13. Structures, unions, enums, and typedef

## 13.1 Structure

```c
struct point {
    int x;
    int y;
};

struct point p = { .x = 3, .y = 4 };
struct point *q = &p;
printf("%d %d\n", p.x, q->y);
```

A structure groups named fields. Structure assignment copies members by value, including embedded arrays as part of the whole struct. Passing a large struct by value copies it; a `const` pointer can avoid copying.

## 13.2 Nested structures and arrays

```c
struct rectangle {
    struct point low;
    struct point high;
};

struct contact contacts[20];
```

The supplied contact application demonstrates CRUD-like operations over an array of structs with linear search. It must also enforce capacity and bounded input—its `i++` can otherwise overflow the fixed array.

## 13.3 `typedef`

```c
typedef struct point Point;
```

This creates an alias, not a new runtime object. In C it can remove repeated `struct` spelling. Do not hide pointer ownership merely to make a pointer look like a value.

## 13.4 Padding and layout

Compilers may insert padding for alignment, so `sizeof(struct)` may exceed sum of field sizes. Do not serialize raw structs as a portable interchange format: padding, endianness, integer sizes, alignment, and version changes differ.

## 13.5 Union and enum

A union overlays members in the same storage; track which member is active. An enum gives named integral constants, useful for states/tags. A safe tagged-union design stores an enum tag beside the union and accesses the matching member.

---

# 14. File I/O and the fourteen supplied programs

## 14.1 Streams and modes

```c
FILE *fp = fopen("data.txt", "r");
if (!fp) {
    perror("data.txt");
    return 1;
}
/* use fp */
if (fclose(fp) == EOF) { /* close/flush error */ }
```

Modes: `r`, `w`, `a`; add `+` for update and `b` for binary where relevant. `w` truncates/create; `a` writes at end; `r` requires existence.

## 14.2 Character and line I/O

```c
int ch;
while ((ch = fgetc(fp)) != EOF) putchar(ch);
if (ferror(fp)) { /* I/O error */ }
```

`fgetc` returns `int`, not `char`, so it can represent every unsigned-char value plus `EOF`.

Do not write `while (!feof(fp))`. EOF is set only after a read attempt fails, so that pattern often processes stale data once. Test the read function directly:

```c
char line[256];
while (fgets(line, sizeof line, fp)) {
    fputs(line, stdout);
}
```

The provided `demo_feof.c`, `file5.c`, `file6.c`, and the text contact loader illustrate this classic trap.

## 14.3 Formatted files

```c
while (fscanf(fp, "%79s %d %79s", name, &age, phone) == 3) {
    /* complete record */
}
```

Whitespace-delimited formats cannot represent names containing spaces without escaping/quoting or a line-based parser.

## 14.4 Binary I/O

```c
size_t written = fwrite(a, sizeof a[0], n, fp);
size_t read = fread(a, sizeof a[0], n, fp);
```

Check returned element counts. Raw binary arrays of fixed-width numeric types may still have endianness/representation portability issues. Raw structs are especially nonportable.

## 14.5 Random access

- `fseek(fp, offset, SEEK_SET/CUR/END)` repositions where supported;
- `ftell` reports a position representation;
- `rewind` returns to beginning and clears error/EOF indicators;
- for fully portable large-file/structured data, do not assume arbitrary arithmetic on text-stream positions.

## 14.6 Redirection

`freopen` can associate a standard stream with a file. Shell redirection is usually cleaner:

```text
program < in.txt > out.txt
```

Always consider buffering and whether closing redirected `stdout` loses unreported flush errors.

---

# 15. Bitwise operations and masks

Use unsigned types for predictable shifts and bit fields.

| Operation | Meaning |
|---|---|
| `x & mask` | retain selected bits |
| `x | mask` | set selected bits |
| `x ^ mask` | toggle selected bits |
| `x & ~mask` | clear selected bits |
| `(x >> k) & mask` | extract field |
| `(value & mask) << k` | place field |

## 15.1 Single bit

```c
uint32_t set_bit(uint32_t x, unsigned b)   { return x |  (UINT32_C(1) << b); }
uint32_t clear_bit(uint32_t x, unsigned b) { return x & ~(UINT32_C(1) << b); }
uint32_t flip_bit(uint32_t x, unsigned b)  { return x ^  (UINT32_C(1) << b); }
int test_bit(uint32_t x, unsigned b)       { return (x >> b) & 1u; }
```

Require `b<32`. Shifting by a negative amount or at least the width is undefined. Left-shifting into/through the sign bit of signed `int` is dangerous/undefined; several supplied examples use `1 << 31` and signed left shifts, which should be rewritten with unsigned types.

## 15.2 Packing fields from `encodeDecode.c`

Layout:

```text
bits  0..19 : roll    (20 bits)
bits 20..23 : subject (4 bits)
bits 24..31 : score   (8 bits)
```

```c
uint32_t encode(uint32_t roll, uint32_t subject, uint32_t score) {
    return (roll & 0xFFFFFu)
         | ((subject & 0xFu) << 20)
         | ((score & 0xFFu) << 24);
}

void decode(uint32_t x, uint32_t *roll,
            uint32_t *subject, uint32_t *score) {
    *roll = x & 0xFFFFFu;
    *subject = (x >> 20) & 0xFu;
    *score = (x >> 24) & 0xFFu;
}
```

Validate semantic ranges before packing; masking silently truncates out-of-range values.

## 15.3 XOR swap

The supplied code demonstrates XOR swap, but a temporary-variable swap is clearer and handles aliasing. If `x` and `y` point to the same object, XOR swap zeros it. Optimizing compilers generate efficient code for the ordinary form.

## 15.4 Reversing bits

The supplied algorithm compares low/high bits with masks and toggles when they differ. Complexity is `Θ(w)` for word width `w`; treat the word as unsigned and derive the high mask from width rather than hardcoding 31.

---

# 16. Dynamic memory — standard-core supplement

The local PDF sequence stops at pointers, but allocation is a high-yield C viva continuation.

```c
size_t n = 100;
int *a = malloc(n * sizeof *a);
if (!a) { /* allocation failed */ }
/* use a[0..n-1] */
free(a);
a = NULL;
```

- `malloc`: uninitialized allocated bytes;
- `calloc`: array allocation with all bytes zero;
- `realloc`: resize, possibly moving;
- `free`: end allocated lifetime.

Check multiplication overflow before allocation:

```c
if (n > SIZE_MAX / sizeof *a) { /* impossible size */ }
```

Safe `realloc` pattern:

```c
int *tmp = realloc(a, new_n * sizeof *a);
if (tmp) a = tmp;
else { /* old a is still valid */ }
```

Errors:

- leak: ownership lost without `free`;
- use-after-free: dereference after lifetime ends;
- double free;
- invalid free of stack/static/interior pointer;
- buffer overflow;
- assuming `realloc` never moves.

Define ownership: who allocates, who frees, and whether a pointer is borrowed or owning.

---

# 17. Preprocessor and separate compilation

## 17.1 Macros

```c
#define SQUARE(x) ((x) * (x))
```

Even parenthesized, `SQUARE(i++)` evaluates `i++` twice. Prefer a function or `static inline` where type checking/single evaluation matters.

## 17.2 Include guards

```c
#ifndef POINT_H
#define POINT_H

typedef struct { int x, y; } Point;
int distance2(Point a, Point b);

#endif
```

Headers normally contain declarations; one `.c` file contains each externally linked definition. Include what you use; do not include `.c` files as a substitute for linking.

## 17.3 Conditional compilation

```c
#ifdef DEBUG
#define TRACE(...) fprintf(stderr, __VA_ARGS__)
#else
#define TRACE(...) ((void)0)
#endif
```

It is useful for portability/debug builds but too many branches make testing/configuration difficult.

---

# 18. Undefined, unspecified, and implementation-defined behavior

- **Undefined behavior:** standard imposes no requirements; examples include signed overflow, out-of-bounds access, use-after-free, invalid format type, division by zero.
- **Unspecified behavior:** implementation may choose among permitted alternatives without documenting which; example: order of evaluating function arguments.
- **Implementation-defined behavior:** implementation chooses and documents; examples include signedness of plain `char` and right shift of negative signed values.

Undefined behavior is not guaranteed to crash. It may appear to work until optimization/input/platform changes.

High-yield defects in teaching code:

- `gets`;
- `void main`;
- `%d` for `size_t` instead of `%zu`;
- printing non-null-terminated arrays with `%s`;
- `while (!feof(fp))`;
- ignoring `fopen`/read/write return values;
- unbounded `%s`;
- signed `1 << 31` and signed left shifts;
- unchecked fixed-array capacity;
- raw struct persistence assumed portable;
- `atoi` without validation;
- string comparison with `==`.

---

# 19. Exact audit of all 35 supplied C programs

## 19.1 Strings — 10/10

| File | Recall purpose | Important correction/trap |
|---|---|---|
| `string1.c` | array initializers, terminator, `%s`, `sizeof` | several arrays lack `\0`; printing them as strings is undefined |
| `string2.c` | word input using `%s` | add field width; array name already points to first element |
| `string3.c` | line input | `gets` removed; replace with `fgets` |
| `string4.c` | `strcpy`, `strcat`, `strlen`, `strcmp` | verify capacities; use `size_t` for length |
| `string5.c` | textual calculator, `atoi`, `strcmp` | validate input with `strtol`; handle division by zero distinctly |
| `string6.c` | manual copy/length/concat/compare | caller must supply enough destination capacity |
| `string7.c` | terminator-as-condition variants | signed `char` subtraction issue; same capacity concerns |
| `string8.c` | assignment in loop for copy/concat | concise but require careful sequencing and bounds |
| `string9.c` | full/prefix comparison | audit `n` boundary and parameter naming/order |
| `string10.c` | naive substring search | worst `O(nm)`; empty-pattern and restart correctness |

## 19.2 Structures — 7/7

| File | Recall purpose | Important correction/trap |
|---|---|---|
| `struct1.c` | declaration, initialization, member access | bounded string copying/input |
| `struct2.c` | global struct variables, pass by value | globals reduce modularity; `%s` needs width |
| `struct3.c` | nested `point` in rectangle | statements shown at file scope outside function are invalid C; keep executable assignments inside functions |
| `struct4.c` | make/return/add structs | structure return/assignment is by value and valid |
| `struct5.c` | `typedef` aliases | alias does not create a new runtime type/object |
| `struct6.c` | array of structs and function parameter | VLA/support version and bounded input |
| `struct7.c` | phone-book application/search | enforce capacity, safe line input, duplicate policy, persistence/error policy |

## 19.3 Files — 14/14

| File | Recall purpose | Important correction/trap |
|---|---|---|
| `demo_feof.c` | illustrates EOF behavior | classic extra-read problem; test `fgetc` result |
| `file1.c` | `FILE *`, `fopen`, null check, close | error message should match mode/cause; use `perror` |
| `file2.c` | character output with `fputc` | check close/flush error too |
| `file3.c` | character input with `fgetc` | store result in `int`, loop on result |
| `file4.c` | file copy | use `while ((c=fgetc(from)) != EOF)` and check both streams |
| `file5.c` | string line read/write | replace `gets`; loop on `fgets`, not `feof` |
| `file6.c` | `fprintf`/`fscanf` records | loop while conversion count equals expected fields |
| `file7.c` | binary scalar `fwrite`/`fread` | representation/endianness portability |
| `file8.c` | binary 1D array | distinguish requested and returned element counts |
| `file9.c` | binary 2D array | contiguous fixed array; portable format concerns |
| `file10.c` | `fseek`, `ftell`, random access | validate location/range and text/binary semantics |
| `file11.c` | contact persistence text/binary | avoid `feof` loader; raw struct file is nonportable; check capacity/errors |
| `freopen.c` | redirect `stdout` | check `freopen`; flushing/close matters |
| `redirect.c` | redirect `stdin` and `stdout` | shell redirection is often simpler; check returns |

## 19.4 Bitwise — 4/4

| File | Recall purpose | Important correction/trap |
|---|---|---|
| `Bitwise 1.c` | AND/OR/XOR/NOT/shifts/printing | use unsigned; avoid signed overflow in shifts |
| `Bitwise 2.c` | XOR swap, high 16 bits, bit reversal | XOR alias trap; derive width portably; remove unused variables |
| `encodeDecode.c` | pack/unpack roll/subject/score | mask and validate field widths; use `uint32_t` |
| `Sample_Online.c` | bit count/set/reset/next larger same-popcount idea | use unsigned masks and carefully prove boundary/no-next case |

---

# 20. Board-ready explanations

## 20.1 Teach a function using sum `1..n`

Start from repeated code:

```c
int sum = 0;
for (int i = 1; i <= n; ++i) sum += i;
```

Motivation: if several parts of a program need this idea, copying creates duplication and inconsistent fixes. Name the computation:

```c
long long sum_to(int n) {
    long long sum = 0;
    for (int i = 1; i <= n; ++i) sum += i;
    return sum;
}
```

Explain contract (`n>=0`), argument, local variable, return value, call, test cases `0,1,5`, and reuse. Only then compare `n(n+1)/2` and discuss overflow.

## 20.2 Pointer versus ordinary parameter

Draw two boxes:

```text
caller x=5
ordinary call f(x): parameter receives copy 5
pointer call g(&x): parameter receives copy of x's address -> *p names caller x
```

This is not pass-by-reference at the language level; it is pass-by-value of a pointer.

## 20.3 Array/pointer trace

For `int a[]={10,20,30}`:

```text
a      -> &a[0]
a+1    -> &a[1]
*(a+1) -> 20
&a     -> pointer to the whole 3-int array
```

`a+3` is a valid one-past pointer but `*(a+3)` is invalid.

---

# 21. Rapid viva questions

**Compiler versus linker?** Compiler translates/checks each translation unit; linker combines objects/libraries and resolves external symbols.

**Declaration versus definition?** Declaration introduces type/name; definition also provides storage or function body. Every definition is a declaration, but not every declaration is a definition.

**Why `&` in `scanf`?** The function must receive an address to modify caller storage. Arrays commonly decay to a pointer already.

**Why does `%s` need `\0`?** No length is passed; the function reads until terminator, so absence within bounds causes out-of-bounds access.

**Array versus pointer?** Array is contiguous element storage; pointer is an address-valued object. Array expressions often decay, creating syntactic similarities.

**Stack versus heap?** Informal implementation terms: automatic function-local state is commonly stack-managed; dynamic allocation comes from a heap-like allocator. The C standard defines storage durations, not a mandatory physical stack/heap organization.

**What is a dangling pointer?** It retains an address after the referenced object’s lifetime ended.

**Why is `while(!feof(fp))` wrong?** EOF becomes known after a read fails; loop on successful read instead.

**Text versus binary file?** Text streams may translate representations such as newline; binary streams preserve bytes as defined by implementation, but raw numeric/struct bytes are not automatically cross-platform.

**Recursion versus iteration?** Compare clarity, structure, stack depth, auxiliary state, and complexity. Neither is universally superior.

**What is undefined behavior?** A program execution for which C imposes no requirements; compiler may assume it never happens.

**Why use unsigned for bit operations?** Unsigned modulo arithmetic and right shifts are better specified; signed shifts/overflow have traps.

**`struct` versus `union`?** Struct members have distinct storage and coexist; union members overlap and normally only one representation is active.

**Shallow versus deep copy?** Struct assignment copies pointer values, not pointed-to allocations. A deep copy allocates/copies owned referents according to ownership rules.

---

# 22. Final C self-test

- [ ] Write, compile, and explain a conforming minimal program.
- [ ] Trace preprocessing, compilation, assembly, linking, and loading.
- [ ] Match every `printf`/`scanf` conversion to the exact argument type.
- [ ] Distinguish arrays, pointers, strings, and string literals.
- [ ] Explain scope, storage duration, linkage, and lifetime.
- [ ] Trace precedence separately from evaluation order/side effects.
- [ ] Prove one loop invariant and one recursive termination argument.
- [ ] Implement factorial, GCD, Hanoi, binary search, and state complexity.
- [ ] Implement array traversal/search/sort/insert/delete safely.
- [ ] Implement matrix addition/multiplication/transpose with dimension checks.
- [ ] Explain pointer arithmetic, `const`, aliasing, and dangling pointers.
- [ ] Implement bounded string input and manual string operations.
- [ ] Explain struct copy, padding, typedef, and raw serialization limits.
- [ ] Write correct stream loops for characters, lines, records, and binary arrays.
- [ ] Build and explain masks for set/clear/test/extract/pack.
- [ ] Diagnose every modern-correction item in §18.
- [ ] Account for all 35 supplied programs using the audit in §19.

