from math import sqrt
from random import randint, choices, random
import matplotlib.pyplot as plt

#==========================================================================================================================================================================

d_vetor = 1 # Cada vetor poderá ter um valor entre (- d_vetor e + d_vetor) em x e (0 e +d_vetor em y)
n_genes = 250 # Número de pares de vetores (x,y) e consequentemente pares de posições da bola
n_bolas = 250 # Cada bola recebe n vetores (n_genes) que vão ditar sua movimentação, formando n_genes de posições (genes)
vel = 10 # Velocidade aplicada a cada vetor para movimentar cada bola
xi_bola = 0 # Posição inicial da bola em x
yi_bola = 0 # Posição inicial da bola em y
bolas = []
x_obj = 250 # Posição final desejada em x
y_obj = 250 # Posição final desejada em y
dist_max = sqrt(x_obj**2 + y_obj**2)
mut_prob = 0.20

# É importante ressaltar que cada bola corresponde a um conjunto de posições (x,y) que descrevem o caminho que essa bola percorreu!
#==========================================================================================================================================================================

# Criar vetores aleatoriamente (sequência de vetores (x,y) que ditarão o caminho da bola);
# Criar sequência de posições da bola a partir da velocidade e vetores (criar genes);
# Equivalente a "mover bola" com os vetores aleatórios
def gerar_genoma (xi_bola, yi_bola, n_genes):
    vetores = [(randint(-d_vetor,d_vetor), randint(-d_vetor, d_vetor)) for _ in range (n_genes)]
    genoma = [] # Lista com posições da bola no eixo cartesiano
    for vetor in vetores:
        genoma.append((xi_bola, yi_bola))
        xi_bola += vel*vetor[0]
        yi_bola += vel*vetor[1]
    return genoma

#==========================================================================================================================================================================

# Gerar população de bolas aleatórias
def gerar_populacao (n_bolas):
    return [gerar_genoma (xi_bola, yi_bola, n_genes) for _ in range (n_bolas)] 

#==========================================================================================================================================================================

def fitness (genoma):
    global x_obj, y_obj
    x, y = genoma[-1][0], genoma[-1][1]
    d = sqrt((x_obj - x)**2+(y_obj - y)**2)
    d_normalisada = d/dist_max
    return max(0, 1 - d_normalisada)

#==========================================================================================================================================================================

def selecionar_par (populacao):
    return choices(
        population = populacao,
        weights = [fitness(genoma)*100 for genoma in populacao],
        k = 2)
     
#==========================================================================================================================================================================

def crossover (a, b):
    p = randint(1, n_genes - 1)
    # Retorna uma tupla de "filhos" por meio de um single point crossover
    return a[0:p] + b[p:], b[0:p] + a[p:]

#==========================================================================================================================================================================

def mutacao (genoma, mut_prob):
    if random() > mut_prob:
        genoma = genoma
    else:
        genoma = gerar_genoma(xi_bola,yi_bola, n_genes)
    return genoma
#==========================================================================================================================================================================

def run_evolucao (limite_fitness, limite_geracoes):
    # Gerar população inicial e criar lista para armazenar todas as gerações
    populacao = gerar_populacao(n_bolas)
    geracoes = []
    fitness_values = []
    # Entrar no loop para criar n_gerações
    for i in range (limite_geracoes):
        populacao = sorted(populacao, key = lambda genoma: fitness(genoma), reverse = True)
        # Se o fitness for maior que o limite, sair do loop e retornar a solução
        if fitness(populacao[0]) >= limite_fitness:
            break

        #Elitismo (duas melhores bolas passam para a próxima geração)
        prox_geracao = populacao[0:2]

        # Definir o resto da próxima geração com filhos provenientes dos crossovers
        for _ in range(int(len(populacao)/2)-1):
            pais = selecionar_par(populacao)
            filho_a, filho_b = crossover(pais[0], pais[1])
            filho_a = mutacao (filho_a, mut_prob)
            filho_b = mutacao (filho_b, mut_prob)
            prox_geracao += [filho_a, filho_b]    
        populacao = prox_geracao
        populacao = sorted(populacao, key = lambda genoma: fitness(genoma), reverse = True)
        print(f"Geração: {i}")
        geracoes.append(i)
        fitness_values.append(fitness(populacao[0]))
    return geracoes, fitness_values

geracoes, fitness_values = run_evolucao(limite_fitness = 1, limite_geracoes = 1000)
plt.plot(geracoes, fitness_values)
plt.xlabel('Geração')
plt.ylabel("Valor Fitness")
plt.show()
