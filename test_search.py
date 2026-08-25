"""Public tests. The autograder also runs a hidden set on other city pairs."""
import pytest

import search
from romania_map import GRAPH

from _expected_visible import EXPECTED

# Every test gets its own 10-second limit, so a submission that loses a
# visited-set check fails one category instead of hanging the whole suite.
pytestmark = pytest.mark.timeout(10)

ALGOS = ["bfs", "dfs", "ucs", "astar"]
PAIRS = sorted(EXPECTED)


# --------------------------------------------------------------- helpers
class Collector:
    """Gather every failure in a category, then report them together.

    One reported test per category, but the message still names exactly which
    city pairs failed and why, so a student is never left guessing.
    """

    def __init__(self):
        self.problems = []

    def check(self, condition, message):
        if not condition:
            self.problems.append(message)

    def compare(self, label, got, want):
        if got != want:
            self.problems.append(f"{label}: got {got!r}, expected {want!r}")

    def report(self):
        if not self.problems:
            return
        shown = self.problems[:6]
        more = len(self.problems) - len(shown)
        lines = [f"{len(self.problems)} problem(s) found:"]
        lines += [f"  - {p}" for p in shown]
        if more:
            lines.append(f"  ... and {more} more of the same kind")
        raise AssertionError("\n".join(lines))


def run(alg, start, goal):
    return getattr(search, alg)(start, goal)


def path_problems(c, alg, start, goal, path, cost):
    where = f"{alg} {start} -> {goal}"
    if path is None:
        c.check(False, f"{where}: returned None, expected a path")
        return
    if path[0] != start or path[-1] != goal:
        c.check(False, f"{where}: path runs {path[0]} -> {path[-1]}")
        return
    if len(set(path)) != len(path):
        c.check(False, f"{where}: path revisits a city")
        return
    for a, b in zip(path, path[1:]):
        if b not in GRAPH[a]:
            c.check(False, f"{where}: no road from {a} to {b}")
            return
    walked = sum(GRAPH[a][b] for a, b in zip(path, path[1:]))
    c.check(cost == walked, f"{where}: cost {cost} disagrees with its own path ({walked})")
    c.check(float(cost).is_integer(),
            f"{where}: cost {cost!r} is not a whole number - did the heuristic "
            "leak into the path cost?")
    c.compare(f"{where} path", path, EXPECTED[(start, goal)][alg][0])
    c.compare(f"{where} cost", cost, EXPECTED[(start, goal)][alg][1])


def check_algorithm(alg, expansions=True):
    c = Collector()
    for start, goal in PAIRS:
        result = run(alg, start, goal)
        if not (isinstance(result, tuple) and len(result) == 3):
            c.check(False, f"{alg} {start} -> {goal}: did not return a 3-tuple")
            continue
        path, cost, expanded = result
        path_problems(c, alg, start, goal, path, cost)
        if expansions:
            c.compare(f"{alg} {start} -> {goal} expansions",
                      expanded, EXPECTED[(start, goal)][alg][2])
    return c


# ------------------------------------------------- 1. signatures and edges
def test_signatures_and_edge_cases():
    c = Collector()
    for alg in ALGOS:
        result = run(alg, "Arad", "Bucharest")
        c.check(isinstance(result, tuple) and len(result) == 3,
                f"{alg}: must return a 3-tuple (path, cost, expanded)")
        c.compare(f"{alg}(Arad, Arad)", run(alg, "Arad", "Arad"), (["Arad"], 0, 0))
        c.compare(f"{alg}(Arad, Atlantis)", run(alg, "Arad", "Atlantis"), (None, None, 0))
    c.report()


# --------------------------------------------------- 2. distance functions
def test_distance_functions():
    import numpy as np
    c = Collector()
    a = np.array([0.0, 0.0])
    b = np.array([3.0, 4.0])
    c.check(abs(search.euclidean(a, b) - 5.0) < 1e-9,
            f"euclidean((0,0),(3,4)) = {search.euclidean(a, b)!r}, expected 5.0")
    c.check(abs(search.manhattan(a, b) - 7.0) < 1e-9,
            f"manhattan((0,0),(3,4)) = {search.manhattan(a, b)!r}, expected 7.0")
    c.check(abs(search.chebyshev(a, b) - 4.0) < 1e-9,
            f"chebyshev((0,0),(3,4)) = {search.chebyshev(a, b)!r}, expected 4.0")
    c.check(abs(search.euclidean(a, a)) < 1e-9, "euclidean of a point with itself must be 0")

    v = search.coords_of("Arad")
    c.check(isinstance(v, np.ndarray), "coords_of must return a numpy array")
    c.check(getattr(v, "shape", None) == (2,), "coords_of must return a length-2 array")
    c.check(tuple(float(x) for x in v) == (0.0, 12.0),
            f"coords_of('Arad') = {tuple(v)!r}, expected (0.0, 12.0)")

    for city in ("Arad", "Bucharest", "Neamt"):
        h = search.heuristic(city, city)
        c.check(abs(h) < 1e-9, f"heuristic({city}, {city}) = {h!r}, must be 0.0")
    c.report()


# ------------------------------------------------------ 3, 4, 5. BFS/DFS/UCS
def test_bfs():
    check_algorithm("bfs").report()


def test_dfs():
    c = check_algorithm("dfs", expansions=False)
    c.report()


def test_ucs():
    c = check_algorithm("ucs")
    for start, goal in PAIRS:
        _, cost, _ = run("ucs", start, goal)
        best = min(EXPECTED[(start, goal)][a][1] for a in ALGOS)
        c.check(cost == best, f"ucs {start} -> {goal}: cost {cost} is not optimal ({best})")
    c.report()


# --------------------------------------------------- 6. A* path and cost
def test_astar_paths_are_optimal():
    c = check_algorithm("astar", expansions=False)
    for start, goal in PAIRS:
        _, cost, _ = run("astar", start, goal)
        want = EXPECTED[(start, goal)]["ucs"][1]
        c.check(cost == want,
                f"astar {start} -> {goal}: cost {cost}, optimal is {want}. An "
                "inadmissible heuristic loses A*'s optimality guarantee.")
    c.report()


# ----------------------------------------------------- 7. A* expansions
def test_astar_expansion_counts():
    c = Collector()
    for start, goal in PAIRS:
        _, _, expanded = run("astar", start, goal)
        allowed = EXPECTED[(start, goal)]["astar_expanded_ok"]
        c.check(expanded in allowed,
                f"astar {start} -> {goal}: expanded {expanded}, an admissible "
                f"heuristic gives one of {allowed}")
    c.report()


# ------------------------------------------------ 8. A* uses the heuristic
def test_astar_uses_heuristic():
    c = Collector()
    for start, goal in PAIRS:
        _, _, e_ast = run("astar", start, goal)
        _, _, e_ucs = run("ucs", start, goal)
        c.check(e_ast < e_ucs,
                f"astar {start} -> {goal}: expanded {e_ast}, ucs expanded "
                f"{e_ucs}; A* must expand strictly fewer")

    original = search.heuristic
    try:
        search.heuristic = lambda city, goal: 0.0
        for start, goal in PAIRS:
            c.compare(f"with h=0, astar {start} -> {goal} should equal ucs",
                      run("astar", start, goal), run("ucs", start, goal))
    finally:
        search.heuristic = original
    c.report()
