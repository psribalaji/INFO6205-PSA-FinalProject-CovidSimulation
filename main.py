import tkinter as tk

# from simulation import set_values
import Simulation_Isolation
import Simulation_Vaccination

# from simulation import set_values
from tkinter.ttk import Combobox

from Simulation import set_values
import CompareViruses
from Graph import Graph

from Simulation import set_values
from configparser import ConfigParser

file = 'config.ini'
config = ConfigParser()
config.read(file)


def normal():
    set_values(int((config['Covid 19 Parameters']['Population'])),
               int((config['Covid 19 Parameters']['Infected_Percent'])),
               int((config['Covid 19 Parameters']['Rate_Transmission'])),
               int((config['Covid 19 Parameters']['Probability_Transmission'])),
               int((config['Covid 19 Parameters']['Probability_Quarantine'])),
               int((config['Covid 19 Parameters']['Recovery_Time'])),
               int((config['Covid 19 Parameters']['Mortality_Time'])),
               int((config['Covid 19 Parameters']['Risk_Age'])),
               int((config['Covid 19 Parameters']['Death_Percent'])),
               int((config['Covid 19 Parameters']['Young_Death_Percent'])), config, "Without Mask Mandate")
    pass


def with_mask():
    set_values(int((config['Mask_Mandate']['Population'])),
               int((config['Mask_Mandate']['Infected_Percent'])),
               int((config['Mask_Mandate']['Rate_Transmission'])),
               int((config['Mask_Mandate']['Probability_Transmission'])),
               int((config['Mask_Mandate']['Probability_Quarantine'])),
               int((config['Mask_Mandate']['Recovery_Time'])),
               int((config['Mask_Mandate']['Mortality_Time'])),
               int((config['Mask_Mandate']['Risk_Age'])),
               int((config['Mask_Mandate']['Death_Percent'])),
               int((config['Mask_Mandate']['Young_Death_Percent'])),
               config, "With Mask Mandate")


def stop():
    Graph.vis()


def compare_viruses():
    CompareViruses.set_comparevalues(int((config['Comparison_Scenario']['Population'])),
                                     int((config['Comparison_Scenario']['Infected_Percent'])),
                                     int((config['Comparison_Scenario']['Rate_Transmission'])),
                                     int((config['Comparison_Scenario']['Probability_Transmission'])),
                                     int((config['Comparison_Scenario']['Probability_Quarantine'])),
                                     int((config['Comparison_Scenario']['Recovery_Time'])), config)


def with_isolation():
    Simulation_Isolation.set_value_isolation(int((config['Isolation']['Population'])),
                                             int((config['Isolation']['Probability_Transmission'])),
                                             float((config['Isolation']['Death_Percent'])),
                                             float((config['Isolation']['Young_Death_Percent'])),
                                             int((config['Isolation']['Risk_Age'])),
                                             config)


def vaccine_availability_efficacy():
    Simulation_Vaccination.set_values_vaccine(int((config['Vaccine_Efficacy']['Population'])),
                                              int((config['Vaccine_Efficacy']['Probability_Transmission'])),
                                              int((config['Vaccine_Efficacy']['Probability_Quarantine'])),
                                              int((config['Vaccine_Efficacy']['Vaccine_Efficacy_Percent'])),
                                              float(
                                                  (config['Vaccine_Efficacy']['Vaccine_Availability_Per_Day_Percent'])),
                                              float((config['Vaccine_Efficacy']['Total_Vaccination_Percent'])),
                                              float((config['Vaccine_Efficacy']['Death_Percent'])),
                                              float((config['Vaccine_Efficacy']['Young_Death_Percent'])),
                                              int((config['Vaccine_Efficacy']['Risk_Age'])),
                                              config)


def insert():
    print("Hello " + a1.get())


def test():
    if a1.get() == "" or b1.get() == "" or c1.get() == "" or d1.get() == "" or e1.get() == "" or f1.get() == "":
        print("Fill all the required fields!")
    else:
        set_values(int(a1.get()), int(b1.get()), int(c1.get()), int(d1.get()), int(e1.get()), int(f1.get()),
                   int((config['Covid 19 Parameters']['Mortality_Time'])),
                   int((config['Covid 19 Parameters']['Risk_Age'])),
                   int((config['Covid 19 Parameters']['Death_Percent'])),
                   int((config['Covid 19 Parameters']['Young_Death_Percent'])), config,
                   "Covid-19 Simulation")


