def main():
    nota1 = float(input("Digite a primeira nota: "))
    nota2 = float(input("Digite a segunda nota: "))

    media = (nota1 + nota2) / 2

    if media >= 30 and media < 70:
        print("Você está em RECUPERAÇÃO!!!")


if __name__ == "__main__":
    main()