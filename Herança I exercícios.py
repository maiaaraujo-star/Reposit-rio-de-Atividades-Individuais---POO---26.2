"""Exercicios de heranca: especializacao, sobrescrita e substituibilidade.

UML (PlantUML):

@startuml
class Animal {
  # nome: str
  # peso: float
  # posicao: int
  + mover_se(): None
  + apresentar(): None
}
class Gato {
  - na_arvore: bool
  + miar(): None
  + subir_na_arvore(): None
  + descer_da_arvore(): None
  + esta_na_arvore(): bool
}
class Cachorro {
  - qtd_saltos: int
  + latir(): None
  + saltar(): None
  + descansar(): None
  + esta_cansado(): bool
}
class Passaro {
  + envergadura: float
  + __str__(): str
}
Animal <|-- Gato
Animal <|-- Cachorro
Animal <|-- Passaro

class Funcionario {
  # nome: str
  # salario: float
  + apresentar(): None
}
class Gerente {
  + equipe: list[str]
  + apresentar(): None
}
Funcionario <|-- Gerente

class Retangulo {
  + largura: float
  + altura: float
  + redimensionar(largura, altura): None
}
class RetanguloColorido {
  + cor: str
}
class Quadrado
Retangulo <|-- RetanguloColorido
Retangulo <|-- Quadrado
@enduml

RetanguloColorido preserva o contrato geometrico de Retangulo: a cor nao
altera largura, altura ou redimensionamento, entao e substituivel.
Quadrado pode violar o principio de substituicao de Liskov se Retangulo
permite alterar largura e altura independentemente. O exemplo abaixo mostra
um cliente que aumenta apenas a largura e espera que a altura nao mude.
"""

from abc import ABC, abstractmethod


class Animal(ABC):
    def __init__(self, nome: str, peso: float, posicao: int = 0) -> None:
        if not nome.strip():
            raise ValueError("O nome do animal nao pode ficar vazio.")
        if peso <= 0:
            raise ValueError("O peso deve ser positivo.")
        self.nome = nome
        self.peso = peso
        self.posicao = posicao

    @abstractmethod
    def emitir_som(self) -> str:
        raise NotImplementedError

    def mover_se(self) -> None:
        self.posicao += 1
        print(f"{self.nome} se moveu para a posicao {self.posicao}.")

    def apresentar(self) -> None:
        print(
            f"{self.__class__.__name__}: {self.nome}, "
            f"{self.peso:.1f} kg, posicao {self.posicao}. "
            f"Som: {self.emitir_som()}"
        )

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}: {self.nome}, "
            f"{self.peso:.1f} kg, posicao {self.posicao}."
        )


class Gato(Animal):
    def __init__(self, nome: str, peso: float, posicao: int = 0) -> None:
        super().__init__(nome, peso, posicao)
        self.na_arvore = False

    def emitir_som(self) -> str:
        return "Miau!"

    def miar(self) -> None:
        print(f"{self.nome}: {self.emitir_som()}")

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

    def emitir_som(self) -> str:
        return "Au au!"

    def latir(self) -> None:
        print(f"{self.nome}: {self.emitir_som()}")

    def saltar(self) -> None:
        self.qtd_saltos += 1
        print(f"{self.nome} saltou. Total de saltos: {self.qtd_saltos}.")

    def descansar(self) -> None:
        self.qtd_saltos = max(0, self.qtd_saltos - 1)
        print(f"{self.nome} descansou. Total de saltos: {self.qtd_saltos}.")

    def esta_cansado(self) -> bool:
        return self.qtd_saltos > self.LIMITE_SALTOS_CANSADO


class Passaro(Animal):
    def __init__(
        self,
        nome: str,
        peso: float,
        envergadura: float,
        posicao: int = 0,
    ) -> None:
        super().__init__(nome, peso, posicao)
        if envergadura <= 0:
            raise ValueError("A envergadura deve ser positiva.")
        self.envergadura = envergadura

    def emitir_som(self) -> str:
        return "Piu!"

    def __str__(self) -> str:
        return f"{super().__str__()} Envergadura: {self.envergadura:.2f} m."


