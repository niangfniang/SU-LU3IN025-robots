# Projet "robotique" IA&Jeux 2021
#
# Binome:
#  Prénom Nom: _________
#  Prénom Nom: _________

import random
import math
import braitenberg_loveBot as blb
import braitenberg_loveWall  as blw
import braitenberg_avoider as av
import braitenberg_hateBot as bhb
import braitenberg_hateWall  as bhw
import subsomption as s
import randomsearch as rch
def get_team_name():
    return "Ngamy-Niang" # à compléter (comme vous voulez)

def get_extended_sensors(sensors):
    for key in sensors:
        sensors[key]["distance_to_robot"] = 1.0
        sensors[key]["distance_to_wall"] = 1.0
        if sensors[key]["isRobot"] == True:
            sensors[key]["distance_to_robot"] = sensors[key]["distance"]
        else:
            sensors[key]["distance_to_wall"] = sensors[key]["distance"]
    return sensors

def step0(robotId, sensors):

    translation = 1 # vitesse de translation (entre -1 et +1)
    rotation = 0 # vitesse de rotation (entre -1 et +1)

    if sensors["sensor_front_left"]["distance"] < 1 or sensors["sensor_front"]["distance"] < 1:
        rotation = 0.5  # rotation vers la droite
    elif sensors["sensor_front_right"]["distance"] < 1:
        rotation = -0.5  # rotation vers la gauche

    if sensors["sensor_front"]["isRobot"] == True and sensors["sensor_front"]["isSameTeam"] == False:
        enemy_detected_by_front_sensor = True # exemple de détection d'un robot de l'équipe adversaire (ne sert à rien)

    return translation, rotation

#1-Braitenberg - lovebot

def step1(robotId, sensors): # <<<<<<<<<------- lovebot

  return av.step(robotId, sensors)


#2-Genetique

def fitness(vt,vr, sensors):

    return vt * (1-vr) *min([e["distance"] for e  in sensors.values()])
indice = 0
iterations = 0
def step(robotId, sensors):

    global iterations, indice
    # cet exemple montre comment générer au hasard, et évaluer, des stratégies comportementales
    # Remarques:
    # - l'évaluation est ici la distance moyenne parcourue, mais on peut en imaginer d'autres
    # - la liste "param", définie ci-dessus, permet de stocker les paramètres de la fonction de contrôle
    # - la fonction de controle est une combinaison linéaire des senseurs, pondérés par les paramètres

    # toutes les 400 itérations: le robot est remis au centre de l'arène avec une orientation aléatoire
    
    sensors = get_extended_sensors(sensors)
    """
    print (
        "[robot #",robotId,"] senseur frontal: (distance à l'obstacle =",sensors["sensor_front"]["distance"],")",
        "(robot =",sensors["sensor_front"]["isRobot"],")",
        "(distance_to_wall =", sensors["sensor_front"]["distance_to_wall"],")", # renvoie 1.0 si ce n'est pas un mur
        "(distance_to_robot =", sensors["sensor_front"]["distance_to_robot"],")"  # renvoie 1.0 si ce n'est pas un robot
    )"""

    comportement = [blb.step(robotId, sensors), av.step(robotId, sensors), s.step(robotId, sensors)]
   
    if iterations % 20 == 0:
        if iterations > 0 :            
            param = []
            for i in range(0, 8):
                param.append(random.randint(-1, 1))
   
            generation = 500

            for i in range(generation):
                j = random.randint(0,len(param)-1)
                fils = param[:]
                fils[j]=random.choice([e for e in range(-1,2) if e != param[j]])
                translation, rotation = comportement[indice] 
                indiceBestcomp = 0

                for k in range(0, len(comportement)):
                    translationFils ,rotationFils = comportement[k]
                    if fitness(translationFils, rotationFils, sensors) > fitness(translation, rotation, sensors):
                        indiceBestcomp = k
                        print("nouveau fils")
                        param = fils[:]
                        indice = k
                        translation = translationFils
                        rotation = rotationFils
    if indice == 1: 
        return (comportement[indice][0],comportement[indice][1] + random.random()-random.random())
                
    iterations += 1
    print("nb iterations : ", iterations)
    print("indice du comportement : ", indice)

    return comportement[indice]   #translation, rotation
