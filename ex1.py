import collections

def compter_lettre(word, letter):
	i = word.count(letter)
	print(f'dans le mot "{word}" il y a "{i}" fois la lettre "{letter}"')
	
def compter_lettres(word):
	i  = {
		x: word.count(x) 
		for x in word
		
	}
	print (i)

	
def compter_lettres_bis(word) :
	res = dict(collections.Counter(word))	
	print(res)
	
#compter_lettre("programmation",'m')
#compter_lettres("programmation")
compter_lettres_bis("programmation")
