from typing import List, Tuple
import pandas as pd
import numpy as np


# =====================================================
# Differential Evolution (DE/rand/1/bin)
# =====================================================

class DifferentialEvolution:
    def __init__(
        self,
        upperbound,
        lowerbound,
        objective_function,
        population_size=80,
        generation_size=300,
        F=0.8,        # Mutation factor
        CR=0.9,       # Crossover rate
    ):
        self.objective_function = objective_function
        self.upperbound = upperbound
        self.lowerbound = lowerbound
        self.num_parameters = len(self.upperbound)

        self.population_size = population_size
        self.generation_size = generation_size
        self.F = F
        self.CR = CR

        self.best_obj_history = []
        self.best_solution_history = []

    # -------------------------------------------------
    # Initialize population
    # -------------------------------------------------
    def generate_population(self):
        return np.random.uniform(
            self.lowerbound,
            self.upperbound,
            (self.population_size, self.num_parameters),
        )

    # -------------------------------------------------
    # Evaluate fitness
    # -------------------------------------------------
    def evaluate(self, population):
        return np.array([self.objective_function(ind) for ind in population])

    # -------------------------------------------------
    # Run DE
    # -------------------------------------------------
    def run(self):

        population = self.generate_population()
        fitness = self.evaluate(population)

        best_idx = np.argmin(fitness)
        best_solution = population[best_idx].copy()
        best_value = fitness[best_idx]

        self.best_obj_history.append(best_value)
        self.best_solution_history.append(best_solution)

        for gen in range(self.generation_size):

            new_population = np.zeros_like(population)

            for i in range(self.population_size):

                # --- Mutation (rand/1) ---
                idxs = list(range(self.population_size))
                idxs.remove(i)
                r1, r2, r3 = np.random.choice(idxs, 3, replace=False)

                mutant = (
                    population[r1]
                    + self.F * (population[r2] - population[r3])
                )

                # Bound control
                mutant = np.clip(mutant, self.lowerbound, self.upperbound)

                # --- Crossover (binomial) ---
                trial = population[i].copy()
                j_rand = np.random.randint(self.num_parameters)

                for j in range(self.num_parameters):
                    if np.random.rand() < self.CR or j == j_rand:
                        trial[j] = mutant[j]

                # --- Greedy Selection ---
                trial_fitness = self.objective_function(trial)

                if trial_fitness < fitness[i]:
                    new_population[i] = trial
                    fitness[i] = trial_fitness
                else:
                    new_population[i] = population[i]

            population = new_population

            # Update global best
            current_best_idx = np.argmin(fitness)
            current_best_val = fitness[current_best_idx]

            if current_best_val < best_value:
                best_value = current_best_val
                best_solution = population[current_best_idx].copy()

            self.best_obj_history.append(best_value)
            self.best_solution_history.append(best_solution)

        return (
            pd.DataFrame(self.best_obj_history, columns=["obj_hist"]),
            pd.DataFrame(self.best_solution_history),
        )
