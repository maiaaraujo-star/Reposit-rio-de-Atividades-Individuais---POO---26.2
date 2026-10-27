"""Exercicios em sala: Relacionamentos I - Associacao e Agregacao.

UML (PlantUML), para reproduzir em uma ferramenta de diagramacao:

@startuml
class Motorista {
  +nome: str
  +dirigir(veiculo: Veiculo): None
}
class Veiculo {
  +modelo: str
}
Motorista "0..*" -- "0..*" Veiculo : dirige

class Playlist {
  +adicionar(musica: Musica): None
  +remover(musica: Musica): None
  +duracao_total(): int
  +tocar(caixa_de_som: CaixaDeSom): None
}
class Musica {
  +titulo: str
  +duracao_segundos: int
}
class CaixaDeSom {
  +reproduzir(playlist: Playlist): None
}
Playlist "1" o-- "0..*" Musica : agrega
Playlist ..> CaixaDeSom : usa
@enduml

Playlist agrega Musica porque guarda referencias a objetos criados fora dela.
O uso de CaixaDeSom como parametro e uma dependencia (relacao de uso).
Biblioteca e Livro normalmente representam agregacao: um livro pode existir
independentemente da biblioteca. Se a regra do problema disser que os livros
so existem enquanto pertencem a uma biblioteca, a relacao seria composicao.
"""


class Motorista:
    def __init__(self, nome: str):
        self.nome = nome

    def dirigir(self, veiculo: "Veiculo") -> None:
        print(f"{self.nome} dirige o veiculo {veiculo.modelo}.")


class Veiculo:
    def __init__(self, modelo: str):
        self.modelo = modelo


class Musica:
    def __init__(self, titulo: str, duracao_segundos: int):
        self.titulo = titulo
        self.duracao_segundos = duracao_segundos


class CaixaDeSom:
    def reproduzir(self, playlist: "Playlist") -> None:
        for musica in playlist.musicas:
            print(f"Tocando: {musica.titulo}")


class Playlist:
    def __init__(self, nome: str):
        self.nome = nome
        self.musicas: list[Musica] = []

    def adicionar(self, musica: Musica) -> None:
        self.musicas.append(musica)

    def remover(self, musica: Musica) -> None:
        self.musicas.remove(musica)

    def duracao_total(self) -> int:
        return sum(musica.duracao_segundos for musica in self.musicas)

    def tocar(self, caixa_de_som: CaixaDeSom) -> None:
        caixa_de_som.reproduzir(self)


def main() -> None:
    motorista = Motorista("Ana")
    veiculo = Veiculo("hatch")
    motorista.dirigir(veiculo)

    musica_1 = Musica("Primeira musica", 180)
    musica_2 = Musica("Segunda musica", 210)
    playlist = Playlist("Favoritas")
    playlist.adicionar(musica_1)
    playlist.adicionar(musica_2)
    print(f"Duracao total: {playlist.duracao_total()} segundos.")

    caixa_de_som = CaixaDeSom()
    playlist.tocar(caixa_de_som)


if __name__ == "__main__":
    main()
