from utils import generate_variables, generate_domains, generate_neighbors
from colorama import Fore, Style, init
init(autoreset=True)

def check_constraint(val1, val2):
    return val1 != val2

class CSP:
    def __init__(self, variables, domains, neighbors):
        # list of vars
        self.variables = variables
        # dict of domains for each var
        self.domains = domains
        # dict of neighbours for each var
        self.neighbors = neighbors


    def is_consistent(self, variable, assignment):
        # we need to check that the variable and it's neighbours are consistent
        for neighbor in self.neighbors[variable]:
            if neighbor in assignment and (assignment[variable] == assignment[neighbor]):
                return False
        return True

    def ac3(self):
        # adding all the arcs to the queue
        queue = [(xi, xj) for xi in self.variables for xj in self.neighbors[xi]]
        while queue:
            # popping one arc
            (xi, xj) = queue.pop(0)
            if self.revise(xi, xj):
                if len(self.domains[xi]) == 0:
                    return False
                # adding the affected arcs
                for xk in self.neighbors[xi]:
                    if xk != xj:
                        queue.append((xk, xi))
        return True

    def revise(self, xi, xj):
        is_revised = False
        # for each value in xi's domain
        for dom_xi in set(self.domains[xi]):
            # we need to check that there is valid value in xj's domain
            if not any(check_constraint(dom_xi, dom_xj) for dom_xj in self.domains[xj]):
                # we need to remove the dom_xi from the xi's domain as no valid dom_xj for it
                self.domains[xi].remove(dom_xi)
                # flag to add the arcs
                is_revised = True
        return is_revised

    def backtracking_search(self, assignment={}):
        # checking that there is no need for backtracking
        if len(assignment) == len(self.variables):
            return assignment

        # choosing un-assigned variables
        var = self.select_unassigned_variable(assignment)
        for value in self.domains[var]:
            new_assignment = assignment.copy()
            # assigning the value to the var
            new_assignment[var] = value
            # checking consistency with other neighbours
            if self.is_consistent(var, new_assignment):
                # continuing to the next vars
                result = self.backtracking_search(new_assignment)
                if result:
                    return result
        return None

    def select_unassigned_variable(self, assignment):
        # looping on the vars to pick un-assigned var
        for var in self.variables:
            if var not in assignment:
                return var
        return None


def print_sudoku_grid(solution):
    number_colors = {
        1: Fore.RED,
        2: Fore.GREEN,
        3: Fore.YELLOW,
        4: Fore.BLUE,
        5: Fore.MAGENTA,
        6: Fore.CYAN,
        7: Fore.WHITE,
        8: Fore.LIGHTBLACK_EX,
        9: Fore.LIGHTCYAN_EX
    }

    for i in range(9):
        row = ""
        for j in range(9):
            value = solution.get(f"R{i + 1}C{j + 1}", " ")
            if value != " ":
                row += f"{number_colors[int(value)]}{value} "
            else:
                row += f"{Fore.RED} {Style.BRIGHT}"
        print(row.strip())
def main():
    initial_board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    variables = generate_variables()
    domains = generate_domains(initial_board)
    neighbors = generate_neighbors()

    csp = CSP(variables, domains, neighbors)
    if csp.ac3():
        # continuing the solution by backtracking 
        solution = csp.backtracking_search()
        if solution:
            print("Solution found:\n")
            print_sudoku_grid(solution)
        else:
            print("No solution found")
    else:
        print("No solution found")

if __name__ == "__main__":
    main()
