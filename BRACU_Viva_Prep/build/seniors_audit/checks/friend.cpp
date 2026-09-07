#include <iostream>
class Second;
class First {
    int a;
    friend class Second;
public:
    explicit First(int value) : a(value) {}
};
class Second {
    int b;
public:
    explicit Second(int value) : b(value) {}
    int sum(const First& other) const { return other.a + b; }
};
int main() {
    First x(4);
    Second y(7);
    std::cout << y.sum(x) << '\n'; // 11
}