import math
import pylab
import spicy

from scipy.optimize import linprog

def forwardRate (s, i, j):
    sj = (1+s[j - 1])**j
    si = (1+s[i - 1])**i
    fij = (sj/si)**(1/j-i) - 1
    return fij

spotRates = [5.04, 5.94, 6.36, 7.18, 7.89, 8.39]
f12 = forwardRate (spotRates, 1, 2) + 1
f23 = forwardRate (spotRates, 2, 3) + 1
f34 = forwardRate (spotRates, 3, 4) + 1
f45 = forwardRate (spotRates, 4, 5) + 1
f56 = forwardRate (spotRates, 5, 6) + 1

# Coefficients of the objective function
c = [109, 94.8, 99.5, 93.1, 97.2, 96.3, 92.9, 110, 104, 101, 107, 102, 1, 0, 0, 0, 0, 0]  # Minimize: -x1 - 2x2

# Inequality constraints (A_ub * x <= b_ub)
A_ub = [[10, 7, 8, 6, 7, 6, 5, 10, 8, 6, 10, 7, spotRates[0], -1, 0, 0, 0, 0],[10, 7, 8, 6, 7, 6, 5 , 10, 8, 6, 110, 107, 0, f12, -1, 0, 0, 0],[10, 7, 8, 6, 7, 6, 5,  110, 108, 106,0,0,0, 0, f23, -1, 0, 0],[10, 7, 8, 6, 7, 106, 105,0,0,0,0,0,0, 0, 0, f34, -1, 0],[10, 7, 8, 106, 107,0,0,0,0,0,0,0, 0, 0,0, 0, f45, -1],[110,107,108,0,0,0,0,0,0,0,0,0, 0, 0, 0,0, 0, f56]]
b_ub = [500, 200, 800, 200, 800, 1200]

for i in range(0, len(A_ub)):
    for j in range(0, len(A_ub[i])):
        A_ub[i][j] = -A_ub[i][j]

for i in range(0, len(b_ub)):
    b_ub[i] = -b_ub[i]
    
print(A_ub)

# Bounds for x1 and x2
x_bounds = [(0, None), (0, None), (0, None), (0, None), (0, None), (0, None), (0, None), (0, None), (0, None), (0, None), (0, None), (0, None), (0, None), (0, None), (0, None), (0, None), (0, None), (0, None)]  # x1 >= 0, x2 >= 0

# Solve the linear program
result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=x_bounds, method='highs')

# Display results
if result.success:
    print("Optimal value:", result.fun)
    print("Optimal solution:", result.x)
else:
    print("Optimization failed:", result.message)