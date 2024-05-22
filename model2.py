import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

x = .5
X = .5
p = 1

def f(x, X):
    return p * (3*X+1) * x * (1-x)


fig = plt.figure()
fig.subplots_adjust(left=0.25, bottom=0.25)
fig.suptitle(r'$x_{n+1}=p(3\bar{X}_n+1)x_n(1-x_n)$')

fig2, ax2 = plt.subplots()
fig2.suptitle(r'$x_{n+1}=p(3\bar{X}_n+1)x_n(1-x_n)$')

ax2.set_xlim((-.25, 1.25))
ax2.set_ylim((-.25, 1.25))
ax2.set_xlabel(r'$x_n$')
ax2.set_ylabel(r'$x_{n+1}$')

t = np.linspace(ax2.get_xlim()[0], ax2.get_xlim()[1], 1000)

ax2.plot([ax2.get_xlim()[0], ax2.get_xlim()[1]], [0, 0], lw=.9, c=(0,0,0))
ax2.plot([0, 0], [ax2.get_ylim()[0], ax2.get_ylim()[1]], lw=.9, c=(0,0,0))
curve, = ax2.plot(t, f(t, X))
x_n, = ax2.plot([x, x], [0, f(x, X)])
x_n1, = ax2.plot([f(x, X), f(x, X)], [0, f(f(x, X), X)], c = x_n.get_c(), ls = '--')

ax = fig.add_subplot(111, projection='3d')

def draw_ax():
    ax.cla()
    ax.set_xlim((0, 1))
    ax.set_ylim((0, 1))
    ax.set_zlim((0, 1.25))

    ax.set_xlabel(r'$x_n$')
    ax.set_ylabel(r'$\bar{X}_n$')
    ax.set_zlabel(r'$x_{n+1}$')

    density = 100

    t_x = np.linspace(ax.get_xlim()[0], ax.get_xlim()[1], density)
    t_X = np.linspace(ax.get_ylim()[0], ax.get_ylim()[1], density)
    x_mesh, X_mesh = np.meshgrid(t_x, t_X)


    # Plot the surface
    ax.plot_surface(x_mesh, X_mesh , f(x_mesh, X_mesh), cmap='viridis', alpha =.6)
    ax.plot3D(t_x, X * np.ones(density), f(t_x, X), c='C0')
    ax.plot3D(x * np.ones(density), t_X, f(x, t_X), c='C0')
    ax.scatter(x, X, f(x, X), s=25, c='black', zorder=100)
    ax.plot3D([x, x], [X, X], [0, f(x, X)], c='C1')
    ax.plot3D([f(x, X), f(x, X)], [X, X], [0, f(f(x, X), X)], c='C1', ls = '--')
draw_ax()


p_slider = Slider(
    ax=fig.add_axes([0.1, 0.25, 0.0225, 0.63]),
    label='p',
    valmin=0.1,
    valmax=5,
    valinit=p,
    orientation="vertical"
)

x_slider = Slider(
    ax=fig.add_axes([0.25, 0.1, 0.65, 0.03]),
    label=r'$x_n$',
    valmin=ax.get_xlim()[0],
    valmax= ax.get_xlim()[1],
    valinit=x
)

X_slider = Slider(
    ax=fig.add_axes([0.25, 0.15, 0.65, 0.03]),
    label=r'$\bar{X}_n$',
    valmin=ax.get_xlim()[0],
    valmax= ax.get_xlim()[1],
    valinit=X
)

def update(_):
    global x, X, p
    p = p_slider.val
    x = x_slider.val
    X = X_slider.val
    draw_ax()
    fig.canvas.draw_idle()
    
    curve.set_ydata(f(t, X))
    x_n.set_data([x, x], [0, f(x, X)])  
    x_n1.set_data([f(x, X), f(x, X)], [0, f(f(x, X), X)])
    fig2.canvas.draw_idle()

p_slider.on_changed(update)
x_slider.on_changed(update)
X_slider.on_changed(update)

button = Button(
    fig.add_axes([0.8, 0.025, 0.1, 0.04]), 
    'step', 
    hovercolor='0.975')


def step(_):
    x_slider.set_val(f(x, X))

button.on_clicked(step)

plt.show()
