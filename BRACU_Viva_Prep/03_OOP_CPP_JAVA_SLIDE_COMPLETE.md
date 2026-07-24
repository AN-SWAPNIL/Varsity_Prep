# Bismillah.

# Object-Oriented Programming: C++ and Java — Current-Slide Viva Recall

> **Current source basis (re-audited 24 July 2026):** `107-OOP/C++_Merged.pdf` (**192 pages**) and `107-OOP/Java-merged.pdf` (**244 pages**), for **436 current pages**. The C++ merge contains fourteen lecture segments. The Java merge concentrates on platform/object fundamentals, arrays and language details, strings, inheritance/equality, packages/interfaces/exceptions, threads, and generics/collections. The obsolete inventory of 178 removed `.java` files, modules, Apache POI, and removed networking examples has been deleted. A few compact standard-Java supplements remain only when they are likely viva follow-ups and are labeled as such.

## How to answer an OOP viva question

Use four short moves:

1. **Define it:** one precise sentence.
2. **Explain the mechanism:** what is selected, copied, hidden, allocated, or dispatched, and when.
3. **Give a tiny example:** preferably one line of code or one object relationship.
4. **State the trap or trade-off:** this proves understanding rather than memorization.

Example: “Runtime polymorphism means a base reference or pointer invokes the override belonging to the actual object. In C++ the base method must be `virtual`; in Java ordinary instance methods are dynamically dispatched by default. Static methods are hidden, not overridden.”

---

# Part I — OOP foundations

## Object, class, state, behavior, and identity

- A **class** is a user-defined type or blueprint that declares representation (fields/data members), behavior (methods/member functions), and invariants.
- An **object** is a runtime instance of a class.
- **State** is the current value of its fields.
- **Behavior** is what its methods do.
- **Identity** distinguishes two objects even when their visible state is equal.

```text
Class: BankAccount
State: owner, balance
Behavior: deposit(), withdraw()
Invariant: balance must not become negative
Objects: accountA and accountB have separate identities
```

An object is not merely “data plus functions.” Good class design protects a valid state and exposes operations meaningful in the problem domain.

## The four central ideas

### Encapsulation

Encapsulation bundles state and behavior and controls access to the representation. Data hiding is one consequence of encapsulation.

```java
final class Account {
    private long balance;

    Account(long opening) {
        if (opening < 0) throw new IllegalArgumentException();
        balance = opening;
    }

    public void deposit(long amount) {
        if (amount <= 0) throw new IllegalArgumentException();
        balance += amount;
    }

    public long balance() { return balance; }
}
```

Why not make `balance` public? A caller could set it to an invalid value and bypass validation.

### Abstraction

Abstraction presents essential behavior and hides irrelevant implementation detail. An interface such as `Shape.area()` says **what** is available; subclasses decide **how** it is computed.

### Inheritance

Inheritance creates an **is-a** relationship: a `Rectangle` is a `Shape`. It supports reuse and substitutability, but it also creates coupling. Use it when the subtype truly satisfies the supertype contract, not merely to reuse a few lines.

### Polymorphism

Polymorphism means “one interface, multiple implementations.”

- **Compile-time/ad-hoc polymorphism:** overload resolution and C++ operator overloading.
- **Runtime/subtype polymorphism:** an overridden method is selected from the actual object at runtime.
- **Parametric polymorphism:** C++ templates and Java generics apply an abstraction to many types.

Do not say that overloading and overriding are the same. Overloading selects among different parameter lists at compile time; overriding replaces inherited instance behavior and enables runtime dispatch.

## Relationships between objects

- **Association:** one object knows or uses another; e.g., `Teacher` teaches `Course`.
- **Aggregation:** weak whole–part relation; parts may outlive the whole, e.g., `Department` and `Teacher`.
- **Composition:** strong ownership; the whole controls the part's lifetime, e.g., a `House` owns its `Room` objects.
- **Dependency:** temporary use, often through a parameter or local variable.
- **Inheritance:** an is-a/type relationship.

Viva line: “Prefer composition for has-a behavior because it reduces coupling; choose inheritance only when substitutability is valid.”

## Small design principles worth saying aloud

- Keep representation private and expose intention-revealing operations.
- Aim for **high cohesion** inside a class and **low coupling** between classes.
- **Single responsibility:** one main reason for a class to change.
- **Open/closed:** extend behavior through abstractions without repeatedly modifying stable code.
- **Liskov substitution:** code expecting a base type must remain correct for every subtype.
- **Interface segregation:** prefer focused interfaces over one large interface.
- **Dependency inversion:** high-level policy should depend on abstractions, not concrete details.
- Prefer immutability when state does not need to change.
- In C++, prefer RAII/value types and the Rule of Zero; in Java, close external resources deterministically with try-with-resources.

## C++ versus Java at a glance

| Issue | C++ | Java |
|---|---|---|
| Compilation | Native code is typical | Source → bytecode → JVM/JIT machine code |
| Object variables | Can hold an object value directly | Class variable holds a reference value |
| Memory | Automatic storage, RAII, and explicit dynamic allocation | Heap objects plus garbage collection |
| Destruction | Deterministic destructor at lifetime end | GC is nondeterministic; use `close()` for resources |
| Inheritance | Multiple class inheritance is allowed | One superclass; multiple interfaces |
| Runtime dispatch | Base function must normally be `virtual` | Ordinary overridable instance methods dispatch dynamically |
| Operator overloading | User-defined operators supported | No general user-defined operator overloading |
| Generic programming | Templates instantiate code, including primitives | Generics are mainly erased and require reference types |
| Parameters | Value, pointer, or reference | Always pass-by-value, including copied reference values |
| Exceptions | No checked-exception category | Checked and unchecked exceptions |
| Root class | No universal mandatory root | Every class ultimately extends `Object` |

---

# Part II — C++ lecture-complete recall

## Lecture 1 — Overview of C++ and the OOP model

### Class versus struct

Both can contain data, functions, constructors, destructors, operators, and inheritance. The default differs:

- `class`: members and base inheritance are `private` by default.
- `struct`: members and base inheritance are `public` by default.

```cpp
struct S { int x; };       // x is public
class C { int x; };        // x is private
```

Conventionally, a `struct` represents a simple record/value and a `class` protects invariants, but the language capabilities are nearly identical.

### Basic program and access control

```cpp
#include <iostream>

class Counter {
    int value;                         // private by default
public:
    Counter() : value(0) {}
    void increment() { ++value; }
    int get() const { return value; }
};

int main() {
    Counter c;
    c.increment();
    std::cout << c.get() << '\n';      // 1
}
```

### Namespace and scope resolution

A namespace prevents global name collisions. `::` qualifies a namespace/class member and can select a hidden global name.

```cpp
#include <iostream>
int count = 1;

namespace first { int count = 2; }

int main() {
    int count = 3;
    std::cout << count << ' '          // local: 3
              << ::count << ' '        // global: 1
              << first::count << '\n';// namespace: 2
}
```

Prefer `std::cout` or narrow `using std::cout;` declarations in headers; `using namespace std;` in a header can pollute every including translation unit.

### Console I/O

- `std::cin >> x` performs formatted extraction and normally skips leading whitespace.
- `std::cout << x` performs insertion.
- `std::cerr` is the standard error stream and is normally unbuffered/unit-buffered.
- `std::clog` is a buffered logging stream.
- `std::wcin`, `std::wcout`, `std::wcerr`, and `std::wclog` are wide-character variants.

Important `cin` trap: `operator>>` leaves the newline behind, so a following `getline` may read an empty line. Use `std::getline(std::cin >> std::ws, line)`.

### C versus C++ points from the lecture

- Modern C++ headers omit `.h`: `<iostream>`, `<cstring>`, `<cmath>`.
- C++ requires a declared return type and supports `bool`, `true`, and `false`.
- Variables may be introduced near first use.
- Function declarations/prototypes enable type checking before calls.
- `//` is a single-line comment; `/* ... */` is a block comment.

## Lecture 2 — Introducing classes

### Constructors

A constructor establishes the initial valid state. It has the class name and no return type. It is called when an object is created.

```cpp
class Point {
    int x, y;
public:
    Point() : Point(0, 0) {}             // delegating constructor
    Point(int x, int y) : x(x), y(y) {}  // member-initializer list
};
```

Prefer an initializer list: members are initialized directly rather than default-initialized and then assigned. `const` and reference members must be initialized there.

### Destructor and lifetime

A destructor `~ClassName()` runs when an object's lifetime ends. It has no return type, parameters, or overloads.

- Local automatic object: destroyed when its scope ends.
- Temporary: destroyed according to temporary-lifetime rules.
- Dynamically allocated object: destroyed by matching `delete`.
- Static/global object: destroyed during program shutdown, in reverse construction order within a translation unit.

