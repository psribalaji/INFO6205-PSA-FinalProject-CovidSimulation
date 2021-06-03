from random import random
from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D
from Graph import Graph
from Person import Person
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import defaultdict
from matplotlib.widgets import Button
import random


def set_values(n, infected, rateOfTrans, transmission, quarantine, timeToRecover, t_mortality,
               risk_age, death_percentage, young_death_percentage, config, window_title):
    print(n)
    n = n  # number of individuals
    infected_percent = infected  # percentage of infected people at the beginning of the simulation (0-100%)
    r_transmission = rateOfTrans  # radius of transmission in pixels (0-100)
    p_transmission = transmission  # probability of transmission in percentage (0-100%)
    p_quarantine = quarantine  # percentage of the people in quarantine (0-100%)
    t_recover = timeToRecover  # time taken to recover in number of frames (0-infinity)

    infected = 0
    persons = []
    graph = defaultdict(list)
    g = Graph()

    # creating all the individuals in random positions. Infecting some of them
    for i in range(n):
        p = Person(i, np.random.random() * 100, np.random.random() * 100,
                   np.random.random() * 100, np.random.random() * 100,
                   (np.random.random() + 0.5) * 100, t_recover, False, [], random.randint(1, 100))
        if check_if_infected(infected_percent, p, np.random.random()):
            infected = infected + 1
        check_if_quarantine(p_quarantine, p, np.random.random())
        persons.append(p)

    # Creates two subplots one for the scatter plot and the second for the graph
    fig = plt.figure(figsize=(18, 9))
    fig.canvas.set_window_title(window_title)
    fig.suptitle('Simulation for ' + window_title, fontsize=14, fontweight='bold')
    ax = fig.add_subplot(1, 2, 1)
    ax.axis('on')
    scat = ax.scatter([p.posx for p in persons],
                      [p.posy for p in persons], c='blue', s=8)
    legend_elems = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor="deepskyblue", label="Susceptible", markersize=9),
        Line2D([0], [0], marker='o', color='w', markerfacecolor="red", label="Infected", markersize=9),
        Line2D([0], [0], marker='o', color='w', markerfacecolor="green", label="Recovered", markersize=9),
        Line2D([0], [0], marker='o', color='w', markerfacecolor="black", label="Mortality", markersize=9)]
    fontP = FontProperties()
    fontP.set_size('xx-small')
    ax.legend(handles=legend_elems, loc='upper center', bbox_to_anchor=(1.05, 1), prop=fontP)
    box = plt.Rectangle((0, 0), 100, 100, fill=False)
    ax.add_patch(box)

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

    # function executed frame by frame
    def update(frame, rt, ct, t, mt):
        infected = 0
        recovered = 0
        mortality = 0
        colors = []
        sizes = [8 for p in persons]
        for p in persons:
            # check how much time the person has been sick
            p.check_infected(frame)
            # animate the movement of each person
            p.update_pos(0, 0)
            if p.recovered:
                recovered += 1  # count the amount of recovered
            if p.death:
                mortality += 1  # count the amount of people died
            if p.infected and p.age > risk_age and np.random.random() < death_percentage / 100 and (
                    frame - p.i_infected) > t_mortality:
                p.death_of_person()
            elif p.infected and p.age <= risk_age and np.random.random() < young_death_percentage / 100 and (
                    frame - p.i_infected) > t_mortality:
                p.death_of_person()
            if p.infected:
                infected = infected + 1  # count the amount of infected
                # check for people around the sick individual and infect the ones within the
                # transmission radius given the probability
                for per in persons:
                    if per.index == p.index or per.infected or per.recovered or per.death:
                        pass
                    else:
                        d = p.get_dist(per.posx, per.posy, per.name)
                        if d < r_transmission:
                            if infect_person_on_transmission(per, p_transmission, np.random.random(),
                                                             frame):
                                sizes[per.index] = 50
                                print(p.name + "==>" + per.name)
                                g.addEdge(p.name, per.name)
                                print(g.graph)

            colors.append(p.get_color())  # change dot color according to the person's status

        # update the plotting data
        ct.append(infected)
        rt.append(recovered)
        mt.append(mortality)
        t.append(frame)

        # tramsfer the data to the matplotlib graphics
        offsets = np.array([[p.posx for p in persons],
                            [p.posy for p in persons]])
        scat.set_offsets(np.ndarray.transpose(offsets))
        scat.set_color(colors)
        scat.set_sizes(sizes)
        cvst.set_data(t, ct)
        rvst.set_data(t, rt)
        mvst.set_data(t, mt)
        return scat, cvst, rvst, mvst

    def onClick(event):
        print("Clicked")
        g.findRandKfactor("SARS 2")
        g.vis()

    # run the animation indefinitely
    animation = FuncAnimation(fig, update, interval=25, fargs=(rt, ct, t, mt), blit=True)
    # callback = ()

    axcut = plt.axes([0.9, 0.0, 0.1, 0.075])
    bcut = Button(axcut, 'Stop & View result', color='red', hovercolor='green')
    bcut.on_clicked(onClick)
    plt.show()


def check_if_infected(infected_percent, p, infect_val):
    if infect_val < infected_percent / 100:
        p.infect(0)
        return True


def check_if_quarantine(p_quarantine, p, quarantine_val):
    if quarantine_val < p_quarantine / 100:
        p.quarantine = True


def infect_person_on_transmission(per, p_transmission, val, frame):
    if val < p_transmission / 100:
        per.infect(frame)
        return True
