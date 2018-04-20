import random

def comparison(pc, utilisateur) :
	liste_result = ["Egalité", "Vous avez perdu", "Bravo ! Vous avez gagné"]
	print(f'Le choix du PC est {pc}, le votre est {utilisateur}')
	computer = liste_pfc.index(pc)
	player = liste_pfc.index(utilisateur)
	result = (computer - player + 3) %3
	print(liste_result[result])

def ask_to_user(text, choices) :
	print(f'{text} : {choices}')
	while True:
		choix_utilisateur = input().lower()
		if choix_utilisateur in choices :
			break
		print(f'Merci de saisir une des valeurs proposées {choices}')
	return choix_utilisateur

liste_pfc = ["pierre", "feuille", "ciseaux"]
liste_fin = ["o", "n"]


while True :

	answer = ask_to_user('Veuillez choisir une valeur de la liste suivante', liste_pfc)

	choix_pc = random.choice(liste_pfc)
	comparison(choix_pc, answer)

	answer = ask_to_user('Voulez-vous recommencer ? ', liste_fin)
	if answer == 'n' :
		break