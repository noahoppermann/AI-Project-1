"""
Uninformed and informed search on the course map.

MY HEURISTIC CHOICE: ______________________
Justification (2-3 sentences): is it admissible on this map? is it consistent?
why?


Implement the functions below. Do not rename them or change their signatures.
Do not modify romania_map.py.

Each search returns a 3-tuple:

    (path, cost, expanded)

    path      list of city names from start to goal, inclusive.
              None if no path exists.
    cost      total cost of that path, an integer. None if no path exists.
    expanded  number of nodes your search expanded. See the handout for the
              exact counting rule -- this is graded.

If no path exists, a search returns (None, None, 0).

Run the public tests with:   python run_tests.py
"""

import heapq
from collections import deque

import numpy as np

from romania_map import GRAPH, COORDS


# --------------------------------------------------------------- distances
def coords_of(city):
    """Return a city's (x, y) from COORDS as a length-2 numpy array of floats."""
    raise NotImplementedError


def euclidean(a, b):
    """Euclidean (L2) distance between two length-2 numpy arrays.

    Write the formula yourself with numpy operations. Do not call
    numpy.linalg.norm, math.dist, or scipy.
    """
    raise NotImplementedError


def manhattan(a, b):
    """Manhattan (L1) distance between two length-2 numpy arrays."""
    raise NotImplementedError


def chebyshev(a, b):
    """Chebyshev (L-infinity) distance between two length-2 numpy arrays."""
    raise NotImplementedError


def heuristic(city, goal):
    """Estimated distance from `city` to `goal`, as a float.

    Call coords_of() for each city, then return the result of ONE of
    euclidean / manhattan / chebyshev.

    YOU CHOOSE which one. Read the handout first -- one of the three can
    overestimate the true remaining cost on this map, which breaks A*'s
    optimality guarantee.

    Must return 0.0 when city == goal.
    Your astar() must CALL this function -- do not inline the formula.
    """
    raise NotImplementedError


# ------------------------------------------------------------------ search
def bfs(start, goal):
    """Breadth-first search. Goal-test children as they are GENERATED."""
    raise NotImplementedError


def dfs(start, goal):
    """Depth-first graph search. Never expand a city twice.

    Push successors in reverse alphabetical order so the alphabetically
    first neighbour is popped first.
    """
    raise NotImplementedError


def ucs(start, goal):
    """Uniform-cost search. Goal-test nodes as they are EXPANDED."""
    raise NotImplementedError


def astar(start, goal):
    """A* search using heuristic(city, goal)."""
    raise NotImplementedError
