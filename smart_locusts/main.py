import csv
from functions import *
from pso import run_pso
from mosquitos import run_mosquitos
from bees import run_bees

def run_test_set(test_pso=False, test_mosquito=False, test_bees=True, writer=None):

    if writer is not None:
        writer = csv.writer(writer, delimiter='\t', quoting=csv.QUOTE_ALL)

    functions = [
                 (griewank, (-600, 600), 2),
                 (sphere, (-100, 100), 2),
                 (rosenbrok, (-10, 10), 2),
                 (rastrigin, (-5.12, 5.12), 2),
                 ]

    for fun in functions:
        print "Run simulation for function ", fun[0].__name__

        if test_mosquito:
            if writer is not None:
                writer.writerow(("Function", "Initial num swarms", "Final num swarms", "Starvation kt", "Score", "Error", "Position", "Iter"))
            run_mosquitos(fun, writer=writer)

        if test_pso:
            if writer is not None:
                writer.writerow(("Function", "Topology", "PSO", "Phi", "Score", "Error", "Position", "Iter"))
            run_pso(fun, writer=writer)

        if test_bees:
            if writer is not None:
                writer.writerow(("Function", "Employed %", "Onlooker %", "Scout Num", "Score", "Error", "Position", "Iter"))
            run_bees(fun, writer=writer)



def solve(save_result=True):

    if save_result:
        with open("results.csv", "w") as f:
            run_test_set(test_pso=False, writer=f)
    else:
        run_test_set(test_pso=False)

if __name__ == "__main__":
    solve()
