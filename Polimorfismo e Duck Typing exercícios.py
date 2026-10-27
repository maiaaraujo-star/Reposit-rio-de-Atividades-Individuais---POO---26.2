"""Exercicios de polimorfismo, duck typing e injecao de dependencia.

Diagramas de classes UML (PlantUML):

@startuml
abstract class Animal {
  +nome: str
  +mover(): str
  +emitir_som(): str
}
class Leao
class Macaco
class Arara
class Cobra
class Zoologico {
  +animais: list[Animal]
  +mover_todos(): None
  +emitir_sons(): None
}
Animal <|-- Leao
Animal <|-- Macaco
Animal <|-- Arara
Animal <|-- Cobra
Zoologico "1" o-- "0..*" Animal
@enduml

@startuml
abstract class Forma {
  +area(): float
}
class Retangulo
class Circulo
class Triangulo
Forma <|-- Retangulo
Forma <|-- Circulo
Forma <|-- Triangulo

interface Tocavel {
  +tocar(): str
}
class TocadorMP3
class Radio
TocadorMP3 ..|> Tocavel
Radio ..|> Tocavel
@enduml

@startuml
class RelatorioPedidos {
  -saida: SaidaRelatorio
  +gerar(pedidos): None
}
interface SaidaRelatorio {
  +escrever(texto: str): None
}
class Tela
class ArquivoFake {
  +linhas: list[str]
}
RelatorioPedidos --> SaidaRelatorio : injeta
Tela ..|> SaidaRelatorio
ArquivoFake ..|> SaidaRelatorio
@enduml

O zoologico e mover_todos trabalham com o metodo mover(), sem verificar a
classe concreta. Por isso Cobra e adicionada sem alterar mover_todos().
As formas usam area() polimorficamente. TocadorMP3 e Radio tem tocar() e
nao compartilham superclasse; o laço depende apenas desse comportamento.
RelatorioPedidos recebe sua saida no construtor, permitindo trocar Tela por
ArquivoFake sem alterar a classe do relatorio.
"""

from abc import ABC, abstractmethod
from math import pi, sqrt
from typing import Protocol