Its central use is releasing owned resources. Modern C++ wraps resources in RAII objects such as `std::vector`, `std::string`, and `std::unique_ptr`, reducing manual cleanup.

### Object pointers

Use `.` with an object and `->` with a pointer:

```cpp
Point p(2, 3);
Point* q = &p;
// p.show();
// q->show();       // equivalent to (*q).show()
```

Pointer arithmetic advances in units of the pointed-to type and is valid only within an array (or one past it).

### Union and anonymous union

A union's non-static data members overlap the same storage; normally only the active member may be read safely. Unlike a regular class, it cannot be a base or derived class and cannot have virtual functions. An anonymous union exposes its members directly in the enclosing scope.

Modern safe alternative for “one of several types”: `std::variant<Ts...>`.

### Inline functions

`inline` permits identical definitions in multiple translation units and suggests—but does not force—call-site expansion. A function defined inside a class definition is implicitly inline. Modern optimizers decide actual inlining; “inline always makes it faster” is not correct.

## Lecture 3 — Assignment, copying, parameters, returns, and friends

### Copy initialization versus assignment

```cpp
T b = a;   // initialization: invokes copy constructor
T c(a);    // initialization: invokes copy constructor
c = a;     // existing object: invokes copy-assignment operator
```

Compiler-generated copying performs memberwise copying. For a raw owning pointer, that is a shallow copy: two objects point to one allocation, leading to aliasing, double deletion, or dangling pointers.

### Rule of Three, Five, and Zero

- If a class manually owns a resource and defines any of destructor, copy constructor, or copy assignment, it usually needs all three: **Rule of Three**.
- In C++11+, also consider move constructor and move assignment: **Rule of Five**.
- Best default: store resources in standard RAII members so none of those five needs custom code: **Rule of Zero**.

### Complete runnable ownership/copying example

```cpp
#include <algorithm>
#include <cstddef>
#include <iostream>
#include <utility>

class Buffer {
    std::size_t size_{};
    int* data_{};
public:
    explicit Buffer(std::size_t n)
        : size_(n), data_(n ? new int[n]{} : nullptr) {}

    ~Buffer() { delete[] data_; }

    Buffer(const Buffer& other)
        : Buffer(other.size_) {
        if (size_ != 0)
            std::copy(other.data_, other.data_ + size_, data_);
    }

    Buffer& operator=(const Buffer& other) {
        if (this != &other) {
            Buffer copy(other);   // deep copy
            swap(copy);           // old resource dies with copy
        }
        return *this;
    }

    Buffer(Buffer&& other) noexcept
        : size_(std::exchange(other.size_, 0)),
          data_(std::exchange(other.data_, nullptr)) {}

    Buffer& operator=(Buffer&& other) noexcept {
        if (this != &other) {
            delete[] data_;
            size_ = std::exchange(other.size_, 0);
            data_ = std::exchange(other.data_, nullptr);
        }
        return *this;
    }

    void swap(Buffer& other) noexcept {
        std::swap(size_, other.size_);
        std::swap(data_, other.data_);
    }

    int& operator[](std::size_t i) { return data_[i]; }
    const int& operator[](std::size_t i) const { return data_[i]; }
};

int main() {
    Buffer a(2);
    a[0] = 7;
    Buffer b = a;       // deep copy
    b[0] = 99;
    std::cout << a[0] << ' ' << b[0] << '\n'; // 7 99
}
```

In real code, `std::vector<int>` would give Rule-of-Zero behavior with much less risk.

### Parameter passing

- `void f(T x)`: copy/move a value; changes affect only `x`.
- `void f(T& x)`: modifiable reference; no copy.
- `void f(const T& x)`: read-only reference; avoids copying and accepts temporaries.
- `void f(T* x)`: pointer may be null and uses `->`.

The old slide wording that a by-value copy “does not call a constructor” is historical/oversimplified. Semantically, the parameter is initialized; copy elision may remove some physical copies.

Returning an object by value is normal modern C++. Copy elision/NRVO and moves make it efficient. Never return a reference or pointer to a destroyed local object.

### Friend

A `friend` is not a class member, but it is granted access to private/protected members. Typical cases are symmetric operators, stream insertion/extraction, or a function coordinating two classes.

Friendship is explicit, not inherited, not transitive, and not reciprocal.

## Lecture 4 — Arrays, pointers, dynamic allocation, `this`, and references

### Arrays of objects

```cpp
#include <array>
struct Item {
    int id;
    explicit Item(int id = 0) : id(id) {}
};

int main() {
    std::array<Item, 3> a{Item{1}, Item{2}, Item{3}};
}
```

A built-in array default-constructs each element unless each initializer is supplied. Prefer `std::array` for fixed size and `std::vector` for dynamic size.

### `this`

Inside a non-static member function, `this` points to the current object. It resolves shadowing (`this->x = x`) and permits returning the current object (`return *this`). Static member functions have no `this`.

### `new` and `delete`

```cpp
Widget* p = new Widget(7);
delete p;

Widget* a = new Widget[10];
delete[] a;                         // array form must match
```

Modern `new` throws `std::bad_alloc` on failure. `new (std::nothrow) T` returns `nullptr`. Never mix `new/delete` with `malloc/free`; never use `delete` for an array created with `new[]`.

Prefer:

```cpp
auto one = std::make_unique<Widget>(7);
std::vector<Widget> many(10);
```

### References

A reference is an alias and normally must be initialized. It is not reseatable.

```cpp
void square(int& x) { x *= x; }

int main() {
    int n = 5;
    int& alias = n;
    square(alias);                 // n becomes 25
}
```

Do not return a reference to a local variable. A `const T&` may bind to a temporary and extend its lifetime in specific initialization contexts.

## Lecture 5 — Function/constructor overloading, defaults, and ambiguity

### Overloading rules

Functions may share a name when their parameter lists differ sufficiently. Return type alone cannot distinguish overloads.

Overload resolution considers exact matches, promotions, standard conversions, user-defined conversions, and ellipsis. If no unique best viable function exists, compilation fails as ambiguous.

```cpp
void print(int);
void print(double);
// int print(int); // return type alone cannot overload void print(int)
```

Constructors are commonly overloaded for flexible creation and array support. A destructor cannot be overloaded.

### Copy constructor

Canonical form:

```cpp
T(const T& other);
```

The `const` reference avoids recursively copying the parameter and accepts const objects. It is used when a new object is initialized from an existing object; assignment uses `operator=`.

### Default arguments

```cpp
double area(double length, double width = 0.0);
```

- After the first defaulted parameter, every parameter to its right must also have a default.
- Specify the default in one visible declaration, not both declaration and definition.
- Defaults are substituted at the call site and are statically bound.
- Combining overloads and defaults can create ambiguity.

### Common ambiguities

- `f(float)` and `f(double)`, called with `int`: neither conversion may be better.
- `f(int)` and `f(int, int = 0)`, called with one argument.
- Value and reference overloads that are equally viable.
- Two user-defined conversions of equal rank.

### Address of an overloaded function

The target function-pointer type selects the overload:

```cpp
void space(int);
void space(int, char);

void (*p1)(int) = space;
void (*p2)(int, char) = space;
```

## Lecture 6 — Operator overloading

Operator overloading gives an existing operator meaning for a user-defined type. It cannot change precedence, associativity, arity, or evaluation rules, and at least one operand must be user-defined.

Operators that cannot be overloaded include `.`, `.*`, `::`, `?:`, `sizeof`, `typeid`, and the preprocessing operators.

### Member versus non-member

- Member binary operator: left operand is implicit `*this`; right operand is the explicit parameter.
- Non-member/friend binary operator: both operands are explicit; useful for symmetry such as `2 + complexNumber`.
- `operator=`, `operator[]`, `operator()`, and `operator->` must be members.

### Complete runnable value-type example

```cpp
#include <iostream>

class Point {
    int x_, y_;
public:
    Point(int x = 0, int y = 0) : x_(x), y_(y) {}

    Point& operator+=(const Point& rhs) {
        x_ += rhs.x_; y_ += rhs.y_;
        return *this;
    }

    friend Point operator+(Point lhs, const Point& rhs) {
        lhs += rhs;
        return lhs;
    }

    Point& operator++() {             // prefix
        ++x_; ++y_; return *this;
    }

    Point operator++(int) {           // postfix dummy int
        Point old(*this);
        ++(*this);
        return old;
    }

    friend bool operator==(const Point& a, const Point& b) {
        return a.x_ == b.x_ && a.y_ == b.y_;
    }

    friend std::ostream& operator<<(std::ostream& out, const Point& p) {
        return out << '(' << p.x_ << ',' << p.y_ << ')';
    }
};

int main() {
    Point p{1, 2}, q{3, 4};
    std::cout << p + q << '\n';       // (4,6)
    std::cout << p++ << ' ' << p << '\n'; // (1,2) (2,3)
}
```

