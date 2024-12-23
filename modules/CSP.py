from modules.utils import generate_variables, generate_domains, generate_neighbors
from colorama import Fore, Style, init
import random
init(autoreset=True)

def check_constraint(val1, val2):
    return val1 != val2

class CSP:
    def __init__(self, board: list[list[int]]):
        # list of vars
        self.variables = generate_variables()
        # dict of domains for each var
        self.domains = generate_domains(board)
        # dict of neighbours for each var
        self.neighbors = generate_neighbors()


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
                print(f"Inconsistent arc detected: ({xi}, {xj})")
                print(f"  - Value {dom_xi} from {xi}'s domain is inconsistent with {xj}'s domain.")
                print(f"  - {xi}'s domain before removal: {self.domains[xi]}")
                print(f"  - {xj}'s domain: {self.domains[xj]}")
                # we need to remove the dom_xi from the xi's domain as no valid dom_xj for it
                self.domains[xi].remove(dom_xi)
                print(f"  - {xi}'s domain after removal: {self.domains[xi]}")
                print(f"  - {xj}'s domain: {self.domains[xj]}")
                # flag to add the arcs
                is_revised = True
        return is_revised

    # def backtracking_search(self, assignment={}):
    #     # checking that there is no need for backtracking
    #     if len(assignment) == len(self.variables):
    #         return assignment
    #
    #     # choosing un-assigned variables
    #     var = self.select_unassigned_variable(assignment)
    #     for value in self.domains[var]:
    #         new_assignment = assignment.copy()
    #         # assigning the value to the var
    #         new_assignment[var] = value
    #         # checking consistency with other neighbours
    #         if self.is_consistent(var, new_assignment):
    #             # continuing to the next vars
    #             result = self.backtracking_search(new_assignment)
    #             if result:
    #                 return result
    #     return None

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

            # saving original domains in case we need to backtrack
            original_domains = {v: self.domains[v][:] for v in self.variables}

            # if valid assignment
            if self.is_consistent(var, new_assignment):
                # assigning it
                self.domains[var] = [value]
                if self.ac3():
                    result = self.backtracking_search(new_assignment)
                    if result:
                        return result

            # back to original domains before backtracking
            self.domains = original_domains
        return None

    def select_unassigned_variable(self, assignment):
        candidates = []
        smallest_domain_size = float('inf')

        for var in self.variables:
            if var not in assignment:
                domain_size = len(self.domains[var])

                # getting the minimum domain variable
                if domain_size < smallest_domain_size:
                    smallest_domain_size = domain_size
                    candidates = [var]

                # adding it as a candidate as it's like the best
                elif domain_size == smallest_domain_size:
                    candidates.append(var)

        # no need for the other policy
        if len(candidates) == 1:
            return candidates[0]

        min_conflicts = float('inf')
        best_candidates = []

        # for each var in the candidates calculating the number of conflicts
        for var in candidates:
            conflicts = 0
            for value in self.domains[var]:
                for neighbor in self.neighbors[var]:
                    if neighbor not in assignment and value in self.domains[neighbor]:
                        conflicts += 1

            # adding it as a candidate
            if conflicts < min_conflicts:
                min_conflicts = conflicts
                best_candidates = [var]

            # adding it as it's like the best
            elif conflicts == min_conflicts:
                best_candidates.append(var)

        # broken at random if ties are present
        return random.choice(best_candidates)

    def find_all_solutions(self, assignment={}, limit=2):
        solutions = []

        def recursive_search(assignment):
            if len(assignment) == len(self.variables):
                solutions.append(assignment.copy())
                return

            var = self.select_unassigned_variable(assignment)
            for value in self.domains[var]:
                new_assignment = assignment.copy()
                new_assignment[var] = value

                # Backup the current state of the domains
                original_domains = {v: self.domains[v][:] for v in self.variables}

                if self.is_consistent(var, new_assignment):
                    self.domains[var] = [value]  # Assign the value to the domain
                    if self.ac3():  # Perform AC3 to propagate constraints
                        recursive_search(new_assignment)

                # Restore the original domains after backtracking
                self.domains = original_domains

                if len(solutions) >= limit:  # Stop early if multiple solutions found
                    return

        recursive_search(assignment)
        return solutions


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
        # [5, 3, 0, 0, 7, 0, 0, 0, 0],
        # [6, 0, 0, 1, 9, 5, 0, 0, 0],
        # [0, 9, 8, 0, 0, 0, 0, 6, 0],
        # [8, 0, 0, 0, 6, 0, 0, 0, 3],
        # [4, 0, 0, 8, 0, 3, 0, 0, 1],
        # [7, 0, 0, 0, 2, 0, 0, 0, 6],
        # [0, 6, 0, 0, 0, 0, 2, 8, 0],
        # [0, 0, 0, 4, 1, 9, 0, 0, 5],
        # [0, 0, 0, 0, 8, 0, 0, 7, 9]

        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    csp = CSP(initial_board)
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
