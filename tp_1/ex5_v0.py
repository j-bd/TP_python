
def line_length(line):
	nb_pts = len(line)
	length = 0
	while nb_pts > 1:
		result = distance (line[nb_pts-1], line[nb_pts-2])
		nb_pts = nb_pts - 1
		length = length + result
	print(f"Longueur de la ligne {line} = {length:.3f}")


def distance(point1, point2):
	dist = ((point2[0]-point1[0])**2 + (point2[1]-point1[1])**2)**0.5
	print(f"La distance entre {point1} et {point2} = {dist:.3f}")
	return dist

	
def main():
	print("Merci de saisir votre liste de points sous la forme x1,y1 x2,y2 ... : ")
	user_input = input()

	values = user_input.split(' ')
	print(f"values {values}")
	coordinates = []
	line_tmp = []
	for x in range(0,len(values)):
		coordinates.append(values[x].split(','))
		print(f"coordinates {coordinates}")
		
	for y in range(0, len(coordinates)):
		tmp = []
		for z in range(0, 2):
			tmp.append(float(coordinates[y][z]))
			print(f"tmp {tmp}")
		line_tmp.append(tuple(tmp))
		print(f"line_tmp{line_tmp}")

	line = tuple(line_tmp)
	print(f"Les coordonnées saisies sont {line}")

	line_length(line)

main()

