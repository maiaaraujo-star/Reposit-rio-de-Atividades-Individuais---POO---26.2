def main():
    inicio = float(input("Digite o início do intervalo: "))
    fim = float(input("Digite o fim do intervalo: "))
    valor = float(input("Digite o terceiro valor: "))

    if inicio <= valor <= fim:
        print("O valor está dentro do intervalo.")
    elif valor < inicio:
        print("O valor está fora do intervalo, na parte inferior.")
    else:
        print("O valor está fora do intervalo, na parte superior.")


if __name__ == "__main__":
    main()