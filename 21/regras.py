import os
import time
from cartas import mostra_mesa, distribuir_carta, soma_mao
    
def vez_da_banca(mao_banca, baralho, rodada, ponto_jogador, ponto_banca, mao_jogador, fichas_jogador, fichas_banca, aposta_jogador, aposta_banca):
    os.system('cls')
    mostra_mesa(rodada, ponto_jogador, ponto_banca, mao_jogador, mao_banca, fichas_jogador, fichas_banca, aposta_jogador, aposta_banca)
    
    if soma_mao(mao_banca) >= 17:
        print('Banca parou')
        time.sleep(2)
        return soma_mao(mao_banca)
    
    while soma_mao(mao_banca) < 17:
        print('Banca compra carta...')
        time.sleep(2)
        os.system('cls')
        carta = distribuir_carta(baralho)
        mao_banca.append(carta)
        mostra_mesa(rodada, ponto_jogador, ponto_banca, mao_jogador, mao_banca, fichas_jogador, fichas_banca, aposta_jogador, aposta_banca)
        time.sleep(2)
        
        if soma_mao(mao_banca) > 21:
            print('Banca estorou!')
            time.sleep(2)
            return soma_mao(mao_banca)
        
        elif soma_mao(mao_banca) >= 17:
            print('Banca parou')
            time.sleep(2)
            return soma_mao(mao_banca)
    
    
def verificar_vencedor(mao_jogador, mao_banca, ponto_jogador, ponto_banca, aposta):
    # Verificar vencedor
    if soma_mao(mao_jogador) > soma_mao(mao_banca):
        ponto_jogador += 1
        print(f'\033[32mJogador venceu! {ponto_jogador} x {ponto_banca} Banca\033[m')
        time.sleep(2)
        return "jogador"
    elif soma_mao(mao_banca) > soma_mao(mao_jogador):
        ponto_banca += 1
        print(f'\033[35mBanca venceu! Jogador {ponto_jogador} x {ponto_banca} Banca\033[0m')
        time.sleep(2)
        return "banca"
    else:
        print(f'\033[33mEmpate! Jogador {ponto_jogador} x {ponto_banca} Banca\033[m')
        time.sleep(2)
        return "empate"