class Funcionario:
    def __init__(self, nome: str, salario: float) -> None:
        if not nome.strip():
            raise ValueError("O nome do funcionario nao pode ficar vazio.")
        if salario < 0:
            raise ValueError("O salario nao pode ser negativo.")
        self.nome = nome
        self.salario = salario

    def apresentar(self) -> None:
        print(f"Funcionario: {self.nome}; salario: R$ {self.salario:.2f}.")


class Gerente(Funcionario):
    def __init__(self, nome: str, salario: float, equipe: list[str]) -> None:
        super().__init__(nome, salario)
        self.equipe = list(equipe)

    def apresentar(self) -> None:
        print(
            f"Gerente: {self.nome}; salario: R$ {self.salario:.2f}; "
            f"tamanho da equipe: {len(self.equipe)}."
        )


class Retangulo:
    def __init__(self, largura: float, altura: float) -> None:
        if largura <= 0 or altura <= 0:
            raise ValueError("Largura e altura devem ser positivas.")
        self.largura = largura
        self.altura = altura

    def redimensionar(self, largura: float, altura: float) -> None:
        if largura <= 0 or altura <= 0:
            raise ValueError("Largura e altura devem ser positivas.")
        self.largura = largura
        self.altura = altura

    def area(self) -> float:
        return self.largura * self.altura


class RetanguloColorido(Retangulo):
    def __init__(self, largura: float, altura: float, cor: str) -> None:
        super().__init__(largura, altura)
        if not cor.strip():
            raise ValueError("A cor nao pode ficar vazia.")
        self.cor = cor


class Quadrado(Retangulo):
    def __init__(self, lado: float) -> None:
        super().__init__(lado, lado)

    def redimensionar(self, largura: float, altura: float) -> None:
        if largura != altura:
            raise ValueError("Um quadrado exige largura e altura iguais.")
        super().redimensionar(largura, altura)


def aumentar_largura(retangulo: Retangulo) -> None:
    """Cliente que usa o contrato de retangulo com dimensoes independentes."""
    retangulo.redimensionar(retangulo.largura + 1, retangulo.altura)


def demonstrar_animais() -> None:
    print("=== Animais ===")
    animais: list[Animal] = [
        Gato("Mimi", 4.2),
        Cachorro("Rex", 12.5),
        Passaro("Piu", 0.3, 0.25),
    ]

    print("Todos os animais se movimentam:")
    for animal in animais:
        animal.mover_se()
        animal.apresentar()
    print(f"\n{animais[2]}")

    gato = animais[0]
    cachorro = animais[1]
    if isinstance(gato, Gato):
        gato.miar()
        gato.subir_na_arvore()
        print(f"{gato.nome} esta na arvore? {gato.esta_na_arvore()}")
        gato.descer_da_arvore()
    if isinstance(cachorro, Cachorro):
        cachorro.latir()
        for _ in range(6):
            cachorro.saltar()
        print(f"{cachorro.nome} esta cansado? {cachorro.esta_cansado()}")
        cachorro.descansar()


def demonstrar_funcionarios() -> None:
    print("\n=== Funcionarios ===")
    funcionario = Funcionario("Joao", 3200)
    gerente = Gerente("Ana", 6500, ["Bia", "Caio", "Lia"])
    funcionario.apresentar()
    gerente.apresentar()


def demonstrar_substituibilidade() -> None:
    print("\n=== RetanguloColorido e Quadrado ===")
    retangulo_colorido = RetanguloColorido(4, 2, "azul")
    aumentar_largura(retangulo_colorido)
    print(
        f"RetanguloColorido permanece substituivel: "
        f"{retangulo_colorido.largura} x {retangulo_colorido.altura}, "
        f"cor {retangulo_colorido.cor}."
    )

    quadrado = Quadrado(2)
    try:
        aumentar_largura(quadrado)
    except ValueError as erro:
        print(f"Quadrado nao atende o contrato independente de Retangulo: {erro}")


def main() -> None:
    demonstrar_animais()
    demonstrar_funcionarios()
    demonstrar_substituibilidade()


if __name__ == "__main__":
    main()
