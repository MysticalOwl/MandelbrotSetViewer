import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import multiprocessing as mp

# these are global variables
busy = False

xmin = -2.0
xmax = 0.5
ymin = -1.2
ymax = 1.2

px = 800
max_iters = 50

fig, ax = plt.subplots()

cmapy = "inferno"

# this is going to make the complex matrix of starting points
def build_input_matrix(screensize=200, xmin=-2.0, xmax=2.0, ymin=-2.0, ymax=2.0):
    re = np.linspace(xmin, xmax, screensize)
    im = np.linspace(ymin, ymax, screensize)
    return re[np.newaxis, :] + im[:, np.newaxis] * 1j


def build_iters_matrix(rows, cols):
    return np.zeros((rows, cols))


def draw_mandy(xmin, xmax, ymin, ymax):
    print("drawin mandy")
    global busy, ax
    busy = True
    c_values = build_input_matrix(px, xmin, xmax, ymin, ymax)
    rows, cols = c_values.shape
    color_values = build_iters_matrix(rows, cols)
    for row in range(rows):
        c_vals = c_values[row][:]
    ax.clear()
    print("clearing")
    ax.imshow(color_values, extent=[xmin, xmax, ymin, ymax], aspect="auto", cmap=mpl.colormaps[cmapy])
    print("xmin=", xmin, " xmax=", xmax, " ymin=", ymin, " ymax=", ymax)
    print(color_values)
    print(c_values)
    ax.figure.canvas.draw()
    busy = False
    connect_callbacks()
    print("connected callbacks")


# this is the thing that counts iterations until divergence
def mandel_iters(c):
    iters = 0
    z = 0
    oldabsz = 0
    k10 = 0
    for iters in range(max_iters):
        z = z**2 + c
        newabsz = np.abs(z)
        if newabsz > 10:
            m = (oldabsz - newabsz) / -1.0
            b = oldabsz - m*(iters-1)
            k10 = (10-b) / m
            break
    if iters >= (max_iters-1):
        color = 0
    else:
        color = k10
    return color


def change_xlims(event_ax):
    print("changing xlims")
    global busy, xmin, xmax, ax
    if busy:
        return
    xmin, xmax = event_ax.get_xlim()


def change_ylims(event_ax):
    print("changing ylims")
    global busy, xmin, xmax, ymin, ymax
    if busy:
        return
    ymin, ymax = event_ax.get_ylim()
    draw_mandy(xmin, xmax, ymin, ymax)


def connect_callbacks():
    global ax
    ax.callbacks.connect('xlim_changed', change_xlims)
    ax.callbacks.connect('ylim_changed', change_ylims)


# this is the main code
ax.set_autoscale_on(False)
draw_mandy(xmin, xmax, ymin, ymax)
connect_callbacks()
plt.show()
