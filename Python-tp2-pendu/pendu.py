#!/usr/bin/python3.6
# -*-coding:utf-8 -*

"""Pendu Game"""

import pickle
import random

import pack.donnees
import pack.fonctions


print("Bienvenue dans le jeu du Pendu")
scores_dict = pack.fonctions.scores_checking()
player, score, scores_dict = pack.fonctions.gamer_history(scores_dict)
attempt = 0

with open("pack/scores", "wb") as scores_file:

    word_to_guess = list(random.choice(pack.donnees.WORDS))
    gamer_answer = ["*"] * len(word_to_guess)
    print(''.join(gamer_answer))

    while attempt < pack.donnees.LIFE:
        l = pack.fonctions.gamer_letter()
        for i in range(len(word_to_guess)):
            if word_to_guess[i] == l:
                gamer_answer[i] = l
        print(''.join(gamer_answer))

        if "*" not in gamer_answer:
            print(f"Vous avez gagne en {attempt + 1} coups. " +
                  f"Votre score est de {score + pack.donnees.LIFE - attempt}")
            scores_dict[player] = score + pack.donnees.LIFE - attempt
            break
        elif attempt + 1 < pack.donnees.LIFE:
            print(f"Il vous reste {pack.donnees.LIFE - attempt- 1} coups")
            attempt += 1
        else:
            print(f"Vous avez perdu. La reponse est : {''.join(word_to_guess)}")
            if pack.fonctions.replay() == 'o':
                word_to_guess = list(random.choice(pack.donnees.WORDS))
                gamer_answer = ["*" for x in word_to_guess]
                print(''.join(gamer_answer))
                attempt = 0
            else:
                attempt += 1

    pickle.dump(scores_dict, scores_file)
