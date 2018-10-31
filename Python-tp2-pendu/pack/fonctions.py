#!/usr/bin/python3.6
# -*-coding:utf-8 -*

"""Pendu Game functions"""

import pickle


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
    print("Saisissez votre nom de joureur : ")
    answer = input()
    if answer in scores_dict.keys():
        return answer, scores_dict.get(answer), scores_dict
    else:
        return answer, 0, scores_dict


def gamer_letter(letter="0"):
    """Asking  the gamer to choose a letter and return it"""
    while letter.isalpha() != True or len(letter) > 1:
        print("S'il vous plait, choisissez votre lettre: ")
        letter = input()
    return letter.lower()


def replay(answer="0"):
    """Offer the possibility to play again"""
    while answer.lower() != "o" and answer.lower() != "n":
        print("Souhaitez-vous rejouer (o/n) ?")
        answer = input()
    return answer
    