class Animal(ABC):
    def __init__(self, nome: str) -> None:
        if not nome.strip():
            raise ValueError("O nome do animal nao pode ficar vazio.")
        self.nome = nome

    @abstractmethod
    def mover(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def emitir_som(self) -> str:
        raise NotImplementedError


class Leao(Animal):
    def mover(self) -> str:
        return f"{self.nome} caminha pelo recinto."

    def emitir_som(self) -> str:
        return f"{self.nome} ruge: ROAR!"


class Macaco(Animal):
    def mover(self) -> str:
        return f"{self.nome} escala e pula entre os galhos."

    def emitir_som(self) -> str:
        return f"{self.nome} grita: Uh uh ah ah!"


class Arara(Animal):
    def mover(self) -> str:
        return f"{self.nome} voa pelo viveiro."

    def emitir_som(self) -> str:
        return f"{self.nome} grasna: Craa!"


class Cobra(Animal):
    def mover(self) -> str:
        return f"{self.nome} rasteja pelo terrario."

    def emitir_som(self) -> str:
        return f"{self.nome} sibila: Sss!"


class Zoologico:
    def __init__(self, animais: list[Animal]) -> None:
        self.animais = list(animais)

    def adicionar_animal(self, animal: Animal) -> None:
        self.animais.append(animal)

    def mover_todos(self) -> None:
        for animal in self.animais:
            print(animal.mover())

    def emitir_sons(self) -> None:
        for animal in self.animais:
            print(animal.emitir_som())


def mover_todos(animais: list[Animal]) -> list[str]:
    """Rotina original: aceita qualquer animal que implemente mover()."""
    movimentos = [animal.mover() for animal in animais]
    for movimento in movimentos:
        print(movimento)
    return movimentos


class Forma(ABC):
    @abstractmethod
    def area(self) -> float:
        raise NotImplementedError


class Retangulo(Forma):
    def __init__(self, largura: float, altura: float) -> None:
        if largura <= 0 or altura <= 0:
            raise ValueError("Largura e altura devem ser positivas.")
        self.largura = largura
        self.altura = altura

    def area(self) -> float:
        return self.largura * self.altura


class Circulo(Forma):
    def __init__(self, raio: float) -> None:
        if raio <= 0:
            raise ValueError("O raio deve ser positivo.")
        self.raio = raio

    def area(self) -> float:
        return pi * self.raio**2


class Triangulo(Forma):
    def __init__(self, lado_a: float, lado_b: float, lado_c: float) -> None:
        if min(lado_a, lado_b, lado_c) <= 0:
            raise ValueError("Os lados devem ser positivos.")
        if (
            lado_a + lado_b <= lado_c
            or lado_a + lado_c <= lado_b
            or lado_b + lado_c <= lado_a
        ):
            raise ValueError("As medidas nao formam um triangulo.")
        self.lado_a = lado_a
        self.lado_b = lado_b
        self.lado_c = lado_c

    def area(self) -> float:
        semiperimetro = (self.lado_a + self.lado_b + self.lado_c) / 2
        return sqrt(
            semiperimetro
            * (semiperimetro - self.lado_a)
            * (semiperimetro - self.lado_b)
            * (semiperimetro - self.lado_c)
        )


def area_total(formas: list[Forma]) -> float:
    return sum(forma.area() for forma in formas)


class Tocavel(Protocol):
    def tocar(self) -> str: ...


class TocadorMP3:
    def tocar(self) -> str:
        return "Tocador MP3: reproduzindo arquivo de audio."


class Radio:
    def tocar(self) -> str:
        return "Radio: reproduzindo uma estacao."


def tocar_todos(dispositivos: list[Tocavel]) -> None:
    for dispositivo in dispositivos:
        print(dispositivo.tocar())


class SaidaRelatorio(Protocol):
    def escrever(self, texto: str) -> None: ...


class Tela:
    def escrever(self, texto: str) -> None:
        print(texto)


class ArquivoFake:
    def __init__(self) -> None:
        self.linhas: list[str] = []

    def escrever(self, texto: str) -> None:
        self.linhas.append(texto)


class RelatorioPedidos:
    def __init__(self, saida: SaidaRelatorio) -> None:
        self.saida = saida

    def gerar(self, pedidos: list[str]) -> None:
        self.saida.escrever("Relatorio de pedidos")
        for pedido in pedidos:
            self.saida.escrever(f"- {pedido}")


def demonstrar_zoologico() -> None:
    print("=== Zoologico: Cobra sem mudar mover_todos ===")
    animais: list[Animal] = [
        Leao("Simba"),
        Macaco("Kiko"),
        Arara("Luna"),
    ]
    zoologico = Zoologico(animais)
    print("Movimentos antes de adicionar Cobra:")
    mover_todos(zoologico.animais)

    zoologico.adicionar_animal(Cobra("Naja"))
    print("Movimentos com Cobra, usando a mesma funcao:")
    movimentos = mover_todos(zoologico.animais)
    assert len(movimentos) == 4 and "Naja rasteja pelo terrario." in movimentos
    print("Verificado: mover_todos nao precisou de alteracoes para Cobra.")

    print("Sons dos animais (sem ramificacoes por tipo):")
    zoologico.emitir_sons()


def demonstrar_formas() -> None:
    print("\n=== Areas polimorficas ===")
    formas: list[Forma] = [
        Retangulo(4, 3),
        Circulo(2),
        Triangulo(3, 4, 5),
    ]
    for forma in formas:
        print(f"{forma.__class__.__name__}: area = {forma.area():.2f}")
    print(f"Area total: {area_total(formas):.2f}")


def demonstrar_duck_typing() -> None:
    print("\n=== Duck typing: objetos sem superclasse comum ===")
    dispositivos = [TocadorMP3(), Radio()]
    tocar_todos(dispositivos)


def demonstrar_injecao_de_dependencia() -> None:
    print("\n=== Injecao da saida do relatorio ===")
    pedidos = ["Pedido 101 - R$ 35.00", "Pedido 102 - R$ 18.50"]

    print("Saida pela tela:")
    RelatorioPedidos(Tela()).gerar(pedidos)

    saida_falsa = ArquivoFake()
    RelatorioPedidos(saida_falsa).gerar(pedidos)
    print("Conteudo capturado pelo ArquivoFake:")
    print("\n".join(saida_falsa.linhas))


def main() -> None:
    demonstrar_zoologico()
    demonstrar_formas()
    demonstrar_duck_typing()
    demonstrar_injecao_de_dependencia()


if __name__ == "__main__":
    main()
