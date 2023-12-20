import ac
import acsys
import configparser
import sys
import os
import platform
import re

if platform.architecture()[0] == "64bit":
    libdir = 'third_party_tiretemp/lib64'
else:
    libdir = 'third_party_tiretemp/lib'
sys.path.insert(0, os.path.join(os.path.dirname(__file__), libdir))
os.environ['PATH'] = os.environ['PATH'] + ";."

import ctypes
from third_party_tiretemp.sim_info import info
from ctypes.wintypes import MAX_PATH

appName = "Tire Temps"
app_path = "apps/python/Tire Temp/"
width, height = 260 , 230 
tyre_outline = ac.newTexture(app_path + "tyre_outline.png")
tyre_temp_inside = [100, 100, 100, 100]
ideal_pressure_front = 0
ideal_pressure_rear = 0
tyre_practical_temperature = [0] * 4
tyre_temperature = [0] * 4
tyre_temperatureI = [0] * 4
tyre_temperatureM = [0] * 4
tyre_temperatureO = [0] * 4
tyre_color = [0.8, 0.82, 0.92, 1] * 4
outline_color = [0.8, 0.82, 0.92, 1] * 4
minimum_optimal_temperature = 0
maximum_optimal_temperature = 0
tyre_compound = 0
compound_cleaned = ""
config_path = app_path + "config.ini"
compounds_path = app_path + "compounds/"
car_name = ""
tyre_temperatureI_label_FL = ""
tyre_temperatureI_label_FR = ""
tyre_temperatureI_label_RL = ""
tyre_temperatureI_label_RR = ""
tyre_temperatureI_FL = ""
tyre_temperatureI_FR = ""
tyre_temperatureI_RL = ""
tyre_temperatureI_RR = ""
tyre_temperatureM_label_FL = ""
tyre_temperatureM_label_FR = ""
tyre_temperatureM_label_RL = ""
tyre_temperatureM_label_RR = ""
tyre_temperatureM_FL = ""
tyre_temperatureM_FR = ""
tyre_temperatureM_RL = ""
tyre_temperatureM_RR = ""
tyre_temperatureO_label_FL = ""
tyre_temperatureO_label_FR = ""
tyre_temperatureO_label_RL = ""
tyre_temperatureO_label_RR = ""
tyre_temperatureO_FL = ""
tyre_temperatureO_FR = ""
tyre_temperatureO_RL = ""
tyre_temperatureO_RR = ""
tyre_core_temp_label_FL = ""
tyre_core_temp_label_FR = ""
tyre_core_temp_label_RL = ""
tyre_core_temp_label_RR = ""
tyre_core_temp_FL = ""
tyre_core_temp_FR = ""
tyre_core_temp_RL = ""
tyre_core_temp_RR = ""

config = configparser.ConfigParser()
config.read(config_path)

