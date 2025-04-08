import sys

def posicao_para_xy(pos):
    return pos % 5, pos // 5

def distancia(p1, p2):
    x1, y1 = posicao_para_xy(p1)
    x2, y2 = posicao_para_xy(p2)
    return abs(x1 - x2) + abs(y1 - y2)

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

    # Regra 1, 5, 6
    if estou_perto:
        if vida_inimigo <= 1:
            print("attack")
            return
        if minha_vida >= vida_inimigo and (not inimigo_armado or estou_armado):
            print("attack")
            return
        if minha_vida < vida_inimigo:
            if pos_vida != -1 and minha_vida < 9:
                direcao = direcao_para(pos_jogador, pos_vida, pos_inimigo)
                if direcao:
                    print(direcao)
                    return
            direcao = direcao_para(pos_jogador, pos_inimigo, pos_inimigo)
            if not direcao:
                if not estou_armado and (minha_vida <= vida_inimigo // 2 or minha_vida <= 2):
                    print("block")
                    return
                print("attack")
                return
            else:
                print("attack")
                return

    # Nova Regra: Se estou ao lado da arma e posso pegar com segurança, priorizar pegar
    if not estou_armado and pos_arma != -1 and distancia(pos_jogador, pos_arma) == 1:
        if minha_vida >= vida_inimigo and minha_vida > 2:
            direcao = direcao_para(pos_jogador, pos_arma, pos_inimigo)
            if direcao:
                print(direcao)
                return

    # Regra 2
    if not estou_armado and pos_arma != -1:
        direcao = direcao_para(pos_jogador, pos_arma, pos_inimigo)
        if direcao:
            print(direcao)
            return

    # Regra 3
    if minha_vida < vida_inimigo and distancia(pos_jogador, pos_inimigo) <= 2:
        if pos_vida != -1 and minha_vida < 9:
            direcao = direcao_para(pos_jogador, pos_vida, pos_inimigo)
            if direcao:
                print(direcao)
                return
        if not estou_armado and pos_arma != -1:
            direcao = direcao_para(pos_jogador, pos_arma, pos_inimigo)
            if direcao:
                print(direcao)
                return
        direcao = direcao_para(pos_jogador, pos_inimigo, pos_inimigo)
        if direcao:
            print(direcao)
            return

    # Regra 4
    if estou_armado and minha_vida >= vida_inimigo:
        direcao = direcao_para(pos_jogador, pos_inimigo, pos_inimigo)
        if direcao:
            print(direcao)
            return

    # Regra 9
    if inimigo_armado and not estou_armado:
        if pos_vida != -1 and minha_vida < 9:
            direcao = direcao_para(pos_jogador, pos_vida, pos_inimigo)
            if direcao:
                print(direcao)
                return
        direcao = direcao_para(pos_jogador, pos_inimigo, pos_inimigo)
        if direcao:
            print(direcao)
            return

    # Regra 11 - só busca vida se tiver tomado dano
    if pos_vida != -1 and minha_vida < 9:
        direcao = direcao_para(pos_jogador, pos_vida, pos_inimigo)
        if direcao:
            print(direcao)
            return

    # Regra 7 - só defende se em desvantagem total
    if not estou_armado and (minha_vida <= vida_inimigo // 2 or minha_vida <= 2):
        print("block")
        return

    # Regra 10 - proibido ficar parado (movimenta-se)
    direcao = direcao_para(pos_jogador, pos_inimigo, pos_inimigo)
    if direcao:
        print(direcao)
        return

    print("block")

main()
