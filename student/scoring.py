from planforge.core.geometry import used_area, bounding_box, is_connected_layout, aspect_ratio, distance_to_point, touches_boundary, adjacent

def score_assignment(problem, assignment):
    if not assignment:
        return 0.0

    score = 40.0  
    rects = list(assignment.values())

    
    total_area = problem.width * problem.height
    used = used_area(rects)
    coverage_ratio = used / total_area
    score += coverage_ratio * 35.0

    
    bbox = bounding_box(rects)
    if bbox.area > 0:
        compactness = used / bbox.area
        score += compactness * 10.0

    
    if is_connected_layout(assignment):
        score += 5.0
        
    avg_aspect = sum(aspect_ratio(r) for r in rects) / len(rects)
    score += max(0.0, 5.0 - (avg_aspect - 1.0) * 2.0)

    
    if hasattr(problem, 'entrance'):
        entrance_pt = problem.entrance
        
        for name, rect in assignment.items():
            dist_to_ent = distance_to_point(rect, entrance_pt)
            
            if "Bedroom" in name:     
                score += min(1.0, dist_to_ent * 0.1) 
            elif "Living" in name:
                score += max(0.0, 1.0 - (dist_to_ent * 0.1)) 
            elif "Bathroom" in name and "Hall" in assignment:
                if adjacent(rect, assignment["Hall"]):
                    score += 1.5
            elif "Kitchen" in name and "Living" in assignment:
                if adjacent(rect, assignment["Living"]):
                    score += 1.5

    return max(0.0, min(100.0, score))