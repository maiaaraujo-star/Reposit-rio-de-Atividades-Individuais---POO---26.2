"""Exercicios de composicao, agregacao e associacao.

Sistema de pedidos - diagrama de classes UML (PlantUML):

@startuml
class Cliente {
  +nome: str
  +fazer_pedido(): Pedido
}
class Pedido {
  +adicionar_item(produto: Produto, quantidade: int): None
  +total(): float
  +__str__(): str
}
class ItemPedido {
  +quantidade: int
  +preco_unitario: float
  +subtotal(): float
}
class Produto {
  +codigo: str
  +nome: str
  +preco: float
}
class Catalogo {
  +adicionar(produto: Produto): None
  +remover(codigo: str): Produto
}

Cliente "1" --> "0..*" Pedido : faz / associado a
Pedido "1" *-- "0..*" ItemPedido : compoe
ItemPedido "0..*" --> "1" Produto : referencia
Catalogo "1" o-- "0..*" Produto : agrega
@enduml

Cliente.fazer_pedido cria um Pedido e estabelece um vinculo Cliente-Pedido.
Esse vinculo e uma associacao, nao necessariamente composicao: o fato de o
cliente criar o pedido nao determina que o pedido deixe de existir se o
cliente for removido. Pedidos normalmente precisam ser mantidos como historico.
O pedido compoe seus itens, que nao fazem sentido sem ele; o catalogo agrega
produtos, que existem independentemente do catalogo. A linha do pedido apenas
referencia o produto para identificar o item comprado.

Predio e Apartamento usam composicao: os apartamentos sao criados pelo predio.
Time e Jogador usam agregacao: jogadores existem independentemente e podem
trocar de time.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Produto:
    codigo: str
    nome: str
    preco: float

    def __post_init__(self) -> None:
        if not self.codigo.strip():
            raise ValueError("O codigo do produto nao pode ficar vazio.")
        if not self.nome.strip():
            raise ValueError("O nome do produto nao pode ficar vazio.")
        if self.preco < 0:
            raise ValueError("O preco nao pode ser negativo.")

    def apresentar_informacoes(self) -> str:
        return f"{self.codigo} - {self.nome}: R$ {self.preco:.2f}"


class Catalogo:
    def __init__(self) -> None:
        self.produtos: dict[str, Produto] = {}

    def adicionar(self, produto: Produto) -> None:
        if produto.codigo in self.produtos:
            raise ValueError(f"O produto {produto.codigo} ja esta no catalogo.")
        self.produtos[produto.codigo] = produto

    def remover(self, codigo: str) -> Produto:
        try:
            return self.produtos.pop(codigo)
        except KeyError as erro:
            raise ValueError(f"Produto {codigo} nao encontrado.") from erro

    def apresentar_informacoes(self) -> None:
        print("\nCatalogo:")
        for produto in self.produtos.values():
            print(f"- {produto.apresentar_informacoes()}")


@dataclass(frozen=True)
class ItemPedido:
    produto: Produto
    quantidade: int
    preco_unitario: float

    def __post_init__(self) -> None:
        if self.quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")

    def subtotal(self) -> float:
        return self.quantidade * self.preco_unitario

    def apresentar_informacoes(self) -> str:
        return (
            f"{self.produto.nome} x {self.quantidade} "
            f"(R$ {self.preco_unitario:.2f} cada): R$ {self.subtotal():.2f}"
        )


class Pedido:
    def __init__(self, cliente: Cliente) -> None:
        self.cliente = cliente
        self.itens: list[ItemPedido] = []

    def adicionar_item(self, produto: Produto, quantidade: int) -> None:
        item = ItemPedido(produto, quantidade, produto.preco)
        self.itens.append(item)

    def total(self) -> float:
        return sum(item.subtotal() for item in self.itens)

    def __str__(self) -> str:
        linhas = [
            f"Pedido de {self.cliente.nome}:",
            *(f"- {item.apresentar_informacoes()}" for item in self.itens),
            f"Total: R$ {self.total():.2f}",
        ]
        return "\n".join(linhas)

    def apresentar_informacoes(self) -> None:
        print(self)


class Cliente:
    def __init__(self, nome: str) -> None:
        if not nome.strip():
            raise ValueError("O nome do cliente nao pode ficar vazio.")
        self.nome = nome
        self.pedidos: list[Pedido] = []

    def fazer_pedido(self) -> Pedido:
        pedido = Pedido(self)
        self.pedidos.append(pedido)
        return pedido

    def apresentar_informacoes(self) -> None:
        print(f"Cliente: {self.nome}; pedidos: {len(self.pedidos)}.")


class Apartamento:
    def __init__(self, andar: int, numero: int) -> None:
        self.andar = andar
        self.numero = numero

    def apresentar_informacoes(self) -> None:
        print(f"Apartamento {self.numero}, andar {self.andar}.")


class Predio:
    def __init__(self, numero_andares: int, apartamentos_por_andar: int = 1) -> None:
        if numero_andares <= 0:
            raise ValueError("O predio deve ter pelo menos um andar.")
        if apartamentos_por_andar <= 0:
            raise ValueError("Deve haver pelo menos um apartamento por andar.")
        self.numero_andares = numero_andares
        self.apartamentos: list[Apartamento] = [
            Apartamento(andar, numero)
            for andar in range(1, numero_andares + 1)
            for numero in range(
                (andar - 1) * apartamentos_por_andar + 1,
                andar * apartamentos_por_andar + 1,
            )
        ]

    def apresentar_informacoes(self) -> None:
        print(
            f"\nPredio com {self.numero_andares} andar(es) "
            f"e {len(self.apartamentos)} apartamento(s):"
        )
        for apartamento in self.apartamentos:
            apartamento.apresentar_informacoes()


class Jogador:
    def __init__(self, nome: str) -> None:
        if not nome.strip():
            raise ValueError("O nome do jogador nao pode ficar vazio.")
        self.nome = nome
        self.time: Time | None = None

    def trocar_de_time(self, novo_time: Time) -> None:
        novo_time.adicionar_jogador(self)

    def apresentar_informacoes(self) -> None:
        nome_time = self.time.nome if self.time is not None else "sem time"
        print(f"Jogador: {self.nome}; time: {nome_time}.")


class Time:
    def __init__(self, nome: str) -> None:
        if not nome.strip():
            raise ValueError("O nome do time nao pode ficar vazio.")
        self.nome = nome
        self.jogadores: list[Jogador] = []

    def adicionar_jogador(self, jogador: Jogador) -> None:
        if jogador.time is self:
            return
        if jogador.time is not None:
            jogador.time.remover_jogador(jogador)
        self.jogadores.append(jogador)
        jogador.time = self
        print(f"{jogador.nome} agora faz parte do time {self.nome}.")

    def remover_jogador(self, jogador: Jogador) -> None:
        if jogador not in self.jogadores:
            raise ValueError(f"{jogador.nome} nao pertence ao time {self.nome}.")
        self.jogadores.remove(jogador)
        jogador.time = None

    def apresentar_informacoes(self) -> None:
        nomes = ", ".join(jogador.nome for jogador in self.jogadores) or "nenhum"
        print(f"Time {self.nome}; jogadores: {nomes}.")


def demonstrar_sistema_de_pedidos() -> None:
    print("=== Sistema de pedidos ===")
    catalogo = Catalogo()
    produto_1 = Produto("P001", "Caderno", 18.50)
    produto_2 = Produto("P002", "Caneta", 4.25)
    catalogo.adicionar(produto_1)
    catalogo.adicionar(produto_2)
    catalogo.apresentar_informacoes()

    cliente = Cliente("Marina")
    pedido = cliente.fazer_pedido()
    pedido.adicionar_item(produto_1, 2)
    pedido.adicionar_item(produto_2, 3)
    cliente.apresentar_informacoes()
    pedido.apresentar_informacoes()


def demonstrar_predio() -> None:
    print("\n=== Predio e apartamentos ===")
    Predio(numero_andares=3, apartamentos_por_andar=2).apresentar_informacoes()


def demonstrar_times() -> None:
    print("\n=== Time agrega jogadores ===")
    time_azul = Time("Azul")
    time_verde = Time("Verde")
    jogador = Jogador("Rafa")

    time_azul.adicionar_jogador(jogador)
    time_azul.apresentar_informacoes()
    jogador.trocar_de_time(time_verde)
    time_azul.apresentar_informacoes()
    time_verde.apresentar_informacoes()
    jogador.apresentar_informacoes()


def main() -> None:
    demonstrar_sistema_de_pedidos()
    demonstrar_predio()
    demonstrar_times()


if __name__ == "__main__":
    main()
