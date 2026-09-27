import random
import math
import csv

random.seed(42)

def colebrook_residual(f, Re, rel_rough):
    if f <= 0:
        return 1e9
    term = (rel_rough / 3.7) + (2.51 / (Re * math.sqrt(f)))
    if term <= 0:
        return 1e9
    return (1 / math.sqrt(f)) + 2 * math.log10(term)

def objective(f, Re, rel_rough):
    return abs(colebrook_residual(f, Re, rel_rough))

def fitness(f, Re, rel_rough):
    return 1.0 / (1.0 + objective(f, Re, rel_rough))

def tournament_selection(population, Re, rel_rough, k=3):
    candidates = random.sample(population, k)
    candidates.sort(key=lambda x: objective(x, Re, rel_rough))
    return candidates[0]

def crossover(parent1, parent2, crossover_rate=0.8):
    if random.random() < crossover_rate:
        alpha = random.random()
        child1 = alpha * parent1 + (1 - alpha) * parent2
        child2 = alpha * parent2 + (1 - alpha) * parent1
        return child1, child2
    return parent1, parent2

def mutate(child, mutation_rate=0.1, f_min=0.008, f_max=0.1):
    if random.random() < mutation_rate:
        child += random.uniform(-0.002, 0.002)
    return max(f_min, min(f_max, child))

def genetic_algorithm(Re, rel_rough, pop_size=50, generations=100,
                      crossover_rate=0.8, mutation_rate=0.1,
                      f_min=0.008, f_max=0.1, tolerance=1e-6):

    population = [random.uniform(f_min, f_max) for _ in range(pop_size)]

    best_solution = None
    best_error = float("inf")

    for _ in range(generations):
        population.sort(key=lambda x: objective(x, Re, rel_rough))
        current_best = population[0]
        current_error = objective(current_best, Re, rel_rough)

        if current_error < best_error:
            best_error = current_error
            best_solution = current_best

        if best_error < tolerance:
            break

        new_population = population[:2]

        while len(new_population) < pop_size:
            p1 = tournament_selection(population, Re, rel_rough)
            p2 = tournament_selection(population, Re, rel_rough)

            c1, c2 = crossover(p1, p2, crossover_rate)
            c1 = mutate(c1, mutation_rate, f_min, f_max)
            c2 = mutate(c2, mutation_rate, f_min, f_max)

            new_population.extend([c1, c2])

        population = new_population[:pop_size]

    return best_solution, best_error

def newton_raphson(Re, rel_rough, f0=0.02, tol=1e-6, max_iter=100):
    f = f0

    for _ in range(max_iter):
        r = colebrook_residual(f, Re, rel_rough)

        h = 1e-6
        derivative = (colebrook_residual(f + h, Re, rel_rough) -
                      colebrook_residual(f - h, Re, rel_rough)) / (2 * h)

        if abs(derivative) < 1e-12:
            return None

        f_new = f - r / derivative

        if f_new <= 0:
            return None

        if abs(f_new - f) < tol:
            return f_new

        f = f_new

    return f

if __name__ == "__main__":

    test_cases = [
        (1e4, 0.0001),
        (5e4, 0.00015),
        (1e5, 0.0002),
        (5e5, 0.00025),
        (1e6, 0.0003),
        (1e6, 0.005),
        (1e7, 0.01)
    ]

    print("\n" + "="*105)
    print("                COLEBROOK EQUATION SOLVER (Genetic Algorithm (GA) vs Newton Raphson (NR))")
    print("="*105)

    header = f"| {'Reynold No':>10} | {'Roughness':>12} | {'f (from GA)':>12} | {'f (from NR)':>12} | {'GA Residual Error':>12} |"
    print(header)
    print("-"*105)

    for Re, rel_rough in test_cases:
        ga_f, ga_err = genetic_algorithm(Re, rel_rough)
        nr_f = newton_raphson(Re, rel_rough)

        nr_display = f"{nr_f:.8f}" if nr_f else "DIVERGED"
        diff = abs(ga_f - nr_f) if nr_f else None
        diff_display = f"{diff:.2e}" if diff else "N/A"

        print(f"| {Re:10.0f} | {rel_rough:12.6f} | "
              f"{ga_f:12.8f} | {nr_display:>12} | "
              f"{ga_err:12.2e} |")

    print("="*105)