Return `T&` from assignment and prefix increment to support chaining. Postfix normally returns the old value. Preserve the operator's intuitive meaning; surprising overloads are legal but poor design.

### Stream extractor

```cpp
friend std::istream& operator>>(std::istream& in, Point& p);
```

The object must be passed by non-const reference because extraction modifies it. Returning the stream supports chaining and preserves its error state.

## Lecture 7 — Inheritance, access, construction order, and the diamond

### Inheritance access matrix

| Base member | Public inheritance | Protected inheritance | Private inheritance |
|---|---|---|---|
| `public` | public in derived | protected in derived | private in derived |
| `protected` | protected in derived | protected in derived | private in derived |
| `private` | inaccessible directly | inaccessible directly | inaccessible directly |

Private base state still exists inside the derived object; derived code accesses it through accessible base operations.

Default inheritance is private for `class Derived : Base` and public for `struct Derived : Base`.

### Construction/destruction order

1. Virtual base subobjects.
2. Direct base subobjects in declaration order.
3. Data members in declaration order.
4. Derived constructor body.

Destruction is the exact reverse. Initializer-list textual order does not change declaration order.

```cpp
class Derived : public Base {
    Member m;
public:
    Derived(int x) : Base(x), m(x) {}
};
```

### Multiple and multilevel inheritance

- Multilevel: `A <- B <- C`.
- Multiple: `D : public B1, public B2`.
- Hierarchical: multiple derived classes share one base.

In the diamond, non-virtual inheritance gives the most-derived object two copies of the common base. Virtual inheritance makes it share one common base subobject:

```text
Type relationship:

             B
            / \
          D1   D2
            \ /
           Final

Object subobjects:

non-virtual Final = [D1 [B]] + [D2 [B]]   -> two B objects; B member is ambiguous
virtual Final     = [shared B] + [D1] + [D2] -> one B object
```

```cpp
struct B { int value{}; };
struct D1 : virtual B {};
struct D2 : virtual B {};
struct Final : D1, D2 {};             // one B inside Final
```

The most-derived class constructs a virtual base.

## Lecture 8 — C++ stream I/O and formatting

### Stream hierarchy idea

`basic_streambuf` handles low-level buffering. `basic_ios` holds formatting/status; `basic_istream`, `basic_ostream`, and `basic_iostream` support input/output. Character specializations give `istream`, `ostream`, `iostream`, `ifstream`, `ofstream`, and `fstream`.

### Formatting state

Common flags/manipulators:

- alignment: `left`, `right`, `internal`
- base: `dec`, `oct`, `hex`, `showbase`
- floating format: `fixed`, `scientific`, `showpoint`, `setprecision`
- sign/case/bool: `showpos`, `uppercase`, `boolalpha`
- spacing/buffering: `skipws`, `unitbuf`, `flush`, `endl`
- field: `setw`, `setfill`

```cpp
#include <iomanip>
#include <iostream>

int main() {
    std::cout << std::showbase << std::hex << 100 << '\n'; // 0x64
    std::cout << std::dec << std::fixed << std::setprecision(2)
              << 12.345 << '\n';                           // 12.35
    std::cout << std::left << std::setfill('.') << std::setw(8)
              << "hi" << '\n';                            // hi......
}
```

`setw` normally affects only the next formatted field. Other flags such as `fixed` persist until changed. `endl` writes a newline **and flushes**; use `'\n'` when a flush is unnecessary.

The member alternatives are `setf`, `unsetf`, `flags`, `width`, `precision`, and `fill`. A custom parameterless manipulator has the form `std::ostream& f(std::ostream&)`.

## Lecture 9 — C++ file I/O

### File stream classes and modes

- `std::ifstream`: input.
- `std::ofstream`: output.
- `std::fstream`: both.
- modes: `ios::in`, `out`, `app`, `ate`, `trunc`, `binary`.

`app` forces each write to the end. `ate` initially positions at the end but permits later seeking. The old `nocreate` flag in the slides is non-standard/obsolete.

### Correct read loop

Do not write `while (!file.eof())`; EOF becomes known only after a read fails. Make the read itself the condition.

```cpp
#include <fstream>
#include <iostream>
#include <string>

int main() {
    std::ifstream in("input.txt");
    if (!in) {
        std::cerr << "cannot open input.txt\n";
        return 1;
    }
    std::string line;
    while (std::getline(in, line)) {
        std::cout << line << '\n';
    }
    if (in.bad()) return 2;            // genuine I/O failure
}
```

### Formatted and unformatted I/O

- formatted: `>>`, `<<`
- character/block: `get`, `put`, `read`, `write`, `gcount`
- look/restore: `peek`, `putback`
- flush: `flush`

Raw binary dumping of a class is unsafe when it contains pointers, virtual functions, padding, endianness-sensitive fields, or versioned data. Serialize defined fields instead.

### Random access and status

- get pointer: `seekg`, `tellg`
- put pointer: `seekp`, `tellp`
- origins: `beg`, `cur`, `end`
- status: `goodbit`, `eofbit`, `failbit`, `badbit`; query with `good()`, `eof()`, `fail()`, `bad()`, `rdstate()`; reset with `clear()`.

`failbit` is a recoverable formatting/logical failure; `badbit` indicates a serious stream error. Seeking after EOF generally requires `clear()` first.

## Lecture 10 — Virtual functions and runtime polymorphism

### Early versus late binding

- **Early/static binding:** target resolved at compile time; examples include overloads, non-virtual C++ methods, and static functions.
- **Late/dynamic binding:** target resolved at runtime from the actual object; implemented in C++ with virtual functions.

A base pointer/reference can point/refer to a derived object. The reverse conversion is not automatically safe.

The dispatch picture:

```text
source expression:       Shape* p = pointer to a Triangle object
                                  |
call:                     p->area()
                                  |
compile time:             verify Shape declares area(); choose virtual slot
                                  |
runtime object/vptr:      select Triangle's final overrider
                                  |
executed function:        Triangle::area()

If area() were non-virtual, the static type Shape* would select Shape::area().
```

Dynamic dispatch therefore needs both facts: the call is through a pointer/reference (not a sliced base value), and the member is virtual. Java ordinary overridable instance methods follow the same runtime-object idea by default; overload resolution and static-method hiding remain compile-time.

### Complete runnable runtime-polymorphism example

```cpp
#include <iostream>
#include <memory>
#include <vector>

class Shape {
public:
    virtual double area() const = 0;   // pure virtual
    virtual const char* name() const = 0;
    virtual ~Shape() = default;        // essential for polymorphic deletion
};

class Rectangle final : public Shape {
    double w_, h_;
public:
    Rectangle(double w, double h) : w_(w), h_(h) {}
    double area() const override { return w_ * h_; }
    const char* name() const override { return "rectangle"; }
};

class Triangle final : public Shape {
    double b_, h_;
public:
    Triangle(double b, double h) : b_(b), h_(h) {}
    double area() const override { return 0.5 * b_ * h_; }
    const char* name() const override { return "triangle"; }
};

int main() {
    std::vector<std::unique_ptr<Shape>> shapes;
    shapes.push_back(std::make_unique<Rectangle>(4, 5));
    shapes.push_back(std::make_unique<Triangle>(4, 3));
    for (const auto& s : shapes)
        std::cout << s->name() << ": " << s->area() << '\n';
}
```

Output:

```text
rectangle: 20
triangle: 6
```

An abstract class has at least one pure virtual function and cannot be instantiated, but pointers/references to it are allowed. A derived class remains abstract until it implements all required pure virtual functions.

### Virtual-destructor rule

If an object may be deleted through a base pointer, the base destructor must be virtual. Otherwise behavior is undefined and derived cleanup may not run.

Use `override` so the compiler catches signature mismatches; use `final` to prevent further overriding or derivation.

### Object slicing

```cpp
Derived d;
Base b = d;       // derived portion is sliced away
```

Pass/store polymorphic objects through references, pointers, or smart pointers—not base values.

## Lecture 11 — Templates and exception handling

### Function and class templates

```cpp
template<class T>
T maximum(const T& a, const T& b) {
    return b < a ? a : b;
}

template<class T, std::size_t N>
class Stack {
    T data_[N];
    std::size_t top_{};
public:
    void push(const T& x) {
        if (top_ == N) throw std::overflow_error("full stack");
        data_[top_++] = x;
    }
    T pop() {
        if (top_ == 0) throw std::underflow_error("empty stack");
        return data_[--top_];
    }
};
```

`typename` and `class` are equivalent in a type-parameter declaration. Each used specialization is instantiated as needed. Non-type template parameters such as `N` are compile-time values. Template definitions normally live in headers because the compiler needs the definition at the point of instantiation.

A non-template overload may be preferred when it is a better/equally specialized match. Modern C++ also has constraints/concepts, but they are beyond the slides.

### Exception mechanics

