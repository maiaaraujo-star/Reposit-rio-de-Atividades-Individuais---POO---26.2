def main():
    quantidade = int(input("Quantas equações serão calculadas? "))

    valores_a = []
    valores_b = []
    valores_x = []

    for indice in range(quantidade):
        print(f"\nEquação {indice + 1}:")
        valores_a.append(float(input("Digite o valor de a: ")))
        valores_b.append(float(input("Digite o valor de b: ")))
        valores_x.append(float(input("Digite o valor de x: ")))

    print("\nResultados:")
    for indice in range(quantidade):
        a = valores_a[indice]
        b = valores_b[indice]
        x = valores_x[indice]
        y = a * x + b

        print(f"y = {a:g}*{x:g} + {b:g}")
        print(f"Valor de y: {y:g}")


if __name__ == "__main__":
    main()