Apresentação do Projeto: Q-Learning com Múltiplos Agentes
Objetivo do Projeto
Apresentar uma simulacao de aprendizado por reforco (Q-Learning) com multiplos agentes em um labirinto.
O objetivo dos agentes e alcancar a meta (canto inferior direito) da forma mais eficiente possivel.
O que e Q-Learning?
Q-Learning e um algoritmo de aprendizado por reforco onde agentes aprendem por tentativa e erro.
- Q-Table: Mapeia estados para acoes com valores de recompensa esperada.
- Formula de atualizacao:
 Q(s, a) = Q(s, a) + a * (r + g * max(Q(s', a')) - Q(s, a))
 - a (alpha): taxa de aprendizado
 - g (gamma): fator de desconto
 - e (epsilon): taxa de exploracao
Detalhes do Codigo
1. Canvas e Desenho:
- Usado <canvas> HTML para desenhar o labirinto.
- Celulas pretas = obstaculos. Agentes = circulos coloridos.
2. Estrutura do Labirinto:
- Tamanho 10x10 com obstaculos fixos e mais dificeis.
- Ponto inicial: canto superior esquerdo.
- Objetivo: canto inferior direito.
3. Agentes:
- 3 agentes treinando simultaneamente.
- Cada agente aprende individualmente.
- O primeiro a chegar ganha mais recompensa.
4. Treinamento:
- 5000 episodios, atualizando Q-Table a cada passo.
Apresentação do Projeto: Q-Learning com Múltiplos Agentes
- Controle de taxa de exploracao (e) e aprendizado (a).
- E possivel pausar, retomar, salvar e carregar o Q-Table.
Visualizacoes
- Mostra a politica aprendida com setas (setas direcionais).
- Grafico de recompensas por episodio.
- Exibicao completa da Q-Table em nova aba.
Funcionalidades Extras
- Salvar e carregar Q-Table no navegador.
- Reset geral com reinicio do aprendizado.
- Exibir a politica aprendida.
- Controle de treinamento passo a passo, pausado ou continuo.
Demonstracao Sugerida
1. Explicar os conceitos brevemente.
2. Iniciar o treinamento.
3. Mostrar agentes se movendo e aprendendo.
4. Ativar a exibicao da politica aprendida.
5. Abrir a Q-Table.
6. Demonstrar controle de pausa e retomada.
Conclusao
Este projeto demonstra como agentes autonomos podem aprender estrategias eficientes por meio de
tentativa e erro. Mesmo sem conhecimento previo, eles encontram o melhor caminho com o tempo, mesmo
em um ambiente desafiador.