- `try` marks protected code.
- `throw expression` creates/transfers an exception.
- `catch (const Type& e)` handles a matching type.
- `catch (...)` is a catch-all and must be last.
- `throw;` inside a handler rethrows the current exception.

When an exception propagates, automatic objects in exited scopes are destroyed: **stack unwinding**. This is why RAII is fundamental.

```cpp
#include <iostream>
#include <stdexcept>

double divide(double a, double b) {
    if (b == 0) throw std::invalid_argument("division by zero");
    return a / b;
}

int main() {
    try {
        std::cout << divide(10, 0) << '\n';
    } catch (const std::invalid_argument& e) {
        std::cout << e.what() << '\n';
    }
}
```

Catch derived exception types before base types. Catch by `const&` to avoid copying and slicing. Destructors should not normally let exceptions escape.

`new` throws `std::bad_alloc`; `new (std::nothrow)` returns null. Dynamic exception specifications such as `void f() throw(int)` in the old lecture are removed from modern C++; use `noexcept` only when a function promises not to throw.

## Lecture 12 — RTTI and casts

### RTTI

For a polymorphic base, `typeid(*basePointer)` reports the dynamic type. Without polymorphism it generally reports the static type. `typeid` produces a `std::type_info`; `name()` is implementation-defined and may be mangled.

### Four named casts

- `static_cast<T>(x)`: checked at compile time for related/conventional conversions; downcasting is unchecked at runtime.
- `dynamic_cast<T>(x)`: runtime-checked navigation in a polymorphic hierarchy. Failed pointer cast returns `nullptr`; failed reference cast throws `std::bad_cast`.
- `const_cast<T>(x)`: adds/removes `const`/`volatile`. Modifying an object originally defined const is undefined behavior.
- `reinterpret_cast<T>(x)`: low-level reinterpretation; highly implementation-dependent and unsafe for ordinary object conversion.

```cpp
Base* b = new Derived;
if (auto* d = dynamic_cast<Derived*>(b)) {
    d->derivedOnlyOperation();
}
delete b;
```

Prefer virtual behavior over repeated type tests; `dynamic_cast` is useful when behavior genuinely depends on a more specific runtime type.

## Lecture 13 — Namespaces, conversion, static, const, linkage, and string streams

### User-defined conversions and `explicit`

A one-argument constructor can convert **to** a class; a conversion operator converts **from** a class.

```cpp
class Distance {
    double meters_;
public:
    explicit Distance(double m) : meters_(m) {}
    explicit operator double() const { return meters_; }
};

Distance d{3.5};
double x = static_cast<double>(d);
```

Mark converting constructors/operators `explicit` unless implicit conversion is intentionally safe. It prevents surprising chains and overload ambiguities.

### Static members

A static data member is shared by all objects. A static member function has no `this` and directly accesses only static members.

```cpp
class User {
    inline static int count_ = 0;      // C++17 inline definition
public:
    User() { ++count_; }
    static int count() { return count_; }
};
```

Older style declares in the class and defines once outside: `int User::count_ = 0;`.

### Const member and mutable

```cpp
class Cache {
    mutable int hits_{};
public:
    int value() const { ++hits_; return 42; }
};
```

A `const` member function promises not to modify the object's logical state. `mutable` permits carefully chosen bookkeeping even in a const function. Const and non-const overloads are common for element access.

### Linkage and embedded assembly

`extern "C"` requests C language linkage, mainly to interoperate with C APIs and suppress C++ name mangling. It does not compile C syntax inside C++ or make types ABI-portable automatically.

`asm`/`__asm` is compiler-specific embedded assembly and sacrifices portability; it is rarely appropriate in ordinary application code.

### Array-based I/O

The lecture's `istrstream`, `ostrstream`, and `<strstream>` are deprecated. Modern replacement:

```cpp
#include <sstream>
#include <string>

std::ostringstream out;
out << 12 << ' ' << 3.5;
std::string text = out.str();

std::istringstream in(text);
int a; double b;
in >> a >> b;
```

## Lecture 14 — STL: containers, algorithms, and iterators

### The three cooperating ideas

- **Containers** store values.
- **Iterators** identify positions and connect containers to generic code.
- **Algorithms** operate on iterator ranges and are usually independent of the container.

Ranges are normally half-open: `[first, last)`. `end()` is one past the final element and must not be dereferenced.

### Main container families and costs

| Container | Key strengths | Typical costs/traps |
|---|---|---|
| `array<T,N>` | Fixed contiguous storage | O(1) indexing; fixed size |
| `vector<T>` | Dynamic contiguous array | O(1) access/amortized append; middle insertion O(n); reallocation invalidates pointers/iterators |
| `deque<T>` | Fast both ends, random access | O(1) ends/access; not contiguous as one block |
| `list<T>` | Doubly linked list | O(1) insert/erase with iterator; O(n) search; no random access |
| `set`/`map` | Ordered tree keys | O(log n) search/insert/erase |
| `unordered_set`/`unordered_map` | Hash-based | Average O(1), worst O(n); rehash invalidation rules |
| `stack` | LIFO adapter | `push`, `top`, `pop` |
| `queue` | FIFO adapter | `push`, `front`, `pop` |
| `priority_queue` | Highest-priority top | O(log n) push/pop, O(1) top |

`map` has unique keys; `multimap` allows duplicates. `set` stores keys only; `multiset` allows duplicate keys. Ordered associative containers compare keys; unordered ones use a hash plus equality.

### Iterator categories

- input: single-pass read
- output: single-pass write
- forward: multi-pass forward
- bidirectional: forward/backward (`list`, tree iterators)
- random access: jumps/difference (`vector`, `deque`, array)
- contiguous: adjacent elements in memory (`array`, `vector`, raw array)

An algorithm's iterator requirement matters: `std::sort` needs random-access iterators, so use `list.sort()` for a list.

### Complete runnable STL example

```cpp
#include <algorithm>
#include <iostream>
#include <map>
#include <numeric>
#include <string>
#include <vector>

int main() {
    std::vector<int> v{5, 2, 8, 2, 1};
    std::sort(v.begin(), v.end());                 // 1 2 2 5 8
    auto firstEven = std::find_if(v.begin(), v.end(),
                                  [](int x) { return x % 2 == 0; });
    std::cout << "first even=" << *firstEven << '\n';
    std::cout << "count(2)=" << std::count(v.begin(), v.end(), 2) << '\n';
    std::cout << "sum=" << std::accumulate(v.begin(), v.end(), 0) << '\n';

    std::map<std::string, int> marks{{"Ada", 90}, {"Linus", 85}};
    marks["Grace"] = 95;                           // inserts if absent
    if (auto it = marks.find("Ada"); it != marks.end())
        std::cout << it->first << '=' << it->second << '\n';
}
```

Output:

```text
first even=2
count(2)=2
sum=18
Ada=90
```

Important algorithms from the slides: `find`, `find_if`, `count`, `sort`, `search`, `merge`, `for_each`, and `transform`. `merge` expects sorted input ranges. Prefer a range `for` for simple traversal; use algorithms when they state intent more clearly.

---
# Part III — Java current-merged-slide recall

## Java Lecture 1 — Platform, classes, objects, types, and references

### Why Java is portable

The Java compiler `javac` translates source into platform-neutral JVM bytecode. A platform-specific JVM loads, verifies, interprets and/or JIT-compiles that bytecode to native instructions.

```text
Welcome.java --javac--> Welcome.class --class loader/verifier/JVM--> machine code
```

- **JDK:** development kit—compiler, tools, libraries, and runtime components.
- **JVM:** abstract execution machine for bytecode.
- **JRE:** historically the runtime distribution; modern JDK distributions supply runtime modules and can create custom images with `jlink`.
- **Class loader:** locates and loads class definitions.
- **Bytecode verifier:** checks structural/type-safety constraints before execution.
- **JIT compiler:** compiles frequently executed bytecode to optimized native code at runtime.

Java's advertised properties in the lecture include simple, object-oriented, distributed, robust, secure, architecture-neutral, portable, multithreaded, and dynamic. “Interpreted” is incomplete today: JVMs combine interpretation and JIT compilation.

### Source-file and entry-point rules

- A source file may contain several top-level classes, but at most one public top-level class.
- The file name must match that public class.
- Each compiled class normally gets its own `.class` file, including nested/anonymous generated classes.
- Package declaration comes first (apart from comments), then imports, then types.

```java
public class Welcome {
    public static void main(String[] args) {
        System.out.println("Hello Java");
    }
}
```

`main` is public so the launcher can access it, static so no `Welcome` object is needed, void because no result is returned to the JVM, and receives command-line strings.

### Primitive versus reference types

Java primitives:

