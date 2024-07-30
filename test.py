import numpy as np

# Coefficient matrix
A = np.array([[100, 10, 10], [3, 4, 4]])

# Constant vector
b = np.array([972, 12])

# Solving for x using least squares method
x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)

print("Solution:")
print("a:", x[0])
print("b:", x[1])
print("c:", x[2])
print("Residuals:", residuals)
