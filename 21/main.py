from cartas import mostra_mesa, distribuir_mao, distribuir_carta, criar_baralho
from regras import verificar_vencedor, soma_mao, vez_da_banca

import time
import random 
import os   

# Variáveis do jogo
ponto_jogador , ponto_banca, fichas_jogador, fichas_banca = 0, 0, 500, 500 
rodada = 1

aposta_jogador , aposta_banca = 0, 0

while fichas_jogador > 0 and fichas_banca > 0:
    time.sleep(3)
    print()
    print(f"Suas fichas: {fichas_jogador} | Fichas da banca: {fichas_banca}")
 
    aposta = input("Valor da aposta: ").strip()
    try:
        aposta = int(aposta)
    except ValueError:
        print("Digite um número válido!")
        continue

    if aposta > fichas_jogador:
        print("Jogador não tem fichas suficientes!")
        continue
    elif aposta > fichas_banca:
        print("Banca não tem fichas suficientes!")
        continue
    
    if aposta <= 0:
        print("Aposta deve ser maior que 0!")
        continue
    
    fichas_jogador -= aposta
    fichas_banca -= aposta
    
    baralho = criar_baralho()
    random.shuffle(baralho)
    
    mao_jogador = distribuir_mao(baralho)
    mao_banca = distribuir_mao(baralho)
    
    aposta_jogador = aposta
    aposta_banca = aposta
    
    os.system('cls')
    mostra_mesa(rodada, ponto_jogador, ponto_banca, mao_jogador, mao_banca, fichas_jogador, fichas_banca, aposta_jogador, aposta_banca)

    while True:
        if soma_mao(mao_jogador) > 21:
            os.system('cls')
            mostra_mesa(rodada, ponto_jogador, ponto_banca, mao_jogador, mao_banca, fichas_jogador, fichas_banca, aposta_jogador, aposta_banca)
            time.sleep(3)
            print(f'\033[31m\nJogador estorou!\033[m')
            time.sleep(3)
            ponto_banca += 1
            fichas_banca += aposta * 2  # Banca ganha o dobro
            print(f'\033[31m\nBanca venceu! Jogador {ponto_jogador} x {ponto_banca} Banca\033[m')
            time.sleep(3)
            break
        
        print()
        continuar = input('Comprar carta? (S/N): ').lower().strip()
        
        if continuar == 's':
            # Jogador compra carta
            carta = distribuir_carta(baralho)
            mao_jogador.append(carta)
            
            print('Comprando carta...')
            time.sleep(3)
            os.system('cls')
            mostra_mesa(rodada, ponto_jogador, ponto_banca, mao_jogador, mao_banca, fichas_jogador, fichas_banca, aposta_jogador, aposta_banca)     
            
        elif continuar == 'n':
            # vez da banca
            print('Jogador parou, vez da banca')
            time.sleep(3)            
            resultado = vez_da_banca(mao_banca, baralho, rodada, ponto_jogador, ponto_banca, mao_jogador, fichas_jogador, fichas_banca, aposta_jogador, aposta_banca)
            
            if resultado > 21:
                ponto_jogador += 1
                print(f'\033[32mJogador venceu! {ponto_jogador} x {ponto_banca} Banca\033[m')
                fichas_jogador += aposta * 2  
                time.sleep(3)
                break
   
            else:
                resultado_vencedor = verificar_vencedor(mao_jogador, mao_banca, ponto_jogador, ponto_banca, aposta)
                if resultado_vencedor == "banca":
                    fichas_banca += aposta * 2
                elif resultado_vencedor == "jogador":
                    fichas_jogador += aposta * 2
                else:  # empate
                    fichas_jogador += aposta
                    fichas_banca += aposta
                break
            
        else:
            print('Opção inválida. Tente novamente.')
            time.sleep(3)
    
    rodada += 1
    os.system('cls')

print(f"\n=== FIM DE JOGO ===")
if fichas_jogador <= 0:
    print(f"Você ficou sem fichas! A banca venceu!")
    print(f"Placar final: Jogador {ponto_jogador} x {ponto_banca} Banca")
elif fichas_banca <= 0:
    print(f"A banca ficou sem fichas! Você venceu!")
    print(f"Placar final: Jogador {ponto_jogador} x {ponto_banca} Banca")

    
    
    
