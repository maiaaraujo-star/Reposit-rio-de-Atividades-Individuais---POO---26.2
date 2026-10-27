"""Exercicios de heranca multipla, MRO, autenticacao e mixins.

UML (PlantUML):

@startuml
class ExportavelCSV {
  + linha_csv(): str
}
class Funcionario {
  + nome: str
  + cargo: str
  + salario: float
  + apresentar(): None
}
class Autenticavel {
  - senha: str
  + cadastrar_senha(senha): None
  + autenticar(senha): bool
}
class Diretor {
  + departamento: str
}
class Cliente {
  + numero_conta: str
}
ExportavelCSV <|.. Funcionario
Funcionario <|-- Diretor
Autenticavel <|-- Diretor
Autenticavel <|-- Cliente

class A
class B
class C
class D
A <|-- B
A <|-- C
B <|-- D
C <|-- D
@enduml

Com D(B, C), a MRO e D -> B -> C -> A -> object. Como B.ola e C.ola
chamam super(), a saida e B.ola, C.ola, A.ola.
Com D(C, B), a MRO se torna D -> C -> B -> A -> object e a saida passa
a C.ola, B.ola, A.ola. O C3 linearization mantem uma ordem consistente
das classes-base e visita cada classe uma vez.
"""

import csv
from io import StringIO


class ExportavelCSV:
    def linha_csv(self) -> str:
        buffer = StringIO()
        valores_publicos = (
            valor
            for nome, valor in vars(self).items()
            if not nome.startswith("_")
        )
        csv.writer(buffer, lineterminator="").writerow(valores_publicos)
        return buffer.getvalue()


class Funcionario(ExportavelCSV):
    def __init__(self, nome: str, cargo: str, salario: float) -> None:
        if not nome.strip() or not cargo.strip():
            raise ValueError("Nome e cargo nao podem ficar vazios.")
        if salario < 0:
            raise ValueError("O salario nao pode ser negativo.")
        self.nome = nome
        self.cargo = cargo
        self.salario = salario

    def apresentar(self) -> None:
        print(
            f"{self.cargo}: {self.nome}; salario: R$ {self.salario:.2f}."
        )


class Autenticavel:
    def __init__(self) -> None:
        self._senha: str | None = None

    def cadastrar_senha(self, senha: str) -> None:
        if len(senha) < 4:
            raise ValueError("A senha deve ter pelo menos 4 caracteres.")
        self._senha = senha
        print("Senha cadastrada.")

    def autenticar(self, senha: str) -> bool:
        autenticado = self._senha is not None and senha == self._senha
        resultado = "sucesso" if autenticado else "falha"
        print(f"Autenticacao: {resultado}.")
        return autenticado


class Diretor(Funcionario, Autenticavel):
    def __init__(
        self,
        nome: str,
        salario: float,
        departamento: str,
    ) -> None:
        Funcionario.__init__(self, nome, "Diretor", salario)
        Autenticavel.__init__(self)
        if not departamento.strip():
            raise ValueError("O departamento nao pode ficar vazio.")
        self.departamento = departamento

    def apresentar(self) -> None:
        print(
            f"Diretor: {self.nome}; departamento: {self.departamento}; "
            f"salario: R$ {self.salario:.2f}."
        )


class Gerente(Diretor):
    def __init__(
        self,
        nome: str,
        salario: float,
        departamento: str,
    ) -> None:
        super().__init__(nome, salario, departamento)
        self.cargo = "Gerente"

    def apresentar(self) -> None:
        print(
            f"Gerente: {self.nome}; departamento: {self.departamento}; "
            f"salario: R$ {self.salario:.2f}."
        )


class Cliente(Autenticavel):
    def __init__(self, nome: str, numero_conta: str) -> None:
        super().__init__()
        if not nome.strip() or not numero_conta.strip():
            raise ValueError("Nome e numero da conta nao podem ficar vazios.")
        self.nome = nome
        self.numero_conta = numero_conta

    def apresentar(self) -> None:
        print(f"Cliente: {self.nome}; conta: {self.numero_conta}.")


class A:
    def ola(self) -> None:
        print("A.ola")


class B(A):
    def ola(self) -> None:
        print("B.ola")
        super().ola()


class C(A):
    def ola(self) -> None:
        print("C.ola")
        super().ola()


class D(B, C):
    pass


D_BC = D


class D(C, B):
    pass


def formato_mro(classe: type) -> str:
    return " -> ".join(base.__name__ for base in classe.__mro__)


def demonstrar_banco() -> None:
    print("=== Sistema bancario e autenticacao ===")
    gerente = Gerente("Marina", 8200.00, "Operacoes")
    cliente = Cliente("Rafael", "CC-1042")

    gerente.apresentar()
    gerente.cadastrar_senha("gerente123")
    print("Testando senha correta do gerente:")
    gerente.autenticar("gerente123")
    print("Testando senha incorreta do gerente:")
    gerente.autenticar("senha-errada")

    cliente.apresentar()
    cliente.cadastrar_senha("cliente456")
    print("Testando senha correta do cliente:")
    cliente.autenticar("cliente456")
    print("Testando senha incorreta do cliente:")
    cliente.autenticar("senha-errada")

    funcionario = Funcionario("Joao Silva", "Analista", 4300.00)
    print(f"\nFuncionario em CSV: {funcionario.linha_csv()}")
    print(f"Gerente em CSV: {gerente.linha_csv()}")


def demonstrar_diamante() -> None:
    print("\n=== Diamante de heranca e MRO ===")
    print("Declaracao original: class D(B, C)")
    # Saida prevista de D().ola():
    # B.ola
    # C.ola
    # A.ola
    D_BC().ola()
    print(f"D.__mro__: {formato_mro(D_BC)}")
    # MRO prevista: D -> B -> C -> A -> object

    print("\nDeclaracao invertida: class D(C, B)")
    # Saida prevista de D().ola() com as bases invertidas:
    # C.ola
    # B.ola
    # A.ola
    D().ola()
    print(f"D.__mro__: {formato_mro(D)}")
    # MRO prevista: D -> C -> B -> A -> object
    print(
        "A inversao muda qual ramo e consultado primeiro. super() segue a "
        "MRO, entao as implementacoes de B e C trocam de ordem; A ainda e "
        "chamada uma unica vez."
    )


def main() -> None:
    demonstrar_banco()
    demonstrar_diamante()


if __name__ == "__main__":
    main()
