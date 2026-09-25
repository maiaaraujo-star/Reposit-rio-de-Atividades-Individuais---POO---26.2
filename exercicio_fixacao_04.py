def main():
    distancia_ab = int(input("Digite a distância entre A e B: "))
    distancia_ac = int(input("Digite a distância entre A e C: "))
    distancia_bc = int(input("Digite a distância entre B e C: "))
    distancia_be = int(input("Digite a distância entre B e E: "))
    distancia_ce = int(input("Digite a distância entre C e E: "))

    distancia_a_b_e = distancia_ab + distancia_be
    distancia_a_c_e = distancia_ac + distancia_ce
    distancia_a_b_c_e = distancia_ab + distancia_bc + distancia_ce

    if distancia_a_b_e <= distancia_a_c_e and distancia_a_b_e <= distancia_a_b_c_e:
        print("Caminho percorrido: A → B → E")
        print(f"Distância percorrida: {distancia_a_b_e}")
    elif distancia_a_c_e <= distancia_a_b_e and distancia_a_c_e <= distancia_a_b_c_e:
        print("Caminho percorrido: A → C → E")
        print(f"Distância percorrida: {distancia_a_c_e}")
    else:
        print("Caminho percorrido: A → B → C → E")
        print(f"Distância percorrida: {distancia_a_b_c_e}")


if __name__ == "__main__":
    main()