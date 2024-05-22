import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
import numpy as np

x = .5
p = 1

def f(x):
    return p * x * (1-x)

fig, ax = plt.subplots()
fig.suptitle(r'$x_{n+1}=p x_n(1-x_n)$')

ax.set_xlim((-.25, 1.25))
ax.set_ylim((-.25, 1.25))
ax.set_xlabel(r'$x_n$')
ax.set_ylabel(r'$x_{n+1}$')

t = np.linspace(ax.get_xlim()[0], ax.get_xlim()[1], 1000)

ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [0, 0], lw=.9, c=(0,0,0))
ax.plot([0, 0], [ax.get_ylim()[0], ax.get_ylim()[1]], lw=.9, c=(0,0,0))
curve, = ax.plot(t, f(t))
x_n, = ax.plot([x, x], [0, f(x)])
x_n1, = ax.plot([f(x), f(x)], [0, f(f(x))], c = x_n.get_c(), ls = '--')



fig.subplots_adjust(left=0.25, bottom=0.25)

# Make a horizontal slider to control the frequency.

p_slider = Slider(
    ax=fig.add_axes([0.1, 0.25, 0.0225, 0.63]),
    label='p',
    valmin=0.1,
    valmax=5,
    valinit=1,
    orientation="vertical"
)
x_slider = Slider(
    ax=fig.add_axes([0.25, 0.1, 0.65, 0.03]),
    label=r'$x_n$',
    valmin=ax.get_xlim()[0],
    valmax= ax.get_xlim()[1],
    valinit=x
)

button = Button(
    fig.add_axes([0.8, 0.025, 0.1, 0.04]), 
    'step', 
    hovercolor='0.975')


def update(_):
    global x, p
    # p_slider change
    p = p_slider.val
    curve.set_ydata(f(t))
    
    # x_slider change
    x = x_slider.val
    x_n.set_data([x, x], [0, f(x)])
    
    x_n1.set_data([f(x), f(x)], [0, f(f(x))])
    
    fig.canvas.draw_idle()

p_slider.on_changed(update)
x_slider.on_changed(update)

def step(_):
    x_slider.set_val(f(x))
    
button.on_clicked(step)


plt.show()