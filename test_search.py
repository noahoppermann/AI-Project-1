"""Public tests. The autograder also runs a hidden set on other city pairs."""
import pytest

import search
from romania_map import GRAPH

from _expected_visible import EXPECTED

ALGOS = ["bfs", "dfs", "ucs", "astar"]
OPTIMAL = ["ucs", "astar"]


def run(alg, start, goal):
    return getattr(search, alg)(start, goal)


def assert_valid_path(path, start, goal):
    assert path is not None, "expected a path, got None"
    assert path[0] == start, f"path must begin at {start}, began at {path[0]}"
    assert path[-1] == goal, f"path must end at {goal}, ended at {path[-1]}"
    assert len(set(path)) == len(path), f"path revisits a city: {path}"
    for a, b in zip(path, path[1:]):
        assert b in GRAPH[a], f"no road from {a} to {b}"


def declared_cost(path):
    return sum(GRAPH[a][b] for a, b in zip(path, path[1:]))


# --------------------------------------------------------------- structure
@pytest.mark.parametrize("alg", ALGOS)
def test_returns_triple(alg):
    result = run(alg, "Arad", "Bucharest")
    assert isinstance(result, tuple) and len(result) == 3, (
        f"{alg} must return a 3-tuple (path, cost, expanded)")


@pytest.mark.parametrize("alg", ALGOS)
def test_start_equals_goal(alg):
    path, cost, expanded = run(alg, "Arad", "Arad")
    assert path == ["Arad"]
    assert cost == 0
    assert expanded == 0


@pytest.mark.parametrize("alg", ALGOS)
def test_unknown_city(alg):
    assert run(alg, "Arad", "Atlantis") == (None, None, 0)


# ------------------------------------------------------------- distances
def test_distance_functions():
    """The three distance helpers must agree with their definitions."""
    import numpy as np
    a = np.array([0.0, 0.0])
    b = np.array([3.0, 4.0])
    assert search.euclidean(a, b) == pytest.approx(5.0)
    assert search.manhattan(a, b) == pytest.approx(7.0)
    assert search.chebyshev(a, b) == pytest.approx(4.0)
    assert search.euclidean(a, a) == pytest.approx(0.0)


def test_coords_of_returns_array():
    import numpy as np
    v = search.coords_of("Arad")
    assert isinstance(v, np.ndarray), "coords_of must return a numpy array"
    assert v.shape == (2,), "coords_of must return a length-2 array"
    assert tuple(float(x) for x in v) == (0.0, 12.0)


def test_heuristic_zero_at_goal():
    for city in ("Arad", "Bucharest", "Neamt"):
        assert search.heuristic(city, city) == pytest.approx(0.0)


# ---------------------------------------------------- heuristic is wired in
def test_astar_actually_calls_heuristic():
    """Swap in a zero heuristic; A* must then behave exactly like UCS."""
    original = search.heuristic
    try:
        search.heuristic = lambda city, goal: 0.0
        for start, goal in sorted(EXPECTED):
            assert run("astar", start, goal) == run("ucs", start, goal), (
                "with h = 0, astar must reduce to ucs -- make sure astar "
                "calls heuristic() rather than inlining the formula")
    finally:
        search.heuristic = original


# ------------------------------------------------------------ path & cost
@pytest.mark.parametrize("start,goal", sorted(EXPECTED))
@pytest.mark.parametrize("alg", ALGOS)
def test_cost_is_integral(alg, start, goal):
    """Costs are sums of integer road costs. A fractional cost means a
    heuristic value leaked into your path cost."""
    _, cost, _ = run(alg, start, goal)
    assert float(cost).is_integer(), (
        f"{alg} returned a non-integer cost {cost!r} -- did you add the "
        "heuristic into the path cost instead of keeping them separate?")


@pytest.mark.parametrize("start,goal", sorted(EXPECTED))
@pytest.mark.parametrize("alg", ALGOS)
def test_path_matches(alg, start, goal):
    path, cost, _ = run(alg, start, goal)
    assert_valid_path(path, start, goal)
    assert cost == declared_cost(path), "returned cost disagrees with returned path"
    assert path == EXPECTED[(start, goal)][alg][0]
    assert cost == EXPECTED[(start, goal)][alg][1]


@pytest.mark.parametrize("start,goal", sorted(EXPECTED))
@pytest.mark.parametrize("alg", OPTIMAL)
def test_optimal_cost(alg, start, goal):
    _, cost, _ = run(alg, start, goal)
    best = min(EXPECTED[(start, goal)][a][1] for a in ALGOS)
    assert cost == best, f"{alg} must return an optimal-cost path"


@pytest.mark.parametrize("start,goal", sorted(EXPECTED))
def test_astar_path_is_optimal(start, goal):
    """An inadmissible heuristic can return a cheap-looking but suboptimal
    path. This is where a poor choice of heuristic shows up."""
    path, cost, _ = run("astar", start, goal)
    assert_valid_path(path, start, goal)
    assert cost == EXPECTED[(start, goal)]["ucs"][1], (
        "A* returned a suboptimal path. If your heuristic can overestimate "
        "the true remaining cost, A* loses its optimality guarantee.")


# ------------------------------------------------------------- expansions
@pytest.mark.parametrize("start,goal", sorted(EXPECTED))
@pytest.mark.parametrize("alg", ["bfs", "ucs"])
def test_expansion_count(alg, start, goal):
    """BFS and UCS expansions involve no heuristic, so these are exact."""
    _, _, expanded = run(alg, start, goal)
    assert expanded == EXPECTED[(start, goal)][alg][2], (
        f"{alg} expanded {expanded} nodes, expected "
        f"{EXPECTED[(start, goal)][alg][2]}; see the handout for how to count")


@pytest.mark.parametrize("start,goal", sorted(EXPECTED))
def test_astar_expansion_count(start, goal):
    """A* expansions depend on which admissible heuristic you chose, so any
    permitted admissible choice is accepted -- but the count must match one
    of them exactly, not merely be small."""
    _, _, expanded = run("astar", start, goal)
    allowed = EXPECTED[(start, goal)]["astar_expanded_ok"]
    assert expanded in allowed, (
        f"A* expanded {expanded} nodes on {start} -> {goal}. An admissible "
        f"heuristic on this map gives one of {allowed}. Check your goal test "
        "placement and that you skip nodes already expanded.")


@pytest.mark.parametrize("start,goal", sorted(EXPECTED))
def test_astar_beats_ucs(start, goal):
    """Any admissible heuristic must beat UCS on these pairs."""
    _, _, e_ucs = run("ucs", start, goal)
    _, _, e_ast = run("astar", start, goal)
    assert e_ast < e_ucs, (
        f"A* expanded {e_ast} nodes, UCS expanded {e_ucs}. A* must expand "
        "strictly fewer -- is your heuristic actually being used?")


@pytest.mark.parametrize("start,goal", sorted(EXPECTED))
def test_dfs_is_not_bfs(start, goal):
    """DFS must follow the stack discipline, not rediscover BFS."""
    assert run("dfs", start, goal)[0] == EXPECTED[(start, goal)]["dfs"][0]
