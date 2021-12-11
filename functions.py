import numpy as np
import random
from heapq import nlargest
import matplotlib.pyplot as plt

def init_population(n):
    pop = list(range(n))
    random.shuffle(pop)
    return pop


def fittness(chrom):
    n = len(chrom)
    cost = 0
    diagonals_r = {key: 0 for key in range(-n, n + 1)}
    diagonals_l = {key: 0 for key in range(2 * n - 1)}
    for i in range(n):
        diagonals_r[i - chrom[i]] += 1
        diagonals_l[i + chrom[i]] += 1
    diagonals = list(diagonals_r.values()) + list(diagonals_l.values())
    for diagonal in diagonals:
        if (diagonal > 0):
            cost += diagonal - 1
    return cost


def crossover(parent_1,parent_2,n):
    child = [0]*n
    point_1 = random.randint(0,n-1)
    point_2 = random.randint(0,n-1)
    if point_1 > point_2:
        point_1, point_2 = point_2, point_1
    
#     print(point_1)
#     print(point_2)
#     print(parent_1)
#     print(parent_2)

    cross = parent_1[point_1:point_2]

    t = 0
    z = 0
    for j in range(n):
#         print('j: ' + str(j))
        if j not in range(point_1,point_2):
#             print('z: '+ str(z))

            while True:
#                 print('t: '+ str(t))
                if parent_2[t] not in cross:
                    child[j] = parent_2[t]
                    t += 1
                    t = t%n
                    break
                else:
                    t += 1
                    t = t%n
        else:
            child[j] = cross[z]
            z += 1
            z = z%n
            

    return child



def mutation(chrom,n):
    point_1 = random.randint(0,n-1)
    point_2 = random.randint(0,n-1)
    
    mutated = chrom[:]
    mutated[point_1], mutated[point_2] = mutated[point_2], mutated[point_1]
    
    return mutated


def selection(population,fittness_function,k):
    pop = sorted(population,key=fittness_function)
    return pop[:k]



def local_search(chrom,n,temp,k_near):
    last_score = fittness(chrom)
    itter = 0
    while True:
        if itter > k_near:
            break
        itter += 1        
        point_1 = random.randint(0,n-1)
        point_2 = random.randint(0,n-1)

        mutated = chrom[:]
        mutated[point_1], mutated[point_2] = mutated[point_2], mutated[point_1]
        chrom_ch = mutated
        next_score = fittness(chrom_ch)
        delta = last_score - next_score
        max_prob = np.exp(delta/temp)
        prob = random.random()
        
        if delta >= 0 or prob < max_prob:
            chrom = chrom_ch
            break
        else:
            pass
    return chrom


def one_step(population,m,n,selection_rate,cross_rate,mutation_rate,temp,k_near):
    population = selection(population,fittness,selection_rate)
#     print(len(population))
    cross_pop = []
    for _ in range(cross_rate): 
        a = random.randint(0,selection_rate-1)
        chrom1 = population[a]
        a = random.randint(0,selection_rate-1)
        chrom2 = population[a]
        cross_pop.append(crossover(chrom1,chrom2,n))
    
    mutation_pop = []
    for _ in range(mutation_rate):
        a = random.randint(0,selection_rate-1)
        chrom = population[a]
        mutation_pop.append(mutation(chrom,n))

    population = population+cross_pop+mutation_pop
    sorted(population,key=fittness)
    population = population[:m]
#     local_search_index = random.sample(list(range(m-2)),(1*m)//5)
    for i in range(len(population)-1):
        population[i] = local_search(population[i],n,temp,k_near)
    
    return population


def check_finished(itter,iter_hist,max_itter):
    if itter > max_itter:
        return True
    elif fittness(iter_hist[-1]) == 0:
        return True
    

def training(n,m,selection_rate, cross_rate, mutation_rate,temp,cooling,k_near,itteration=100,repetition=2):
    repeat_hist = []
    
    for i in range(repetition):
        population = []
        for _ in range(m):
            population.append(init_population(n))
            
        iter_history = []
        iterr = 0
        while True:
            temp *= cooling
            if iterr%10==0 and iterr>1: 
                print(str(iterr)+': ')
                print(fittness(iter_history[-1]))
            population = one_step(population,m ,n , selection_rate, cross_rate, mutation_rate,temp,k_near)
            
            sorted(population,key=fittness)
            best_res = population[0]
            
            iter_history.append(best_res)
            
            if check_finished(iterr,iter_history,max_itter=itteration): break
            
            iterr += 1
        
        repeat_hist.append(iter_history)    

    
    return repeat_hist

def visualizition(chrom,n):
    grid = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            grid[i][j] = 240-50*((i+j)%2)
    for i in range(n):
        grid[i][chrom[i]] = 1
    
    return grid


