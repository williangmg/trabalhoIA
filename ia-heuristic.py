import sys

# Converte posição linear (0 a 24) para coordenadas (x, y)
def posicao_para_xy(pos):
    return pos % 5, pos // 5

# Calcula distância de Manhattan
def distancia(p1, p2):
    x1, y1 = posicao_para_xy(p1)
    x2, y2 = posicao_para_xy(p2)
    return abs(x1 - x2) + abs(y1 - y2)

# Calcula direção de movimento evitando colisão direta com o inimigo
def direcao_para(pos_inicial, pos_destino, pos_inimigo):
    x1, y1 = posicao_para_xy(pos_inicial)
    x2, y2 = posicao_para_xy(pos_destino)
    inimigo_x, inimigo_y = posicao_para_xy(pos_inimigo)

    if x1 < x2 and x1 + 1 != inimigo_x:
        return "right"
    if x1 > x2 and x1 - 1 != inimigo_x:
        return "left"
    if y1 < y2 and y1 + 1 != inimigo_y:
        return "down"
    if y1 > y2 and y1 - 1 != inimigo_y:
        return "up"
    return None

# Verifica se duas posições estão adjacentes
def perto(pos1, pos2):
    x1, y1 = posicao_para_xy(pos1)
    x2, y2 = posicao_para_xy(pos2)
    return abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1

def main():
    args = sys.argv
    jogador = int(args[1])
    estado = args[2]
    vida1, vida2 = int(args[3]), int(args[4])
    balas1, balas2 = int(args[5]), int(args[6])

    pos_jogador = estado.index(str(jogador))
    pos_inimigo = estado.index(str(2 if jogador == 1 else 1))
    pos_arma = estado.index("3") if "3" in estado else -1
    pos_vida = estado.index("4") if "4" in estado else -1

    minha_vida = vida1 if jogador == 1 else vida2
    vida_inimigo = vida2 if jogador == 1 else vida1
    minhas_balas = balas1 if jogador == 1 else balas2
    balas_inimigo = balas2 if jogador == 1 else balas1

    estou_armado = minhas_balas > 0
    inimigo_armado = balas_inimigo > 0
    estou_perto = perto(pos_jogador, pos_inimigo)

    # ⚔️ Se estou perto do inimigo
    if estou_perto:
        # Se posso matar o inimigo com 1 ataque, ataco!
        if vida_inimigo <= 1:
            print("attack")
            return
        # Se tenho mais vida, vale trocar
        if minha_vida > vida_inimigo:
            print("attack")
            return
        # Se tenho mesma vida E posso atacar primeiro, ataco
        if minha_vida == vida_inimigo and estou_armado:
            print("attack")
            return
        # Se estou em desvantagem de vida, evito confronto mesmo atacando primeiro
        if minha_vida < vida_inimigo:
            # Se tem vida no mapa e estou ferido, busco
            if pos_vida != -1 and minha_vida < 9:
                direcao = direcao_para(pos_jogador, pos_vida, pos_inimigo)
                if direcao:
                    print(direcao)
                    return
            # Se estou desarmado e inimigo armado, tento fugir
            if not estou_armado and inimigo_armado:
                if pos_vida != -1:
                    direcao = direcao_para(pos_jogador, pos_vida, pos_inimigo)
                    if direcao:
                        print(direcao)
                        return
            # Último recurso: atacar
            print("attack")
            return

    # 🛑 Se inimigo está armado e estou desarmado, fugir
    if inimigo_armado and not estou_armado:
        if pos_vida != -1 and minha_vida < 9:
            direcao = direcao_para(pos_jogador, pos_vida, pos_inimigo)
            if direcao:
                print(direcao)
                return
        if pos_vida != -1:
            direcao = direcao_para(pos_jogador, pos_vida, pos_inimigo)
            if direcao:
                print(direcao)
                return
        print("block")
        return

    # 🔫 Se estou desarmado e posso pegar a arma
    if not estou_armado and pos_arma != -1:
        # Se estou em desvantagem ou empate e NÃO posso atacar primeiro, pego a arma
        if minha_vida <= vida_inimigo:
            direcao = direcao_para(pos_jogador, pos_arma, pos_inimigo)
            if direcao:
                print(direcao)
                return
        # Se tenho mais vida E posso atacar primeiro, prefiro atacar
        if minha_vida > vida_inimigo and estou_perto:
            print("attack")
            return

    # 💊 Buscar vida se estiver ferido
    if pos_vida != -1 and minha_vida < 9:
        direcao = direcao_para(pos_jogador, pos_vida, pos_inimigo)
        if direcao:
            print(direcao)
            return

    # 👣 Aproxima-se do inimigo se nada mais a fazer
    direcao = direcao_para(pos_jogador, pos_inimigo, pos_inimigo)
    if direcao:
        print(direcao)
        return

    # 🧱 Último recurso: defende
    print("block")

main()
