import enum
import numpy as np

a = np.array([0, 1, 2, 3])
b = a < 2
print(b.all())




# a = np.random.normal(
#         loc=100, scale=1/np.sqrt(2), size=100000)
# b = np.random.normal(
#         loc=100, scale=1/np.sqrt(2), size=100000)

# print(np.var(a))
# print(np.var(b))

# c = np.sqrt(a**2 + b**2)
# print(np.shape(c))
# print(np.var(c))
