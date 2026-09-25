"""Lista de Exercício 02 - POO."""


# Questão 1:
# _saldo é um atributo protegido por convenção: o código externo ainda pode
# acessá-lo, mas deve tratá-lo como um detalhe interno. __saldo sofre name
# mangling: o Python altera internamente seu nome para _Classe__saldo, o que
# dificulta o acesso direto e evita colisões em subclasses.

# Questão 2:
# Se total for uma property sem setter, p.total = 10 gera AttributeError,
# porque a propriedade permite leitura, mas não permite atribuição.

# Questão 3:
# Validar no setter centraliza a regra em um único ponto. Assim, qualquer
# alteração passa pela mesma validação e não é necessário repetir a regra em
# todos os locais que usam o atributo.

# Questão 4:
# except Exception: pass captura praticamente qualquer erro e o ignora. Isso
# esconde bugs e dificulta descobrir por que o programa falhou. O correto é
# capturar exceções específicas e tratá-las ou informá-las adequadamente.

# Questão 5:
# class MeuErro(Exception) herda de Exception e, portanto, representa uma
# exceção personalizada que pode ser lançada e capturada com raise e except.


SALARIO_MINIMO = 1_518.00


class SalarioInvalidoError(ValueError):
    pass


class EmailInvalidoError(ValueError):
    pass


class ErroDeConta(Exception):
    pass


class ValorInvalidoError(ErroDeConta):
    pass


class SaldoInsuficienteError(ErroDeConta):
    pass


class LimiteExcedidoError(ErroDeConta):
    pass


class Funcionario:
    # Questão 6: salário validado por property e aumento limitado a 30%.
    def __init__(self, nome: str, salario: float):
        self.nome = nome
        self.salario = salario

    @property
    def salario(self) -> float:
        return self._salario

    @salario.setter
    def salario(self, valor: float) -> None:
        if valor < SALARIO_MINIMO:
            raise SalarioInvalidoError(
                f"O salário não pode ser menor que R$ {SALARIO_MINIMO:.2f}."
            )
        self._salario = valor

    def aumentar(self, percentual: float) -> None:
        if not 0 < percentual <= 30:
            raise ValueError("O aumento deve ser maior que 0% e menor ou igual a 30%.")
        self.salario = self.salario * (1 + percentual / 100)


class Email:
    # Questão 7: endereço validado por property.
    def __init__(self, endereco: str):
        self.endereco = endereco

    @property
    def endereco(self) -> str:
        return self._endereco

    @endereco.setter
    def endereco(self, valor: str) -> None:
        if "@" not in valor or "." not in valor:
            raise EmailInvalidoError("O e-mail deve conter @ e .")
        self._endereco = valor


class ContaBancaria:
    # Questão 9: conta com saldo protegido, depósitos e saques validados.
    LIMITE_SAQUE = 1_000.00

    def __init__(self, saldo_inicial: float = 0.0):
        if saldo_inicial < 0:
            raise ValorInvalidoError("O saldo inicial não pode ser negativo.")
        self._saldo = saldo_inicial

    @property
    def saldo(self) -> float:
        return self._saldo

    def depositar(self, valor: float) -> None:
        if valor <= 0:
            raise ValorInvalidoError("O valor do depósito deve ser positivo.")
        self._saldo += valor

    def sacar(self, valor: float) -> None:
        if valor <= 0:
            raise ValorInvalidoError("O valor do saque deve ser positivo.")
        if valor > self.LIMITE_SAQUE:
            raise LimiteExcedidoError("O saque máximo por operação é de R$ 1.000,00.")
        if valor > self._saldo:
            raise SaldoInsuficienteError("Saldo insuficiente para realizar o saque.")
        self._saldo -= valor


def testar_funcionario() -> None:
    # Questão 8: dois casos de erro da classe Funcionario.
    print("Testes de erro de Funcionario:")
    try:
        Funcionario("Ana", 1_000.00)
    except SalarioInvalidoError as erro:
        print(erro)

    funcionario = Funcionario("Bruno", 2_000.00)
    try:
        funcionario.aumentar(35)
    except ValueError as erro:
        print(erro)


def testar_email() -> None:
    # Questão 8: dois casos de erro da classe Email.
    print("\nTestes de erro de Email:")
    for endereco in ("email-sem-arroba.com", "email@sem-ponto"):
        try:
            Email(endereco)
        except EmailInvalidoError as erro:
            print(f"{endereco}: {erro}")


def main() -> None:
    testar_funcionario()
    testar_email()

    conta = ContaBancaria()
    conta.depositar(500)
    print(f"\nSaldo da conta: R$ {conta.saldo:.2f}")


if __name__ == "__main__":
    main()