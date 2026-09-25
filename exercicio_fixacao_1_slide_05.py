class No:
    def __init__(self, letra):
        self.letra = letra
        self.prox = None


def exibir_letras(inicio):
    letras = []
    atual = inicio

    while atual is not None:
        letras.append(atual.letra)
        atual = atual.prox

    print(" → ".join(letras))


def main():
    no_a = No("a")
    no_b = No("b")
    no_c = No("c")
    no_d = No("d")
    no_e = No("e")
    no_f = No("f")
    no_g = No("g")
    no_h = No("h")
    no_i = No("i")
    no_j = No("j")

    no_a.prox = no_b
    no_b.prox = no_c
    no_c.prox = no_d
    no_d.prox = no_e
    no_e.prox = no_f
    no_f.prox = no_g
    no_g.prox = no_h
    no_h.prox = no_i
    no_i.prox = no_j

    print("Letras em ordem alfabética:")
    exibir_letras(no_a)

    no_b.prox = no_d
    print("\nSem a letra c:")
    exibir_letras(no_a)

    no_b.prox = no_j
    no_j.prox = no_d
    no_i.prox = None
    print("\nLetra j na posição do nó c:")
    exibir_letras(no_a)

    print(
        "\nCategoria de alocação: memória dinâmica (heap). "
        "Os nós são objetos criados durante a execução, e o campo prox "
        "armazena referências para conectá-los."
    )


if __name__ == "__main__":
    main()