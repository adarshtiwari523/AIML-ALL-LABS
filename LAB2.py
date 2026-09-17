from collections import deque

def bfs(graph, start, goal):
    print(f"\n--- BFS Traversal ({start} -> {goal}) ---")
    queue = deque([[start]])
    visited = []

    step = 1
    while queue:
        queue_state = [path[-1] for path in queue]
        print(f"Step {step}:")
        print(f"  Queue: {queue_state}")
        print(f"  Visited: {visited}")

        path = queue.popleft()
        node = path[-1]

        if node == goal:
            print(f"Goal '{goal}' reached!")
            print(f"  Final Path Found by BFS: {' -> '.join(path)}")
            return path

        if node not in visited:
            visited.append(node)

            for neighbor in sorted(graph.get(node, [])):
                if neighbor not in visited:
                    queue.append(path + [neighbor])

        step += 1


def dfs(graph, start, goal):
    print(f"\n--- DFS Traversal ({start} -> {goal}) ---")
    stack = [[start]]
    visited = []

    step = 1
    while stack:
        stack_state = [path[-1] for path in stack]
        print(f"Step {step}:")
        print(f"  Stack: {stack_state}")
        print(f"  Visited: {visited}")

        path = stack.pop()
        node = path[-1]

        if node == goal:
            print(f"Goal '{goal}' reached!")
            print(f"  Final Path Found by DFS: {' -> '.join(path)}")
            return path

        if node not in visited:
            visited.append(node)

            # Reverse order so alphabetical order is followed
            for neighbor in sorted(graph.get(node, []), reverse=True):
                if neighbor not in visited:
                    stack.append(path + [neighbor])

        step += 1


if __name__ == "__main__":

    social_network = {
        'Alice': ['Charlie', 'David'],
        'Bob': ['Emma', 'Fred'],
        'Charlie': ['Alice', 'Emma'],
        'David': ['Alice', 'Emma', 'Fred'],
        'Emma': ['Bob', 'Charlie', 'David'],
        'Fred': ['Bob', 'David']
    }

    bfs(social_network, 'Alice', 'Bob')
    dfs(social_network, 'Alice', 'Bob')