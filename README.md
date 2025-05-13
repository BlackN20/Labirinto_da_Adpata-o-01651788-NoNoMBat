# Labirinto com Agentes Simultâneos e Q-Learning

## 1. Introdução

Este projeto tem como objetivo demonstrar a aplicação de conceitos de **Aprendizado por Reforço (Reinforcement Learning)** em um ambiente de labirinto. Utilizamos o algoritmo **Q-Learning** para treinar múltiplos agentes, que operam de forma simultânea, para encontrar a saída de um labirinto gerado aleatoriamente. O sistema utiliza uma estratégia **ε-greedy** para balancear a exploração versus a exploração, atualiza dinamicamente a Q-Table, ajusta a taxa de exploração ao longo do tempo, e aplica recompensas e penalidades para guiar o comportamento dos agentes.

Ao final do treinamento, o desempenho dos agentes é visualizado por meio de um gráfico que ilustra a evolução da recompensa total por episódio.

## 2. Estrutura do Projeto


labirinto_da_adaptação/
├── README.md
├── requirements.txt
└── labirinto_agentes_simultaneos.py


## 3. Tecnologias e Bibliotecas Utilizadas

- **Python 3.x**: Linguagem principal utilizada.
- **pygame**: Criação da interface gráfica do labirinto e visualização dos movimentos dos agentes.
- **numpy**: Criação e manipulação da Q-Table e cálculos numéricos.
- **matplotlib**: Geração e exibição do gráfico que mostra a evolução das recompensas durante o treinamento.

## 4. Algoritmo e Conceitos Aplicados

### Q-Learning

O algoritmo Q-Learning é implementado para que os agentes aprendam, por meio de tentativa e erro, qual a melhor ação a ser tomada em cada estado do ambiente. A atualização da Q-Table segue a fórmula:


Q(s, a) = Q(s, a) + α * (reward + γ * max(Q(s', a')) - Q(s, a))


Onde:
- **α (learning_rate)**: Taxa de aprendizado.
- **γ (discount_factor)**: Fator de desconto para recompensas futuras.
- **reward**: Recompensa recebida após executar uma ação.
- **s'**: Próximo estado.

### Conteúdo Mínimo Obrigatório

1. **Redução de Incertezas (Exploração vs. Exploração):**
   Utilizamos a estratégia ε-greedy para balancear ações exploratórias (ação aleatória) e ações exploratórias (escolher a ação com maior valor na Q-Table).

2. **Atualização Dinâmica de Aprendizado (Q-Table):**
   A Q-Table é atualizada a cada interação entre o agente e o ambiente, incorporando as recompensas obtidas para melhorar o aprendizado.

3. **Ajuste de Taxa de Exploração:**
   A taxa de exploração (ε) inicia alta e decai a cada episódio, permitindo maior exploração no início e mais exploração do conhecimento adquirido conforme o treinamento progride.

4. **Aplicação de Recompensa e Penalidade:**
   São aplicadas recompensas positivas quando o agente alcança a saída e penalidades (pequeno custo por movimento) para estimular trajetórias mais curtas e eficientes.

5. **Visualização de Métricas/Comportamento Aprendido:**
   Ao final do treinamento, um gráfico é gerado com o `matplotlib`, mostrando a evolução das recompensas totais por episódio para cada agente.

## 5. Cálculos e Parâmetros

- **learning_rate (α):** Influencia o quanto a nova informação substitui o valor antigo na Q-Table.
- **discount_factor (γ):** Define a importância das futuras recompensas frente à recompensa imediata.
- **ε (epsilon):** Taxa de exploração inicial, que decai a cada episódio (por meio do ε_decay) para favorecer ações mais otimizadas.

## 6. Como Treinar e Testar o Agente

### Pré-requisitos

- Instale as dependências utilizando o arquivo `requirements.txt`:
  ```bash
  pip install -r requirements.txt

Execução

Para iniciar o treinamento dos agentes no labirinto com interface gráfica, execute:
python labirinto_da_adptação.py


Durante o treinamento, a janela do labirinto exibirá os agentes se movimentando de forma simultânea. Ao final do treinamento, um gráfico será exibido mostrando a evolução das recompensas obtidas em cada episódio.

7. Dificuldades Encontradas

Balanceamento de Exploração vs. Exploração: Ajustar a taxa de exploração para que os agentes explorem o ambiente inicialmente e, conforme o treinamento, converjam para as melhores ações.

Sincronização dos Agentes: Implementar um loop que permita aos agentes operarem simultaneamente, garantindo atualização individual sem interferência mútua.

Interface Gráfica: Desenvolver uma interface visual atrativa e responsiva utilizando pygame para exibir o labirinto e o movimento dos agentes.

8. Resultados Obtidos

Gráfico de Evolução: Ao final do treinamento, um gráfico mostra a evolução da recompensa total por episódio para cada agente. Esse gráfico permite visualizar se os agentes estão convergindo para um comportamento ótimo de navegação pelo labirinto.

Comportamento dos Agentes: Os agentes aprendem a minimizar movimentos desnecessários, buscando ativamente a saída do labirinto e, assim, atingindo melhores recompensas.

Desenvolvido por: Victor Hugo Coriolano Borges
Matrícula: 01651788
Data de Criação: 13/05/2025
