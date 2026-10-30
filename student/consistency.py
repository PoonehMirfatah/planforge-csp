from __future__ import annotations
from planforge.core.models import CSPProblem, Assignment, Rect
from planforge.core.geometry import inside_boundary, overlaps
from planforge.core.constraints import constraint_is_satisfied

def is_consistent(problem: CSPProblem, assignment: Assignment, variable: str, value: Rect) -> bool:
   
    if not inside_boundary(value, problem.width, problem.height):
        return False

    room_spec = problem.room_specs[variable]
    if value.area < room_spec.min_area or value.area > room_spec.max_area:
        return False

    for assigned_var, assigned_rect in assignment.items():
        if overlaps(value, assigned_rect):
            return False

    temp_assignment = assignment.copy()
    temp_assignment[variable] = value
    for constraint in problem.constraints:
       
        if not constraint_is_satisfied(problem, constraint, temp_assignment):
            return False

    return True