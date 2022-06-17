import enum
import numpy as np

a = np.array([1, 1])
b = np.array([2, 2])

list= np.array([0, 0])
list= np.row_stack((list, a))
list= np.row_stack((list, b))
print(list[1:,:])



# a = np.random.normal(
#         loc=100, scale=1/np.sqrt(2), size=100000)
# b = np.random.normal(
#         loc=100, scale=1/np.sqrt(2), size=100000)

# print(np.var(a))
# print(np.var(b))

# c = np.sqrt(a**2 + b**2)
# print(np.shape(c))
# print(np.var(c))
