import numpy as np
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import CanvasGrid, ChartModule

from violence.agents import Person, Family
from violence.input.generator import metropolis
from violence.model import Home

# dark grey
ADULT = "#757575"
# strong red
AGGRESSOR = "#CC0000"
# strong blue
VICTIM = "#0066CC"
# From Champagne to Bistre
colors = ["#ecd8beff", "#e7cfb7ff", "#e3c8b2ff", "#d7b8a3ff", "#c09987ff", "#c09987ff", "#ab7e6aff", "#966450ff",
          '#794d39ff', "#794d39ff", "#794d39ff", "#6b422dff", "#2c1903ff"]


def home_violence_portrayal(agent):
    if agent is None:
        return

    portrayal = {"Shape": "circle",
                 "x": agent.pos[0], "y": agent.pos[1],
                 "Filled": "true"}

    if type(agent) is Person:
        if agent.category == 'person':
            portrayal["Color"] = ADULT
            portrayal["r"] = 0.3
            portrayal["Layer"] = 1

        elif agent.category == 'victim':
            portrayal["Color"] = VICTIM
            portrayal["r"] = 0.1
            portrayal["Layer"] = 2

        elif agent.category == 'aggressor':
            portrayal["Color"] = AGGRESSOR
            portrayal["r"] = 0.3
            portrayal["Layer"] = 3

    elif type(agent) is Family:
        f, b = np.histogram(agent.context_stress, bins=len(colors), range=(0, 1))
        portrayal["Color"] = colors[f.argmax()]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


canvas_element = CanvasGrid(home_violence_portrayal, 40, 40, 480, 480)
chart_element = ChartModule([{"Label": "Person", "Color": ADULT},
                             {"Label": "Aggressor", "Color": AGGRESSOR},
                             {"Label": "Victim", "Color": VICTIM}])
another_chart = ChartModule([{"Label": "Stress", "Color": AGGRESSOR}])

model_params = {"model_scale": UserSettableParameter('slider', 'Model Scale', 1000, 100, 2000),
                "initial_families": UserSettableParameter('slider', 'Initial Families', 500, 20, 1000),
                "gender_stress": UserSettableParameter('slider', "Male Gender Stress", 0.80, 0.1, 1.0, 0.05),
                "is_working_pct": UserSettableParameter('slider', 'Percentage Employed', 0.9, 0.01, 1.0, 0.01),
                "chance_changing_working_status": UserSettableParameter('slider', 'Chance of Changing Working Status',
                                                                        0.05, 0.05, 1.0, 0.05),
                "pct_change_wage": UserSettableParameter('slider', 'Percentage of Changing Wage Chance',
                                                         0.05, 0.05, 1.0, 0.05),
                "metro": UserSettableParameter('choice', 'Metropolis to sample population', 'BRASILIA',
                                               choices=metropolis),
                "quarantine": UserSettableParameter('choice', 'Quarantine', False, choices=[False, True])
                }

server = ModularServer(Home, [canvas_element, chart_element, another_chart], "Home Violence", model_params)
server.port = 8521
