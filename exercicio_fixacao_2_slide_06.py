def pais_com_maior_populacao(populacoes):
    return max(populacoes, key=populacoes.get)


def alunos_aprovados(notas):
    aprovados = {}

    for aluno, notas_aluno in notas.items():
        media = sum(notas_aluno) / len(notas_aluno)

        if media >= 7:
            aprovados[aluno] = round(media, 2)

    return aprovados


def main():
    populacoes = {"Brasil": 211.8, "China": 1400.5, "Índia": 1366.4}
    notas = {
        "Ana": [8.5, 9.0, 7.5],
        "Bruno": [6.0, 5.5, 4.0],
        "Carla": [7.0, 8.0, 9.0],
    }

    print(f"País com maior população: {pais_com_maior_populacao(populacoes)}")
    print(f"Alunos aprovados: {alunos_aprovados(notas)}")


if __name__ == "__main__":
    main()