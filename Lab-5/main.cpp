int main() {
    int v;
    int p;

    cin >> v >> p;

    int result = 1;
    while (p > 0) {

        if (p % 2 == 1) {
            result *= v;
        }

        v *= v;
        p = p / 2;
    }
    cout << result;
    return 0;
}

void func() {
    v + p;
}
