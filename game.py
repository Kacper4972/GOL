import numpy as np

class GameOfLife:
    def __init__(self, rows=20, cols=20):
        self.rows = rows
        self.cols = cols
        self.grid = np.random.choice([0, 1], size=(rows, cols)).tolist()  # Plansza jako lista

    def next_generation(self):
        self.grid = np.array(self.grid)  # Konwersja listy na NumPy array
        
        new_grid = np.copy(self.grid)
        for row in range(self.rows):
            for col in range(self.cols):
                alive_neighbors = np.sum(self.grid[max(row-1, 0):min(row+2, self.rows),
                                                   max(col-1, 0):min(col+2, self.cols)]) - self.grid[row, col]
                if self.grid[row, col] == 1 and (alive_neighbors < 2 or alive_neighbors > 3):
                    new_grid[row, col] = 0  # Umiera
                elif self.grid[row, col] == 0 and alive_neighbors == 3:
                    new_grid[row, col] = 1  # Ożywa
        
        self.grid = new_grid.tolist()  # Konwersja na listę

    def get_grid(self):
        return self.grid  # Zwracamy listę dla JSON
