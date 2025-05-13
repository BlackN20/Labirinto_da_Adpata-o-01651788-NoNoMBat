import pygame
import numpy as np
import random
import matplotlib.pyplot as plt

# Definições do Labirinto
class Labirinto:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.mapa = self.gerar_labirinto()
        self.posicao_inicial = self.encontrar_posicao_inicial()
        self.posicao_final = self.encontrar_posicao_final()
        self.posicoes_agentes = [[x for x in self.posicao_inicial] for _ in range(3)]  # Lista de posições dos agentes

    def gerar_labirinto(self):
        # Algoritmo para gerar um labirinto
        mapa = [[1 for _ in range(self.width)] for _ in range(self.height)]
        for i in range(1, self.height - 1):
            for j in range(1, self.width - 1):
                if random.random() > 0.3:
                    mapa[i][j] = 0
        return mapa

    def encontrar_posicao_inicial(self):
        # Encontra uma posição inicial vazia
        for i in range(1, self.height - 1):
            for j in range(1, self.width - 1):
                if self.mapa[i][j] == 0:
                    return [i, j]
        return [1, 1]

    def encontrar_posicao_final(self):
        # Encontra uma posição final vazia
        for i in range(self.height - 2, 0, -1):
            for j in range(self.width - 2, 0, -1):
                if self.mapa[i][j] == 0:
                    return [i, j]
        return [self.height - 2, self.width - 2]

    def reset(self, agente_id):
        # Reseta a posição do agente para a posição inicial
        self.posicoes_agentes[agente_id] = [x for x in self.posicao_inicial]
        return self.posicoes_agentes[agente_id]

    def step(self, agente_id, action):
        x, y = self.posicoes_agentes[agente_id]
        nova_posicao = [x, y]

        # Define as ações
        if action == 0:   # cima
            nova_posicao[0] -= 1
        elif action == 1: # direita
            nova_posicao[1] += 1
        elif action == 2: # baixo
            nova_posicao[0] += 1
        elif action == 3: # esquerda
            nova_posicao[1] -= 1

        # Confere se a nova posição é válida
        if (0 <= nova_posicao[0] < self.height and
            0 <= nova_posicao[1] < self.width and
            self.mapa[nova_posicao[0]][nova_posicao[1]] != 1):
            self.posicoes_agentes[agente_id] = nova_posicao
        else:
            nova_posicao = [x, y]

        # Define as recompensas
        if self.posicoes_agentes[agente_id] == self.posicao_final:
            return self.posicoes_agentes[agente_id], 1, True
        else:
            return self.posicoes_agentes[agente_id], -0.01, False

# Definições da Janela
class Janela:
    def __init__(self, labirinto, tile_size=30):
        pygame.init()
        self.labirinto = labirinto
        self.tile_size = tile_size
        self.width = labirinto.width * tile_size
        self.height = labirinto.height * tile_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Labirinto com Machine Learning")
        self.clock = pygame.time.Clock()

    def draw(self):
        self.screen.fill((240, 240, 240))

        # Desenha o labirinto
        for row in range(self.labirinto.height):
            for col in range(self.labirinto.width):
                if self.labirinto.mapa[row][col] == 1:
                    color = (50, 50, 50)
                else:
                    color = (200, 200, 200)
                pygame.draw.rect(self.screen, color,
                                 (col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size))

        # Desenha a posição final
        pygame.draw.rect(self.screen, (0, 255, 0),
                         (self.labirinto.posicao_final[1] * self.tile_size,
                          self.labirinto.posicao_final[0] * self.tile_size,
                          self.tile_size, self.tile_size))

        # Desenha os agentes
        for agente_id, agente_pos in enumerate(self.labirinto.posicoes_agentes):
            color = [(255, 0, 0), (0, 0, 255), (255, 255, 0)][agente_id % 3]
            pygame.draw.circle(self.screen, color,
                               (agente_pos[1] * self.tile_size + self.tile_size // 2,
                                agente_pos[0] * self.tile_size + self.tile_size // 2),
                               self.tile_size // 3)

        pygame.display.flip()

# Implementação do Q-Learning com agentes simultâneos
def q_learning(labirinto, janela, n_agentes=3, episodes=2000):
    n_actions = 4
    q_tables = [np.zeros((labirinto.height * labirinto.width, n_actions)) for _ in range(n_agentes)]
    recompensa_por_episodio = [[] for _ in range(n_agentes)]

    learning_rate = 0.1
    discount_factor = 0.99
    epsilon = 1.0
    epsilon_decay = 0.995

    for episode in range(episodes):
        states = [labirinto.reset(agente_id) for agente_id in range(n_agentes)]
        dones = [False] * n_agentes
        total_rewards = [0] * n_agentes

        while not all(dones):
            janela.draw()
            janela.clock.tick(30)

            for agente_id in range(n_agentes):
                if not dones[agente_id]:
                    state = states[agente_id]
                    state_idx = state[0] * labirinto.width + state[1]

                    # Escolhe a ação baseada no epsilon-greedy
                    if random.random() < epsilon:
                        action = random.randint(0, n_actions - 1)
                    else:
                        action = np.argmax(q_tables[agente_id][state_idx])

                    # Executa a ação e obtém o próximo estado
                    next_state, reward, done = labirinto.step(agente_id, action)
                    next_state_idx = next_state[0] * labirinto.width + next_state[1]

                    # Atualiza a Q-table
                    q_tables[agente_id][state_idx, action] += learning_rate * (reward + discount_factor * np.max(q_tables[agente_id][next_state_idx]) - q_tables[agente_id][state_idx, action])

                    # Atualiza o estado, recompensa e flag done
                    states[agente_id] = next_state
                    total_rewards[agente_id] += reward
                    dones[agente_id] = done

        # Guarda as recompensas
        for agente_id in range(n_agentes):
            recompensa_por_episodio[agente_id].append(total_rewards[agente_id])

        # Decaimento do epsilon
        epsilon *= epsilon_decay

    return q_tables, recompensa_por_episodio

# Função para plotar as recompensas
def plotar_recompensas(recompensas, n_agentes):
    plt.figure(figsize=(10, 6))
    for agente_id in range(n_agentes):
        plt.plot(recompensas[agente_id], label=f'Agente {agente_id + 1}')
    plt.xlabel('Episódio')
    plt.ylabel('Recompensa Total')
    plt.title('Evolução das Recompensas por Episódio')
    plt.legend()
    plt.grid(True)
    plt.show()

# Função principal
def main():
    labirinto = Labirinto(width=15, height=15)
    janela = Janela(labirinto, tile_size=25)
    n_agentes = 3
    q_tables, recompensas = q_learning(labirinto, janela, n_agentes=n_agentes, episodes=2000)

    plotar_recompensas(recompensas, n_agentes)

    pygame.quit()

if __name__ == "__main__":
    main()
