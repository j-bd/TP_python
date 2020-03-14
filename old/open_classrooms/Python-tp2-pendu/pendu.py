#!/usr/bin/python3.6
# -*-coding:utf-8 -*

"""Pendu Game"""

import pickle

import pack.donnees
import pack.fonctions


print("Bienvenue dans le jeu du Pendu")
SCORES_DICT = pack.fonctions.scores_checking()
PLAYER, SCORE, SCORES_DICT = pack.fonctions.gamer_history(SCORES_DICT)
PLAY = bool(1)
ENDED = bool(1)

with open("pack/scores", "wb") as scores_file:

    while PLAY:
        if ENDED:
            word_to_guess, gamer_answer, attempt, ENDED = pack.fonctions.initiate()

        l = pack.fonctions.gamer_letter()
        for i in range(len(word_to_guess)):
            if word_to_guess[i] == l:
                gamer_answer[i] = l
        print(''.join(gamer_answer))

        if "*" not in gamer_answer:
            print(f"Vous avez gagne en {attempt + 1} coups. " +
                  f"Votre score est de {SCORE + pack.donnees.LIFE - attempt}")
            SCORES_DICT[PLAYER] = SCORE + pack.donnees.LIFE - attempt
            PLAY, ENDED = pack.fonctions.replay()
        elif attempt + 1 < pack.donnees.LIFE:
            print(f"Il vous reste {pack.donnees.LIFE - attempt- 1} coups")
            attempt += 1
        else:
            print(f"Vous avez perdu. La reponse est : {''.join(word_to_guess)}")
            PLAY, ENDED = pack.fonctions.replay()

    pickle.dump(SCORES_DICT, scores_file)
