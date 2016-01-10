import csv
from functions import *
from pso import run_pso, run_experiment
from mosquitos import run_mosquitos

def run_test_set(test_pso=True, writer=None):

    if writer is not None:
        writer = csv.writer(writer, delimiter='\t', quoting=csv.QUOTE_ALL)
        writer.writerow(("Function", "Topology", "PSO", "Phi", "Score", "Error", "Position", "Iter"))

    functions = [(griewank, (-600, 600), 2),
                 (sphere, (-100, 100), 2),
                 (rosenbrok, (-10, 10), 2),
                 (rastrigin, (-5.12, 5.12), 2),
                 ]

    if test_pso:
        for fun in functions:
            run_mosquitos(fun, writer=writer)
            # run_pso(fun, writer=writer)



def solve(save_result=True):

    if save_result:
        with open("results.csv", "w") as f:
            run_test_set(test_pso=True, writer=f)
    else:
        run_test_set(test_pso=True)

if __name__ == "__main__":
    solve()
