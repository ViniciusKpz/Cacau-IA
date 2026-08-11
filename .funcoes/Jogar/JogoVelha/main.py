class Tabuleiro:
    TAMANHO_TABULEIRO = 9
    VAZIO = " "

    JOGADOR_X = "X"
    JOGADOR_O = "O" 
    
    def __init__(self):
        self.__posicoes = [self.VAZIO] * self.TAMANHO_TABULEIRO
        self.__jogadas_realizadas = 0

    def __validar_posicao(self, posicao):
        return 0 <= posicao < self.TAMANHO_TABULEIRO

    def obter_posicao(self, indice):
        if self.__validar_posicao(indice):
            return self.__posicoes[indice]
        return None

    def obter_posicoes(self):
        return self.__posicoes.copy() 
    
    def resetar(self):
        self.__posicoes = [self.VAZIO] * self.TAMANHO_TABULEIRO
        self.__jogadas_realizadas = 0

    def exibir(self):
        print(f" {self.__posicoes[0]} | {self.__posicoes[1]} | {self.__posicoes[2]} ")
        print("---+---+---")
        print(f" {self.__posicoes[3]} | {self.__posicoes[4]} | {self.__posicoes[5]} ")
        print("---+---+---")
        print(f" {self.__posicoes[6]} | {self.__posicoes[7]} | {self.__posicoes[8]} ")

    def verificar_posicao_livre(self, posicao):
        return (
            self.__validar_posicao(posicao)
            and self.__posicoes[posicao] == self.VAZIO
        )

    def fazer_jogada(self, posicao, simbolo):
        if simbolo not in [self.JOGADOR_X, self.JOGADOR_O]:
            return False
            
        if self.verificar_posicao_livre(posicao):
            self.__posicoes[posicao] = simbolo
            self.__jogadas_realizadas += 1
            return True
        return False
    
    def obter_total_jogadas(self):
        return self.__jogadas_realizadas
    
    def verificar_vitoria(self, simbolo):
        combinacoes = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8), 
            (0, 3, 6), (1, 4, 7), (2, 5, 8), 
            (0, 4, 8), (2, 4, 6)             
        ]
        for a, b, c in combinacoes:
            if self.__posicoes[a] == self.__posicoes[b] == self.__posicoes[c] == simbolo:
                return True
        return False
        
    def verificar_empate(self):
        return self.VAZIO not in self.__posicoes
    
    def obter_status_jogo(self):
        if self.verificar_vitoria(self.JOGADOR_X):
            return "X ganhou!"
        if self.verificar_vitoria(self.JOGADOR_O):
            return "O ganhou!"
        if self.verificar_empate():
            return "Empate!"
        return "Jogo em andamento"


class Jogador:
    def __init__(self, nome, simbolo):
        self.__nome = nome 
        self.__simbolo = simbolo 
    
    def obter_nome(self):
        return self.__nome
    
    def obter_simbolo(self):
        return self.__simbolo
    

class JogoDaVelha:
    def __init__(self, nome1, nome2):
        self.__tabuleiro = Tabuleiro()
        self.__jogador1 = Jogador(nome1, Tabuleiro.JOGADOR_X)
        self.__jogador2 = Jogador(nome2, Tabuleiro.JOGADOR_O)
        self.__jogadores = [self.__jogador1, self.__jogador2]
        self.__jogador_atual = 0

    def obter_tabuleiro(self):
        return self.__tabuleiro

    def obter_jogador_atual(self):
        return self.__jogadores[self.__jogador_atual]

    def __alternar_jogador(self):
        if self.__jogador_atual == 0:
            self.__jogador_atual = 1
        else:
            self.__jogador_atual = 0

    def fazer_jogada(self, posicao):
        jogador_atual = self.__jogadores[self.__jogador_atual]
        simbolo = player_simbolo = jogador_atual.obter_simbolo()
        
        resultado = self.__tabuleiro.fazer_jogada(posicao, simbolo)

        if resultado:
            self.__alternar_jogador()

        return resultado
    
    def jogo_acabou(self):
        return self.__tabuleiro.obter_status_jogo() != "Jogo em andamento"
    
    def obter_vencedor(self):
        return self.__tabuleiro.obter_status_jogo()
    
    def exibir_tabuleiro(self):
        self.__tabuleiro.exibir()

    def jogar(self):
        print(f"\n{self.__jogador1.obter_nome()} é o X")
        print(f"{self.__jogador2.obter_nome()} é o O")
    
        while not self.jogo_acabou():
            print()
            self.exibir_tabuleiro()

            jogador_atual = self.obter_jogador_atual()
            print(f"Vez de: {jogador_atual.obter_nome()} ({jogador_atual.obter_simbolo()})")

            while True:
                try:
                    posicao = int(input(f"{jogador_atual.obter_nome()}, escolha uma posição (0-8): "))
                    if not (0 <= posicao <= 8):
                        print("Digite uma posição válida! De 0 a 8.")
                        continue
                    if self.fazer_jogada(posicao):
                        break
                    else:
                        print("Posição já usada, use outra.")
                except ValueError:
                    print("Por favor, digite apenas números inteiros!")
        
        print()
        self.exibir_tabuleiro()
        resultado = self.obter_vencedor()

        print("\n--- FIM DE JOGO ---")
        if resultado == "Empate!":
            print(resultado)
        elif resultado == "X ganhou!":
            print(f"Parabéns! {self.__jogador1.obter_nome()} Venceu!")
        else:
            print(f"Parabéns! {self.__jogador2.obter_nome()} Venceu!")


# Método para gerenciar o jogo
def menu_principal():
    while True:
        print("\n=========================")
        print(" JOGO DA VELHA")
        print(" v5.0 do Vinícius Araújo")
        print("=========================")
        print("[1] Jogar")
        print("[2] Sair")
        print("=========================")
        
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            print()
            nome1 = input("Nome do Jogador 1 (X): ")
            nome2 = input("Nome do Jogador 2 (O): ")
            
            # Cria e inicia uma nova partida
            jogo = JogoDaVelha(nome1, nome2)
            jogo.jogar()
            
            input("\nPressione Enter para voltar ao menu...")
        elif opcao == "2":
            print("\nObrigado por jogar! Até a próxima.")
            break
        else:
            print("\nOpção inválida! Digite 1 ou 2.")

# Inicia o programa menu
menu_principal()