# The initializer of the app's window. 
def acMain(ac_version):
    global appWindow 
    global car_name
    global compounds, mod_compounds
    global tyre_temperatureI_label_FL, tyre_temperatureI_label_FR, tyre_temperatureI_label_RL, tyre_temperatureI_label_RR
    global tyre_temperatureM_label_FL, tyre_temperatureM_label_FR, tyre_temperatureM_label_RL, tyre_temperatureM_label_RR
    global tyre_temperatureO_label_FL, tyre_temperatureO_label_FR, tyre_temperatureO_label_RL, tyre_temperatureO_label_RR
    global tyre_core_temp_label_FL, tyre_core_temp_label_FR, tyre_core_temp_label_RL, tyre_core_temp_label_RR

    appWindow = ac.newApp(appName)
    ac.setTitle(appWindow, appName)
    ac.setSize(appWindow, width, height)

    car_name = ac.getCarName(0)

    tyre_temperatureI_label_FL = ac.addLabel(appWindow, "I: ")
    ac.setPosition(tyre_temperatureI_label_FL, 0, 40)
    tyre_temperatureM_label_FL = ac.addLabel(appWindow, "M: ")
    ac.setPosition(tyre_temperatureM_label_FL, 0, 60)
    tyre_temperatureO_label_FL = ac.addLabel(appWindow, "O: ")
    ac.setPosition(tyre_temperatureO_label_FL, 0, 80)

    tyre_temperatureI_label_FR = ac.addLabel(appWindow, "I: ")
    ac.setPosition(tyre_temperatureI_label_FR, 220, 40)
    tyre_temperatureM_label_FR = ac.addLabel(appWindow, "M: ")
    ac.setPosition(tyre_temperatureM_label_FR, 220, 60)
    tyre_temperatureO_label_FR = ac.addLabel(appWindow, "O: ")
    ac.setPosition(tyre_temperatureO_label_FR, 220, 80)

    tyre_temperatureI_label_RL = ac.addLabel(appWindow, "I: ")
    ac.setPosition(tyre_temperatureI_label_RL, 0, 130)
    tyre_temperatureM_label_RL = ac.addLabel(appWindow, "M: ")
    ac.setPosition(tyre_temperatureM_label_RL, 0, 150)
    tyre_temperatureO_label_RL = ac.addLabel(appWindow, "O: ")
    ac.setPosition(tyre_temperatureO_label_RL, 0, 170)

    tyre_temperatureI_label_RR = ac.addLabel(appWindow, "I: ")
    ac.setPosition(tyre_temperatureI_label_RR, 220, 130)
    tyre_temperatureM_label_RR = ac.addLabel(appWindow, "M: ")
    ac.setPosition(tyre_temperatureM_label_RR, 220, 150)
    tyre_temperatureO_label_RR = ac.addLabel(appWindow, "O: ")
    ac.setPosition(tyre_temperatureO_label_RR, 220, 170)
 
    tyre_core_temp_label_FL = ac.addLabel(appWindow, "TEMP: ")
    ac.setPosition(tyre_core_temp_label_FL, 90, 30)
    tyre_core_temp_label_FR = ac.addLabel(appWindow, "TEMP: ")
    ac.setPosition(tyre_core_temp_label_FR, 140, 30)
    tyre_core_temp_label_RL = ac.addLabel(appWindow, "TEMP: ")
    ac.setPosition(tyre_core_temp_label_RL, 90, 180)
    tyre_core_temp_label_RR = ac.addLabel(appWindow, "TEMP: ")
    ac.setPosition(tyre_core_temp_label_RR, 140, 180)

    ac.addRenderCallback(appWindow, appGL) 

    compounds = configparser.ConfigParser()
    compounds.read(compounds_path + "compounds.ini")
    mod_compounds = configparser.ConfigParser()
    mod_compounds.read(compounds_path + "mod_compounds.ini")

    return appName

