def line_count(file_stream):
	l =  file_stream.read()
	for i, c in enumerate(l.splitlines(), start = 1):
		print(f"La ligne numero {i} a pour contenu : {c}")

def character_count(file_stream):
	l =  list(file_stream.read())
	for j, d in enumerate(l, start = 1):
		print(f"Caractere {j} a pour valeur : {d}")

def word_count(file_stream):
	l =  file_stream.read()
	for j, d in enumerate(l.split(), start = 1):
		print(f"Le mot {j} a pour valeur : {d}")
		
print("Veuillez renseignez le chemin d'accès à votre fichier : ")
path = input()

with open(path, 'r', encoding = 'utf8') as f:
	line_count(f)

with open(path, 'r', encoding = 'utf8') as f:	
	character_count(f)

with open(path, 'r', encoding = 'utf8') as f:	
	word_count(f)