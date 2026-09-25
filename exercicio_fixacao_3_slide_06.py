def elementos_em_comum(conjunto_a, conjunto_b):
    return conjunto_a.intersection(conjunto_b)


def palindromos(palavras):
    return {palavra for palavra in palavras if palavra == palavra[::-1]}


def main():
    conjunto_a = {1, 2, 3, 4}
    conjunto_b = {3, 4, 5, 6}
    palavras = {"arara", "casa", "ovo", "radar"}

    comuns = elementos_em_comum(conjunto_a, conjunto_b)
    palavras_palindromas = palindromos(palavras)

    print(f"Elementos em ambos os conjuntos: {sorted(comuns)}")
    print(f"Palíndromos: {sorted(palavras_palindromas)}")


if __name__ == "__main__":
    main()