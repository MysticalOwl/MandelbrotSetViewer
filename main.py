import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from matplotlib.widgets import TextBox
from matplotlib.widgets import Button


# these are global variables
busy = False

xmin = -2.0
xmax = 0.5
ymin = -1.2
ymax = 1.2

px = 50

fig, ax = plt.subplots(figsize=(9, 10))
plt.subplots_adjust(bottom=0.3)

cmapy = "inferno"

xminbox_ax = plt.axes([0.1, 0.2 , 0.2, 0.04])
xminbox = TextBox(xminbox_ax, 'xmin', initial=xmin)
xmaxbox_ax = plt.axes([0.35, 0.2, 0.2, 0.04])
xmaxbox = TextBox(xmaxbox_ax, 'xmax', initial=xmax)
yminbox_ax = plt.axes([0.1, 0.125, 0.2, 0.04])
yminbox = TextBox(yminbox_ax, 'ymin', initial=ymin)
ymaxbox_ax = plt.axes([0.35, 0.125, 0.2, 0.04])
ymaxbox = TextBox(ymaxbox_ax, 'ymax', initial=ymax)
axbtn = plt.axes([0.6, 0.125, 0.2, 0.115])
button = Button(axbtn, 'go')


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
        for col in range(cols):
            c = c_values[row][col]
            count = mandel_iters(c)
            color_values[row][col] = count
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
    for iters in range(100):
        z = z**2 + c
        newabsz = np.abs(z)
        if newabsz > 10:
            m = (oldabsz - newabsz) / -1.0
            b = oldabsz - m*(iters-1)
            k10 = (10-b) / m
            break
    if iters == 100:
        return 0
    else:
        return k10


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
    xminbox.set_val(str(xmin))
    xmaxbox.set_val(str(xmax))
    yminbox.set_val(str(ymin))
    ymaxbox.set_val(str(ymax))
    draw_mandy(xmin, xmax, ymin, ymax)


def connect_callbacks():
    global ax
    ax.callbacks.connect('xlim_changed', change_xlims)
    ax.callbacks.connect('ylim_changed', change_ylims)


def onclick(event):
    xmin = eval(xminbox.text)
    xmax = eval(xmaxbox.text)
    ymin = eval(yminbox.text)
    ymax = eval(ymaxbox.text)
    draw_mandy(xmin, xmax, ymin, ymax)


# this is the main code
ax.set_autoscale_on(False)
button.on_clicked(onclick)
draw_mandy(xmin, xmax, ymin, ymax)
connect_callbacks()
plt.show()
