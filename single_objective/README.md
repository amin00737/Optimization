

# 🧬 Genetic Algorithm for 2D Grid Path Planning

This project implements a **Genetic Algorithm (GA)** to solve a 2D grid-based path planning problem with obstacles.

The algorithm evolves a set of intermediate waypoints between a start and goal position to generate a near-optimal collision-free path with minimal length.

> ⚠️ Note: While classical graph-based algorithms like A* are more efficient for grid shortest-path problems, this project demonstrates evolutionary optimization techniques for learning and experimentation purposes.

---

## 📌 Project Overview

* 2D grid environment (default: 20×20)
* Static obstacles
* Fixed start and goal positions
* Continuous waypoint encoding
* Collision-aware fitness function
* Path visualization

The objective function minimizes:

```
Total Path Length + Collision Penalty
```

---

## 📁 Repository Structure

```
├── GeneticAlgorithm.py          # Genetic Algorithm class implementation
├── GeneticAlgorithmTest.ipynb   # Example usage & visualization
├── README.md
├── LICENSE
```

---

## 🧠 Genetic Algorithm Design

### Representation

Each chromosome encodes waypoint coordinates:

```
[x1, y1, x2, y2, ..., xN, yN]
```

Where:

* N = number of intermediate waypoints
* Start and goal are fixed

---

### Evolution Operators

* **Selection:** Tournament selection
* **Crossover:** Arithmetic recombination
* **Mutation:** Gaussian perturbation
* **Elitism:** Best solution preserved across generations

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/amin00737/Optimization.git
cd Optimization
```

Install required packages:

```bash
pip install numpy pandas matplotlib
```

(Optional if using notebook)

```bash
pip install jupyterlab
```

---

## ▶️ How to Run

### Option 1 — Using Python Script

If using a test script:

```bash
python test.py
```

### Option 2 — Using Notebook

Open the notebook:

```bash
jupyter lab GeneticAlgorithmTest.ipynb
```

The notebook:

* Runs the GA
* Displays convergence curve
* Visualizes the optimized path

---

## 📊 Output

The algorithm produces:

* Best objective value
* Best waypoint solution
* Convergence plot
* Visualization of optimized path avoiding obstacles

---

## 🔧 Customization

You can easily modify:

* Grid size
* Obstacle layout
* Number of waypoints
* Population size
* Number of generations
* Mutation variance

---

## 🎯 Educational Purpose

This project is intended for:

* Learning evolutionary optimization
* Understanding constraint handling in GAs
* Experimenting with metaheuristic path planning
* Comparing GA with deterministic planners (e.g., A*)

---

## 📦 Dependencies

* Python 3.8+
* NumPy
* Pandas
* Matplotlib

---

## 📄 License

This project is licensed under the MIT License.

---

## 👤 Author

**Amin**
GitHub: [https://github.com/amin00737](https://github.com/amin00737)

---

If you want, I can now give you:

* 🚀 A version with GitHub badges
* 🧠 A more academic / thesis-style README
* 💼 A recruiter-optimized portfolio version
* 📊 A version highlighting optimization theory more strongly

Just tell me your goal.
