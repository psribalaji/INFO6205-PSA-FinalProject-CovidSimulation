from configparser import ConfigParser

import numpy as np
import matplotlib.pyplot as plt1
from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D
from matplotlib import pyplot as plt, test
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button

from Graph import Graph
from Person import Person
from collections import defaultdict

file = 'config.ini'
config = ConfigParser()
config.read(file)


def set_comparevalues(n, infected, rateOfTrans, transmission, quarantine, timeToRecover, config):
    print("Recovery Time ", timeToRecover)
    n = n  # number of individuals
    infected_percent = infected  # percentage of infected people at the beginning of the simulation (0-100%)
    r_transmission = rateOfTrans  # radius of transmission in pixels (0-100)
    p_transmission = transmission  # probability of transmission in percentage (0-100%)
    p_quarantine = quarantine  # percentage of the people in quarantine (0-100%)
    t_recover = timeToRecover  # time taken to recover in number of frames (0-infinity)
    t_mortality1 = int(
        (config['Sars-Cov Parameters']['Mortality_Time']))  # the time taken to die in number of frames (0-infinity)
    t_mortality = int(
        (config['Covid 19 Parameters']['Mortality_Time']))  # the time taken to die in number of frames (0-infinity)

    # 100,10,2,80,1,200
    # Assigning values for Sars-Cov person
    infected_percent1 = int((config['Sars-Cov Parameters']['Infected_Percent']))
    r_transmission1 = int((config['Sars-Cov Parameters']['Rate_Transmission']))
    p_transmission1 = int((config['Sars-Cov Parameters']['Probability_Transmission']))
    p_quarantine1 = int((config['Sars-Cov Parameters']['Probability_Quarantine']))

    t_recover1 = int((config['Sars-Cov Parameters']['Recovery_Time']))
    risk_age1 = int((config['Sars-Cov Parameters']['Risk_Age']))
    death_percentage1 = int((config['Sars-Cov Parameters']['Death_Percent']))
    young_death_percentage1 = int((config['Sars-Cov Parameters']['Young_Death_Percent']))

    risk_age = int((config['Covid 19 Parameters']['Risk_Age']))
    death_percentage = int((config['Covid 19 Parameters']['Death_Percent']))
    young_death_percentage = int((config['Covid 19 Parameters']['Young_Death_Percent']))

    infected = 0
    persons = []
    age = int((config['Vaccine_Efficacy']['Risk_Age']))
    infected1 = 0
    persons1 = []
    graph = defaultdict(list)
    g = Graph()
    g1 = Graph()

    # creating all the individuals in random positions. Infecting some of them
    for i in range(n):
        p = Person(i, np.random.random() * 100, np.random.random() * 100,
                   np.random.random() * 100, np.random.random() * 100,
                   (np.random.random() + 0.5) * 100, t_recover, False, [], age)

        p1 = Person(i, np.random.random() * 100, np.random.random() * 100,
                    np.random.random() * 100, np.random.random() * 100,
                    (np.random.random() + 0.5) * 100, t_recover1, False, [], age)

        if check_if_infected_for_compare_viruses(infected_percent, p, np.random.random()):
            infected = infected + 1
        check_if_quarantine_for_compare_viruses(p_quarantine, p, np.random.random())

        # person2
        if check_if_infected_for_compare_viruses(infected_percent1, p1, np.random.random()):
            infected1 = infected1 + 1
        check_if_quarantine_for_compare_viruses(p_quarantine1, p1, np.random.random())

        persons.append(p)
        persons1.append(p1)

    # this creates all the graphics
    fig = plt.figure(figsize=(18, 9))
    fig.suptitle('Comparison between Sars-Cov2 (Covid-19) And Sars-Cov', fontsize=14, fontweight='bold')
    fig.canvas.set_window_title("Comparing Two Viruses")
    ax = fig.add_subplot(2, 2, 1)
    title = ax.set_title("Sars-Cov-2", loc="center", y=1.1)
    cx = fig.add_subplot(2, 2, 3)
    dx = fig.add_subplot(2, 2, 2)
    title1 = dx.set_title("Sars-Cov", loc="center", y=1.1)
    ex = fig.add_subplot(2, 2, 4)

    ax.axis('on')
    cx.axis([0, 1000, 0, n])
    scat = ax.scatter([p.posx for p in persons],
                      [p.posy for p in persons], c='blue', s=8)
    box = plt.Rectangle((0, 0), 100, 100, fill=False)
    ax.add_patch(box)

    dx.axis('on')
    scat1 = dx.scatter([p1.posx for p1 in persons1],
                       [p1.posy for p1 in persons1], c='blue', s=8)
    box1 = plt1.Rectangle((0, 0), 100, 100, fill=False)
    dx.add_patch(box1)

    legend_elems = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor="deepskyblue", label="Susceptible", markersize=9),
        Line2D([0], [0], marker='o', color='w', markerfacecolor="red", label="Infected", markersize=9),
        Line2D([0], [0], marker='o', color='w', markerfacecolor="green", label="Recovered", markersize=9),
        Line2D([0], [0], marker='o', color='w', markerfacecolor="black", label="Mortality", markersize=9)]
    fontP = FontProperties()
    fontP.set_size('xx-small')

    ax.legend(handles=legend_elems, loc='upper center', bbox_to_anchor=(1.05, 1), prop=fontP)
    dx.legend(handles=legend_elems, loc='upper center', bbox_to_anchor=(1.05, 1), prop=fontP)

    cvst, = cx.plot(infected, color="red", label="Infected")
    rvst, = cx.plot(infected, color="green", label="Recovered")
    mvst, = cx.plot(infected, color="black", label="Mortality")

    cx.legend(handles=[cvst, rvst, mvst])
    cx.set_xlabel("Time")
    cx.set_ylabel("Number of People")

    ex.axis([0, 1000, 0, n])
    cvst1, = ex.plot(infected, color="red", label="Infected")
    rvst1, = ex.plot(infected, color="green", label="Recovered")
    mvst1, = ex.plot(infected, color="black", label="Mortality")

    ex.legend(handles=[cvst1, rvst1, mvst1])
    ex.set_xlabel("Time")
    ex.set_ylabel("Number of People")

    ct = [infected]
    rt = [0]
    mt = [0]
    t = [0]

    ct1 = [infected1]
    rt1 = [0]
    mt1 = [0]
    t1 = [0]

    # function executed frame by frame
    def update(frame, rt, ct, t, rt1, ct1, t1, mt, mt1):
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
                            if infect_person_on_transmission_for_compare_viruses(per,
                                                                                 p_transmission,
                                                                                 np.random.random(),
                                                                                 frame):
                                sizes[per.index] = 80
                                # per.addInfectedList(frame)
                                print(p.name + "==>" + per.name)
                                g.addEdge(p.name, per.name)
                                print(g.graph)

            colors.append(p.get_color())  # change dot color according to the person's status

            infected1 = 0
            recovered1 = 0
            mortality1 = 0
            colors1 = []
            sizes1 = [8 for p1 in persons1]

        for p1 in persons1:
            # check how much time the person has been sick
            p1.check_infected(frame)
            # animate the movement of each person
            p1.update_pos(0, 0)
            if p1.recovered:
                recovered1 += 1  # count the amount of recovered
            if p1.death:
                mortality1 += 1  # count the amount of people died
            if p1.infected and p1.age > risk_age1 and np.random.random() < death_percentage1 / 100 and (
                    frame - p1.i_infected) > t_mortality1:
                p1.death_of_person()
            elif p1.infected and p1.age <= risk_age1 and np.random.random() < young_death_percentage1 / 100 and (
                    frame - p1.i_infected) > t_mortality1:
                p1.death_of_person()
            if p1.infected:
                infected1 = infected1 + 1  # count the amount of infected
                # check for people around the sick individual and infect the ones within the
                # transmission radius given the probability
                for per1 in persons1:
                    if per1.index == p1.index or per1.infected or per1.recovered or per1.death:
                        pass
                    else:
                        d = p1.get_dist(per1.posx, per1.posy, per1.name)
                        if d < r_transmission1:
                            if infect_person_on_transmission_for_compare_viruses(per1,
                                                                                 p_transmission1, np.random.random(),
                                                                                 frame):
                                sizes1[per1.index] = 80
                                # per.addInfectedList(frame)
                                print(p1.name + "==>" + per1.name)
                                g1.addEdge(p1.name, per1.name)
                                print(g1.graph)

            colors1.append(p1.get_color())  # change dot color according to the person's status

        # update the plotting data
        ct.append(infected)
        rt.append(recovered)
        mt.append(mortality)
        t.append(frame)

        ct1.append(infected1)
        rt1.append(recovered1)
        mt1.append(mortality1)
        t1.append(frame)

        # transfer the data to the matplotlib graphics
        offsets = np.array([[p.posx for p in persons],
                            [p.posy for p in persons]])
        scat.set_offsets(np.ndarray.transpose(offsets))
        scat.set_color(colors)
        scat.set_sizes(sizes)
        cvst.set_data(t, ct)
        rvst.set_data(t, rt)
        mvst.set_data(t, mt)

        offsets1 = np.array([[p1.posx for p1 in persons1],
                             [p1.posy for p1 in persons1]])
        scat1.set_offsets(np.ndarray.transpose(offsets1))
        scat1.set_color(colors1)
        scat1.set_sizes(sizes1)
        cvst1.set_data(t1, ct1)
        rvst1.set_data(t1, rt1)
        mvst1.set_data(t, mt1)

        return scat, cvst, rvst, scat1, rvst1, cvst1, mvst, mvst1

    def onClick(event):
        print("Clicked")
        g.findRandKfactor("SARS 2")
        g1.findRandKfactor("SARS 1")
        g.vis()

    animation1 = FuncAnimation(fig, update, interval=25, fargs=(rt, ct, t, rt1, ct1, t1, mt, mt1), blit=True)
    axcut = plt.axes([0.9, 0.0, 0.1, 0.075])
    bcut = Button(axcut, 'Stop & View result', color='red', hovercolor='green')
    bcut.on_clicked(onClick)
    plt.show()


def check_if_infected_for_compare_viruses(infected_percent, p, infect_val):
    if infect_val < infected_percent / 100:
        p.infect(0)
        return True


def check_if_quarantine_for_compare_viruses(p_quarantine, p, quarantine_val):
    if quarantine_val < p_quarantine / 100:
        p.quarantine = True


def infect_person_on_transmission_for_compare_viruses(per, p_transmission, val, frame):
    if val < p_transmission / 100:
        per.infect(frame)
        return True
