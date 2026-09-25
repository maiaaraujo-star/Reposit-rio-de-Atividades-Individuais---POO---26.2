class Carro:
    def __init__(self, marca, modelo, cor):
        self.marca = marca
        self.modelo = modelo
        self.cor = cor
        self.velocidade = 0
        self.ligado = False

    def ligar(self):
        self.ligado = True
        print(f"O {self.marca} {self.modelo} foi ligado.")

    def desligar(self):
        if self.velocidade == 0:
            self.ligado = False
            print(f"O {self.marca} {self.modelo} foi desligado.")
        else:
            print("Não é possível desligar o carro em movimento.")

    def acelerar(self, quantidade):
        if self.ligado:
            self.velocidade += quantidade
            print(f"O carro acelerou para {self.velocidade} km/h.")
        else:
            print("Não é possível acelerar um carro desligado.")

    def frear(self, quantidade):
        self.velocidade = max(0, self.velocidade - quantidade)
        print(f"O carro está a {self.velocidade} km/h.")

    def buzinar(self):
        print("Bii bii!")


class Cachorro:
    def __init__(self, nome, raca, idade):
        self.nome = nome
        self.raca = raca
        self.idade = idade

    def latir(self):
        print(f"{self.nome} está latindo: Au au!")

    def comer(self, alimento):
        print(f"{self.nome} está comendo {alimento}.")

    def brincar(self, brinquedo):
        print(f"{self.nome} está brincando com {brinquedo}.")


def main():
    carro = Carro("Toyota", "Corolla", "prata")
    print(f"Carro: {carro.marca} {carro.modelo}, cor {carro.cor}.")
    carro.ligar()
    carro.acelerar(60)
    carro.buzinar()
    carro.frear(60)
    carro.desligar()

    cachorro = Cachorro("Rex", "Labrador", 3)
    print(f"Cachorro: {cachorro.nome}, raça {cachorro.raca}, {cachorro.idade} anos.")
    cachorro.latir()
    cachorro.comer("ração")
    cachorro.brincar("bola")


if __name__ == "__main__":
    main()