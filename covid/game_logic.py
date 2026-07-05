import random

class CovidSimulation:
    def __init__(self, cols, rows, infection_prob=0.04, recovery_time=14, fatality_rate=0.01):
        self.cols = cols
        self.rows = rows
        self.infection_prob = infection_prob
        self.recovery_time = recovery_time
        self.fatality_rate = fatality_rate
        self.dia = 0
        
        self.grid = [[1 if random.random() > 0.25 else 0 for _ in range(cols)] for _ in range(rows)]
        self.timers = [[0 for _ in range(cols)] for _ in range(rows)]

        # 5 pacientes cero
        for _ in range(5):
            rx, ry = random.randint(0, cols-1), random.randint(0, rows-1)
            if self.grid[ry][rx] == 1:
                self.grid[ry][rx] = 2

    def get_state(self):
        """Retorna el estado actual para enviarlo a JavaScript"""
        stats = {'sanos': 0, 'infectados': 0, 'recuperados': 0, 'muertos': 0}
        
        for y in range(self.rows):
            for x in range(self.cols):
                val = self.grid[y][x]
                if val == 1: stats['sanos'] += 1
                elif val == 2: stats['infectados'] += 1
                elif val == 3: stats['recuperados'] += 1
                elif val == 4: stats['muertos'] += 1
                
        return {
            "grid": self.grid,
            "stats": stats,
            "dia": self.dia
        }

    def update_generation(self):
        """Calcula el siguiente turno matemático"""
        next_grid = [[self.grid[y][x] for x in range(self.cols)] for y in range(self.rows)]
        next_timers = [[self.timers[y][x] for x in range(self.cols)] for y in range(self.rows)]

        for y in range(self.rows):
            for x in range(self.cols):
                state = self.grid[y][x]

                if state == 1:
                    infected_neighbors = 0
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if i == 0 and j == 0: continue
                            col = (x + i + self.cols) % self.cols
                            row = (y + j + self.rows) % self.rows
                            if self.grid[row][col] == 2:
                                infected_neighbors += 1
                    
                    for _ in range(infected_neighbors):
                        if random.random() < self.infection_prob:
                            next_grid[y][x] = 2
                            break
                            
                elif state == 2:
                    next_timers[y][x] += 1
                    if next_timers[y][x] >= self.recovery_time:
                        if random.random() < self.fatality_rate:
                            next_grid[y][x] = 4
                        else:
                            next_grid[y][x] = 3
                        next_timers[y][x] = 0

        self.grid = next_grid
        self.timers = next_timers
        self.dia += 1