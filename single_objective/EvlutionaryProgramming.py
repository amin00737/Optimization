from typing import List, Tuple
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# =====================================================
# Evolutionary Programming (Self-Adaptive)
# =====================================================

class EvolutionaryProgramming:
    def __init__(
        self,
        upperbound,
        lowerbound,
        objective_function,
        population_size=80,
        generation_size=300,
        sigma_init=2.0,
    ):
        self.objective_function = objective_function
        self.upperbound = upperbound
        self.lowerbound = lowerbound
        self.num_parameters = len(self.upperbound)

        self.population_size = population_size
        self.generation_size = generation_size

        # Self-adaptive mutation parameters
        self.sigma_init = sigma_init

        self.best_obj_history = []
        self.best_solution_history = []

    # -------------------------------------------------
    # Initialize population
    # -------------------------------------------------
    def generate_population(self):
        population = np.random.uniform(
            self.lowerbound,
            self.upperbound,
            (self.population_size, self.num_parameters),
        )

        sigmas = np.ones_like(population) * self.sigma_init
        return population, sigmas

    # -------------------------------------------------
    # Evaluate fitness
    # -------------------------------------------------
    def evaluate(self, population):
        return np.array([self.objective_function(ind) for ind in population])

    # -------------------------------------------------
    # Run EP
    # -------------------------------------------------
    def run(self):

        tau = 1 / np.sqrt(2 * np.sqrt(self.num_parameters))
        tau_prime = 1 / np.sqrt(2 * self.num_parameters)

        population, sigmas = self.generate_population()
        fitness = self.evaluate(population)

        best_idx = np.argmin(fitness)
        best_solution = population[best_idx].copy()
        best_value = fitness[best_idx]

        self.best_obj_history.append(best_value)
        self.best_solution_history.append(best_solution)

        for gen in range(self.generation_size):

            # --- Mutation with self-adaptation ---
            offspring = np.zeros_like(population)
            offspring_sigmas = np.zeros_like(sigmas)

            for i in range(self.population_size):

                global_noise = np.random.randn()
                local_noise = np.random.randn(self.num_parameters)

                # Self-adaptive sigma update
                offspring_sigmas[i] = sigmas[i] * np.exp(
                    tau_prime * global_noise + tau * local_noise
                )

                # Mutation
                offspring[i] = population[i] + \
                    offspring_sigmas[i] * np.random.randn(self.num_parameters)

            # Bound control
            offspring = np.clip(offspring, self.lowerbound, self.upperbound)

            # Evaluate offspring
            fitness_off = self.evaluate(offspring)

            # --- Combine parents + offspring ---
            combined_pop = np.vstack([population, offspring])
            combined_sigmas = np.vstack([sigmas, offspring_sigmas])
            combined_fitness = np.hstack([fitness, fitness_off])

            # --- Tournament selection ---
            wins = np.zeros(len(combined_pop))

            for i in range(len(combined_pop)):
                opponents = np.random.choice(len(combined_pop), 10)
                wins[i] = np.sum(
                    combined_fitness[i] < combined_fitness[opponents]
                )

            selected_idx = np.argsort(-wins)[:self.population_size]

            population = combined_pop[selected_idx]
            sigmas = combined_sigmas[selected_idx]
            fitness = combined_fitness[selected_idx]

            # Update best
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
