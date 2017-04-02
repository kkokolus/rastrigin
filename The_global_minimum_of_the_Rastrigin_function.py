import random
import math

population = []
translator = [-1,4,2,1,0.5,0.25,0.125,0.0625,0.03125,0.015625,0.0078125,0.00390625]
value_of_adaptation_function = {}
worst_individual = 0
sum_of_adaptation = 0
percentage_of_roulette_wheel = {}
temporary_population = []
number = 0
population_size = 100

def making_a_chromosome(number):
    chromosome = []
    for i in range (number):
       chromosome.append(random.randint(0, 1))
    #ograniczenie wartosci chromosomu do (-5.12, 5.12):
    if chromosome[1] == 1:
        chromosome[2] = 0
        if chromosome[3] == 1:
            chromosome[4] = chromosome[5] = chromosome[6] = 0
    return chromosome
    
def making_a_population(number, size):
    for i in range(size):
        population.append(making_a_chromosome(number))

def minimum_of_a_rastrigin_function(n,m):
        rastr = 10 * n
        for i in range(0,n):
            rastr += m ** 2 - 10 * math.cos(2 * math.pi * m)
        return rastr

def individual_adaptation(chromosome, function):
    for it in chromosome:
        p=1
        x=0          
        for item in it[1::]:
            x += item * translator[p]
            p+=1
        if it[0] == 1:
            x = x * (-1)
        value_of_adaptation_function[function(2,x)] = it
       
def roulette_wheel(size, percent):
    for i in range(0, size):
        temporary_population.append(percent[random.randint(0, len(percent)-1)])

def single_point_crossover(temporary_population):
    random.shuffle(temporary_population)
    for i in range (0, len(temporary_population), 2):
             rand = random.randint(0, 10)
             #if rand value > 5 we're going to chose a point and do a crossover, and both of the new individuals are added to the population 
             #if rand value < 5 both of our individuals are duplicated and added to the population
             if rand > 5:
                point = random.randint(0, 10)
                temp = temporary_population[i+1][:]
                temporary_population[i+1][point:] = temporary_population[i][point:]
                temporary_population[i][point:] = temp[point::]
                population.append(temporary_population[i])
                population.append(temporary_population[i+1])
             else:
                population.append(temporary_population[i])
                population.append(temporary_population[i+1])
            
def mutation(population):
    for individual in population:
        for gene in range(0,len(individual)):
            rand = random.randint(0,100)
            if rand < 3:
                if individual[gene] == 0: 
                    individual[gene] = 1
                else:
                    individual[gene] = 0
    return population

making_a_population(11, population_size)
counter = 0
stop = 0

while ((stop < 1)):

    individual_adaptation(population, minimum_of_a_rastrigin_function)

    for val in value_of_adaptation_function:
        counter +=1
        if val < 0.01:
            x=0
            p=1
            for item in value_of_adaptation_function[val][1::]:
                x += item * translator[p]
                p+=1
            print ("The minimum of Rastrigin function was found in x = " + str(x) + " after " + str(counter) + " iterations")
            stop = 2

    for value_of_adapt in value_of_adaptation_function:
        sum_of_adaptation += value_of_adapt
        if value_of_adapt > worst_individual:
            worst_individual = value_of_adapt

    #each number have its own value of adaptation function, according to its probability
    for value_of_adapt in value_of_adaptation_function:
        probability_of_a_roulette_wheel = value_of_adapt / sum_of_adaptation
        probability_of_a_roulette_wheel = round(probability_of_a_roulette_wheel,5)
        probability_of_a_roulette_wheel *= 1000
        probability_of_a_roulette_wheel = math.ceil(probability_of_a_roulette_wheel)
        for i in range (number,number+probability_of_a_roulette_wheel):
            percentage_of_roulette_wheel[i] = value_of_adaptation_function[value_of_adapt]
            number += 1

    population = []

    roulette_wheel(population_size, percentage_of_roulette_wheel)
    
    single_point_crossover(temporary_population)
    mutation(population)

    if (counter > 10000):
        print("The solution wasn't found after 10000 iterations, you have to change the original population")
        break
