"""Course map for the search assignment.

Cities carry Romanian names but the geometry is synthetic. Edge costs are
ceil(euclidean distance) between the integer coordinates below, so no road is
ever cheaper than the straight-line gap it spans. Do not modify this file.
"""

COORDS = {
    'Arad': (0, 12),
    'Bucharest': (26, 8),
    'Craiova': (20, 4),
    'Drobeta': (16, 2),
    'Eforie': (36, 6),
    'Fagaras': (17, 19),
    'Giurgiu': (26, 2),
    'Hirsova': (34, 12),
    'Iasi': (28, 24),
    'Lugoj': (8, 2),
    'Mehadia': (12, 0),
    'Neamt': (24, 26),
    'Oradea': (6, 22),
    'Pitesti': (20, 10),
    'Rimnicu Vilcea': (14, 10),
    'Sibiu': (10, 14),
    'Timisoara': (2, 4),
    'Urziceni': (30, 12),
    'Vaslui': (32, 20),
    'Zerind': (2, 18),
}

GRAPH = {
    'Arad': {'Sibiu': 11, 'Timisoara': 9, 'Zerind': 7},
    'Bucharest': {'Fagaras': 15, 'Giurgiu': 6, 'Pitesti': 7, 'Urziceni': 6},
    'Craiova': {'Drobeta': 5, 'Pitesti': 6, 'Rimnicu Vilcea': 9},
    'Drobeta': {'Craiova': 5, 'Mehadia': 5},
    'Eforie': {'Hirsova': 7},
    'Fagaras': {'Bucharest': 15, 'Sibiu': 9},
    'Giurgiu': {'Bucharest': 6},
    'Hirsova': {'Eforie': 7, 'Urziceni': 4},
    'Iasi': {'Neamt': 5, 'Vaslui': 6},
    'Lugoj': {'Mehadia': 5, 'Timisoara': 7},
    'Mehadia': {'Drobeta': 5, 'Lugoj': 5},
    'Neamt': {'Iasi': 5},
    'Oradea': {'Sibiu': 9, 'Zerind': 6},
    'Pitesti': {'Bucharest': 7, 'Craiova': 6, 'Rimnicu Vilcea': 6},
    'Rimnicu Vilcea': {'Craiova': 9, 'Pitesti': 6, 'Sibiu': 6},
    'Sibiu': {'Arad': 11, 'Fagaras': 9, 'Oradea': 9, 'Rimnicu Vilcea': 6},
    'Timisoara': {'Arad': 9, 'Lugoj': 7},
    'Urziceni': {'Bucharest': 6, 'Hirsova': 4, 'Vaslui': 9},
    'Vaslui': {'Iasi': 6, 'Urziceni': 9},
    'Zerind': {'Arad': 7, 'Oradea': 6},
}
