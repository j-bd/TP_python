#!/usr/bin/python3.6
# -*-coding:utf-8 -*

"""Roboc in a Labyrinth Game"""

import os
from datetime import datetime

from map import Map
from labyrinth import Labyrinth


VICTORY = False
LEAVE = False
POS = True


def labyrinth_offer():
    """List of existing labyrinths"""
    maps = list()
    for file in os.listdir("cartes"):
        if file.endswith(".txt"):
            maps.append(file)

    print("Labyrinthes existants :")
    for i, path in enumerate(maps):
        print(f"{i+1} - {path[:-3]}")

    return maps


def gamer_choice(maps):
    """Return the labyrinth choosen by the gamer and the name of the party"""
    choice = int()
    while choice not in range(1, len(maps) + 1):
        try:
            choice = int(input(f"Entrez un numéro de labyrinthe entre 1 et {len(maps)}"
                               " pour commencer à jouer : "))
        except ValueError:
            print("Veuillez saisir une valeur numerique.")

    path = os.path.join("cartes", maps[choice-1])

    # Recuperation du labyrinth
    with open(path, "r") as lab:
        labyrinth = lab.read()

    date_string = f'{datetime.now():%Y%m%d-%H_%M_%S}'
    file = os.path.join("cartes", maps[choice-1][:6] + date_string + '.txt')

    return labyrinth, file


def leaving(victory, file):
    """Execution of the end of the game either the gamer win or decide to leave"""
    if victory:
        os.remove(file)
        input("Félicitations ! Vous avez gagné !\n"
              "Appuyer sur n'importe quelle touche pour quitter")
    else:
        input(f"La partie a ete sauvegardee sous le nom \"{file}\"\n"
              "Appuyer sur n'importe quelle touche pour quitter")


#Beginning of the game
labyrinth, file = gamer_choice(labyrinth_offer())

with open(file, "w") as game:
    current_map = Map("lab_choosen", labyrinth)
    game.write(current_map.map)

    map_ongoing = Labyrinth(current_map.player_coordinates(), current_map)
    print(current_map)

    #Explanation
    print("Les fonctions de deplacement possible sont : \n"
          "A droite : 'E'    A gauche : 'O'    En haut : 'N'    En bas : 'S'\n"
          "Suivi du nombre de deplacement. Exemple : 'E2' ou 'S3' ou 'N'"
          " (pour un seul deplacement)\n"
          "Pour sauvegarder et quitter la partie : 'Q'\n")

    #The game
    while VICTORY is False and LEAVE is False:
        direction, number, POS = map_ongoing.movement_choice()
        if direction == "q":
            LEAVE = True
            game.seek(0)
            game.truncate()
            game.write(current_map.map)
        elif direction in ["n", "s"]:
            movement, VICTORY = map_ongoing.movement_possibility(number, 0, POS)
            for loop in range(0, movement):
                map_ongoing.coordinates_setter(1, 0, POS)
                game.write(current_map.map)
                print(current_map)
        else:
            movement, VICTORY = map_ongoing.movement_possibility(0, number, POS)
            for loop in range(0, movement):
                map_ongoing.coordinates_setter(0, 1, POS)
                game.write(current_map.map)
                print(current_map)

leaving(VICTORY, file)
