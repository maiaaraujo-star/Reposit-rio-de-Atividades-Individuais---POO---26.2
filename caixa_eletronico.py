from lista_exercicio_02 import ContaBancaria, ErroDeConta


def exibir_menu() -> None:
    print("\n1 - Depositar")
    print("2 - Sacar")
    print("3 - Consultar saldo")
    print("4 - Sair")


def main() -> None:
    conta = ContaBancaria()

    while True:
        exibir_menu()

        try:
            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                valor = float(input("Valor do depósito: "))
                conta.depositar(valor)
                print("Depósito realizado com sucesso.")
            elif opcao == "2":
                valor = float(input("Valor do saque: "))
                conta.sacar(valor)
                print("Saque realizado com sucesso.")
            elif opcao == "3":
                print(f"Saldo atual: R$ {conta.saldo:.2f}")
            elif opcao == "4":
                print("Caixa eletrônico encerrado.")
                break
            else:
                print("Opção inválida.")
        except ErroDeConta as erro:
            print(f"Erro: {erro}")
        except ValueError:
            print("Digite uma opção ou valor numérico válido.")
        except (EOFError, KeyboardInterrupt):
            print("\nCaixa eletrônico encerrado.")
            break


if __name__ == "__main__":
    main()