import heapq

def heuristic(a, b):
    """
    Calculate the Manhattan distance between two points a and b.
    a and b are tuples (x, y).
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(node, grid):
    """
    Given a node (x, y) and a grid, return valid neighbor nodes.
    Only returns neighbors that are within bounds and are free (grid value 0).
    """
    # Convert coordinates to integers
    x, y = int(node[0]), int(node[1])
    neighbors = []
    # Define 4-connected grid moves: up, down, left, right.
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
            if grid[ny][nx] == 0:  # 0 means walkable
                neighbors.append((nx, ny))
    return neighbors


def reconstruct_path(came_from, current):
    """
    Reconstructs the path from start to goal using the came_from dictionary.
    """
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()  # so that it starts at the beginning
    return path

def a_star(grid, start, goal):
    """
    Executes the A* algorithm on a grid.
    
    :param grid: 2D list, where 1 represents a wall and 0 represents open space.
    :param start: Tuple (x, y) representing the start cell.
    :param goal: Tuple (x, y) representing the goal cell.
    :return: A list of (x, y) tuples representing the path from start to goal, or None if no path found.
    """
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    
    while open_set:
        # Pop the node with the lowest f_score
        current = heapq.heappop(open_set)[1]
        
        if current == goal:
            return reconstruct_path(came_from, current)
        
        for neighbor in get_neighbors(current, grid):
            tentative_g_score = g_score[current] + 1  # assume cost between adjacent nodes is 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                # Only add the neighbor if it's not already in the open set.
                if neighbor not in [item[1] for item in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    
    # No path found
    return None