| Type | Size/meaning |
|---|---|
| `byte` | 8-bit signed integer |
| `short` | 16-bit signed integer |
| `int` | 32-bit signed integer |
| `long` | 64-bit signed integer |
| `float` | IEEE 754 32-bit floating point |
| `double` | IEEE 754 64-bit floating point |
| `char` | 16-bit UTF-16 code unit, not necessarily a complete Unicode character |
| `boolean` | `true` or `false`; it is not an integer |

Classes, interfaces, arrays, enums, and strings are reference types. A reference variable stores either `null` or a reference to an object; Java does not expose ordinary pointer arithmetic or address-of/dereference operators.

### The pass-by-value correction

**Java is always pass-by-value.** For an object argument, the value copied into the parameter is a reference. Therefore:

- mutating the referenced object is visible to the caller;
- reassigning the parameter to another object is not visible to the caller.

```java
static void change(int[] a) {
    a[0] = 99;          // changes caller's array object
    a = new int[3];     // changes only local copied reference
    a[0] = 7;
}

public static void main(String[] args) {
    int[] x = {1};
    change(x);
    System.out.println(x[0]); // 99
}
```

Viva answer: “The object itself is not copied, but Java still passes the reference value by value.”

### Object creation, aliasing, and garbage collection

```java
Box a = new Box(1, 2, 3);
Box b = a;                 // aliases the same object
a = new Box(4, 5, 6);     // b still refers to the first object
```

Assignment of references does not clone an object. An object becomes *eligible* for garbage collection when no reachable reference can lead to it; collection time is not guaranteed. Garbage collection manages memory, not timely release of files, sockets, or locks.

Conceptual JVM memory view:

- each thread has JVM stack frames containing local variables, operand-stack data, and return/control information;
- objects and arrays normally live in the shared heap;
- class metadata is managed separately by the JVM (HotSpot commonly uses metaspace);
- references may be optimized into registers or elsewhere, so “all local variables are physically on the stack” is not a language guarantee;
- GC starts from roots such as active stack references, static fields, and JNI roots and traces reachable objects.

### Java constructors and `this`

A constructor has the class name and no declared return type. If a class declares no constructor, the compiler may provide a default no-argument constructor; once any constructor is declared, that implicit one is not supplied.

```java
class Point {
    private final int x, y;
    Point() { this(0, 0); }       // constructor delegation; must be first
    Point(int x, int y) {
        this.x = x;               // field versus parameter
        this.y = y;
    }
}
```

`this` is the current object reference. `this(...)` calls another constructor in the same class; `super(...)` calls a superclass constructor. Neither can appear together in one constructor because either, if explicit, must be the first statement.

### Java object lifecycle

1. Class initialization occurs when first actively used: static fields/blocks run in textual order.
2. `new` allocates an object and initializes fields to defaults.
3. Instance field initializers and instance initializer blocks run in textual order after the superclass constructor begins the chain.
4. The constructor body runs.
5. The object remains reachable or becomes GC-eligible.

There is no C++-style deterministic destructor. `finalize()` is deprecated and unreliable. Use try-with-resources for `AutoCloseable` resources.

## Java Lecture 2 — Arrays, input, static/final, nested classes, varargs, and `var`

### Arrays

Arrays are fixed-length objects. `a.length` is a final field-like property, not a method.

```java
int[] values = new int[3];       // {0, 0, 0}
String[] names = new String[3];  // {null, null, null}
int[][] jagged = {{1, 2}, {3, 4, 5}};
```

- Indices are `0` through `length - 1`; invalid access throws `ArrayIndexOutOfBoundsException`.
- An array of class type creates reference slots, not the objects in those slots.
- Multidimensional arrays are arrays of arrays and may be jagged.
- `int[] a, b;` makes both arrays; `int a[], b;` makes only `a` an array.
- Enhanced `for (int x : array)` copies each element into `x`; assigning to `x` does not replace the array element.

### Command line and input

`java CommandLineTest hello 2` produces `args.length == 2`, `args[0] == "hello"`, and `args[1] == "2"`.

`Scanner` token methods such as `nextInt()` and `next()` differ from `nextLine()`. A common trap is that `nextInt()` leaves the newline; consume it before a subsequent `nextLine()`.

`JOptionPane.showInputDialog` returns text; numeric conversion such as `Integer.parseInt` may throw `NumberFormatException`.

### Static and initialization order

- A static field belongs to the class and has one shared value per class loader.
- A static method has no `this` or `super` and cannot directly access instance fields.
- A static initializer runs once when the class is initialized.
- An instance initializer runs before each constructor body, after the superclass constructor.

```java
class Counted {
    private static int count;
    private final int id;
    static { count = 0; }
    { id = ++count; }
    static int count() { return count; }
    int id() { return id; }
}
```

### `final`

- final variable: assigned once. For a reference, the reference cannot be reassigned, but the object may still be mutable.
- final method: cannot be overridden.
- final class: cannot be extended.

A blank final field may be assigned in every constructor. Compile-time constants are conventionally named `UPPER_SNAKE_CASE` and usually `static final`.

### Signed and unsigned right shift

- `>>` is arithmetic right shift and replicates the sign bit.
- `>>>` is logical right shift and inserts zero bits.

For `int a = -1`, `a >>> 24` yields `255`.

### Nested classes

- **Static nested class:** no implicit outer object; directly accesses only outer static members. Instantiate with `new Outer.Nested()`.
- **Inner class:** has an enclosing instance and may directly access its private fields. Instantiate externally with `outer.new Inner()`.
- **Local class:** declared inside a block/method; may capture effectively-final local variables.
- **Anonymous class:** unnamed one-off subclass/implementation.

Inside an inner class, `Outer.this.x` selects the enclosing object's field when shadowed.

### Varargs

```java
static int sum(int... values) { // internally an int[]
    int s = 0;
    for (int x : values) s += x;
    return s;
}
```

The varargs parameter must be last. Overloads such as `f(int...)` and `f(boolean...)` make `f()` ambiguous. Prefer fixed-arity overloads when both are equally meaningful.

### Local variable type inference

`var` asks the compiler to infer a **static** local type; it is not dynamic typing.

```java
var n = 10;                   // int
var list = new ArrayList<String>();
```

It requires a non-null initializer and is not allowed for fields, return types, ordinary parameters, or `var[]`. `var a = new int[10]` is valid; `var a = {1,2}` is not. With inheritance, inference follows the initializer's compile-time type, not the runtime object's type.

## Java Lecture 3 — Strings

### Immutability and the string pool

`String` is immutable: an operation returns another string rather than changing the original. Literals and compile-time constant strings may share interned objects in the string pool.

```java
String a = "Hello";
String b = "Hel" + "lo";             // compile-time constant, often same pooled object
String c = new String("Hello");       // distinct object

System.out.println(a == b);            // true in this example
System.out.println(a == c);            // false
System.out.println(a.equals(c));       // true
```

Never use `==` for logical string content. It compares reference identity.

### Core operations

- length/character extraction: `length()`, `charAt`, `getChars`
- slices: `substring(begin)`, `substring(begin, end)` where end is exclusive
- equality/order: `equals`, `equalsIgnoreCase`, `compareTo`
- regions/prefix/suffix: `regionMatches`, `startsWith`, `endsWith`
- search: `indexOf`, `lastIndexOf`
- build/replace: `concat`, `replace`, `toUpperCase`, `toLowerCase`, `trim`/`strip`
- conversion: `String.valueOf`, `Integer.parseInt`, etc.
- split: `split(regex)` takes a regular expression, not a literal delimiter in general.

By default `split` discards trailing empty strings but retains interior empty tokens. Use `split(regex, -1)` to retain trailing empties.

### `StringBuilder`, `StringBuffer`, and tokenizer

- `StringBuilder`: mutable and unsynchronized; usually fastest for local construction.
- `StringBuffer`: mutable and synchronized; legacy thread-safe counterpart.
- Common operations: `append`, `insert`, `delete`, `replace`, `reverse`, `length`, `capacity`.
- `StringTokenizer` is a legacy delimiter tokenizer; prefer `split`, `Scanner`, or regex APIs for new code.

Repeated `result = result + ch` in a loop creates many intermediate strings; use `StringBuilder`.

## Java Lecture 4 — Inheritance, dispatch, `Object`, equality, and ordering

### Inheritance and `super`

Java permits one direct superclass with `extends`. A class inherits accessible instance behavior; private members remain part of the object but are not directly accessible in the subclass.

`super(...)` invokes a superclass constructor and, if written, must be the first constructor statement. If omitted, the compiler inserts `super()` only when an accessible no-argument superclass constructor exists. `super.member` selects a hidden superclass member or implementation.

Construction proceeds from `Object` down to the most-derived class.

### Overriding, hiding, and dispatch

An override has the same signature and a compatible covariant return. It cannot reduce access and cannot throw broader checked exceptions. Use `@Override`.