# Updates the data on the app. 
def acUpdate(deltaT):
    global tyre_temperatureI_label_FL, tyre_temperatureI_FL, tyre_temperatureI_label_FR, tyre_temperatureI_FR, tyre_temperatureI_label_RL, tyre_temperatureI_RL, tyre_temperatureI_label_RR, tyre_temperatureI_RR
    global tyre_temperatureM_label_FL, tyre_temperatureM_FL, tyre_temperatureM_label_FR, tyre_temperatureM_FR, tyre_temperatureM_label_RL, tyre_temperatureM_RL, tyre_temperatureM_label_RR, tyre_temperatureM_RR
    global tyre_temperatureO_label_FL, tyre_temperatureO_FL, tyre_temperatureO_label_FR, tyre_temperatureO_FR, tyre_temperatureO_label_RL, tyre_temperatureO_RL, tyre_temperatureO_label_RR, tyre_temperatureO_RR
    global tyre_core_temp_label_FL, tyre_core_temp_FL, tyre_core_temp_label_FR, tyre_core_temp_FR, tyre_core_temp_label_RL, tyre_core_temp_RL, tyre_core_temp_label_RR, tyre_core_temp_RR

    tyre_temperatureI_FL = info.physics.tyreTempI[0]
    tyre_temperatureM_FL = info.physics.tyreTempM[0]
    tyre_temperatureO_FL = info.physics.tyreTempO[0]

    tyre_temperatureI_FR = info.physics.tyreTempI[1]
    tyre_temperatureM_FR = info.physics.tyreTempM[1]
    tyre_temperatureO_FR = info.physics.tyreTempO[1]

    tyre_temperatureI_RL = info.physics.tyreTempI[2]
    tyre_temperatureM_RL = info.physics.tyreTempM[2]
    tyre_temperatureO_RL = info.physics.tyreTempO[2]

    tyre_temperatureI_RR = info.physics.tyreTempI[3]
    tyre_temperatureM_RR = info.physics.tyreTempM[3]
    tyre_temperatureO_RR = info.physics.tyreTempO[3]

    tyre_core_temp_FL = info.physics.tyreCoreTemperature[0]
    tyre_core_temp_FR = info.physics.tyreCoreTemperature[1]
    tyre_core_temp_RL = info.physics.tyreCoreTemperature[2]
    tyre_core_temp_RR = info.physics.tyreCoreTemperature[3]

    ac.setText(tyre_temperatureI_label_FL, "I: {:.0f}".format(tyre_temperatureI_FL))
    ac.setText(tyre_temperatureM_label_FL, "M: {:.0f}".format(tyre_temperatureM_FL))
    ac.setText(tyre_temperatureO_label_FL, "O: {:.0f}".format(tyre_temperatureO_FL))

    ac.setText(tyre_temperatureI_label_FR, "I: {:.0f}".format(tyre_temperatureI_FR))
    ac.setText(tyre_temperatureM_label_FR, "M: {:.0f}".format(tyre_temperatureM_FR))
    ac.setText(tyre_temperatureO_label_FR, "O: {:.0f}".format(tyre_temperatureO_FR))

    ac.setText(tyre_temperatureI_label_RL, "I: {:.0f}".format(tyre_temperatureI_RL))
    ac.setText(tyre_temperatureM_label_RL, "M: {:.0f}".format(tyre_temperatureM_RL))
    ac.setText(tyre_temperatureO_label_RL, "O: {:.0f}".format(tyre_temperatureO_RL))

    ac.setText(tyre_temperatureI_label_RR, "I: {:.0f}".format(tyre_temperatureI_RR))
    ac.setText(tyre_temperatureM_label_RR, "M: {:.0f}".format(tyre_temperatureM_RR))
    ac.setText(tyre_temperatureO_label_RR, "O: {:.0f}".format(tyre_temperatureO_RR))

    ac.setText(tyre_core_temp_label_FL, "{}°C".format(round(tyre_core_temp_FL)))
    ac.setText(tyre_core_temp_label_FR, "{}°C".format(round(tyre_core_temp_FR)))
    ac.setText(tyre_core_temp_label_RL, "{}°C".format(round(tyre_core_temp_RL)))
    ac.setText(tyre_core_temp_label_RR, "{}°C".format(round(tyre_core_temp_RR)))    

    update_tyres()


# OpenGL update. 
def appGL(deltaT):
    ac.glColor4f(tyre_color[0][0], tyre_color[0][1], tyre_color[0][2], tyre_color[0][3]) # FL
    tyre(90, 100, 25, -50 * tyre_temp_inside[0] / 100)

    ac.glColor4f(tyre_color[2][0], tyre_color[2][1], tyre_color[2][2], tyre_color[2][3]) # RL
    tyre(90, 180, 25, -50 * tyre_temp_inside[2] / 100)

    ac.glColor4f(tyre_color[1][0], tyre_color[1][1], tyre_color[1][2], tyre_color[1][3]) # FR
    tyre(140, 100, 25, -50 * tyre_temp_inside[1] / 100)

    ac.glColor4f(tyre_color[3][0], tyre_color[3][1], tyre_color[3][2], tyre_color[3][3]) # RR
    tyre(140, 180, 25, -50 * tyre_temp_inside[3] / 100)

# Draws the tyres. 
def tyre(x, y, width, height):
    ac.glBegin(acsys.GL.Quads)
    ac.glVertex2f(x, y)
    ac.glVertex2f(x, (y + height))
    ac.glVertex2f((x + width), (y + height))
    ac.glVertex2f((x + width), y)
    ac.glEnd()

