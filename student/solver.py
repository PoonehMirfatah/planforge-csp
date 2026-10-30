from __future__ import annotations
from planforge.core.models import CSPProblem, Assignment, Rect
from planforge.core.engine import SolverContext

from student.consistency import is_consistent
from student.heuristics import select_unassigned_variable, order_domain_values
from student.inference import forward_check, ac3

def solve(problem: CSPProblem, ctx: SolverContext) -> Assignment | None:

    domains = ctx.copy_domains()
    # ---------------------------------------------------------
    from student.inference import ac3
    domains = ac3(problem, {}, domains)
    if domains is None:
        return None
    # ---------------------------------------------------------
    backtrack(problem, {}, domains, ctx)
    return ctx.best_assignment

def backtrack(problem, assignment, domains, ctx):
    if ctx.should_stop:
        return
    ctx.on_node()
    if len(assignment) == len(problem.variables):
        ctx.on_solution(assignment)
        return

    from .heuristics import select_unassigned_variable, order_domain_values
    var = select_unassigned_variable(problem, assignment, domains)
    
    if hasattr(ctx, 'on_select_variable'):
        ctx.on_select_variable(var, assignment)

    for val in order_domain_values(problem, var, assignment, domains):
        ctx.on_assignment_tried()
        ctx.on_consistency_check()
        
        from .consistency import is_consistent
        if is_consistent(problem, assignment, var, val):
            assignment[var] = val
            if hasattr(ctx, 'on_assign'):
                ctx.on_assign(var, val, assignment)
            before_count = sum(len(d) for d in domains.values())
            
            from .inference import forward_check
            pruned_domains = forward_check(problem, var, val, assignment, domains)
            
            if pruned_domains is not None:
                after_count = sum(len(d) for d in pruned_domains.values())
                
                if hasattr(ctx, 'on_prune') and before_count > after_count:
                    ctx.on_prune(before_count, after_count)
                    
                backtrack(problem, assignment, pruned_domains, ctx)
    
            del assignment[var]
            if hasattr(ctx, 'on_unassign'):
                ctx.on_unassign(var, assignment)

    ctx.on_backtrack()

def is_complete(problem, assignment) -> bool:
    return len(assignment) == len(problem.variables)