- Instance method: runtime dispatch based on actual object.
- Static method: hidden; selected by compile-time reference/type.
- Field: hidden; selected by compile-time reference type.
- `private`, `static`, `final` methods and constructors are not overridden.

```java
class Base { void speak() { System.out.println("Base"); } }
class Child extends Base {
    @Override void speak() { System.out.println("Child"); }
}

Base x = new Child();
x.speak();                              // Child
```

The reference type controls which members are *accessible* at compile time; the actual type controls the selected override at runtime.

### Abstract classes and anonymous subclasses

An abstract class cannot be instantiated and may contain state, constructors, concrete methods, and abstract methods. A concrete subclass must implement all abstract methods. An anonymous subclass can provide a one-off implementation at the creation site.

### `Object`

Every class ultimately extends `Object`. Important methods include `toString`, `equals`, `hashCode`, `getClass`, `wait`, `notify`, and `notifyAll`.

### Equality contract

`==` compares primitive values or reference identity. `Object.equals` also uses identity unless overridden. Logical equality should satisfy:

- reflexive: `x.equals(x)`
- symmetric: `x.equals(y) == y.equals(x)`
- transitive
- consistent while relevant state is unchanged
- non-null: `x.equals(null)` is false

Hash rule: equal objects **must** have equal hash codes. Unequal objects may collide. Fields used by `equals` must align with `hashCode`; mutating them while an object is a hash key can make the entry unreachable.

### Complete equality and sorting example

```java
import java.util.*;

final class Student implements Comparable<Student> {
    private final int id;
    private final String name;

    Student(int id, String name) {
        this.id = id;
        this.name = Objects.requireNonNull(name);
    }
    int id() { return id; }
    String name() { return name; }

    @Override public boolean equals(Object obj) {
        if (this == obj) return true;
        if (!(obj instanceof Student other)) return false;
        return id == other.id && name.equals(other.name);
    }
    @Override public int hashCode() { return Objects.hash(id, name); }
    @Override public String toString() { return id + ":" + name; }

    @Override public int compareTo(Student other) {
        int byName = name.compareTo(other.name);
        return byName != 0 ? byName : Integer.compare(id, other.id);
    }
}

public class EqualitySortDemo {
    public static void main(String[] args) {
        Student a = new Student(2, "Ada");
        Student b = new Student(2, "Ada");
        System.out.println(a == b);                     // false
        System.out.println(a.equals(b));                // true
        System.out.println(new HashSet<>(List.of(a, b)).size()); // 1

        List<Student> s = new ArrayList<>(List.of(
                new Student(3, "Grace"), a,
                new Student(1, "Ada")));
        Collections.sort(s);                            // natural order
        System.out.println(s);                          // [1:Ada, 2:Ada, 3:Grace]
        s.sort(Comparator.comparingInt(Student::id).reversed());
        System.out.println(s);                          // [3:Grace, 2:Ada, 1:Ada]
    }
}
```

Use `Integer.compare(a, b)`, not `a - b`, because subtraction can overflow. `Comparable.compareTo` defines one natural order; `Comparator` defines external/alternative orders. Ideally natural-order equality is consistent with `equals`, especially for sorted sets/maps.

## Java Lecture 5 — Packages, interfaces, and exceptions

### Packages and imports

A package creates a namespace and an access boundary. Directory layout normally matches the package name.

```java
package university.people;
import java.util.List;
```

`import` avoids writing fully qualified names; it does not copy or load code. `import p.*` imports types in `p`, not subpackages. The unnamed/default package is unsuitable for multi-package applications.

### Java access table

| Member access | Same class | Same package | Subclass, other package | Unrelated other package |
|---|---:|---:|---:|---:|
| `private` | yes | no | no | no |
| package-private (no modifier) | yes | yes | no | no |
| `protected` | yes | yes | yes, through inheritance rules | no |
| `public` | yes | yes | yes | yes |

Top-level classes/interfaces may be `public` or package-private, not `private`/`protected`. In another package, protected access by a subclass is tied to inheritance and is not general access through any arbitrary base object.

### Interfaces

An interface specifies a role/capability. A class can implement several interfaces, enabling multiple inheritance of type.

- Ordinary interface methods are implicitly `public abstract`.
- Fields are implicitly `public static final`.
- Default methods have implementations and are inherited.
- Static interface methods belong to the interface and are not inherited as instance methods.
- Private interface methods (Java 9+) share code among default/static interface methods.
- Interfaces may extend multiple interfaces.

An implementing method must be public. If a class inherits conflicting unrelated default methods, it must override and resolve the conflict; it may explicitly call `InterfaceName.super.method()`.

```java
interface Printable { void print(); }
interface Resettable { default void reset() { System.out.println("reset"); } }

class Report implements Printable, Resettable {
    @Override public void print() { System.out.println("report"); }
}
```

Abstract class versus interface: use an abstract class for shared state/implementation in a close family; use an interface for a capability that unrelated types can implement. Modern interfaces are not literally “pure abstract classes” because they can contain default, static, and private methods.

### Exception hierarchy and checked/unchecked distinction

```text
Throwable
├── Error                    serious JVM/environment conditions
└── Exception
    ├── RuntimeException     unchecked programming/precondition failures
    └── other Exceptions     checked; catch or declare
```

Examples:

- unchecked: `NullPointerException`, `ArithmeticException`, `IllegalArgumentException`, `IndexOutOfBoundsException`
- checked: `IOException`, `ClassNotFoundException`
- `Error` is generally not caught for normal recovery.

### Five keywords and control flow

- `try`: code that may fail
- `catch`: compatible handler
- `finally`: cleanup path after try/catch, even across most returns
- `throw`: actually throws an object
- `throws`: declares possible checked exceptions in a method signature

Only the first matching catch runs; put specific types before general types. Multi-catch alternatives cannot have a subtype relationship, e.g., `catch (ArithmeticException | Exception e)` is illegal.

`finally` is not guaranteed after JVM/process termination or a catastrophic failure, and a `return`/throw in `finally` can suppress an earlier result/exception—avoid that.

### Complete checked/custom exception example

```java
import java.util.NoSuchElementException;

class StackFullException extends Exception {
    StackFullException(int rejected) {
        super("stack full; rejected " + rejected);
    }
}

final class IntStack {
    private final int[] data;
    private int size;
    IntStack(int capacity) { data = new int[capacity]; }
    void push(int x) throws StackFullException {
        if (size == data.length) throw new StackFullException(x);
        data[size++] = x;
    }
    int pop() {
        if (size == 0) throw new NoSuchElementException("empty stack");
        return data[--size];
    }
}

public class ExceptionDemo {
    public static void main(String[] args) {
        IntStack s = new IntStack(1);
        try {
            s.push(10);
            s.push(20);
        } catch (StackFullException e) {
            System.out.println(e.getMessage());
        }
    }
}
```

Choose checked exceptions when a caller can reasonably be required to recover; use unchecked exceptions for programming-contract violations. Do not catch broad `Exception` merely to print and continue in an invalid state.

### Try-with-resources

```java
try (BufferedReader br = Files.newBufferedReader(path, StandardCharsets.UTF_8)) {
    return br.readLine();
}
```

Resources are closed in reverse declaration order. If work and closing both throw, the close exception is available via `getSuppressed()` instead of replacing the primary exception.

## Java Lecture 6 — Threads and concurrency

### Process, thread, concurrency, and parallelism

- A process has its own address space/resources.
- Threads are execution paths within a process and share heap state.
- **Concurrency:** tasks make progress during overlapping time.
- **Parallelism:** tasks execute simultaneously on multiple cores.

Threads are cheaper to communicate between than processes but shared state creates races, visibility problems, deadlocks, and ordering uncertainty.

### Creating and controlling threads

Prefer separating task from thread:

```java
Runnable task = () -> System.out.println(Thread.currentThread().getName());
Thread t = new Thread(task, "worker");
t.start();           // creates a new execution path; do not call run() directly
t.join();            // caller waits for t to terminate
```

Implementing `Runnable` is normally better than extending `Thread`: the class keeps its inheritance option and the task is decoupled from execution policy. `sleep` pauses the current thread and does **not** release monitors. `isAlive` reports whether a started thread has not terminated. On interruption, usually restore status with `Thread.currentThread().interrupt()` unless the method deliberately propagates `InterruptedException`.

Avoid starting a thread from a constructor because `this` may escape before construction completes.

### Thread states

Java's `Thread.State` values are `NEW`, `RUNNABLE`, `BLOCKED`, `WAITING`, `TIMED_WAITING`, and `TERMINATED`. “Running” and “ready” are both represented by `RUNNABLE` at this API level.

### Race condition, visibility, and atomicity

`counter++` is a read-modify-write sequence, not atomic. Without synchronization, two threads can lose updates.

`volatile` provides visibility and ordering for reads/writes of that variable, but does not make a compound action like `counter++` atomic. Use synchronization, a lock, or `AtomicInteger.incrementAndGet()`.

