# Colebrook Equation Solver using Genetic Algorithm and Newton-Raphson

## Overview
This project solves the **Colebrook equation**, an implicit nonlinear equation used in fluid mechanics and chemical engineering to determine the **Darcy friction factor** for turbulent flow in rough pipes.

The project compares two approaches:

- **Genetic Algorithm (GA)** — an AI-based optimization technique
- **Newton-Raphson (NR)** — a traditional numerical method

The goal is to show how an optimization-based AI method can be used to solve a classical engineering equation and compare its performance with a standard numerical approach.

---

## Colebrook Equation

The Colebrook equation is:

$$
\frac{1}{\sqrt{f}} = -2 \log_{10}\left(\frac{\varepsilon / D}{3.7} + \frac{2.51}{Re \sqrt{f}}\right)
$$

Where:

- `f` = Darcy friction factor
- `Re` = Reynolds number
- `ε / D` = relative roughness of the pipe

Since the equation is **implicit in `f`**, it cannot be solved directly and requires iterative or optimization-based techniques.

---

## Objective

The objective of this project is to find the friction factor `f` such that the Colebrook residual becomes as close to zero as possible.

The residual function used is:

$$
R(f) = \frac{1}{\sqrt{f}} + 2\log_{10}\left(\frac{\varepsilon/D}{3.7} + \frac{2.51}{Re\sqrt{f}}\right)
$$

The solver tries to minimize:

$$
|R(f)|
$$

---

## Methods Used

### 1. Genetic Algorithm
The Genetic Algorithm searches for the best friction factor value by:

- generating a random population of candidate solutions,
- evaluating each candidate using the Colebrook residual,
- selecting the fittest candidates,
- applying crossover and mutation,
- repeating the process over several generations.

### 2. Newton-Raphson Method
The Newton-Raphson method is used as a benchmark numerical method. It iteratively updates the friction factor using the derivative of the residual function until convergence.

---

## Features

- Solves the Colebrook equation for multiple test cases
- Compares **GA** and **Newton-Raphson**
- Displays:
  - Reynolds number
  - relative roughness
  - GA friction factor
  - NR friction factor
  - GA residual error
- Demonstrates an AI-based optimization approach for a chemical engineering problem

---

## File Structure

```text
├── Project Code.py
└── README.md
