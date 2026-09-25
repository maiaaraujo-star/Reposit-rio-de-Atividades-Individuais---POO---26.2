class Aluno:
    # Questão 6: classe Aluno com lista interna de notas.
    def __init__(self, nome: str, matricula: str):
        self.nome = nome
        self.matricula = matricula
        self.notas: list[float] = []

    def lancar_nota(self, valor: float) -> None:
        self.notas.append(valor)

    def media(self) -> float:
        if not self.notas:
            return 0.0
        return sum(self.notas) / len(self.notas)

    def aprovado(self) -> bool:
        return self.media() >= 6

    def __str__(self) -> str:
        return f"{self.nome} ({self.matricula}) — média {self.media():g}"


class Retangulo:
    # Questão 8: classe Retangulo com área, perímetro e comparação.
    def __init__(self, base: float, altura: float):
        self.base = base
        self.altura = altura

    def area(self) -> float:
        return self.base * self.altura

    def perimetro(self) -> float:
        return 2 * (self.base + self.altura)

    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, Retangulo):
            return NotImplemented
        return self.base == outro.base and self.altura == outro.altura


class Data:
    # Questão 9: classe Data com construtor por texto e ano bissexto.
    def __init__(self, dia: int, mes: int, ano: int):
        self.dia = dia
        self.mes = mes
        self.ano = ano

    @classmethod
    def de_texto(cls, texto: str) -> "Data":
        dia, mes, ano = (int(parte) for parte in texto.split("/"))
        return cls(dia, mes, ano)

    @staticmethod
    def bissexto(ano: int) -> bool:
        return ano % 400 == 0 or (ano % 4 == 0 and ano % 100 != 0)

    def __str__(self) -> str:
        return f"{self.dia:02d}/{self.mes:02d}/{self.ano:04d}"


def main() -> None:
    # Questão 7: criação de três alunos e impressão apenas dos aprovados.
    alunos = [
        Aluno("Ana", "20261234"),
        Aluno("Bruno", "20261235"),
        Aluno("Carla", "20261236"),
    ]

    alunos[0].lancar_nota(8.0)
    alunos[0].lancar_nota(7.0)
    alunos[1].lancar_nota(5.0)
    alunos[1].lancar_nota(4.5)
    alunos[2].lancar_nota(6.0)
    alunos[2].lancar_nota(6.5)

    print("Alunos aprovados:")
    for aluno in alunos:
        if aluno.aprovado():
            print(aluno)

    retangulo_a = Retangulo(5.0, 3.0)
    retangulo_b = Retangulo(5.0, 3.0)
    print(f"\nÁrea do retângulo: {retangulo_a.area():g}")
    print(f"Perímetro do retângulo: {retangulo_a.perimetro():g}")
    print(f"Retângulos iguais: {retangulo_a == retangulo_b}")

    data = Data.de_texto("09/08/2026")
    print(f"Data: {data}")
    print(f"2026 é bissexto: {Data.bissexto(2026)}")


if __name__ == "__main__":
    main()