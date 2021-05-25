
# HLF 2D ("Hidden Linear Function, 2-Dimensional")
# Examples from Google Cirq tutorial
# https://quantumai.google/cirq/tutorials/hidden_linear_function

import numpy as np
import cirq


class HiddenLinearFunctionProblem:
    """Instance of Hidden Linear Function problem.

    The problem is defined by matrix A and vector b, which are
    the coefficients of quadratic form, in which linear function
    is "hidden".
    """

    def __init__(self, A, b):
        self.n = A.shape[0]
        assert A.shape == (self.n, self.n)
        assert b.shape == (self.n, )
        for i in range(self.n):
            for j in range(i+1):
                assert A[i][j] == 0, 'A[i][j] can be 1 only if i<j'

        self.A = A
        self.b = b

    def q(self, x):
        """Action of quadratic form on binary vector (modulo 4).

        Corresponds to `q(x)` in problem definition.
        """
        assert x.shape == (self.n, )
        return (2 * (x @ self.A @ x) + (self.b @ x)) % 4

    def bruteforce_solve(self):
        """Calculates, by definition, all vectors `z` which are solutions to the problem."""

        # All binary vectors of length `n`.
        all_vectors = [np.array([(m >> i) % 2 for i in range(self.n)])
                       for m in range(2**self.n)]

        def vector_in_L(x):
            for y in all_vectors:
                if self.q((x + y) % 2) != (self.q(x) + self.q(y)) % 4:
                    return False
            return True

        # L is subspace to which we restrict domain of quadratic form.
        # Corresponds to `L_q` in the problem definition.
        self.L = [x for x in all_vectors if vector_in_L(x)]

        # All vectors `z` which are solutions to the problem.
        self.all_zs = [z for z in all_vectors if self.is_z(z)]

    def is_z(self, z):
        """Checks by definition, whether given vector `z` is solution to this problem."""
        assert z.shape == (self.n, )
        assert self.L is not None
        for x in self.L:
            if self.q(x) != 2 * ((z @ x) % 2):
                return False
        return True

# end class, functions here


def random_problem(n, seed=None):
    """Generates instance of the problem with given `n`.

    Args:
        n: dimension of the problem.
    """
    if seed is not None:
        np.random.seed(seed)
    A = np.random.randint(0, 2, size=(n, n))
    for i in range(n):
        for j in range(i+1):
            A[i][j] = 0
    b = np.random.randint(0, 2, size=n)
    problem = HiddenLinearFunctionProblem(A, b)
    return problem


def find_interesting_problem(n, min_L_size):
    """Generates "interesting" instance of the problem.

    Returns instance of problem with given `n`, such that size of 
    subspace `L_q` is at least `min_L_size`.

    Args:
        n: dimension of the problem.
        min_L_size: minimal cardinality of subspace L.
    """
    for _ in range(1000):
        problem = random_problem(n)
        problem.bruteforce_solve()
        if len(problem.L) >= min_L_size and not np.max(problem.A) == 0:
            return problem
    return None


# quantum solution starts here
def edge_coloring(A):
    """Solves edge coloring problem.

    Args:
        A: adjacency matrix of a graph.

    Returns list of lists of edges, such as edges in each list 
    do not have common vertex. 
    Tries to minimize length of this list.
    """
    A = np.copy(A)
    n = A.shape[0]
    ans = []
    while np.max(A) != 0:
        edges_group = []
        used = np.zeros(n, dtype=np.bool)
        for i in range(n):
            for j in range(n):
                if A[i][j] == 1 and not used[i] and not used[j]:
                    edges_group.append((i, j))
                    A[i][j] = 0
                    used[i] = used[j] = True
        ans.append(edges_group)
    return ans


def generate_circuit_for_problem(problem):
    """Generates `cirq.Circuit` which solves instance of Hidden Linear Function problem."""

    qubits = cirq.LineQubit.range(problem.n)
    circuit = cirq.Circuit()

    # Hadamard gates at the beginning (creating equal superposition of all states).
    circuit += cirq.Moment([cirq.H(q) for q in qubits])

    # Controlled-Z gates encoding the matrix A.
    for layer in edge_coloring(problem.A):
        for i, j in layer:
            circuit += cirq.CZ(qubits[i], qubits[j])

    # S gates encoding the vector b.
    circuit += cirq.Moment([cirq.S.on(qubits[i])
                            for i in range(problem.n) if problem.b[i] == 1])

    # Hadamard gates at the end.
    circuit += cirq.Moment([cirq.H(q) for q in qubits])

    # Measurements.
    circuit += cirq.Moment([cirq.measure(qubits[i], key=str(i))
                            for i in range(problem.n)])

    return circuit


def solve_problem(problem, print_circuit=False):
    """Solves instance of Hidden Linear Function problem.

    Builds quantum circuit for given problem and simulates
    it with the Clifford simulator. 

    Returns measurement result as binary vector, which is
    guaranteed to be a solution to given problem.
    """
    circuit = generate_circuit_for_problem(problem)

    if print_circuit:
        print(circuit)

    sim = cirq.CliffordSimulator()
    result = sim.simulate(circuit)
    z = np.array([result.measurements[str(i)][0] for i in range(problem.n)])
    return z


def test1():
    problem = find_interesting_problem(10, 4)
    print("Size of subspace L: %d" % len(problem.L))
    print("Number of solutions: %d" % len(problem.all_zs))


# these variables are used in multiple tests (brute force and quantum)
A = np.array([[0, 1, 1, 0, 0, 1, 0, 0, 1, 1],
              [0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
              [0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
              [0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
              [0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
b = np.array([0, 0, 0, 0, 1, 1, 1, 0, 0, 1])
problem_10_64 = HiddenLinearFunctionProblem(A, b)


def test2():
    # solve, using brute force
    problem_10_64.bruteforce_solve()
    print("Size of subspace L: %d" % len(problem_10_64.L))
    print("Number of solutions: %d" % len(problem_10_64.all_zs))


def test3():
    # solve, using quantum computer simulator
    solve_problem(problem_10_64, print_circuit=True)

# there are additional tests in the original google source
