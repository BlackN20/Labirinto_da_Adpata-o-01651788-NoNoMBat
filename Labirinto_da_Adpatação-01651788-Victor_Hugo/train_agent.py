#!/usr/bin/env python3
import pygame
import numpy as np
import random
import time
import sys

class Labirinto:
    def __init__(self, width=15, height=15):
        self.width = width
        self.height = height
        self.mapa = self._gerar_labirinto()
        self.posicao_inicial = self._encontrar_posicao_inicial()
        self.posicao_final = self._encontrar_posicao_final()
        self.posicoes_agentes = [list(self.posicao_inicial) for _ in range(3)]

    def _gerar_labirinto(self):
        mapa = [[1] * self.width for _ in range(self.height)]
        for i in range(1, self.height - 1):
            for j in range(1, self.width - 1):
                mapa[i][j] = 0 if random.random() > 0.3 else 1
        return mapa

    def _encontrar_posicao_inicial(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.mapa[i][j] == 0:
                    return [i, j]
        return [1, 1]

    def _encontrar_posicao_final(self):
        for i in range(self.height - 1, -1, -1):
            for j in range(self.width - 1, -1, -1):
                if self.mapa[i][j] == 0:
                    return [i, j]
        return [self.height - 2, self.width - 2]

    def reset(self, agente_id):
        self.posicoes_agentes[agente_id] = list(self.posicao_inicial)
        return list(self.posicao_inicial)

    def step(self, agente_id, action):
        x, y = self.posicoes_agentes[agente_id]
        nova = [x, y]
        if action == 0: nova[0] -= 1  # cima
        elif action == 1: nova[1] += 1  # direita
        elif action == 2: nova[0] += 1  # baixo
        elif action == 3: nova[1] -= 1  # esquerda

        if (0 <= nova[0] < self.height and 0 <= nova[1] < self.width and self.mapa[nova[0]][nova[1]] == 0):
            self.posicoes_agentes[agente_id] = nova

        if self.posicoes_agentes[agente_id] == self.posicao_final:
            return list(self.posicoes_agentes[agente_id]), 10.0, True  # Recompensa grande por alcançar o objetivo
        else:
            return list(self.posicoes_agentes[agente_id]), -0.01, False  # Recompensa negativa por cada passo

class Janela:
    def __init__(self, labirinto, tile_size=25):
        pygame.init()
        self.lab = labirinto
        self.tile = tile_size
        self.width = self.lab.width * self.tile
        self.height = self.lab.height * self.tile
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Labirinto com Agentes Simultâneos")
        self.clock = pygame.time.Clock()

    def draw(self, agentes_tempos):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.screen.fill((240, 240, 240))  # Fundo claro

        # Desenha o labirinto
        for i in range(self.lab.height):
            for j in range(self.lab.width):
                cor = (50, 50, 50) if self.lab.mapa[i][j] == 1 else (200, 200, 200)
                pygame.draw.rect(self.screen, cor,
                                 (j * self.tile, i * self.tile, self.tile, self.tile))

        # Desenha o objetivo (verde)
        fi = self.lab.posicao_final
        pygame.draw.rect(self.screen, (0, 255, 0),
                         (fi[1] * self.tile, fi[0] * self.tile, self.tile, self.tile))

        # Define uma cor para cada agente
        cores_agentes = [(255, 0, 0), (0, 0, 255), (255, 165, 0)]  # vermelho, azul, laranja

        for aid, pos in enumerate(self.lab.posicoes_agentes):
            cor = cores_agentes[aid % len(cores_agentes)]  # seleciona a cor correspondente

            # Desenha o agente como círculo colorido
            pygame.draw.circle(self.screen, cor,
                               (pos[1] * self.tile + self.tile // 2,
                                pos[0] * self.tile + self.tile // 2),
                               self.tile // 3)

        # Exibe o tempo de cada agente na tela
        font = pygame.font.SysFont(None, 24)
        for aid, tempo in enumerate(agentes_tempos):
            texto = font.render(f'Agente {aid + 1}: {tempo:.2f}s', True, (0, 0, 0))
            self.screen.blit(texto, (10, 30 + aid * 30))

        pygame.display.flip()

def q_learning(labirinto, janela, n_agentes=3, episodes=2000, max_steps=1000, print_every=100):
    n_actions = 4
    n_states = labirinto.width * labirinto.height
    q_tables = [np.zeros((n_states, n_actions)) for _ in range(n_agentes)]
    recompensas = [[] for _ in range(n_agentes)]

    alpha = 0.1
    gamma = 0.99
    epsilon = 1.0
    eps_decay = 0.995

    for ep in range(1, episodes + 1):
        states = [labirinto.reset(i) for i in range(n_agentes)]
        dones = [False] * n_agentes
        total_rewards = [0.0] * n_agentes
        step = 0

        agentes_tempos = [0.0] * n_agentes
        agentes_tempos_iniciais = [None] * n_agentes  # Lista para armazenar o tempo de início de cada agente

        while step < max_steps:
            for aid in range(n_agentes):
                if dones[aid]:
                    continue

                # Se o agente não começou o cronômetro, inicia o cronômetro
                if agentes_tempos_iniciais[aid] is None:
                    agentes_tempos_iniciais[aid] = time.time()

                s = states[aid]
                s_idx = s[0] * labirinto.width + s[1]
                if random.random() < epsilon:
                    a = random.randint(0, n_actions - 1)  # exploração
                else:
                    a = np.argmax(q_tables[aid][s_idx])   # exploração

                ns, r, done = labirinto.step(aid, a)
                ns_idx = ns[0] * labirinto.width + ns[1]

                # Atualização da Q-table
                q_tables[aid][s_idx, a] += alpha * (
                    r + gamma * np.max(q_tables[aid][ns_idx]) - q_tables[aid][s_idx, a]
                )

                states[aid] = ns
                total_rewards[aid] += r
                dones[aid] = done

                # Se o agente chegou no objetivo, para o cronômetro
                if dones[aid] and agentes_tempos_iniciais[aid] is not None:
                    agentes_tempos[aid] = time.time() - agentes_tempos_iniciais[aid]
                    agentes_tempos_iniciais[aid] = None  # Reseta o tempo de início, pois o cronômetro já foi parado

            janela.draw(agentes_tempos)
            janela.clock.tick(30)
            step += 1

            if all(dones):  # Todos os agentes concluíram
                break

        # Ajusta o epsilon a cada episódio
        epsilon *= eps_decay

        # Exibe progresso no terminal
        if ep % print_every == 0:
            avg_r = np.mean([recompensas[aid][-1] for aid in range(n_agentes)])
            print(f"Episode {ep}/{episodes} - Avg reward: {avg_r:.3f} - Epsilon: {epsilon:.4f}")

def main():
    lab = Labirinto(width=15, height=15)
    jan = Janela(lab, tile_size=25)
    q_learning(lab, jan, n_agentes=3, episodes=2000, max_steps=1000, print_every=100)
    pygame.quit()

if __name__ == "__main__":
    main()
