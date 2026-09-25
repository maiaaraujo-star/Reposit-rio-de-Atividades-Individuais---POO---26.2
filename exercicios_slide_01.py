def main():
    a = int(input("Digite o valor de A: "))
    b = int(input("Digite o valor de B: "))

    print(f"A + B = {a + b}")
    print(f"A * B = {a * b}")
    print(f"A - B = {a - b}")

    if b == 0:
        print("A / B = divisão por zero não é permitida")
    else:
        print(f"A / B = {a / b}")

    print(f"A > B = {a > b}")
    print(f"A <= B = {a <= b}")
    print(f"A != B = {a != b}")
    print(f"A == B = {a == b}")


if __name__ == "__main__":
    main()