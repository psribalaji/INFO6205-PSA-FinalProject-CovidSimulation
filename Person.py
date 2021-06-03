import math
import numpy as np
import random


class Person:
    def __init__(self, i, posx, posy, objx, objy, v, t_infected, quarantine, infectionList, age):
        # movement speed
        self.v = v
        # target position
        self.objx = objx
        self.objy = objy
        # ID and name
        self.index = i
        self.name = "Person " + str(i)
        self.age = age
        # State: Susceptible, Infected or Recovered
        self.infected = False
        self.susceptible = True
        self.recovered = False
        self.vaccinated = False
        self.vaccineImmunityBuilt = False
        self.death = False
        # is it fixed (in quarantine)?
        self.quarantine = quarantine
        # Current position
        self.posx = posx
        self.posy = posy

        self.infectionList = infectionList
        self.rFactor = 0

        # displacement per iteration
        self.deltax = (self.objx - self.posx) / self.v
        self.deltay = (self.objy - self.posy) / self.v
        # time in which the person was infected
        self.i_infected = -1
        # time that the infection lasts, recover time
        self.t_infected = t_infected
        self.i_vaccinated = -1

    def __str__(self):
        return self.name + " in position " + str(self.posx) + ", " + str(self.posy)

    def __repr__(self):
        return self.name

    def addInfectedList(self, l):
        self.infectionList.append(l)

    def infect(self, i):
        self.infected = True
        self.susceptible = False
        self.recovered = False
        self.vaccineImmunityBuilt = False
        self.death = False
        self.i_infected = i

    def recover(self):
        # heal
        self.recovered = True
        self.susceptible = False
        self.infected = False
        self.quarantine = False
        self.vaccineImmunityBuilt = False
        self.death = False

    def vaccine(self, i):
        self.vaccinated = True
        self.recovered = False
        self.susceptible = False
        self.infected = False
        self.i_vaccinated = i

    def immune(self):
        self.vaccineImmunityBuilt = True
        self.vaccinated = False
        self.recovered = False
        self.susceptible = False
        self.infected = False

    def death_of_person(self):
        self.death = True
        self.vaccineImmunityBuilt = False
        self.vaccinated = False
        self.recovered = False
        self.susceptible = False
        self.infected = False

    def set_object(self, objx, objy):
        # this function is used to create a new target position
        self.objx = objx
        self.objy = objy
        if self.quarantine:
            self.deltax = 0
            self.deltay = 0
        else:
            self.deltax = (self.objx - self.posx) / self.v
            self.deltay = (self.objy - self.posy) / self.v

    def set_object_isolation(self, objx, objy):
        # this function is used to create a new target position
        self.objx = objx
        self.objy = objy
        self.deltax = (self.objx - self.posx) / self.v
        self.deltay = (self.objy - self.posy) / self.v
        # print("New Person   ", self.objx,self.objy,"  ",self.index)

    def check_infected(self, i):
        # this function is used to heal the person if the established infection time has passed
        if self.i_infected > -1 and self.infected:
            if i - self.i_infected > self.t_infected:
                if self.quarantine:
                    self.posx = random.randint(77, 80)
                self.recover()

    def check_vaccinated(self, i):
        # this function is used to immune the person if the established vaccination time has passed
        if self.i_vaccinated > -1 and self.vaccinated and self.death == False and self.infected == False:
            if i - self.i_vaccinated > self.t_infected:
                self.immune()

    def update_pos(self, n_posx, n_posy):
        # this function animates the movement
        if not self.death:
            if n_posx == 0 and n_posy == 0:
                self.posx = self.posx + self.deltax
                self.posy = self.posy + self.deltay
            else:
                self.posx = n_posx
                self.posy = n_posy

            if abs(self.posx - self.objx) < 3 and abs(self.posy - self.objy) < 3:
                self.set_object(np.random.random() * 100, np.random.random() * 100)
            if self.posx > 100:
                self.posx = 100
            if self.posy > 100:
                self.posy = 100
            if self.posx < 0:
                self.posx = 0
            if self.posy < 0:
                self.posy = 0

    def update_pos_isolation(self):
        # this function animates the movement
        if not self.death:
            if self.infected and not self.quarantine:
                self.posx = self.posx + abs(self.deltax)
            else:
                self.posx = self.posx + self.deltax
            self.posy = self.posy + self.deltay

            if abs(self.posx - self.objx) < 3 and abs(self.posy - self.objy) < 3:
                self.set_object_isolation(np.random.random() * 100, np.random.random() * 100)

            if self.infected and self.posx > 80:
                self.quarantine = True

            if not self.quarantine:
                if self.posx > 80:
                    self.posx = 79
                if self.posy > 100:
                    self.posy = 99
                if self.posx < 0:
                    self.posx = 1
                if self.posy < 0:
                    self.posy = 1
            else:
                if self.posx > 100:
                    self.posx = 99
                if self.posx < 80:
                    self.posx = 81
                if self.posy < 0:
                    self.posy = 1
                if self.posy > 100:
                    self.posy = 99

    def get_color(self):
        if self.infected:
            return 'red'
        if self.susceptible:
            return 'deepskyblue'
        if self.recovered:
            return 'green'
        if self.vaccinated:
            return 'purple'
        if self.vaccineImmunityBuilt:
            return 'orange'
        if self.death:
            return 'black'

    def get_pos(self):
        return (self.posx, self.posy)

    def get_dist(self, x, y, per):
        # this funcion calculates the distance between this person an another.
        return math.sqrt((self.posx - x) ** 2 + (self.posy - y) ** 2)