# code to send the scenario selected by user
def scenarioselected():
    print("After GO: " + sc.get())
    if sc.get() == 'With Mask Mandate':
        with_mask()
    if sc.get() == 'Without Mask Mandate':
        normal()
    if sc.get() == 'Compare Two Viruses':
        compare_viruses()
    if sc.get() == 'Isolation':
        with_isolation()
    if sc.get() == 'Vaccine Availability and Efficacy':
        vaccine_availability_efficacy()
    else:
        pass


master = tk.Tk()
master.title("Covid Simulation")
master.geometry('800x800')

heading = tk.Label(master, text="Covid-19 Simulation", font="Arial 16 bold")

a = tk.Label(master, text="Population: ", font="Arial 14 ").grid(row=1, column=0)
b = tk.Label(master, text="Infected Percentage: ", font="Arial 14 ").grid(row=2, column=0)
c = tk.Label(master, text="Rate of Transmission: ", font="Arial 14 ").grid(row=3, column=0)
d = tk.Label(master, text="Probability of Transmission: ", font="Arial 14 ").grid(row=4, column=0)
e = tk.Label(master, text="Probability of Quarantine: ", font="Arial 14 ").grid(row=5, column=0)
f = tk.Label(master, text="Probability of Recovery Time: ", font="Arial 14 ").grid(row=6, column=0)

a1 = tk.Label(master, text="( Enter any number between the range 0 - infinity )", font="Calibri 8 ").grid(row=1,
                                                                                                          column=2)
b1 = tk.Label(master, text="( Enter any number between the range 0 - 50 ) ", font="Calibri  8 ").grid(row=2, column=2)
c1 = tk.Label(master, text="( Enter any number between the range 0 - 5 )  ", font="Calibri 8 ").grid(row=3, column=2)
d1 = tk.Label(master, text="( Enter any number between the range 0 - 100 )", font="Calibri 8 ").grid(row=4, column=2)
e1 = tk.Label(master, text="( Enter any number between the range 0 - 10 ) ", font="Calibri 8 ").grid(row=5, column=2)
f1 = tk.Label(master, text="( Enter any number between the range 0 - 300 )", font="Calibri 8 ").grid(row=6, column=2)

heading.grid(row=0, column=1, padx=10, pady=15)
a1 = tk.Entry(master)
b1 = tk.Entry(master)
c1 = tk.Entry(master)
d1 = tk.Entry(master)
e1 = tk.Entry(master)
f1 = tk.Entry(master)

a1.grid(row=1, column=1)
b1.grid(row=2, column=1)
c1.grid(row=3, column=1)
d1.grid(row=4, column=1)
e1.grid(row=5, column=1)
f1.grid(row=6, column=1)

btn = tk.Button(master, text="Submit", font="Arial 10 bold", fg="black", bg="light blue",
                command=test).grid(row=7, column=1, padx=10, pady=15)

tk.Label(master, text="Covid-19 Simulation", font=("Arial bold", 16))
# Combo Box
tk.Label(master, text="Select A Scenario", font=("Arial bold", 16)).grid(row=10, column=1, padx=20, pady=25)

# label
g = tk.Label(master, text="Select the Scenario to Simulate :", font="Arial 14").grid(row=12, column=0)

# Combobox creation
sc = tk.StringVar()
scenarioChoosen = Combobox(master, width=27, textvariable=sc)

# Adding combobox drop down list
scenarioChoosen['values'] = ("With Mask Mandate",
                             "Without Mask Mandate",
                             "Compare Two Viruses",
                             "Isolation",
                             "Vaccine Availability and Efficacy")

scenarioChoosen.grid(column=1, row=12)
scenarioChoosen.current(0)

go = tk.Button(master, text="GO", font="Arial 10 bold", fg="black", bg="light blue",
               command=scenarioselected).grid(row=13, column=1, padx=10, pady=12)

tk.mainloop()
