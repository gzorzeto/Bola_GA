from math import sqrt
from random import randint, choices, random, randrange

#==========================================================================================================================================================================

d_vetor = 2 # Cada vetor poderá ter um valor entre (- d_vetor e + d_vetor)
n_genes = 250 # Número de pares de vetores (x,y) e consequentemente pares de posições da bola
n_bolas = 100 # Cada bola recebe n vetores (n_genes) que vão ditar sua movimentação, formando n_genes de posições (genes)
vel = 25 # Velocidade aplicada a cada vetor para movimentar cada bola
xi_bola = 1 # Posição inicial da bola em x
yi_bola = 1 # Posição inicial da bola em y
bolas = []
x_obj = 50 # Posição final desejada em x
y_obj = 50 # Posição final desejada em y

# É importante ressaltar que cada bola corresponde a um conjunto de posições (x,y) que descrevem o caminho que essa bola percorreu!
#==========================================================================================================================================================================

# Criar vetores aleatoriamente (sequência de vetores (x,y) que ditarão o caminho da bola);
# Criar sequência de posições da bola a partir da velocidade e vetores (criar genes);
# Equivalente a "mover bola" com os vetores aleatórios
def gerar_genoma (xi_bola, yi_bola, n_genes):
    vetores = [(randint(-d_vetor,d_vetor), randint(-d_vetor, d_vetor)) for _ in range (n_genes)]
    genoma = [] # Lista com posições da bola no eixo cartesiano
    for i in vetores:
        genoma.append((xi_bola, yi_bola))
        xi_bola += vel*i[0]
        yi_bola += vel*i[1]
    return genoma

#==========================================================================================================================================================================

# Gerar população de bolas aleatórias
def gerar_populacao (n_bolas, n_genes):
    return [gerar_genoma (xi_bola, yi_bola, n_genes) for _ in range (n_bolas)] 
#print(gerar_populacao(n_bolas, n_genes))

#==========================================================================================================================================================================

#fitness média para todas as posições (x,y) de uma bola (genoma)
def fitness (genoma): 
    # Calcular fitness para cada posição (x,y) da bola
    def individual_fitness (x, y):
        global x_obj, y_obj
        d = sqrt((x_obj - x)**2+(y_obj - y)**2)
        if d == 0:
            return 1000
        else:
            return 1/d
    # Calcular a fitness média para a bola (genoma)
    acum_fitness = 0
    for vetor in genoma:
        acum_fitness += individual_fitness(vetor[0], vetor[1])
    avr_fitness = acum_fitness/len(genoma)
    return avr_fitness


#==========================================================================================================================================================================

def selecionar_par (populacao):
    return choices(
        population = populacao,
        weights = [2**(fitness(genoma)*100) for genoma in populacao],
        k = 2)
        
#==========================================================================================================================================================================

def crossover (a, b):
    p = randint(1, n_genes - 1)
    # Retorna uma tupla de "filhos"
    return a[0:p] + b[p:], b[0:p] + a[p:]

#==========================================================================================================================================================================

def mutacao (genoma, probabilidade = 0.02):
    index = randrange(1, len(genoma)) # Nunca mutar o primeiro gene (primeira posição da bola)
    if random() > probabilidade:
        genoma[index] = genoma[index]
    else:
        vetor_mut = (randint(-d_vetor,d_vetor), randint(-d_vetor, d_vetor))
        # Aplicar vetor mutado na posição anterior da bola em x e y
        x_bola_mut = genoma[index - 1][0] + vel*vetor_mut[0]
        y_bola_mut = genoma[index - 1][1] + vel*vetor_mut[1]
        genoma[index] = (x_bola_mut, y_bola_mut)
    return genoma

#==========================================================================================================================================================================

def run_evolucao (limite_fitness, limite_geracoes):
    # Gerar população inicial
    populacao = gerar_populacao(n_bolas, n_genes)
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
            filho_a = mutacao (filho_a)
            filho_b = mutacao (filho_b)
            prox_geracao += [filho_a, filho_b]
        print(f"Geração: {i}")
        print(f"Fitness:{fitness(populacao[0])}")
        print("=====================================================================================================================")
        populacao = prox_geracao
    populacao = sorted(populacao, key = lambda genoma: fitness(genoma), reverse = True)

    return populacao, i

run_evolucao(limite_fitness = 1, limite_geracoes = 100)
            
