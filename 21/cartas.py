
def criar_baralho():
    baralho_local = []
    naipes = ['ESPADAS', 'COPAS', 'OUROS', 'PAUS']
    
    # Adicionar cartas numéricas (2-10) para cada naipe
    for valor in range(2, 11):
        for naipe in naipes:
            baralho_local.append({'carta': f'{valor}', 'naipe': naipe, 'valor': valor})

    # Adicionar cartas de figura (J, Q, K) para cada naipe
    for carta, valor in [('J', 10), ('Q', 10), ('K', 10)]:
        for naipe in naipes:
            baralho_local.append({'carta': f'{carta}', 'naipe': naipe, 'valor': valor})

    # Adicionar Ás para cada naipe
    for naipe in naipes:
        baralho_local.append({'carta': f'A', 'naipe': naipe, 'valor': 1})
    
    return baralho_local


def distribuir_carta(baralho):
    if baralho:
        return baralho.pop() 
    return None


def distribuir_mao(baralho):
    mao = []
    for _ in range(2):
        carta = distribuir_carta(baralho)
        if carta:
            mao.append(carta)
    return mao

def simbolo_naipe(naipe):
    simbolos = {
        'ESPADAS': '♠', 
        'COPAS': '\033[31m♥\033[m', 
        'OUROS': '\033[31m♦\033[m',
        'PAUS': '♣'
    }
    return simbolos.get(naipe, naipe)


def mostrar_mao_horizontal(mao, nome="Mão"):
    print(f"\n{nome}:")
    
    if not mao:
        print("Nenhuma carta")
        return
    
    linhas_cartas = []
    for carta in mao:
        simbolo = simbolo_naipe(carta['naipe'])

        if len(carta['carta']) == 1:
    
            linhas = [
                "┌───────┐",
                f"│ {carta['carta']}     │",
                "│       │",
                f"│   {simbolo}   │",
                "│       │",
                f"│     {carta['carta']} │",
                "└───────┘"
            ]
        else:

            linhas = [
                "┌───────┐",
                f"│ {carta['carta']}    │",
                "│       │",
                f"│   {simbolo}   │",
                "│       │",
                f"│    {carta['carta']} │",
                "└───────┘"
            ]
        linhas_cartas.append(linhas)
    
 
    for i in range(7):  
        for j, carta_linhas in enumerate(linhas_cartas):
            print(carta_linhas[i], end="  ")
        print()
    
    print(f"Total: {soma_mao(mao)}")
    print()

def mostrar_mao(mao, nome="Mão"):
    mostrar_mao_horizontal(mao, nome)

def soma_mao(mao):
    soma = sum(carta['valor'] for carta in mao)
    return soma


def mostra_aposta(aposta_jogador, aposta_banca):
    print("VALOR DAS APOSTAS".center(50))
    print(f"Jogador {aposta_jogador} x {aposta_banca} Banca".center(50))
    print()
    
    
def mostra_mesa(rodada, ponto_jogador, ponto_banca, mao_jogador, mao_banca, fichas_jogador, fichas_banca, aposta_jogador, aposta_banca):
    print("=" * 50)
    print(f"🎲 RODADA {rodada}".center(50))
    print("=" * 50)
    mostra_aposta(aposta_jogador, aposta_banca)
    
    print("PLACAR".center(25) + "FICHAS".center(25))
    print(f"Jogador {ponto_jogador} x {ponto_banca} Banca".center(25) + 
          f"{fichas_jogador} x {fichas_banca}".center(25))
    print()
    
    print("🃏 CARTAS".center(50))
    mostrar_mao(mao_jogador, '\033[36mJogador\033[0m')
    mostrar_mao(mao_banca, '\033[35mBanca\033[0m')
    
    print("=" * 50)
    print()

