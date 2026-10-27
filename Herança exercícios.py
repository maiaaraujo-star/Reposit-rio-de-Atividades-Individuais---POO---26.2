"""Exercicios de heranca: animais, ordem de resolucao e mixin CSV.

Exercicio 1 - UML do slide:

@startuml
class Animal {
  # nome: str
  # peso: float
  # posicao: int
  + mover_se(): None
}
class Gato {
  # na_arvore: bool
  + miar(): None
  + subir_na_arvore(): None
  + descer_da_arvore(): None
  + esta_na_arvore(): bool
}
class Cachorro {
  # qtd_saltos: int
  + latir(): None
  + saltar(): None
  + descansar(): None
  + esta_cansado(): bool
}
Animal <|-- Gato
Animal <|-- Cachorro
@enduml

Exercicio 2 - diagrama de heranca e mixin:

@startuml
class A
class B
class C
class D
A <|-- B
A <|-- C
B <|-- D
C <|-- D
class ExportavelCSV {
  + linha_csv(): str
}
class Funcionario {
  + nome: str
  + cargo: str
  + salario: float
}
ExportavelCSV <|.. Funcionario
@enduml
"""

import csv
from io import StringIO


class Animal:
    def __init__(self, nome: str, peso: float, posicao: int = 0) -> None:
        if peso <= 0:
            raise ValueError("O peso deve ser positivo.")
        self.nome = nome
        self.peso = peso
        self.posicao = posicao

    def mover_se(self) -> None:
        self.posicao += 1
        print(f"{self.nome} se moveu para a posicao {self.posicao}.")

    def apresentar_informacoes(self) -> None:
        print(
            f"{self.__class__.__name__}: {self.nome}, "
            f"{self.peso} kg, posicao {self.posicao}."
        )


class Gato(Animal):
    def __init__(self, nome: str, peso: float, posicao: int = 0) -> None:
        super().__init__(nome, peso, posicao)
        self.na_arvore = False

    def miar(self) -> None:
        print(f"{self.nome}: Miau!")

    def subir_na_arvore(self) -> None:
        self.na_arvore = True
        print(f"{self.nome} subiu na arvore.")

    def descer_da_arvore(self) -> None:
        self.na_arvore = False
        print(f"{self.nome} desceu da arvore.")

    def esta_na_arvore(self) -> bool:
        return self.na_arvore


class Cachorro(Animal):
    LIMITE_SALTOS_CANSADO = 5

    def __init__(self, nome: str, peso: float, posicao: int = 0) -> None:
        super().__init__(nome, peso, posicao)
        self.qtd_saltos = 0

    def latir(self) -> None:
        print(f"{self.nome}: Au au!")

    def saltar(self) -> None:
        self.qtd_saltos += 1
        print(f"{self.nome} saltou. Total de saltos: {self.qtd_saltos}.")

    def descansar(self) -> None:
        self.qtd_saltos = max(0, self.qtd_saltos - 1)
        print(f"{self.nome} descansou. Total de saltos: {self.qtd_saltos}.")

    def esta_cansado(self) -> bool:
        return self.qtd_saltos > self.LIMITE_SALTOS_CANSADO


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


class ExportavelCSV:
    def linha_csv(self) -> str:
        buffer = StringIO()
        csv.writer(buffer, lineterminator="").writerow(vars(self).values())
        return buffer.getvalue()


class Funcionario(ExportavelCSV):
    def __init__(self, nome: str, cargo: str, salario: float) -> None:
        if salario < 0:
            raise ValueError("O salario nao pode ser negativo.")
        self.nome = nome
        self.cargo = cargo
        self.salario = salario


def demonstrar_animais() -> None:
    print("=== Exercicio 1: heranca de animais ===")
    gato = Gato("Mimi", 4.2)
    cachorro = Cachorro("Rex", 12.5)

    gato.apresentar_informacoes()
    gato.miar()
    gato.subir_na_arvore()
    print(f"Esta na arvore? {gato.esta_na_arvore()}")
    gato.descer_da_arvore()
    gato.mover_se()

    cachorro.apresentar_informacoes()
    cachorro.latir()
    for _ in range(6):
        cachorro.saltar()
    print(f"Esta cansado? {cachorro.esta_cansado()}")
    cachorro.descansar()
    print(f"Esta cansado depois de descansar? {cachorro.esta_cansado()}")


def nomes_mro(classe: type) -> str:
    return " -> ".join(base.__name__ for base in classe.__mro__)


def demonstrar_diamante() -> None:
    print("\n=== Exercicio 2: heranca multipla em diamante ===")
    print("Ordem original: class D(B, C)")
    # Saida prevista de D().ola():
    # B.ola
    # C.ola
    # A.ola
    D_BC().ola()
    print(f"D.__mro__ com bases (B, C): {nomes_mro(D_BC)}")
    # MRO previsto: D -> B -> C -> A -> object

    print("\nOrdem invertida: class D(C, B)")
    # Saida prevista ao inverter as bases:
    # C.ola
    # B.ola
    # A.ola
    D().ola()
    print(f"D.__mro__ com bases (C, B): {nomes_mro(D)}")
    # MRO previsto: D -> C -> B -> A -> object
    print(
        "A ordem das bases altera a MRO: o Python consulta primeiro C em "
        "D(C, B), mantendo a ordem consistente do diamante. A classe D "
        "original foi guardada como D_BC para comparar as duas declaracoes."
    )


def demonstrar_csv() -> None:
    print("\n=== Exercicio 2: mixin ExportavelCSV ===")
    funcionario = Funcionario("Ana Silva", "Analista", 4500.00)
    print(funcionario.linha_csv())


def main() -> None:
    demonstrar_animais()
    demonstrar_diamante()
    demonstrar_csv()


if __name__ == "__main__":
    main()
