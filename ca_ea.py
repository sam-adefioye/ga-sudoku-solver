from random import choice, random
from copy import deepcopy
from sys import argv

### EVOLUTIONARY ALGORITHM ###

def evolve():
    """
    Evolve population.
    """
    population = create_pop()
    fit_population = evaluate_pop(population)
    for gen in range(GEN_SIZE):
        mating_pool = select_pop(population, fit_population)
        offspring_population = crossover_pop(mating_pool)
        population = mutate_pop(offspring_population)
        fit_population = evaluate_pop(population)
        best_ind, best_fit = best_pop(population, fit_population)
        print("gen: " + str(gen + 1) + ", " + "best fitness: %f" % best_fit, "\n")
        if best_fit == 1.0:  # If the global optimum/solution has been reached
            print_grid(best_ind)
            break

        ''' If the algorithm gets stuck in a local optima, restart with new population
        Restart algorithm every 20 generations if optimum fitness not reached '''
        if gen % RESTART == 0 and best_fit < 1.0:
            population = create_pop()
            population.append(best_ind)  # Add best individual from previous generation to new population
            fit_population = evaluate_pop(population)

### FILE FUNCTIONS ###

def read_file(filename):
    """
    Return 9x9 sudoku grid as multidimensional list of strings read from file with name, filename.
    """
    row = []
    f = open(filename, "r")
    for l in f:
        l = l.split('\n')
        l.pop()
        row.append(l)

    for r in row:
        r[0] = r[0].replace("!", " ")
        r[0] = r[0].replace(".", "0")

    for x in row:
        z = list(x[0])  # Split string of numbers into list and add to list to be returned
        row[row.index(x)] = z

    return row


def create_sudoku(grid):
    """
    Return 9x9 sudoku grid as multidimensional list of numbers.
    """

    # Only convert strings containing integers to int
    for j in grid:
        k = [int(s) for s in j if s is not '.' if s is not ' ' if s is not '-']
        grid[grid.index(j)] = k

    grid.pop(3)  # Remove hyphens
    grid.pop(6)

    return grid

### POPULATION-LEVEL OPERATORS ###

def create_pop():
    """
    Return a newly created population.
    """
    return [create_ind() for _ in range(POP_SIZE)]

def evaluate_pop(population):
    """
    Return fitness score for population.
    """
    return [evaluate_ind(individual) for individual in population]


def select_pop(population, fit_population):
    """
    Return list of selected individuals from population sorted by their fitness scores.
    """
    srtd_pop = sorted(zip(population, fit_population), key=lambda i_fit: i_fit[1], reverse=True)
    return [ind for ind, fit in srtd_pop[:int(POP_SIZE * TRUNCATION_RATE)]]

def crossover_pop(population):
    """
    Return new population from crossover operation.
    """
    return [crossover_ind(choice(population), choice(population)) for _ in range(POP_SIZE)]

def mutate_pop(population):
    """
    Return a mutated population.
    """
    return [mutate_ind(individual) for individual in population]


def best_pop(population, fit_population):
    """
    Return individual from population with the highest fitness score.
    """
    return sorted(zip(population, fit_population), key=lambda i_fit: i_fit[1], reverse=True)[0]

### INDIVIDUAL-LEVEL OPERATORS ###

def create_ind():
    """
    Return a newly created member of the population.
    """
    temp_lst = deepcopy(grids)
    for sub in temp_lst:
        # Store list of numbers in [1..9] not in the current row of the grid
        check = [val for val in space if val not in sub]
        for num in sub:
            if num is 0:
                new_dig = choice(check)
                sub[sub.index(num)] = new_dig
                check.remove(new_dig)
    return temp_lst

def get_sub(grid):
    """
    Return a 3x3 subgrid as a list, from a multidimensional list.
    """
    answer = []
    for r in range(3):
        for c in range(3):
            block = []
            for i in range(3):
                for j in range(3):
                    block.append(grid[3 * r + i][3 * c + j])
            answer.append(block)
    return answer

def consistent(individual):
    """
    Return the number of original integers an individual has.
    """
    return sum(len(set(row)) for row in individual)


def evaluate_ind(individual):
    """
    Return a fitnes score for an individual.
    """
    # Checks rows, columns and subgrids, respectively
    a, b, c = consistent(individual), consistent(list(zip(*individual))), consistent(get_sub(individual))
    return (a + b + c) / 243

def crossover_ind(individual1, individual2):
    """
    Return a new individual formed from crossover between individual1 and individual2.
    """
    return [choice(row_pair) for row_pair in zip(individual1, individual2)]

def swap_digit(row1, grid_row):
    """
    Return a list, row1, with two elements swapped in place.
    """
    temp_l = []
    for j in range(len(row1)):
        if grid_row[j] == 0:
            temp_l.append(j)  # Adds indexes of all occurrences of 0 in row from grid_row
    z = temp_l.pop(choice(range(len(temp_l))))  # Randomly selects two numbers to swap in place
    w = temp_l.pop(choice(range(len(temp_l))))

    row1[z], row1[w] = row1[w], row1[z]
    return row1


def mutate_ind(individual):
    """
    Return an individual, mutated or unmutated.
    """
    # Randomly decides to mutate individual
    if random() < MUTATION_RATE:
        return [swap_digit(individual[ind], grids[ind]) for ind in range(9)]
    return individual

def print_grid(individual):
    """
    Print individual as 9x9 sudoku grid.
    """
    for i in range(3):
        print(" ".join(str(x) for x in individual[i][:3]), "!", " ".join(str(x) for x in individual[i][3:6]), "!",
              " ".join(str(x) for x in individual[i][6:]))
    print("- - - ! - - - ! - - -")

    for i in range(3, 6):
        print(" ".join(str(x) for x in individual[i][:3]), "!", " ".join(str(x) for x in individual[i][3:6]), "!",
              " ".join(str(x) for x in individual[i][6:]))
    print("- - - ! - - - ! - - -")

    for i in range(6, 9):
        print(" ".join(str(x) for x in individual[i][:3]), "!", " ".join(str(x) for x in individual[i][3:6]), "!",
              " ".join(str(x) for x in individual[i][6:]))


### PARAMETER VALUES ###

space = [1, 2, 3, 4, 5, 6, 7, 8, 9]
IND_SIZE = len(space)
GEN_SIZE = 1000
TRUNCATION_RATE = 0.3
MUTATION_RATE = 0.001
RESTART = 20  # Restart threshold for the evolutionary algorithm

if __name__ == "__main__":
    grid_file = str(argv[1])
    POP_SIZE = int(argv[2])
    rows = read_file(grid_file)
    grids = create_sudoku(rows)
    evolve()
