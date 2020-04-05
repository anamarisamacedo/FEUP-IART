# FEUP-IART
Bubble blast implementation in python, along with an AI that finds a level's best solution

### Como iniciar o jogo: 

O projeto é feito na linguagem Python.
Para iniciar o jogo deve-se executar o ficheiro main.py (na linha de comandos python main.py)
Deve-se instalar o módulo pygame.

### Instruções para o jogo:

Ao iniciar o jogo, o utilizador pode selecionar a opção de jogar em modo humano ou modo computador, carregando nas teclas que indicam.

No modo computador, o utilizador pode escolher o nível e depois selecionar um de 4 algoritmos: BFS (Primeiro em Largura), DFS (Primeiro em Profundidade),
    IDDFS (Aprofundamento Iterativo) ou Greedy (Pesquisa gulosa), carregando nas teclas que indicam.

Ao carregar na opção do algoritmo Greedy vão aparecer opções de heurística para o algoritmo:

    Level Heuristic - Esta heurística baseia-se na soma dos níveis de todas as bolhas que ficam no puzzle após uma jogada.
                      O algoritmo escolhe o vizinho cujo resultado é menor.
                      Por exemplo, se após uma jogada ficarem duas bolhas vermelhas (nível 1) e uma verde (nível 2), o resultado vai ser 4.
                      Se após outra jogada ficar uma bolha vermelha (nível 1) e duas verdes (nível 2) o resultado é 5.
                      Como o jogo acaba quando não houver nenhuma bolha no puzzle (soma total de 0 níveis), o algoritmo escolhe a primeira
                        jogada, que é o menor resultado.

    Score Heuristic - Esta heurística baseia-se na pontuação total que se obtém após uma jogada.
                      O algoritmo escolhe o vizinho cujo resultado é maior.

### Dicas do computador para o jogador:
No modo humano, existem duas formas de o jogador obter dicas do computador.
Se o jogador perder o jogo, em qualquer nível, aparece a opção de ter uma dica do computador, em que este diz todas as jogadas que se devem
fazer para solucionar o jogo.
Se o jogador quiser pedir dicas a meio do jogo, o computador gera uma solução/dica para o estado em que o jogador se encontra, mostrando as jogadas necessárias.

## Aspeto do jogo
![Level Screenshot](/assets/LevelScreenshot.png)

## AI a resolver um nivel

<p align="center"><img src="https://i.imgur.com/lF8Ehb7.gif"></p>