# Updates the colors of the tyres depending on the temperature & is used in the acUpdate method. 
def update_tyres():
    global minimum_optimal_temperature, maximum_optimal_temperature, ideal_pressure_front, ideal_pressure_rear
    global tyre_practical_temperature, tyre_compound, compound_cleaned
    global tyre_temperatureI, tyre_temperatureO, tyre_temperatureM
    global car_name

    tyre_compound = info.graphics.tyreCompound
    tyre_temperature = info.physics.tyreCoreTemperature
    tyre_temperatureI = info.physics.tyreTempI
    tyre_temperatureM = info.physics.tyreTempM
    tyre_temperatureO = info.physics.tyreTempO

    # Setting the ideal temps.
    compound_cleaned = re.sub('\_+$', '', re.sub(r'[^\w]+', '_', tyre_compound)).lower()

    if compounds.has_section(car_name + "_" + compound_cleaned):
        ideal_pressure_front = int(compounds.get(car_name + "_" + compound_cleaned, "IDEAL_PRESSURE_F"))
        ideal_pressure_rear = int(compounds.get(car_name + "_" + compound_cleaned, "IDEAL_PRESSURE_R"))

        minimum_optimal_temperature = int(compounds.get(car_name + "_" + compound_cleaned, "MIN_OPTIMAL_TEMP"))
        maximum_optimal_temperature = int(compounds.get(car_name + "_" + compound_cleaned, "MAX_OPTIMAL_TEMP"))

    elif mod_compounds.has_section(compound_cleaned):
        minimum_optimal_temperature = int(mod_compounds.get(compound_cleaned, "MIN_OPTIMAL_TEMP"))
        maximum_optimal_temperature = int(mod_compounds.get(compound_cleaned, "MAX_OPTIMAL_TEMP"))
    
    for i in range(4):
        tyre_practical_temperature[i] = 0.25 * ((tyre_temperatureI[i] + tyre_temperatureM[i] + tyre_temperatureO[i]) / 3) + 0.75 * \
                                           tyre_temperature[i]
        
    # Temperature for determining the color of the tires.   
    if minimum_optimal_temperature:
        for i in range(4):
            temperature = tyre_practical_temperature[i]

            if temperature > (maximum_optimal_temperature + 20):
                # Too hot (Red)
                tyre_color[i] = [1, 0, 0, 1]
            elif temperature > maximum_optimal_temperature:
                # Transition from blue to red as it gets hotter
                factor = (temperature - maximum_optimal_temperature) / 20
                tyre_color[i] = [2.0 + factor * 1.0, 0.18 - factor * 0.18, 0.0, 1]
            elif temperature > minimum_optimal_temperature:
                # Ideal temperature (Light Green)
                factor = (temperature - minimum_optimal_temperature) / (maximum_optimal_temperature - minimum_optimal_temperature)
                tyre_color[i] = [0.0 + factor * 0.6, 3 - factor * 0.8, 0.0 + factor * 0.2, 1]
            elif temperature > (minimum_optimal_temperature - 20):
                # Transition from green to blue as it gets colder
                factor = (temperature - minimum_optimal_temperature) / (20)
                tyre_color[i] = [0.0 + factor * 0.6, 0.0, 0.8 + factor * 0.2, 1]
            else:
                # Too cold (Dark Blue)
                tyre_color[i] = [0, 0.18, 0.80, 1]
    else:
        # Default color when conditions are not met (Ideal temperature)
        tyre_color[0] = [0.8, 255, 0.92, 1]
        tyre_color[1] = [0.8, 255, 0.92, 1]
        tyre_color[2] = [0.8, 255, 0.92, 1]
        tyre_color[3] = [0.8, 255, 0.92, 1]

# Initializes the user's AC folder. 
def init_ac_folder(): 
   global ac_user_folder

   dll = ctypes.windll.shell32
   buf = ctypes.create_unicode_buffer(MAX_PATH + 1)

   if dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False):
      document_folder = buf.value
      ac_folder = os.path.join(document_folder, 'Assetto Corsa')

      if os.path.isdir(ac_folder):
         ac_user_folder = ac_folder
         
# Used for when the application exits. This is here for safety.
def acShutdown():
   return