from random import randint

a = randint(0, 10)
nb_coup = 0
print('Le nombre mystère est une valeur entre 0 et 10. Entrez votre valeur :')

val = 101
while val != a :
	val = int(input())
	if val > a :
		print("Trop grand ! Retentez :")
	if val < a :
		print("Trop petit ! Retentez :")
	nb_coup += 1

print(f'Bravo, vous avez trouvé le nombre mystère en {nb_coup} coup')
