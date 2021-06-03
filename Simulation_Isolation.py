from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D
from matplotlib.widgets import Button
from Person import Person
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Patch
from matplotlib.animation import FuncAnimation
import random
from Graph import Graph


def set_value_isolation(n, p_transmission, death_percentage,
                        young_death_percentage, risk_age, config):
    infected_percent = int((config['Isolation'][
        'Infected_Percent']))  # percentage of the infected people at the beginning of the simulation (0-100%)
    r_transmission = int((config['Isolation']['Rate_Transmission']))  # radius of transmission in pixels (0-100)
    t_recover = int(
        (config['Isolation']['Recovery_Time']))  # the time taken to recover in number of frames (0-infinity)
    t_mortality = int((config['Isolation']['Mortality_Time']))  # the time taken to die in number of frames (0-infinity)
    infected = 0
    persons = []
    g = Graph()

    # Creating all the individuals in random positions. Infecting some of them
    for i in range(n):
        p = Person(i, np.random.random() * 100, np.random.random() * 100,
                   np.random.random() * 100, np.random.random() * 100,
                   (np.random.random() + 0.5) * 100, t_recover, False, [], random.randint(1, 100))
        if check_if_infected_for_isolation(infected_percent, p, np.random.random()):
            infected = infected + 1
        persons.append(p)

    # Creates two subplots one for the scatter plot and the second for the graph
    fig = plt.figure(figsize=(18, 9))
    fig.canvas.set_window_title("Isolation")
    fig.suptitle('Simulation for Isolation', fontsize=14, fontweight='bold')
    ax = fig.add_subplot(1, 2, 1)
    ax.axis('on')
    scat = ax.scatter([p.posx for p in persons],
                      [p.posy for p in persons], c='blue', s=8)
    legend_elems = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor="deepskyblue", label="Susceptible", markersize=9),
        Line2D([0], [0], marker='o', color='w', markerfacecolor="red", label="Infected", markersize=9),
        Line2D([0], [0], marker='o', color='w', markerfacecolor="green", label="Recovered", markersize=9),
        Line2D([0], [0], marker='o', color='w', markerfacecolor="black", label="Mortality", markersize=9),
        Patch(facecolor='w', edgecolor='darkslategray', label='Isolation')]
    fontP = FontProperties()
    fontP.set_size('xx-small')
    ax.legend(handles=legend_elems, loc='upper center', bbox_to_anchor=(1.05, 1), prop=fontP)
    box = plt.Rectangle((0, 0), 100, 100, fill=False)
    ax.add_patch(box)
    left, bottom, width, height = (80, 0, 20, 100)
    rect = mpatches.Rectangle((left, bottom), width, height,
                              fill=False,
                              color="darkslategray",
                              linewidth=2)
    ax.add_patch(rect)

    cx = fig.add_subplot(1, 2, 2)
    cx.axis([0, 1000, 0, n])
    rvst, = cx.plot(infected, color="green", label="Recovered")
    cvst, = cx.plot(infected, color="red", label="Infected")
    mvst, = cx.plot(infected, color="black", label="Mortality")
    cx.legend(loc="upper right", handles=[cvst, rvst, mvst])
    cx.set_xlabel("Time")
    cx.set_ylabel("Number of People")
    ct = [infected]
    rt = [0]
    mt = [0]
    t = [0]

    # Function updates the location and status of a person frame by frame
    def update(frame, rt, ct, mt, t):
        infected = 0
        recovered = 0
        mortality = 0
        colors = []
        sizes = [8 for p in persons]
        for p in persons:
            # checking how much time the person has been sick
            p.check_infected(frame)
            # animating the movement of each person
            p.update_pos_isolation()
            if p.recovered:
                recovered += 1  # count the amount of recovered people
            if p.infected:
                infected += 1  # count the amount of infected people
                # checking for people around the sick individual and infecting the ones within the
                # transmission radius given the probability
                for per in persons:
                    if per.index == p.index or per.infected or per.recovered or per.death:
                        pass
                    else:
                        d = p.get_dist(per.posx, per.posy, per.name)
                        if d < r_transmission:
                            if infect_person_on_transmission_for_isolation(per, p_transmission, np.random.random(),
                                                                           frame):
                                sizes[per.index] = 50
                                print(p.name + "==>" + per.name)
                                g.addEdge(p.name, per.name)
                                print(g.graph)
            if p.death:
                mortality += 1  # count the amount of people died
            if p.infected and p.age > risk_age and np.random.random() < death_percentage / 100 and (
                    frame - p.i_infected) > t_mortality:
                p.death_of_person()
            elif p.infected and p.age <= risk_age and np.random.random() < young_death_percentage / 100 and (
                    frame - p.i_infected) > t_mortality:
                p.death_of_person()
            colors.append(p.get_color())  # change dot color according to the person's status
        # update the plotting data
        ct.append(infected)
        rt.append(recovered)
        mt.append(mortality)
        t.append(frame)

        # transfer the data to the matplotlib graphics
        offsets = np.array([[p.posx for p in persons],
                            [p.posy for p in persons]])
        scat.set_offsets(np.ndarray.transpose(offsets))
        scat.set_color(colors)
        scat.set_sizes(sizes)
        cvst.set_data(t, ct)
        rvst.set_data(t, rt)
        mvst.set_data(t, mt)
        return scat, cvst, rvst, mvst

    # run the animation indefinitely
    animation = FuncAnimation(fig, update, interval=25, fargs=(rt, ct, mt, t), blit=True)

    def onClick(event):
        print("Clicked")
        g.findRandKfactor("SARS 2")
        g.vis()

    axcut = plt.axes([0.9, 0.0, 0.1, 0.075])
    bcut = Button(axcut, 'Stop & View result', color='red', hovercolor='green')
    bcut.on_clicked(onClick)
    plt.show()


def check_if_infected_for_isolation(infected_percent, p, infect_val):
    if infect_val < infected_percent / 100:
        p.infect(0)
        return True


def infect_person_on_transmission_for_isolation(per, p_transmission, val, frame):
    if val < p_transmission / 100:
        per.infect(frame)
        return True
