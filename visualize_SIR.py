import os
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure(facecolor='w')
ax1 = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)

def animate(i):

    graph_data = open(os.path.join(sys.path[0], "data.txt"), "r").read()
    lines = graph_data.split('\n')

    Days = []
    S = []; I = []; R = [] 

    for line in lines:
        if len(line) > 1:
            day, Sy, Iy, Ry = line.split(',')
            Days.append(float(day))
            S.append(float(Sy)/5); I.append(float(Iy)/5); R.append(float(Ry)/5)

    ax1.clear()

    ax1.plot(Days, S, "b", alpha=0.5, lw=2, label = "Susceptible")
    ax1.plot(Days, I, "r", alpha=0.5, lw=2, label='Infected')
    ax1.plot(Days, R, "g", alpha=0.5, lw=2, label='Recovered with immunity')

    ax1.set_xlabel('Time /days')
    ax1.set_ylabel('Population (%)')

    ax1.yaxis.set_tick_params(length=0)
    ax1.xaxis.set_tick_params(length=0)
    ax1.grid(b=True, which='major', c='w', lw=2, ls='-')

    ax1.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left", mode="expand", borderaxespad=0, ncol=3)


ani = animation.FuncAnimation(fig, animate)
plt.show()