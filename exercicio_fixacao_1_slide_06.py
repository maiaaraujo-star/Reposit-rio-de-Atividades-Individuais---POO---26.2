def elementos_pares(numeros):
    return tuple(numero for numero in numeros if numero % 2 == 0)


def strings_ordenadas(strings):
    return tuple(sorted(set(strings)))


def main():
    numeros = (1, 2, 3, 4, 5)
    frutas = ("banana", "maçã", "laranja", "banana", "uva")

    print(f"Tupla com elementos pares: {elementos_pares(numeros)}")
    print(f"Tupla de strings ordenadas: {strings_ordenadas(frutas)}")


if __name__ == "__main__":
    main()