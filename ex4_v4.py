def compter_lignes(chemin_fichier) :
	l =  chemin_fichier.read()
	for i, c in enumerate(l.splitlines(), start = 1) :
		print(f"La ligne numero {i} a pour contenu : {c}")

def compter_caracteres(chemin_fichier) :
	l =  list(chemin_fichier.read())
	for j, d in enumerate(l, start = 1) :
		print(f"Caractere {j} a pour valeur : {d}")

def compter_mots(chemin_fichier) :
	l =  chemin_fichier.read()
	for j, d in enumerate(l.split(), start = 1) :
		print(f"Le mot {j} a pour valeur : {d}")
		
print("Veuillez renseignez le chemin d'accès à votre fichier : ")
path = input()

with open(path, 'r', encoding = 'utf8') as f :
	compter_lignes(f)

with open(path, 'r', encoding = 'utf8') as f :	
	compter_caracteres(f)

with open(path, 'r', encoding = 'utf8') as f :	
	compter_mots(f)