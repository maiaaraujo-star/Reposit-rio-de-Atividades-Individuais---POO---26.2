"""Simulacao de casa: associacao, agregacao e composicao.

Diagrama de classes UML (PlantUML):

@startuml
class Casa {
  +comodos: list[Comodo]
  +adicionar_comodo(comodo): None
  +apresentar_informacoes(): None
}
class Comodo {
  +nome: str
  +cor: str
  +apresentar_informacoes(): None
}
abstract class ComponenteEletrico {
  +ligado: bool
  +alternar(): None
  +apresentar_informacoes(): None
}
class Lampada
class ArCondicionado
class Interruptor {
  +acionar(nome_comodo): None
  +apresentar_informacoes(): None
}
class Porta {
  +abrir(chave, senha): bool
  +apresentar_informacoes(): None
}
abstract class Fechadura {
  +abrir(chave, senha): bool
  +apresentar_informacoes(): None
}
class FechaduraSimples
class FechaduraInteligente
class Pessoa {
  +visitar(casa): None
  +acionar_interruptor(comodo, tipo): None
  +abrir_porta(comodo, chave, senha): bool
}

Casa "1" *-- "1..10" Comodo : possui
Comodo "1" *-- "1" Lampada : possui
Comodo "1" *-- "1..*" Porta : possui
Porta "1" *-- "1" Fechadura : e formada por
Fechadura <|-- FechaduraSimples
Fechadura <|-- FechaduraInteligente
ComponenteEletrico <|-- Lampada
ComponenteEletrico <|-- ArCondicionado
Comodo "1" *-- "1..2" Interruptor : possui
Comodo "1" *-- "0..1" ArCondicionado : pode possuir
Interruptor "1" --> "1" ComponenteEletrico : controla
Pessoa "0..*" -- "0..*" Casa : visita
Pessoa ..> Interruptor : aciona
Pessoa ..> Porta : abre
@enduml

Casa, comodos, componentes, portas e fechaduras usam composicao: seus objetos
sao criados e mantidos dentro da estrutura que os possui. Pessoa visita a Casa
por associacao, e os metodos que recebem interruptores/portas representam uso.
"""

from abc import ABC, abstractmethod
from typing import Optional


class ComponenteEletrico:
    def __init__(self) -> None:
        self.ligado = False

    def alternar(self) -> None:
        self.ligado = not self.ligado

    def apresentar_informacoes(self) -> None:
        estado = "ligado" if self.ligado else "desligado"
        print(f"{self.__class__.__name__}: {estado}.")


class Lampada(ComponenteEletrico):
    pass


class ArCondicionado(ComponenteEletrico):
    pass


class Interruptor:
    def __init__(self, componente: ComponenteEletrico, descricao: str) -> None:
        self.componente = componente
        self.descricao = descricao

    def acionar(self, nome_comodo: str) -> None:
        self.componente.alternar()
        acao = "acendeu" if self.componente.ligado else "apagou"
        print(
            f"{acao.capitalize()} {self.descricao} do comodo {nome_comodo}."
        )

    def apresentar_informacoes(self) -> None:
        print(f"Interruptor: controla {self.descricao}.")


class Fechadura(ABC):
    def __init__(self, chave_correta: str) -> None:
        self._chave_correta = chave_correta

    @abstractmethod
    def abrir(self, chave: str, senha: Optional[str] = None) -> bool:
        raise NotImplementedError

    def apresentar_informacoes(self) -> None:
        print(f"Fechadura: {self.__class__.__name__}.")


class FechaduraSimples(Fechadura):
    def abrir(self, chave: str, senha: Optional[str] = None) -> bool:
        return chave == self._chave_correta


class FechaduraInteligente(Fechadura):
    def __init__(self, chave_correta: str, senha_correta: str) -> None:
        super().__init__(chave_correta)
        self._senha_correta = senha_correta

    def abrir(self, chave: str, senha: Optional[str] = None) -> bool:
        return chave == self._chave_correta or senha == self._senha_correta


class Porta:
    def __init__(self, comodo: str, fechadura: Fechadura) -> None:
        if not isinstance(fechadura, Fechadura):
            raise TypeError("Uma porta deve possuir exatamente uma fechadura.")
        self.comodo = comodo
        self.fechadura = fechadura
        self.aberta = False

    def abrir(self, chave: str, senha: Optional[str] = None) -> bool:
        if self.fechadura.abrir(chave, senha):
            self.aberta = True
            print(f"A porta do comodo {self.comodo} foi aberta.")
            return True

        print(f"A porta do comodo {self.comodo} nao abriu: acesso negado.")
        return False

    def apresentar_informacoes(self) -> None:
        estado = "aberta" if self.aberta else "fechada"
        print(f"Porta do comodo {self.comodo}: {estado}.")
        self.fechadura.apresentar_informacoes()


class Comodo:
    def __init__(
        self,
        nome: str,
        cor: str,
        fechadura: Fechadura,
        possui_ar_condicionado: bool,
    ) -> None:
        self.nome = nome
        self.cor = cor
        self.lampada = Lampada()
        self.interruptor_lampada = Interruptor(self.lampada, "a lampada")
        self.ar_condicionado: Optional[ArCondicionado] = None
        self.interruptor_ar_condicionado: Optional[Interruptor] = None
        if possui_ar_condicionado:
            self.ar_condicionado = ArCondicionado()
            self.interruptor_ar_condicionado = Interruptor(
                self.ar_condicionado, "o ar-condicionado"
            )
        self.portas = [Porta(nome, fechadura)]

    def apresentar_informacoes(self) -> None:
        ar = "sim" if self.ar_condicionado is not None else "nao"
        print(f"\nComodo: {self.nome}; cor: {self.cor}; ar-condicionado: {ar}.")
        self.lampada.apresentar_informacoes()
        self.interruptor_lampada.apresentar_informacoes()
        if self.ar_condicionado is not None:
            self.ar_condicionado.apresentar_informacoes()
            self.interruptor_ar_condicionado.apresentar_informacoes()
        for porta in self.portas:
            porta.apresentar_informacoes()


