import threading




# Semáforos para controlar o acesso ao tabuleiro
semaphores = [threading.Semaphore(1) for i in range(9)]




# Tabuleiro
board = [' ' for i in range(9)]




# Jogador atual
current_player = 'X'




# Placar
placar = {'X': 0, 'O': 0}




# Função para imprimir o tabuleiro
def print_board():
    print(f'{board[0]} | {board[1]} | {board[2]}')
    print(f'{board[3]} | {board[4]} | {board[5]}')
    print(f'{board[6]} | {board[7]} | {board[8]}')




# Função para verificar se um jogador ganhou
def check_winner(player):
    return ((board[0] == player and board[1] == player and board[2] == player) or
            (board[3] == player and board[4] == player and board[5] == player) or
            (board[6] == player and board[7] == player and board[8] == player) or
            (board[0] == player and board[3] == player and board[6] == player) or
            (board[1] == player and board[4] == player and board[7] == player) or
            (board[2] == player and board[5] == player and board[8] == player) or
            (board[0] == player and board[4] == player and board[8] == player) or
            (board[2] == player and board[4] == player and board[6] == player))




# Função para jogar uma rodada
def play(player, position):
    global current_player


    semaphores[position].acquire()
    if board[position] == ' ':
        board[position] = player
        print_board()


        if check_winner(player):
            placar[player] += 1
            print(f'Parabéns, {player} ganhou! Placar: {placar["X"]} X {placar["O"]}')
            exit(0)
        elif ' ' not in board:
            print(f'Empate! Placar: {placar["X"]} X {placar["O"]}')
            exit(0)
        else:
            current_player = 'O' if current_player == 'X' else 'X'
    semaphores[position].release()




# Função para a thread de um jogador
def player_thread(player):
    while True:
        if current_player == player:
            print(f'Thread {player}: current_player = {current_player}')
            position = int(input(f'{player} ({threading.current_thread().name}), escolha uma posição (0-8): '))
            play(player, position)
            with threading.Lock():
                print(f'Threads simultâneas acessando o placar: {threading.active_count() - 1}')
                print(f'Placar atualizado: {placar["X"]} X {placar["O"]}')




# Criação das threads dos jogadores
t1 = threading.Thread(target=player_thread, args=('X',))
t2 = threading.Thread(target=player_thread, args=('O',))


# Início das threads
t1.start()
t2.start()


# Mensagem indicando que as threads foram iniciadas
print("As threads dos jogadores X e O foram iniciadas. Vamos jogar!")