import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation


# settings
global n, number_of_dots

data_file = "testdata.data"
cfg_file = "sim.cfg"
cfg = open(cfg_file, "r")

# read settings fro sim.cfg
n = int(cfg.readline())
total_steps = int(cfg.readline())
number_of_dots = 100
# spread determines the bound of the animation
spread = float(cfg.readline()) * 1.25
file = open(data_file, "r")

# trying to write the animation to a file
# Writer = animation.writers['html']
# writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

# setting up fig and axis
fig, ax = plt.subplots()
ax.set_facecolor('xkcd:black')
ax.set_xlim(-spread, spread)
ax.set_ylim(-spread, spread)


class body():
    def __init__(self):
        self.x = []
        self.y = []
        self.mass = 0.0

def update(frame):
    trail_x, trail_y = [], []

    for i in range(n):
        x = bodies[i].x[frame]
        y = bodies[i].y[frame]

        # merge handling
        if not (x == 0 and y == 0):
            animated_bodies[i].set_data(x,y)
        else:
            animated_bodies[i].set_data([],[])

    # writing in the trace
    for i in range(n):
        body = bodies[i]
        if frame < number_of_dots:
            trail_x.append(body.x[0:frame])
            trail_y.append(body.y[0:frame])

        else:
            trail_x.append(body.x[(frame-number_of_dots):frame])
            trail_y.append(body.y[(frame-number_of_dots):frame])

    animated_bodies[n].set_data(trail_x,trail_y)

    return animated_bodies


# creating objects to that contains the position data
bodies = []
animated_bodies = []

for i in range(n):
    bodies.append(body())

for i in range(total_steps):
    for j in range(n):
        try:
            data = [float (n) for n in file.readline().split()];
            bodies[j].x.append(data[1])
            bodies[j].y.append(data[2])
            bodies[j].mass = data[3]
        except:
            break

# creating aniated objects
for i in range(n):
    new, = plt.plot([],[],color='red',marker='o',markersize=9,animated=True)
    animated_bodies.append(new)

# creating trail of bodies
trail, = plt.plot([], [], 'bo', markersize=0.2, animated=True)
animated_bodies.append(trail)
ani = FuncAnimation(fig, update, interval=1, blit=True)
plt.show()


# fig1 = plt.figure()
# im_ani = animation.ArtistAnimation(fig1, ims, interval=50, repeat_delay=3000,
#                                    blit=True)
# im_ani.save('im.mp4', writer=writer)
