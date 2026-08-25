EXPECTED = {
    ('Arad', 'Bucharest'): {
        'bfs': (['Arad', 'Sibiu', 'Fagaras', 'Bucharest'], 35, 5),
        'dfs': (['Arad', 'Sibiu', 'Fagaras', 'Bucharest'], 35, 4),
        'ucs': (['Arad', 'Sibiu', 'Rimnicu Vilcea', 'Pitesti', 'Bucharest'], 30, 13),
        'astar': (['Arad', 'Sibiu', 'Rimnicu Vilcea', 'Pitesti', 'Bucharest'], 30, 5),
        'astar_expanded_ok': [5],
    },
    ('Arad', 'Craiova'): {
        'bfs': (['Arad', 'Sibiu', 'Rimnicu Vilcea', 'Craiova'], 26, 7),
        'dfs': (['Arad', 'Sibiu', 'Fagaras', 'Bucharest', 'Pitesti', 'Craiova'], 48, 7),
        'ucs': (['Arad', 'Sibiu', 'Rimnicu Vilcea', 'Craiova'], 26, 11),
        'astar': (['Arad', 'Sibiu', 'Rimnicu Vilcea', 'Craiova'], 26, 4),
        'astar_expanded_ok': [4, 5],
    },
    ('Neamt', 'Drobeta'): {
        'bfs': (['Neamt', 'Iasi', 'Vaslui', 'Urziceni', 'Bucharest', 'Pitesti', 'Craiova', 'Drobeta'], 44, 12),
        'dfs': (['Neamt', 'Iasi', 'Vaslui', 'Urziceni', 'Bucharest', 'Fagaras', 'Sibiu', 'Arad', 'Timisoara', 'Lugoj', 'Mehadia', 'Drobeta'], 87, 12),
        'ucs': (['Neamt', 'Iasi', 'Vaslui', 'Urziceni', 'Bucharest', 'Pitesti', 'Craiova', 'Drobeta'], 44, 13),
        'astar': (['Neamt', 'Iasi', 'Vaslui', 'Urziceni', 'Bucharest', 'Pitesti', 'Craiova', 'Drobeta'], 44, 9),
        'astar_expanded_ok': [9, 10],
    },
    ('Fagaras', 'Craiova'): {
        'bfs': (['Fagaras', 'Bucharest', 'Pitesti', 'Craiova'], 28, 5),
        'dfs': (['Fagaras', 'Bucharest', 'Pitesti', 'Craiova'], 28, 5),
        'ucs': (['Fagaras', 'Sibiu', 'Rimnicu Vilcea', 'Craiova'], 24, 10),
        'astar': (['Fagaras', 'Sibiu', 'Rimnicu Vilcea', 'Craiova'], 24, 5),
        'astar_expanded_ok': [5],
    },
    ('Craiova', 'Sibiu'): {
        'bfs': (['Craiova', 'Rimnicu Vilcea', 'Sibiu'], 15, 4),
        'dfs': (['Craiova', 'Drobeta', 'Mehadia', 'Lugoj', 'Timisoara', 'Arad', 'Sibiu'], 42, 7),
        'ucs': (['Craiova', 'Rimnicu Vilcea', 'Sibiu'], 15, 8),
        'astar': (['Craiova', 'Rimnicu Vilcea', 'Sibiu'], 15, 3),
        'astar_expanded_ok': [3],
    },
    ('Sibiu', 'Oradea'): {
        'bfs': (['Sibiu', 'Oradea'], 9, 1),
        'dfs': (['Sibiu', 'Arad', 'Zerind', 'Oradea'], 24, 20),
        'ucs': (['Sibiu', 'Oradea'], 9, 4),
        'astar': (['Sibiu', 'Oradea'], 9, 2),
        'astar_expanded_ok': [2],
    },
}