Key **happens-before** relations make writes visible in a defined way: actions before `Thread.start()` are visible to the started thread; a thread's actions are visible after a successful `join`; unlocking a monitor happens-before a later lock of the same monitor; and a volatile write happens-before a later read of that variable. Mere elapsed time does not create a visibility guarantee.

### Intrinsic monitors and `synchronized`

- Synchronized instance method locks `this`.
- Synchronized static method locks the `Class` object.
- `synchronized(lock) { ... }` locks the specified object.
- Intrinsic locks are reentrant.
- Only code using the **same lock** is mutually exclusive.
- Leaving the block/method releases the monitor, including exceptional exit.

Keep critical sections small but large enough to protect the full invariant.

### `wait`, `notify`, and `notifyAll`

They belong to `Object` and must be called while holding that object's monitor.

- `wait()` releases that monitor and suspends the thread.
- `notify()` wakes one arbitrary waiter.
- `notifyAll()` wakes all; each must reacquire the monitor before proceeding.

Always wait in a loop because conditions can change and spurious wakeups are permitted:

```java
synchronized (queue) {
    while (queue.isEmpty()) queue.wait();
    value = queue.remove();
    queue.notifyAll();
}
```

Higher-level `BlockingQueue` is usually safer for producer–consumer code.

### Complete bounded producer–consumer example

```java
import java.util.concurrent.*;

public class ProducerConsumerDemo {
    private static final int END = -1;

    public static void main(String[] args) throws Exception {
        BlockingQueue<Integer> q = new ArrayBlockingQueue<>(2);
        ExecutorService pool = Executors.newFixedThreadPool(2);

        Future<?> producer = pool.submit(() -> {
            try {
                for (int i = 1; i <= 5; i++) q.put(i);
                q.put(END);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });

        Future<Integer> consumer = pool.submit(() -> {
            int sum = 0;
            while (true) {
                int x = q.take();
                if (x == END) return sum;
                sum += x;
            }
        });

        producer.get();
        System.out.println(consumer.get()); // 15
        pool.shutdown();
    }
}
```

### Deadlock

Deadlock is a cycle of threads each waiting for a resource held by another. The classic four necessary conditions are mutual exclusion, hold-and-wait, no preemption, and circular wait.

Prevention techniques:

- acquire multiple locks in one global order;
- avoid nested locks;
- use `tryLock` with timeout/backoff;
- reduce shared mutable state;
- do not call unknown/external code while holding a lock.

### Executors, futures, locks, atomic types, and fork/join

- `Executor` executes tasks; `ExecutorService` manages task submission and lifecycle.
- A thread pool amortizes thread creation and bounds concurrency/resource use.
- `Callable<V>` returns a result and may throw; `Future<V>.get()` waits and propagates failure via `ExecutionException`.
- `invokeAll` submits a collection and returns futures.
- Always shut down an executor.
- `Lock`/`ReentrantLock` offers `lock`, `tryLock`, interruptible acquisition, conditions; release in `finally`.
- `ReentrantReadWriteLock` permits concurrent readers when no writer owns the write lock.
- `AtomicInteger` offers lock-free atomic operations such as `incrementAndGet` and `compareAndSet`.
- Fork/join recursively splits CPU-bound work; `RecursiveTask<V>` returns a result, `RecursiveAction` does not. It uses work-stealing.

Deprecated `Thread.stop`, `suspend`, and `resume` are unsafe. Cooperative cancellation uses interruption or a condition flag with proper visibility.

## Java current unit 7 — Generics and collections

### Why generics

Generics parameterize classes, interfaces, and methods with types, enabling compile-time type safety and eliminating many casts.

```java
final class Box<T> {
    private T value;
    void set(T value) { this.value = value; }
    T get() { return value; }
}

Box<String> b = new Box<>();
b.set("hello");
String s = b.get();
```

A raw `Box` discards much type safety and may cause delayed `ClassCastException`; avoid raw types except legacy interoperability.

### Bounds, methods, and interfaces

```java
static <T extends Comparable<? super T>> T max(T a, T b) {
    return a.compareTo(b) >= 0 ? a : b;
}
```

- Multiple bound syntax: `<T extends SomeClass & Interface1 & Interface2>`; a class bound, if any, comes first.
- A constructor may declare its own type parameters.
- A generic interface can be implemented for a concrete type or propagated as generic.
- Type arguments must be reference types; use `Integer`, not `int`.

### Invariance, wildcards, and PECS

Even though `Integer` extends `Number`, `List<Integer>` is **not** a subtype of `List<Number>`; otherwise one could insert a `Double` into an integer list.

- `List<?>`: list of unknown element type; safe reads as `Object`, but cannot add non-null values.
- `List<? extends Number>`: producer/read from a subtype of `Number`; do not add a number.
- `List<? super Integer>`: consumer/write `Integer`; reads only as `Object`.

**PECS:** Producer Extends, Consumer Super.

```java
static <T> void copy(List<? extends T> source, List<? super T> destination) {
    destination.addAll(source);
}
```

### Type erasure

Java usually implements generics by erasing type arguments to their bound/Object and inserting casts where necessary. Consequences:

- `List<String>` and `List<Integer>` have the same runtime class.
- Cannot use primitive type arguments.
- Cannot normally write `new T()`, `new T[10]`, or `obj instanceof List<String>`.
- Static fields belong to the raw class, not separately to each type argument.
- Bridge methods may preserve polymorphism after erasure.

C++ templates, by contrast, generally instantiate distinct native code/types for different arguments.

### Collection framework map

```text
Iterable
└── Collection
    ├── List: ArrayList, LinkedList, Vector
    ├── Set: HashSet, LinkedHashSet, TreeSet
    └── Queue/Deque: PriorityQueue, ArrayDeque, LinkedList

Map (separate from Collection): HashMap, LinkedHashMap, TreeMap,
Hashtable, ConcurrentHashMap
```

### Choosing a collection

| Need | Strong default | Key facts |
|---|---|---|
| indexed dynamic sequence | `ArrayList` | O(1) access/amortized append; middle shift O(n) |
| frequent deque operations | `ArrayDeque` | O(1) amortized ends; preferred stack/queue implementation |
| node insertion through iterator | `LinkedList` | O(n) to reach index; linked overhead |
| unique membership | `HashSet` | average O(1), depends on correct equality/hash |
| sorted unique elements | `TreeSet` | O(log n), comparator/natural order |
| key/value lookup | `HashMap` | one null key/many null values; not synchronized |
| insertion-order map | `LinkedHashMap` | predictable iteration order |
| sorted map | `TreeMap` | O(log n) by key order |
| concurrent map | `ConcurrentHashMap` | thread-safe scalable operations; no null key/value |
| blocking producer/consumer | `BlockingQueue` | `put`/`take` coordinate threads |

`Vector` and `Hashtable` are synchronized legacy classes. Their individual synchronized calls do not automatically make a multi-step compound operation atomic.

### Iteration and modification

Use enhanced for, `Iterator`, or `forEach`. Many ordinary iterators are fail-fast on unsupported structural modification, but this is best-effort bug detection, not synchronization. Use `Iterator.remove()` when permitted or a concurrent collection for concurrent access.

`Arrays.asList(array)` returns a fixed-size list backed by the array; `add/remove` fail. `List.of` returns an unmodifiable list and rejects nulls.

### Sorting recall

```java
int[] a = {3, 1, 2};
Arrays.sort(a);                                    // primitives/objects

List<Integer> b = new ArrayList<>(List.of(3, 1, 2));
Collections.sort(b);                              // natural order
b.sort(Comparator.reverseOrder());                // alternative order

students.sort(Comparator.comparing(Student::name)
                        .thenComparingInt(Student::id));
```

`Arrays.binarySearch` requires the array to already be sorted using a compatible order; a negative result encodes the insertion point.

### Hash collections and equality

Lookup broadly computes a hash, selects a bucket, then uses `equals` among candidates. Equal keys must keep stable equality/hash-relevant fields while stored. `HashMap` order is unspecified.

## Compact Java viva supplement — enums, wrappers, and autoboxing

### Enum

An enum defines a class with a fixed set of instances. Enum constants are objects; enums may have fields, methods, constructors, and per-constant behavior, but cannot be instantiated with `new`.

```java
enum Level {
    LOW(1), HIGH(10);
    private final int weight;
    Level(int weight) { this.weight = weight; }
    int weight() { return weight; }
}
```

Every enum gets `values()` and `valueOf(String)`, and inherits `name`, `ordinal`, and identity-based final equality from `Enum`. Compare enum constants safely with `==`; do not persist `ordinal` as a stable business value.

### Wrapper types and boxing

Primitive wrappers: `Byte`, `Short`, `Integer`, `Long`, `Float`, `Double`, `Character`, `Boolean`. They are immutable and enable primitives to participate in generic/object APIs.

