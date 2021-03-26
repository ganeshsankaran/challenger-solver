from z3 import *

A = [
    [12],
    [0, 0, 0, 4, 23],
    [0, 1, 0, 0, 11],
    [6, 0, 0, 0, 21],
    [0, 0, 2, 0, 13],
    [9, 20, 22, 17, 12]
]

n = 1
rows = len(A) - 1
cols = len(A[1]) - 1

smt = ''
solver = Solver()

# Replace 0s with variable numbers
# -i -> variable x_i
for r in range(1, rows):
    for c in range(cols):
        if A[r][c] == 0:
            A[r][c] = -1 * n
            n += 1

# Declarations for x_i, where i in [1, n]
smt = ''
for i in range(1, n):
    smt += '(declare-const x{} Int)\n'.format(i)

# Assertions on x's
for i in range(1, n):
    smt += '(assert (>= x{} 1))\n'.format(i)
    smt += '(assert (<= x{} 9))\n'.format(i)

# Assertions on row sums
for r in range(1, rows):
    lhs = ' '.join([str(c) for c in A[r][:-1]]) # addends
    lhs = lhs.replace('-', 'x')
    rhs = A[r][-1] # sum
    
    smt += '(assert (= (+ {}) {}))\n'.format(lhs, rhs)

# Assertions on column sums
for c in range(cols):
    lhs = ' '.join([str(A[r][c]) for r in range(1, len(A) - 1)]) # addends
    lhs = lhs.replace('-', 'x')
    rhs = A[-1][c] # sum

    smt += '(assert (= (+ {}) {}))\n'.format(lhs, rhs)

# Assertions on diagonal sums
lhs = ' '.join([str(A[r][r - 1]) for r in range(1, rows)]) # addends (main diagonal)
lhs = lhs.replace('-', 'x')
rhs = A[-1][-1] # sum

smt += '(assert (= (+ {}) {}))\n'.format(lhs, rhs)

lhs = ' '.join([str(A[r][cols - r]) for r in range(1, len(A) - 1)]) # addends (main diagonal)
lhs = lhs.replace('-', 'x')
rhs = A[0][-1] # sum

smt += '(assert (= (+ {}) {}))\n'.format(lhs, rhs)

# Solve the puzzle using Z3
solver.add(parse_smt2_string(smt))

if solver.check() == unsat:
    print('Unable to solve Challenger!')
    exit(1)

model = solver.model()

# Replace variables with solutions (from model)
for r in range(1, len(A) - 1):
    for c in range(len(A[1])):
        if A[r][c] < 0:
            x = Int('x{}'.format(-1 * A[r][c]))
            A[r][c] = model[x]

# Print the completed puzzle
for r in range(1, len(A) - 1):
    print(A[r][:-1])