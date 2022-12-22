import matplotlib.pyplot as plt
import numpy as np

#this is gonna make the complex matrix of starting points
def build_input_matrix(screensize=200, xmin=-2.0, xmax=2.0, ymin=-2.0, ymax=2.0):
    re = np.linspace(xmin, xmax, int((xmax - xmin) * screensize))
    im = np.linspace(ymin, ymax, int((ymax - ymin) * screensize))
    return re[np.newaxis, :] + im[:, np.newaxis] * 1j

def build_iters_matrix(rows, cols):
    return np.zeros((rows, cols))


#this is the thing that counts iterations until divergence
def mandel_iters(c):
    z = 0
    for iters in range(256):
        z = z**2 + c
        #print(z)
        if np.abs(z) >10:
            break
    return iters

#this test thingy is going to test if a value belongs in the set
def test_mandel_iters():
    teal = mandel_iters(1+1j)
    print("it took",teal,"iters")

#this is the main code
print("hello! this program is working as of now")
test_mandel_iters()
c_values = build_input_matrix(1000)
rows, cols = c_values.shape
print(c_values)
color_values = build_iters_matrix(rows, cols)
for row in range(rows):
    for col in range(cols):
        c = c_values[row][col]
        count = mandel_iters(c)
        color_values[row][col] = count
plt.imshow(color_values)
plt.show()

"""
outmx = build_iters_matrix(rows, cols)
for row in range(rows):
    for col in range(cols):
        c = inmx[row][col]
        blue = mandel_iters(c)
        print(blue)
        outmx[]
"""

"""
inmx = build_input_matrix(10)
print(inmx)
rows = inmx.len()
cols = inmx[0].len()
outmx = build_iters_matrix(rows, cols)
print(outmx)
"""