```java
Integer boxed = 100;       // autoboxing
int primitive = boxed;     // unboxing
```

Traps:

- Unboxing null throws `NullPointerException`.
- Wrapper `==` compares references. Small cached integers may make it appear to work:

```java
Integer a = 100, b = 100;
Integer x = 1000, y = 1000;
System.out.println(a == b); // commonly true due to required cache range
System.out.println(x == y); // normally false
```

Use `a.equals(b)` or compare unboxed primitives. Wrapper constructors such as `new Integer(100)` are deprecated; use `Integer.valueOf` or autoboxing.

## Compact Java viva supplement — file and stream I/O

### File/path metadata versus contents

Legacy `java.io.File` represents a path and provides metadata/directory operations; it does not itself read file contents. Modern `java.nio.file.Path` and `Files` are generally clearer and more capable.

### Byte versus character streams

- `InputStream` / `OutputStream`: bytes, binary data.
- `Reader` / `Writer`: characters, applying an encoding.
- `FileInputStream` / `FileOutputStream`: file bytes.
- `FileReader` / `FileWriter`: file characters, with charset-capable constructors in modern Java.
- `BufferedReader` / `BufferedWriter`: reduce physical I/O and offer line-oriented operations.

Always choose an explicit charset for portable text, usually UTF-8.

### Correct complete file-copy/text example

```java
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;

public class FileIODemo {
    public static void main(String[] args) throws IOException {
        Path source = Path.of("input.txt");
        Path copy = Path.of("copy.txt");
        Files.copy(source, copy, StandardCopyOption.REPLACE_EXISTING);

        try (BufferedReader in = Files.newBufferedReader(copy, StandardCharsets.UTF_8)) {
            String line;
            while ((line = in.readLine()) != null)
                System.out.println(line);
        }
    }
}
```

`InputStream.available()` is an estimate of bytes readable without blocking, not a general file length or proof that one `read(byte[])` fills the buffer. Correct block loop:

```java
byte[] buffer = new byte[8192];
int n;
while ((n = in.read(buffer)) != -1) out.write(buffer, 0, n);
```

### Data streams, object serialization, console, and random access

- `DataOutputStream`/`DataInputStream` write/read primitives in a defined matching sequence. Reading in a different type/order corrupts interpretation.
- `ObjectOutputStream`/`ObjectInputStream` serialize object graphs whose reachable fields are serializable. Use `transient` to exclude fields and declare `serialVersionUID` for version control.
- Never deserialize untrusted native Java streams without strong filtering: gadget chains can execute dangerous behavior.
- `System.console()` may be null inside an IDE. `readPassword()` avoids echoing and returns `char[]`, which can be cleared.
- `RandomAccessFile("rw")` supports both read/write; `seek` changes its file pointer and `getFilePointer` reports it.

Serialization vocabulary: serialization writes object state to a byte stream; deserialization reconstructs it.

# Part IV — High-yield C++/Java contrasts and viva traps

## Early binding versus late binding

```text
Early: compiler chooses target from declared types/signature.
Late: runtime chooses override from actual object's type.
```

Examples:

- C++ overloaded `print(int)` vs `print(double)`: early.
- C++ non-virtual base method through `Base*`: early.
- C++ virtual method through base pointer/reference: late.
- Java overloaded method: early.
- Java overridden instance method: late by default.
- Java static method/field: early/hiding.

Overloading is not runtime polymorphism, even if the overloads have one name.

## Copying and identity

```cpp
Widget b = a;        // C++ normally constructs a separate Widget value
```

```java
Widget b = a;        // Java copies a reference; a and b alias one object
```

Java cloning is not automatic and `Cloneable` is often awkward; prefer copy constructors/factories or immutable values.

## Destructor versus garbage collector

- C++ destructor is deterministic and can release any owned resource via RAII.
- Java GC reclaims unreachable memory eventually; it does not guarantee prompt external-resource cleanup.
- Java try-with-resources corresponds more closely to RAII for closeable resources.

## Template versus generic

- C++ template: compile-time instantiation, works with primitives, supports non-type parameters/specialization, may increase code size.
- Java generic: reference types, largely type-erased, runtime class usually shared, bounded wildcards support variance use sites.

## Abstract class versus interface in Java

| Abstract class | Interface |
|---|---|
| May hold instance state and constructors | No instance state; constants only |
| Single class inheritance | A class implements many interfaces |
| Any access for concrete members | Contract methods are public |
| Shared base implementation/family | Cross-cutting role/capability |

## Ten answers that should be exact

1. Java passes everything by value; for objects it copies the reference value.
2. `==` is identity for references; `equals` is logical equality when properly overridden.
3. Equal Java objects must have equal hash codes; the converse is not required.
4. Overloading is compile-time; overriding enables runtime dispatch.
5. C++ needs `virtual`; Java ordinary overridable instance methods dispatch dynamically.
6. A C++ polymorphic base destructor should be virtual if deletion through base is possible.
7. Java `volatile` gives visibility/order, not atomic compound updates.
8. `wait()` releases the monitor; `sleep()` does not.
9. Java `List<Integer>` is not a subtype of `List<Number>`; use wildcards.
10. Never loop on `!eof()`; loop on the read operation's success.

---

# Appendix — current two-PDF source coverage

| Current source | Pages | Material represented in this volume |
|---|---:|---|
| `C++_Merged.pdf` | 192 | fourteen lecture segments: OOP foundations; class construction/destruction; copy/reference ownership; arrays/pointers/references; overloads; operators; inheritance and virtual bases; stream/file I/O; virtual functions; templates/exceptions; RTTI/casts; namespaces/conversions/static members; STL |
| `Java-merged.pdf` | 244 | seven main units: Java/JVM/object fundamentals; arrays/static/final/nested classes/varargs; strings; inheritance/dispatch/`Object`/equality; packages/interfaces/exceptions; threads/concurrency; generics/collections |
| **Total** | **436** | current reduced source set |

The enums/boxing and file-stream notes are retained as compact standard-Java follow-ups, not claimed as separate current slide units. Removed-file inventories, Java networking, modules, lambda/stream source audits, and Apache POI were deleted because they no longer belong to the current academic source folder and are lower value for this viva than equality, exceptions, generics, collections, dispatch, ownership, and concurrency.

---
# Final oral-recall drill

Try to answer each in 20–40 seconds before reading the cue.

1. **Why is encapsulation more than making fields private?** It protects invariants by forcing state changes through meaningful operations; private fields without a coherent contract are only data hiding.
2. **Overloading versus overriding?** Different parameter lists selected at compile time versus same inherited signature selected from runtime object; static methods are hidden.
3. **Why virtual destructor?** Deleting a derived object through a base pointer must dispatch full destruction; without a virtual base destructor behavior is undefined.
4. **Why can a shallow copy crash?** Two owners copy one pointer, so one destruction leaves the other dangling and both may delete the same allocation.
5. **Is Java pass-by-reference?** No. It copies all arguments; an object argument's copied value is a reference, enabling mutation but not caller-visible parameter reassignment.
6. **Why override both `equals` and `hashCode`?** Hash containers select by hash then compare equality; equal keys with different hashes may be searched in different buckets.
7. **`Comparable` versus `Comparator`?** Natural order inside the class through `compareTo`; external/alternative order through `compare`.
8. **Checked versus unchecked exception?** Checked exceptions must be caught/declared; runtime exceptions do not. The semantic choice is expected recovery versus programming-contract failure.
9. **`sleep` versus `wait`?** Sleep pauses the current thread without releasing monitors; wait requires the object's monitor, releases it, and waits for notification/timeout/interruption.
10. **How does deadlock arise?** Threads form a circular wait while holding resources; impose consistent lock order or avoid nested locks.
11. **Why is `List<Integer>` not `List<Number>`?** Java generics are invariant; otherwise a `Double` could be inserted into an integer list.
12. **What is type erasure?** Generic type parameters are mostly removed to bounds/Object in bytecode, with casts/bridge methods inserted; parameterized runtime classes are usually shared.
13. **TCP versus UDP code model?** TCP uses connected stream sockets with application framing; UDP sends independent datagrams with preserved boundaries but no delivery/order guarantee.
14. **Byte versus character stream?** Bytes handle binary data; readers/writers decode/encode characters using a charset.
15. **Why not `while (!eof())`?** EOF is set only after a read fails, causing stale/duplicate processing; put the read in the condition.
16. **What do modules add beyond packages?** Explicit dependency/readability and strong encapsulation of non-exported packages.
17. **Lambda requirement?** A target functional interface with exactly one abstract method; captured locals must be effectively final.
18. **When composition over inheritance?** When the relation is has-a/uses-a or behavior should be swappable without claiming subtype substitutability.

If an answer feels vague, return to its lecture section and reproduce the smallest code trace—not merely the definition.
