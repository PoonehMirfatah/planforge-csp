from __future__ import annotations
from planforge.core.models import CSPProblem, Assignment, Rect

def select_unassigned_variable(problem: CSPProblem, assignment: Assignment, domains: dict[str, list[Rect]]) -> str:
    unassigned_vars = [v for v in problem.variables if v not in assignment]
    
    from .consistency import is_consistent
    def count_valid_values(var):
        return sum(1 for val in domains[var] if is_consistent(problem, assignment, var, val))
        
    return min(unassigned_vars, key=count_valid_values)

def order_domain_values(problem: CSPProblem, variable: str, assignment: Assignment, domains: dict[str, list[Rect]]) -> list[Rect]:
    unassigned_vars = [v for v in problem.variables if v not in assignment and v != variable]
    
    total_remaining_options = sum(len(domains[v]) for v in unassigned_vars)
    
    def count_conflicts(val):
        conflicts = 0
        temp_assignment = assignment.copy()
        temp_assignment[variable] = val
        from .consistency import is_consistent
        for other_var in unassigned_vars:
            for other_val in domains[other_var]:
                if not is_consistent(problem, temp_assignment, other_var, other_val):
                    conflicts += 1
        return conflicts

    if total_remaining_options > 50:
        return sorted(domains[variable], key=lambda val: (val.y, val.x))
        
    return sorted(domains[variable], key=lambda val: (count_conflicts(val), val.y, val.x))