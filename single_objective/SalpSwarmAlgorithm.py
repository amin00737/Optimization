import numpy as np
from typing import List, Tuple
import pandas as pd
import matplotlib.pyplot as plt

# =====================================================
# Salp Swarm Algorithm (SSA)
# =====================================================

class SalpSwarmAlgorithm:
    def __init__(
        self,
        upperbound,
        lowerbound,
        objective_function,
        population_size=80,
        generation_size=300,
    ):
        self.objective_function = objective_function
        self.upperbound = upperbound
        self.lowerbound = lowerbound
        self.num_parameters = len(self.upperbound)

        self.population_size = population_size
        self.generation_size = generation_size

        self.best_obj_history = []
        self.best_solution_history = []

    # -------------------------------------------------
    # Initialize salp population
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
    # Run SSA
    # -------------------------------------------------
    def run(self):

        salps = self.generate_population()
        fitness = self.evaluate(salps)

        best_idx = np.argmin(fitness)
        food_position = salps[best_idx].copy()
        food_fitness = fitness[best_idx]

        self.best_obj_history.append(food_fitness)
        self.best_solution_history.append(food_position)

        for t in range(self.generation_size):

            c1 = 2 * np.exp(-((4 * t / self.generation_size) ** 2))

            for i in range(self.population_size):

                if i == 0:
                    # Leader update
                    for j in range(self.num_parameters):

                        c2 = np.random.rand()
                        c3 = np.random.rand()

                        if c3 < 0.5:
                            salps[i, j] = food_position[j] + \
                                c1 * ((self.upperbound[j] - self.lowerbound[j]) * c2 + self.lowerbound[j])
                        else:
                            salps[i, j] = food_position[j] - \
                                c1 * ((self.upperbound[j] - self.lowerbound[j]) * c2 + self.lowerbound[j])
                else:
                    # Follower update
                    salps[i] = 0.5 * (salps[i] + salps[i - 1])

            # Bound control
            salps = np.clip(salps, self.lowerbound, self.upperbound)

            # Evaluate
            fitness = self.evaluate(salps)

            # Update food (global best)
            best_idx = np.argmin(fitness)
            current_best = fitness[best_idx]

            if current_best < food_fitness:
                food_fitness = current_best
                food_position = salps[best_idx].copy()

            self.best_obj_history.append(food_fitness)
            self.best_solution_history.append(food_position)

        return (
            pd.DataFrame(self.best_obj_history, columns=["obj_hist"]),
            pd.DataFrame(self.best_solution_history),
        )
