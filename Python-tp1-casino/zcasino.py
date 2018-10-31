#!/usr/bin/python3.6
# -*-coding:utf-8 -*

"""Casino Game"""

from random import randrange


def selection(text, min_val, max_val):
    """User selection between two values"""
    while True:
        try:
            print(text, min_val, max_val)
            choice = int(input())
            if (choice >= min_val and choice < max_val + 1) == False:
                print(f"Valeur min attendue {min_val}, valeur max attendue {max_val}")
                continue
        except ValueError:
            print("Veuillez saisir un nombre")
        else:
            break
    return choice


def casino(money, choice, bet, result):
    """Result of the gain or of the loss"""
    if result == choice:
        money += bet * 3
        print(f"C'est le bon nombre, la chance est avec vous ! Vous disposez de {money} $")
    elif (choice % 2 == 0 and result % 2 == 0) or (choice % 2 != 0 and result % 2 != 0):
        money += bet * 0.5
        print(f"C'est la bonne couleur, la chance est avec vous ! Vous disposez de {money} $")
    else:
        money -= bet
        print(f"Perdu, n'hesitez pas a retenter votre chance. Vous disposez de {money} $")

    return money


money = 50 #Amount of money at the beginning

while True:
    choice = selection("Merci de rentrer le numero choisi entre:", 0, 49)
    bet = selection("Merci d'indiquer votre mise entre: ", 1, money)

    result = randrange(50)
    print(f"Le numero sortie de la roulette est le {result}")

    money = casino(money, choice, bet, result)

    if money <= 0:
        print("C'est fini, vous n'avez plus d'argent")
        break
    else:
        leave = ""
        while leave.lower() != "o" and leave.lower() != "n":
            print("Voulez-vous continuer (o/n) ?")
            leave = input()
        if leave.lower() == "n":
            print(f"Vous quittez le casino avec un gain de {money}$")
            break
        elif leave.lower() == "o":
            print("C'est reparti !")
