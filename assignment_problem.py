# -*- coding: utf-8 -*-
"""assignment_problem.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-bZZe11xK_NSOb9CTOUYzVJJkakAoXbD
"""

import numpy as np

def reduction(cost):
    min_in_rows = np.min(cost, axis=1)
    min_in_columns = np.min(cost, axis=0)
    for i in range(cost.shape[0]):
        cost[i, :] -= min_in_rows[i]
    for j in range(cost.shape[1]):
        cost[:, j] -= min_in_columns[j]
    return cost

def assignment(cost):
    assigned = np.zeros_like(cost)
    for i in range(cost.shape[0]):
        j = np.argmin(cost[i, :])
        assigned[i, j] = 1
    return assigned

def is_optimal(assigned):
    return np.sum(assigned) == assigned.shape[0]

def mark_assigned_matrix(assigned):
    marked_rows = np.any(assigned == 1, axis=1)
    marked_columns = np.any(assigned == 1, axis=0)
    return marked_rows, marked_columns

def get_new_cost_matrix(cost, marked_rows, marked_columns):
    min_uncovered = np.inf
    for i in range(cost.shape[0]):
        for j in range(cost.shape[1]):
            if not marked_rows[i] and not marked_columns[j] and cost[i, j] < min_uncovered:
                min_uncovered = cost[i, j]

    for i in range(cost.shape[0]):
        for j in range(cost.shape[1]):
            if not marked_rows[i] and not marked_columns[j]:
                cost[i, j] -= min_uncovered
            elif marked_rows[i] and marked_columns[j]:
                cost[i, j] += min_uncovered

    return cost

def get_solution(assigned):
    return list(zip(np.where(assigned == 1)[0], np.where(assigned == 1)[1]))

def hungarian_assignment(cost):
    print("Initial cost:\n")
    print(cost)
    initial_cost = cost.copy()
    cost = reduction(cost)
    print("\nReduced Cost:\n")
    print(cost)
    assigned = assignment(cost)
    print("\nInitial assignment:\n")
    print(assigned)

    iteration = 0
    max_iterations = cost.shape[0] * cost.shape[1]

    while not is_optimal(assigned) and iteration < max_iterations:
        print("\n\nIteration {0}".format(iteration))
        print("\nNot optimal")
        marked_rows, marked_columns = mark_assigned_matrix(assigned)
        print("\nMarked rows:", marked_rows)
        print("\nMarked columns:", marked_columns)
        cost = get_new_cost_matrix(cost, marked_rows, marked_columns)
        print("\nNew cost:\n")
        print(cost)
        assigned = assignment(cost)
        print("\nNew assignment:\n")
        print(assigned)
        iteration += 1

    if iteration == max_iterations:
        print("Max iterations reached without achieving optimality.")

    print("Optimality reached")
    print("\nFinal assigned matrix:\n")
    print(assigned)
    solution = get_solution(assigned)
    print("Solution:", solution)

    total_cost = np.sum(np.multiply(initial_cost, assigned))
    print("\nTotal Cost:", total_cost)

if __name__ == "__main__":
    rows = int(input("Enter the number of rows: "))
    columns = int(input("Enter the number of columns: "))

    cost = np.zeros((rows, columns), dtype=int)
    for i in range(rows):
        for j in range(columns):
            cost[i, j] = int(input(f"Enter cost for row {i + 1}, column {j + 1}: "))

    print("\nInput cost matrix:")
    print(cost)

    hungarian_assignment(cost)
    print("Done!")