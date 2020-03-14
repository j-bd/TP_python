#!/usr/bin/python3.6
# -*-coding:utf-8 -*

"""Pendu Game functions"""

import pickle
import random

import pack.donnees


def scores_checking():
    """Checking and returning if an history of scores is already existing or create it"""
    try:
        players_history = open("pack/scores", "rb")
    except FileNotFoundError:
        players_history = open("pack/scores", "wb")
        scores_dict = dict()
        save = pickle.Pickler(players_history)
        save.dump(scores_dict)
    else:
        scores_history = pickle.Unpickler(players_history)
        scores_dict = scores_history.load()
    finally:
        players_history.close()
    return scores_dict


def gamer_history(scores_dict):
    """Checking if the gamer have already a score and create one if not"""
    answer = input("Saisissez votre nom de joureur : ")
    return answer, scores_dict.get(answer, 0), scores_dict


def gamer_letter():
    """Asking  the gamer to choose a letter and return it"""
    letter = input("S'il vous plait, choisissez votre lettre: ")
    while letter.isalpha() is False or len(letter) > 1:
        letter = input("Veuillez ressaisir votre lettre: ")
    return letter.lower()


def replay():
    """Offer the possibility to play again"""
    answer = input("Souhaitez-vous rejouer (o/n) ?")
    while answer.lower() != "o" and answer.lower() != "n":
        answer = input("Veuillez ressaisir votre choix. Souhaitez-vous rejouer (o/n) ?")

    if answer == 'o':
        play = bool(1)
    else:
        play = bool(0)
    return play, bool(1)


def initiate():
    """Return the word to guess by the player"""
    word_to_guess = list(random.choice(pack.donnees.WORDS))
    gamer_answer = ["*" for x in word_to_guess]
    print(''.join(gamer_answer))
    return word_to_guess, gamer_answer, 0, bool(0)