class Casa:
    LIMITE_COMODOS = 10

    def __init__(self) -> None:
        self.comodos: list[Comodo] = []

    def adicionar_comodo(self, comodo: Comodo) -> None:
        if len(self.comodos) >= self.LIMITE_COMODOS:
            raise ValueError("A casa pode ter no maximo 10 comodos.")
        self.comodos.append(comodo)

    def apresentar_informacoes(self) -> None:
        print(f"\nCasa com {len(self.comodos)} comodo(s).")
        for comodo in self.comodos:
            comodo.apresentar_informacoes()


class Pessoa:
    def __init__(self, nome: str) -> None:
        self.nome = nome
        self.casa_visitada: Optional[Casa] = None

    def visitar(self, casa: Casa) -> None:
        self.casa_visitada = casa
        print(f"\n{self.nome} esta visitando a casa.")

    def _validar_comodo_visitado(self, comodo: Comodo) -> bool:
        if (
            self.casa_visitada is None
            or comodo not in self.casa_visitada.comodos
        ):
            print(f"{self.nome} nao esta visitando o comodo {comodo.nome}.")
            return False
        return True

    def acionar_interruptor(self, comodo: Comodo, tipo: str) -> None:
        if not self._validar_comodo_visitado(comodo):
            return
        if tipo == "lampada":
            interruptor = comodo.interruptor_lampada
        elif tipo == "ar-condicionado":
            interruptor = comodo.interruptor_ar_condicionado
            if interruptor is None:
                print(f"O comodo {comodo.nome} nao possui ar-condicionado.")
                return
        else:
            raise ValueError("Tipo de interruptor deve ser lampada ou ar-condicionado.")
        interruptor.acionar(comodo.nome)

    def abrir_porta(
        self,
        comodo: Comodo,
        chave: str,
        senha: Optional[str] = None,
    ) -> bool:
        if not self._validar_comodo_visitado(comodo):
            return False
        return comodo.portas[0].abrir(chave, senha)

    def apresentar_informacoes(self) -> None:
        print(f"Pessoa visitante: {self.nome}.")


def solicitar_texto(mensagem: str) -> str:
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("O valor nao pode ficar vazio.")


def solicitar_sim_nao(mensagem: str) -> bool:
    while True:
        resposta = input(mensagem).strip().lower()
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "nao", "não"):
            return False
        print("Responda com sim ou nao.")


def solicitar_quantidade_comodos() -> int:
    while True:
        try:
            quantidade = int(input("Quantos comodos a casa tera (1 a 10)? "))
        except ValueError:
            print("Digite um numero inteiro entre 1 e 10.")
            continue
        if 1 <= quantidade <= Casa.LIMITE_COMODOS:
            return quantidade
        print("A quantidade deve estar entre 1 e 10.")


def criar_casa_pelo_terminal() -> tuple[Casa, list[tuple[Comodo, str, Optional[str]]]]:
    casa = Casa()
    credenciais_teste: list[tuple[Comodo, str, Optional[str]]] = []
    quantidade = solicitar_quantidade_comodos()

    for numero in range(1, quantidade + 1):
        print(f"\nConfiguracao do comodo {numero}")
        nome = solicitar_texto("Nome do comodo: ")
        cor = solicitar_texto("Cor do comodo: ")
        possui_ar = solicitar_sim_nao("Possui ar-condicionado? (s/n): ")

        while True:
            tipo_fechadura = input(
                "Tipo de fechadura (simples/inteligente): "
            ).strip().lower()
            if tipo_fechadura in ("simples", "inteligente"):
                break
            print("Escolha simples ou inteligente.")

        chave = solicitar_texto("Defina a unica chave correta da fechadura: ")
        senha: Optional[str] = None
        if tipo_fechadura == "inteligente":
            senha = solicitar_texto("Defina a senha da fechadura: ")
            fechadura: Fechadura = FechaduraInteligente(chave, senha)
        else:
            fechadura = FechaduraSimples(chave)

        comodo = Comodo(nome, cor, fechadura, possui_ar)
        casa.adicionar_comodo(comodo)
        credenciais_teste.append((comodo, chave, senha))

    return casa, credenciais_teste


def executar_cenario_teste(
    casa: Casa,
    credenciais_teste: list[tuple[Comodo, str, Optional[str]]],
) -> None:
    visitante = Pessoa(solicitar_texto("\nNome da pessoa visitante: "))
    visitante.apresentar_informacoes()
    visitante.visitar(casa)
    casa.apresentar_informacoes()

    print("\n--- Cenario de teste: acionamentos e abertura das portas ---")
    for comodo, chave, senha in credenciais_teste:
        visitante.acionar_interruptor(comodo, "lampada")
        if comodo.ar_condicionado is not None:
            visitante.acionar_interruptor(comodo, "ar-condicionado")
        visitante.abrir_porta(comodo, chave, senha)


def main() -> None:
    casa, credenciais_teste = criar_casa_pelo_terminal()
    executar_cenario_teste(casa, credenciais_teste)


if __name__ == "__main__":
    main()
