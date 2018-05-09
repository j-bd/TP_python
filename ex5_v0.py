
def longueur_ligne():
	nb_pts = len(ligne)
	longueur = 0
	while nb_pts > 1 :
		resultat = distance (ligne[nb_pts-1], ligne[nb_pts-2])
		nb_pts = nb_pts - 1
		longueur = longueur + resultat
	print(f"Longueur de la ligne {ligne} = {longueur}")


def distance(point1, point2) :
	dist = round(((point2[0]-point1[0])**2 + (point2[1]-point1[1])**2)**0.5, 3)
	print(f"La distance entre {point1} et {point2} = {dist}")
	return dist

#ligne = ((0, 0), (2, 3), (3, 4), (4, 4))
print("Merci de saisir votre liste de points sous la forme x1,y1 x2,y2 ... : ")
saisie_utilisateur = input()

valeurs = saisie_utilisateur.split(' ')
coordonnees = []
ligne_tmp = []
for x in range(0,len(valeurs)) :
	coordonnees.append(valeurs[x].split(','))
	
for y in range(0, len(coordonnees)) :
	tmp = []
	for z in range(0, 2) :
		tmp.append(int(coordonnees[y][z]))
	ligne_tmp.append(tuple(tmp))

ligne = tuple(ligne_tmp)
print(f"Les coordonnées saisies sont {ligne}")

longueur_ligne()