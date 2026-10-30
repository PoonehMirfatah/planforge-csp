def forward_check(problem, var, val, assignment, domains):
    pruned_domains = {k: list(v) for k, v in domains.items()}
    temp_assignment = assignment.copy()
    temp_assignment[var] = val
    
    changed = True
    while changed:
        changed = False
        
        for unassigned_var in problem.variables:
            if unassigned_var in temp_assignment:
                continue
            
            valid_values = []
            from .consistency import is_consistent
            for unassigned_val in pruned_domains[unassigned_var]:
                if is_consistent(problem, temp_assignment, unassigned_var, unassigned_val):
                    valid_values.append(unassigned_val)
            
            if len(valid_values) < len(pruned_domains[unassigned_var]):
                pruned_domains[unassigned_var] = valid_values
                changed = True  
            
            if len(valid_values) == 0:
                return None
            
            if len(valid_values) == 1:
                temp_assignment[unassigned_var] = valid_values[0]
                
    return pruned_domains


def ac3(problem, assignment, domains):
    
    pruned_domains = {k: list(v) for k, v in domains.items()}
    
    
    unassigned_vars = [v for v in problem.variables if v not in assignment]
    
    queue = []
    for xi in unassigned_vars:
        for xj in unassigned_vars:
            if xi != xj:
                queue.append((xi, xj))
                
    
    while queue:
        xi, xj = queue.pop(0)  
        
    
        if remove_inconsistent_values(problem, assignment, pruned_domains, xi, xj):
    
            if len(pruned_domains[xi]) == 0:
                return None
                
    
            for xk in unassigned_vars:
                if xk != xi and xk != xj:
                    queue.append((xk, xi))
                    
    return pruned_domains


def remove_inconsistent_values(problem, assignment, domains, xi, xj):
    removed = False
    valid_xi_values = []
    
    from planforge.core.geometry import overlaps
    from planforge.core.constraints import constraint_is_satisfied
    
    
    for x in domains[xi]:
        has_support = False
        
        for y in domains[xj]:
        
            if overlaps(x, y):
                continue
                
            temp_assignment = assignment.copy()
            temp_assignment[xi] = x
            temp_assignment[xj] = y
            
            satisfied = True
            for constraint in problem.constraints:
                if xi in constraint.variables or xj in constraint.variables:
                    if not constraint_is_satisfied(problem, constraint, temp_assignment):
                        satisfied = False
                        break
                        
            if satisfied:
                has_support = True
                break
                
        if has_support:
            valid_xi_values.append(x)
        else:
            removed = True  
            
    domains[xi] = valid_xi_values
    return removed