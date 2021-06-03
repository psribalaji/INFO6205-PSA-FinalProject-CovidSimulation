from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D
from Person import Person
import numpy as np
import math
from matplotlib.animation import FuncAnimation
import random
import matplotlib.pyplot as plt
from Graph import Graph
from matplotlib.widgets import Button


def set_values_vaccine(n, p_transmission, p_quarantine, p_vaccine_efficacy,
                       vaccine_avail_percent_per_day, p_vaccination, death_percentage,
                       young_death_percentage, risk_age, config):
    infected_percent = int((config['Vaccine_Efficacy'][
        'Infected_Percent']))  # percentage of infected people at the beginning of the simulation (0-100%)
    r_transmission = int((config['Vaccine_Efficacy']['Rate_Transmission']))  # radius of transmission in pixels (0-100)
    t_recover = int(
        (config['Vaccine_Efficacy']['Recovery_Time']))  # time taken to recover in number of frames (0-infinity)
    t_mortality = int(
        (config['Vaccine_Efficacy']['Mortality_Time']))  # the time taken to die in number of frames (0-infinity)

    infected = 0
    persons = []
    g = Graph()
    # creating all the individuals in random positions. Infecting some of them
    for i in range(n):
        p = Person(i, np.random.random() * 100, np.random.random() * 100,
                   np.random.random() * 100, np.random.random() * 100,
                   (np.random.random() + 0.5) * 100, t_recover, False, [], random.randint(1, 100))
        if check_if_infected_for_vaccine(infected_percent, p, np.random.random()):
            infected = infected + 1
        check_if_quarantine_for_vaccine(p_quarantine, p, np.random.random())
        persons.append(p)

    # Creates two subplots one for the scatter plot and the second for the graph
    fig = plt.figure(figsize=(18, 9))
    fig.canvas.set_window_title("Vaccine Availability and Efficacy")
    fig.suptitle('Simulation for Vaccine Availability and Efficacy', fontsize=14, fontweight='bold')
    ax = fig.add_subplot(1, 2, 1)
    ax.axis('on')
    scat = ax.scatter([p.posx for p in persons],
                      [p.posy for p in persons], c='blue', s=8)
    legend_elems = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor="deepskyblue", label="Susceptible", markersize=9),
        Line2D([0], [0], marker='o', color='w', markerfacecolor="red", label="Infected", markersize=9),
        Line2D([0], [0], marker='o', color='w', markerfacecolor="purple", label="Vaccinated", markersize=9),
        Line2D([0], [0], marker='o', color='w', markerfacecolor="green", label="Recovered", markersize=9),
        Line2D([0], [0], marker='o', color='w', markerfacecolor="black", label="Mortality", markersize=9),
        Line2D([0], [0], marker='o', color='w', markerfacecolor="orange", label="Immune", markersize=9)]
    fontP = FontProperties()
    fontP.set_size('xx-small')
    ax.legend(handles=legend_elems, loc='upper center', bbox_to_anchor=(1.05, 1), prop=fontP)
    box = plt.Rectangle((0, 0), 100, 100, fill=False)
    ax.add_patch(box)

    cx = fig.add_subplot(1, 2, 2)
    cx.axis([0, 1000, 0, n])
    cvst, = cx.plot(0, color="red", label="Infected")
    vvst, = cx.plot(0, color="purple", label="Vaccinated")
    ivst, = cx.plot(0, color="orange", label="Immune")
    mvst, = cx.plot(infected, color="black", label="Mortality")

    cx.legend(handles=[cvst, vvst, ivst, mvst], loc="upper right")
    cx.set_xlabel("Time")
    cx.set_ylabel("Number of People")
    ct = [infected]
    vt = [0]
    it = [0]
    mt = [0]
    t = [0]

    # function executed frame by frame
    def update(frame, vt, ct, t, it, mt):
        infected = 0
        vaccinated = 0
        immunityBuilt = 0
        mortality = 0
        colors = []
        sizes = [8 for p in persons]
        numPeopleNotVaccinated = []
        for p in persons:
            if p.vaccinated == False and p.infected == False:
                numPeopleNotVaccinated.append(p)

        numPeopleCanBeVaccinatedToday = int(
            math.ceil(((vaccine_avail_percent_per_day / 100) * len(numPeopleNotVaccinated))))
        peopleSelectedForVaccine = random.sample(numPeopleNotVaccinated, numPeopleCanBeVaccinatedToday)

        for p in persons:
            if p in peopleSelectedForVaccine and p.vaccineImmunityBuilt == False and p.death == False and p.infected == False \
                    and np.random.random() < p_vaccination / 100:
                p.vaccine(frame)
            if p.vaccinated and np.random.random() < p_vaccine_efficacy / 100 and p.death == False and p.infected == False:
                p.check_vaccinated(frame)
            if p.infected and p.age > risk_age and np.random.random() < death_percentage / 100 and p.vaccineImmunityBuilt == False and (
                    frame - p.i_infected) > t_mortality:
                p.death_of_person()
            elif p.infected and p.age <= risk_age and np.random.random() < young_death_percentage / 100 and p.vaccineImmunityBuilt == False and (
                    frame - p.i_infected) > t_mortality:
                p.death_of_person()

        for p in persons:
            # # check how much time the person has been sick
            p.check_infected(frame)
            # animate the movement of each person
            p.update_pos(0, 0)
            if p.vaccinated:
                vaccinated += 1  # count the amount of recovered
            if p.death:
                mortality += 1  # count the amount of people died
            if p.vaccineImmunityBuilt:
                immunityBuilt += 1  # count the amount of people immune after vaccination
            if p.infected:
                infected = infected + 1  # count the amount of infected
                # check for people around the sick individual and infect the ones within the
                # transmission radius given the probability
                for per in persons:
                    if per.index == p.index or per.infected or per.recovered or per.vaccineImmunityBuilt or per.death:
                        pass
                    else:
                        d = p.get_dist(per.posx, per.posy, per.name)
                        if d < r_transmission:
                            if infect_person_on_transmission_for_vaccine(per, p_transmission, np.random.random(),
                                                                         frame):
                                sizes[per.index] = 50
                                print(p.name + "==>" + per.name)
                                g.addEdge(p.name, per.name)
                                print(g.graph)

            colors.append(p.get_color())  # change dot color according to the person's status

        # update the plotting data
        ct.append(infected)
        vt.append(vaccinated)
        it.append(immunityBuilt)
        mt.append(mortality)
        t.append(frame)

        # transfer the data to the matplotlib graphics
        offsets = np.array([[p.posx for p in persons],
                            [p.posy for p in persons]])
        scat.set_offsets(np.ndarray.transpose(offsets))
        scat.set_color(colors)
        scat.set_sizes(sizes)
        cvst.set_data(t, ct)
        vvst.set_data(t, vt)
        ivst.set_data(t, it)
        mvst.set_data(t, mt)
        return scat, cvst, vvst, ivst, mvst

    def onClick(event):
        print("Clicked")
        g.findRandKfactor("SARS 2")
        g.vis()

    # run the animation indefinitely
    animation = FuncAnimation(fig, update, interval=25, fargs=(vt, ct, t, it, mt), blit=True)
    axcut = plt.axes([0.9, 0.0, 0.1, 0.075])
    bcut = Button(axcut, 'Stop & View result', color='red', hovercolor='green')
    bcut.on_clicked(onClick)
    plt.show()


def check_if_infected_for_vaccine(infected_percent, p, infect_val):
    if infect_val < infected_percent / 100:
        p.infect(0)
        return True


def check_if_quarantine_for_vaccine(p_quarantine, p, quarantine_val):
    if quarantine_val < p_quarantine / 100:
        p.quarantine = True


def infect_person_on_transmission_for_vaccine(per, p_transmission, val, frame):
    if val < p_transmission / 100:
        per.infect(frame)
        return True
