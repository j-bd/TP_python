#!/usr/bin/python3.6
# -*-coding:utf-8 -*

"""Labyrinth class to manage action in the labyrinth"""


class Labyrinth:
    """Labyrinth organization"""

    LIST_CHOICE = ['e', 'o', 'n', 's', 'q']


    def __init__(self, roboc, full_map):
        """Initializing the object"""
        self.roboc = roboc
        self.full_map = full_map


    def movement_choice(self):
        """Offer diferent possibility of movement to the gamer and return the choice"""
        while True:
            movement = input("Veuillez saisir votre choix en respectant le format :")
            while len(movement) > 2 or not movement:
                movement = input("Veuillez saisir votre choix en respectant le format :")
            if (len(movement) == 1 and isinstance(movement, str) and
                    movement.lower() in self.LIST_CHOICE):
                direction = movement.lower()
                number = 1
                break
            elif (len(movement) == 2) and (list(movement)[0].lower() in self.LIST_CHOICE):
                direction = list(movement)[0].lower()
                try:
                    number = int(list(movement)[1])
                except ValueError:
                    continue
                else:
                    break
        if direction in ['n', 'o']:
            pos = False
        else:
            pos = True

        return direction, number, pos


    def movement_possibility(self, line=0, column=0, pos=True):
        """Define the possiblity of moving "X" in the direction choosen
        Return the number of possible movement"""
        line_x, column_x = self.full_map.player_coordinates()
        movement = 0
        victory = False
        if line != 0 and pos:
            for step in range(1, line + 1):
                if self.full_map[line_x + step][column_x] == 'U':
                    movement += 1
                    victory = True
                    break
                elif self.full_map[line_x + step][column_x] != 'O':
                    movement += 1
                else:
                    break
        elif line != 0 and pos is False:
            for step in range(1, line + 1):
                if self.full_map[line_x - step][column_x] == 'U':
                    movement += 1
                    victory = True
                    break
                elif self.full_map[line_x - step][column_x] != 'O':
                    movement += 1
                else:
                    break
        elif column != 0 and pos:
            for step in range(1, column + 1):
                if self.full_map[line_x][column_x + step] == 'U':
                    movement += 1
                    victory = True
                    break
                elif self.full_map[line_x][column_x + step] != 'O':
                    movement += 1
                else:
                    break
        else:
            for step in range(1, column + 1):
                if self.full_map[line_x][column_x - step] == 'U':
                    movement += 1
                    victory = True
                    break
                elif self.full_map[line_x][column_x - step] != 'O':
                    movement += 1
                else:
                    break

        return movement, victory


    def coordinates_setter(self, line=0, column=0, pos=True):
        """Move the roboc 'X'"""
        if (line or column) != 0:
            line_x, column_x = self.full_map.player_coordinates()
            if pos:
                self.full_map[line_x + line, column_x + column] = 'X'
                self.full_map[line_x, column_x] = self.full_map._map_init_shape[line_x][column_x]
            else:
                self.full_map[line_x - line, column_x - column] = 'X'
                self.full_map[line_x, column_x] = self.full_map._map_init_shape[line_x][column_x]
