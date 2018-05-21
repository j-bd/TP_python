import collections

def letter_count(word, letter):
	i = word.count(letter)
	print(f'dans le mot "{word}" il y a "{i}" fois la lettre "{letter}"')
	
def letters_count(word):
	i  = {
		x: word.count(x) 
		for x in word	
		}
	print (i)

def letters_count_bis(word):
	res = dict(collections.Counter(word))	
	print(res)
	
letter_count("programmation",'m')
letters_count("programmation")
letters_count_bis("programmation")
