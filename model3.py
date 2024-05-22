import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

x1 = .5
x2 = .5
p = 1

def f1(x1, x2):
    return p * (3 * x2 + 1) * x1 * (1 - x1)

def f2(x1, x2):
    return p * (3 * x1 + 1) * x2 * (1 - x2)

next_x1 = f1(x1, x2)
next_x2 = f2(x1, x2)


# Create a figure and three subplots
fig = plt.figure(figsize=(9, 5))

ax1 = fig.add_subplot(121, projection='3d')
ax2 = fig.add_subplot(122, projection='3d')

fig.subplots_adjust(left=.1, bottom=.25)

# Remove x-axis ticks from the top plots
ax1.tick_params(axis='x', which='both', bottom=False, top=False)
ax2.tick_params(axis='x', which='both', bottom=False, top=False)


# Adjust the size of the plots
# ax1.set_position([0.1, 0.55, 0.4, 0.35])  # Top left
# ax2.set_position([0.55, 0.55, 0.4, 0.35])  # Top right

density = 100
lim = (0, 1)

t = np.linspace(lim[0], lim[1], density)
x1_mesh, x2_mesh = np.meshgrid(t, t)

def draw_axes():
    ax1.cla()
    ax2.cla()

    ax1.set_title(r'$x^1_{n+1}=p(3x^2_n+1)x^1_n(1-x^1_n)$')
    ax2.set_title(r'$x^2_{n+1}=p(3x^1_n+1)x^2_n(1-x^2_n)$')

    ax1.set_xlim(lim)
    ax1.set_ylim(lim)
    ax1.set_zlim((0, 1.25))

    ax2.set_xlim(lim)
    ax2.set_ylim(lim)
    ax2.set_zlim((0, 1.25))

    ax1.set_xlabel(r'$x^1_n$')
    ax1.set_ylabel(r'$x^2_n$')
    ax1.set_zlabel(r'$x^1_{n+1}$')

    ax2.set_xlabel(r'$x^1_n$')
    ax2.set_ylabel(r'$x^2_n$')
    ax2.set_zlabel(r'$x^2_{n+1}$')


    density = 100

    # Plot the surface
    x1_mesh, x2_mesh = np.meshgrid(t, t)
    ax1.plot_surface(x1_mesh, x2_mesh , f1(x1_mesh, x2_mesh), cmap='viridis', alpha =.6)
    ax2.plot_surface(x1_mesh, x2_mesh , f2(x1_mesh, x2_mesh), cmap='viridis', alpha =.6)

    ax1.plot3D(x1 * np.ones(density), t, f1(x1, t), c='C0')
    ax1.plot3D(t, x2 * np.ones(density), f1(t, x2), c='C0')
    ax2.plot3D(x1 * np.ones(density), t, f2(x1, t), c='C0')
    ax2.plot3D(t, x2 * np.ones(density), f2(t, x2), c='C0')
    
    ax1.plot3D([x1, x1], [x2, x2], [0, f1(x1, x2)], c='C1')
    ax1.plot3D([next_x1, next_x1], [next_x2, next_x2], [0, f1(next_x1, next_x2)], c='C1', ls = '--')
    ax2.plot3D([x1, x1], [x2, x2], [0, f2(x1, x2)], c='C1')
    ax2.plot3D([next_x1, next_x1], [next_x2, next_x2], [0, f2(next_x1, next_x2)], c='C1', ls = '--')
    
    ax1.scatter(x1, x2, f1(x1, x2), s=25, c='black', zorder=100)
    ax2.scatter(x1, x2, f2(x1, x2), s=25, c='black', zorder=100)




draw_axes()

p_slider = Slider(
    ax=fig.add_axes([0.05, 0.25, 0.0225, 0.63]),
    label='p',
    valmin=0.1,
    valmax=5,
    valinit=p,
    orientation="vertical"
)

x1_slider = Slider(
    ax=fig.add_axes([0.25, 0.15, 0.65, 0.03]),
    label=r'$x^1_n$',
    valmin=lim[0],
    valmax=lim[1],
    valinit=x1
)

x2_slider = Slider(
    ax=fig.add_axes([0.25, 0.1, 0.65, 0.03]),
    label=r'$x^2_n$',
    valmin=lim[0],
    valmax= lim[1],
    valinit=x2
)

button = Button(
    fig.add_axes([0.8, 0.025, 0.1, 0.04]), 
    'step', 
    hovercolor='0.975')

b = False

def update(_):
    global x1, x2, p, next_x1, next_x2
    p = p_slider.val
    x1 = x1_slider.val
    x2 = x2_slider.val
    if not b:
        next_x1 = f1(x1, x2)
        next_x2 = f2(x1, x2)
        draw_axes()
        fig.canvas.draw_idle()

def step(_):
    global b
    b = True
    x1_slider.set_val(next_x1)
    b = False
    x2_slider.set_val(next_x2)



p_slider.on_changed(update)
x1_slider.on_changed(update)
x2_slider.on_changed(update)
button.on_clicked(step)


plt.show()