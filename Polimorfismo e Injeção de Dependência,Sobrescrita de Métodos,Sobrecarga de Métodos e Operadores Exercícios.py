"""Exercicios de polimorfismo, injecao de dependencia e sobrecarga.

Diagramas de classes UML (PlantUML):

@startuml
abstract class FiguraGeometrica {
  +area(): float
  +perimetro(): float
  +__add__(outra: FiguraGeometrica): float
}
class Ponto {
  +x: float
  +y: float
  +__add__(outro: Ponto): Ponto
  +__sub__(outro: Ponto): Ponto
}
class Circulo {
  +centro: Ponto
  +raio: float
  +area(): float
  +perimetro(): float
}
class Retangulo {
  +canto_superior_esquerdo: Ponto
  +canto_inferior_direito: Ponto
  +area(): float
  +perimetro(): float
}
FiguraGeometrica <|-- Circulo
FiguraGeometrica <|-- Retangulo
Circulo *-- Ponto : centro
Retangulo *-- Ponto : cantos
@enduml

@startuml
abstract class Animal {
  +nome: str
  +custo_alimentacao_diario: float
  +movimentar(): str
  +emitir_som(): str
}
class Leao
class Macaco
class Arara
abstract class CalculadoraAlimentacao {
  +calcular_total(animais): float
}
class CalculadoraCustoDiario
class Zoologico {
  +animais: list[Animal]
  +apresentar_animais(): None
  +movimentar_animais(): None
  +ouvir_animais(): None
  +custo_total_diario(): float
}
Animal <|-- Leao
Animal <|-- Macaco
Animal <|-- Arara
CalculadoraAlimentacao <|-- CalculadoraCustoDiario
Zoologico "1" o-- "0..*" Animal
Zoologico --> CalculadoraAlimentacao : injeta
@enduml

No exercicio 1, FiguraGeometrica define a interface comum, as subclasses
sobrescrevem area e perimetro, e o operador + soma as areas. Ponto tambem
implementa + e - para operar sobre coordenadas.
No exercicio 2, os animais sobrescrevem movimento e som. Zoologico recebe
animais e calculadora pelo construtor, demonstrando injecao de dependencia.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from math import pi
from types import NotImplementedType


@dataclass(frozen=True)
class Ponto:
    x: float
    y: float

    def __add__(self, outro: object) -> "Ponto | NotImplementedType":
        if not isinstance(outro, Ponto):
            return NotImplemented
        return Ponto(self.x + outro.x, self.y + outro.y)

    def __sub__(self, outro: object) -> "Ponto | NotImplementedType":
        if not isinstance(outro, Ponto):
            return NotImplemented
        return Ponto(self.x - outro.x, self.y - outro.y)


class FiguraGeometrica(ABC):
    @abstractmethod
    def area(self) -> float:
        raise NotImplementedError

    @abstractmethod
    def perimetro(self) -> float:
        raise NotImplementedError

    def __add__(self, outra: object) -> float | NotImplementedType:
        if not isinstance(outra, FiguraGeometrica):
            return NotImplemented
        return self.area() + outra.area()


class Circulo(FiguraGeometrica):
    def __init__(self, centro: Ponto, raio: float) -> None:
        if raio <= 0:
            raise ValueError("O raio do circulo deve ser positivo.")
        self.centro = centro
        self.raio = raio

    def area(self) -> float:
        return pi * self.raio**2

    def perimetro(self) -> float:
        return 2 * pi * self.raio


class Retangulo(FiguraGeometrica):
    def __init__(
        self,
        canto_superior_esquerdo: Ponto,
        canto_inferior_direito: Ponto,
    ) -> None:
        largura = abs(canto_inferior_direito.x - canto_superior_esquerdo.x)
        altura = abs(canto_superior_esquerdo.y - canto_inferior_direito.y)
        if largura == 0 or altura == 0:
            raise ValueError("Os cantos devem formar um retangulo com area positiva.")
        self.canto_superior_esquerdo = canto_superior_esquerdo
        self.canto_inferior_direito = canto_inferior_direito

    @property
    def largura(self) -> float:
        return abs(
            self.canto_inferior_direito.x - self.canto_superior_esquerdo.x
        )

    @property
    def altura(self) -> float:
        return abs(
            self.canto_superior_esquerdo.y - self.canto_inferior_direito.y
        )

    def area(self) -> float:
        return self.largura * self.altura

    def perimetro(self) -> float:
        return 2 * (self.largura + self.altura)


class Animal(ABC):
    def __init__(self, nome: str, custo_alimentacao_diario: float) -> None:
        if custo_alimentacao_diario < 0:
            raise ValueError("O custo de alimentacao nao pode ser negativo.")
        self.nome = nome
        self.custo_alimentacao_diario = custo_alimentacao_diario

    @abstractmethod
    def movimentar(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def emitir_som(self) -> str:
        raise NotImplementedError

    def apresentar_informacoes(self) -> None:
        print(
            f"{self.__class__.__name__} {self.nome}: "
            f"custo diario de alimentacao R$ {self.custo_alimentacao_diario:.2f}."
        )


class Leao(Animal):
    def movimentar(self) -> str:
        return f"{self.nome} caminha pelo recinto."

    def emitir_som(self) -> str:
        return f"{self.nome} ruge: ROAR!"


class Macaco(Animal):
    def movimentar(self) -> str:
        return f"{self.nome} escala e pula entre os galhos."

    def emitir_som(self) -> str:
        return f"{self.nome} grita: Uh uh ah ah!"


class Arara(Animal):
    def movimentar(self) -> str:
        return f"{self.nome} voa pelo viveiro."

    def emitir_som(self) -> str:
        return f"{self.nome} grasna: Craa!"


class CalculadoraAlimentacao(ABC):
    @abstractmethod
    def calcular_total(self, animais: list[Animal]) -> float:
        raise NotImplementedError


class CalculadoraCustoDiario(CalculadoraAlimentacao):
    def calcular_total(self, animais: list[Animal]) -> float:
        return sum(animal.custo_alimentacao_diario for animal in animais)


class Zoologico:
    def __init__(
        self,
        animais: list[Animal],
        calculadora: CalculadoraAlimentacao,
    ) -> None:
        self.animais = list(animais)
        self.calculadora = calculadora

    def apresentar_animais(self) -> None:
        print("\nAnimais do zoologico:")
        for animal in self.animais:
            animal.apresentar_informacoes()

    def movimentar_animais(self) -> None:
        print("\nMovimentacao dos animais:")
        for animal in self.animais:
            print(animal.movimentar())

    def ouvir_animais(self) -> None:
        print("\nSons dos animais:")
        for animal in self.animais:
            print(animal.emitir_som())

    def custo_total_diario(self) -> float:
        return self.calculadora.calcular_total(self.animais)


def demonstrar_figuras() -> None:
    print("=== Exercicio 1: figuras geometricas ===")
    circulo = Circulo(Ponto(0, 0), 3)
    retangulo = Retangulo(Ponto(1, 5), Ponto(7, 1))

    for figura in (circulo, retangulo):
        print(
            f"{figura.__class__.__name__}: area = {figura.area():.2f}; "
            f"perimetro = {figura.perimetro():.2f}."
        )

    print(f"Soma das areas (circulo + retangulo): {circulo + retangulo:.2f}.")
    ponto_a = Ponto(2, 3)
    ponto_b = Ponto(4, 1)
    print(f"Soma dos pontos: {ponto_a + ponto_b}.")
    print(f"Diferenca dos pontos: {ponto_a - ponto_b}.")


def demonstrar_zoologico() -> None:
    print("\n=== Exercicio 2: zoologico ===")
    animais: list[Animal] = [
        Leao("Simba", 125.50),
        Macaco("Kiko", 32.00),
        Arara("Luna", 18.75),
    ]
    calculadora = CalculadoraCustoDiario()
    zoologico = Zoologico(animais, calculadora)

    zoologico.apresentar_animais()
    zoologico.movimentar_animais()
    zoologico.ouvir_animais()
    print(
        "Custo total diario de alimentacao: "
        f"R$ {zoologico.custo_total_diario():.2f}."
    )


def main() -> None:
    demonstrar_figuras()
    demonstrar_zoologico()


if __name__ == "__main__":
    main()
