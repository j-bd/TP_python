#!/usr/bin/python3.6
# -*-coding:utf-8 -*

"""Map class to manage map as an object"""

class Map:
    """Map exploration"""

    def __init__(self, name, shape):
        """Initializing the object"""
        self.name = name
        self.map = shape
        self._player_init_coord = self.player_coordinates()
        self._map_init_shape = self._raw_map()


    def __repr__(self):
        """Display the map (map with a string format)"""
        return self.map


    def __str__(self):
        """Display the map using 'print'"""
        return repr(self)


    def __len__(self):
        """Give the size of the string format map"""
        return len(self.map)


    def __getitem__(self, row):
        """Return the value of a position (line, column) in a string format"""
        map_grid = self.string_to_grid()
        return map_grid[row]


    def __setitem__(self, key, value):
        """Change the value of an element in the map string
        >>labyrinth
        'OOOOOOOOOO\nO O    O O\nO . OO   O\nO O O   XO\nO OOOO O.O\nO O O    U\nOOOOOOOOOO '
        >>l = Map('easy', labyrinth)
        >>l[3]
        ['O', ' ', 'O', ' ', 'O', ' ', ' ', ' ', 'X', 'O']
        >>l[3,2] = '.'
        >>l[3]
        ['O', ' ', '.', ' ', 'O', ' ', ' ', ' ', 'X', 'O']
        """
        map_grid = self.string_to_grid()
        map_grid[key[0]][key[1]] = value
        self.map = self.grid_to_string(map_grid)


    def grid_to_string(self, map_grid):
        """Transform a grid format map (list of list) into a string"""
        list_of_string = list()
        for line in map_grid:
            list_of_string.append(''.join(line))

        return '\n'.join(list_of_string)


    def string_to_grid(self):
        """Transform a string format map into a grid (list of list)"""
        map_grid = list()
        for line in self.map.splitlines():
            map_grid.append(list(line))

        return map_grid


    def player_coordinates(self):
        """Get the coordinates of the 'X' of a map grid. Return a list"""
        map_grid = self.string_to_grid()
        for line in map_grid:
            for element in line:
                if element == 'X':
                    coord_x = [map_grid.index(line), line.index(element)]

        return coord_x


    def _raw_map(self):
        """Return the map without the player 'X'"""
        coord_x = self.player_coordinates()
        map_grid = self.string_to_grid()
        map_grid[coord_x[0]][coord_x[1]] = ' '
        return map_grid


    def size(self):
        """Return the number of lines and columns of a map. A string format map is expected"""
        print(len(self.string_to_grid()), "lines and", len(self.string_to_grid()[0]), "columns")
        return len(self.string_to_grid()), len(self.string_to_grid()[0])
