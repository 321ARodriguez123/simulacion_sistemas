import pygame
import math
import random
import sys
import time

# --- CONFIGURACIÓN Y CONSTANTES ---
WIDTH, HEIGHT = 1100, 600
FPS = 60

# Colores
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
RED = (200, 50, 50)
GREEN = (0, 180, 0)
GOLD = (212, 175, 55)
BG_COLOR = (25, 60, 40) # Verde casino
GRAY = (100, 100, 100)
DARK_GRAY = (40, 40, 40)

# Secuencia europea de la ruleta
ROULETTE_SEQ = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 
                8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]

def get_number_color(num):
    if num == 0: return GREEN
    red_nums = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
    return RED if num in red_nums else BLACK

class RouletteGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Ruleta de Casino Pro - Estadísticas")
        self.clock = pygame.time.Clock()
        
        # Fuentes
        self.font_small = pygame.font.SysFont('Arial', 16, bold=True)
        self.font_med = pygame.font.SysFont('Arial', 24, bold=True)
        self.font_large = pygame.font.SysFont('Arial', 64, bold=True)
        self.font_title = pygame.font.SysFont('Arial', 48, bold=True)
        
        # ESTADOS DEL JUEGO: "START_SCREEN" o "PLAYING"
        self.state = "START_SCREEN"
        self.input_text = "1000" # Valor por defecto
        
        # ESTADÍSTICAS Y SALDO
        self.initial_balance = 0
        self.balance = 0
        self.wins = 0
        self.losses = 0
        
        self.chip_values = [5, 10, 50, 100]
        self.current_chip = 10
        self.bets = {}
        
        # Estado de animación
        self.spinning = False
        self.angle = 0
        self.spin_speed = 0
        self.winner = None
        self.show_winner_timer = 0
        
        # Inicializar gráficos
        self.wheel_radius = 200
        self.wheel_surface = self._create_wheel_surface(self.wheel_radius)
        self.board_zones = self._create_board_zones()
        self.ui_zones = self._create_ui()

    def _create_wheel_surface(self, radius):
        surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        center = (radius, radius)
        slice_angle = 360 / 37
        
        for i, num in enumerate(ROULETTE_SEQ):
            start_angle = math.radians(i * slice_angle)
            end_angle = math.radians((i + 1) * slice_angle)
            color = get_number_color(num)
            
            points = [center]
            for a in range(int(math.degrees(start_angle)), int(math.degrees(end_angle)) + 1):
                rad = math.radians(a)
                points.append((center[0] + radius * math.cos(rad), center[1] + radius * math.sin(rad)))
            pygame.draw.polygon(surface, color, points)
            pygame.draw.polygon(surface, GOLD, points, 1)
            
            text = self.font_small.render(str(num), True, WHITE)
            text_angle = start_angle + (end_angle - start_angle) / 2
            text_x = center[0] + (radius - 30) * math.cos(text_angle) - text.get_width()//2
            text_y = center[1] + (radius - 30) * math.sin(text_angle) - text.get_height()//2
            surface.blit(text, (text_x, text_y))
            
        return surface

    def _create_board_zones(self):
        zones = {}
        start_x, start_y = 550, 200 # Bajé el tablero para dar espacio a las estadísticas
        cell_w, cell_h = 40, 50
        
        zones["0"] = pygame.Rect(start_x - cell_w, start_y, cell_w, cell_h * 3)
        for i in range(1, 37):
            col = (i - 1) // 3
            row = 2 - ((i - 1) % 3)
            zones[str(i)] = pygame.Rect(start_x + col * cell_w, start_y + row * cell_h, cell_w, cell_h)
            
        zones["Rojo"] = pygame.Rect(start_x + 3*cell_w, start_y + 3*cell_h + 10, cell_w*3, cell_h)
        zones["Negro"] = pygame.Rect(start_x + 6*cell_w, start_y + 3*cell_h + 10, cell_w*3, cell_h)
        zones["Par"] = pygame.Rect(start_x, start_y + 3*cell_h + 10, cell_w*3, cell_h)
        zones["Impar"] = pygame.Rect(start_x + 9*cell_w, start_y + 3*cell_h + 10, cell_w*3, cell_h)
        return zones

    def _create_ui(self):
        ui = {}
        ui["btn_spin"] = pygame.Rect(150, 480, 150, 50)
        for i, val in enumerate(self.chip_values):
            ui[f"chip_{val}"] = pygame.Rect(550 + (i*70), 480, 60, 60)
        return ui

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # MODO: Pantalla de inicio (Ingresar Saldo)
            if self.state == "START_SCREEN":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.input_text.strip() and int(self.input_text) > 0:
                            self.initial_balance = int(self.input_text)
                            self.balance = self.initial_balance
                            self.state = "PLAYING"
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        # Solo permitir números, máximo 7 dígitos
                        if event.unicode.isdigit() and len(self.input_text) < 7:
                            self.input_text += event.unicode
                            
            # MODO: Jugando
            elif self.state == "PLAYING":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos)

    def handle_click(self, pos):
        if self.spinning or self.show_winner_timer > 0: return 
        
        for zone, rect in self.board_zones.items():
            if rect.collidepoint(pos):
                if self.balance >= self.current_chip:
                    self.balance -= self.current_chip
                    self.bets[zone] = self.bets.get(zone, 0) + self.current_chip
                    return

        if self.ui_zones["btn_spin"].collidepoint(pos) and len(self.bets) > 0:
            self.start_spin()
                
        for i, val in enumerate(self.chip_values):
            if self.ui_zones[f"chip_{val}"].collidepoint(pos):
                self.current_chip = val

    def start_spin(self):
        self.spinning = True
        self.winner = None
        self.spin_speed = random.uniform(15, 25) 

    def update(self):
        if self.state != "PLAYING": return
        
        if self.spinning:
            self.angle += self.spin_speed
            self.spin_speed *= 0.985 
            if self.spin_speed < 0.05:
                self.spinning = False
                self.spin_speed = 0
                self.calculate_winner()
                self.show_winner_timer = 180 

        if self.show_winner_timer > 0:
            self.show_winner_timer -= 1
            if self.show_winner_timer == 1:
                self.bets.clear()

    def calculate_winner(self):
        final_angle = self.angle % 360
        slice_angle = 360 / 37
        index = int((360 - final_angle) / slice_angle) % 37
        self.winner = ROULETTE_SEQ[index]
        self.payout()

    def payout(self):
        win_amount = 0
        winner_str = str(self.winner)
        winner_color = "Rojo" if get_number_color(self.winner) == RED else "Negro" if get_number_color(self.winner) == BLACK else "Verde"
        
        for zone, amount in self.bets.items():
            if zone == winner_str:
                win_amount += amount * 36
            elif zone == winner_color:
                win_amount += amount * 2
            elif zone == "Par" and self.winner != 0 and self.winner % 2 == 0:
                win_amount += amount * 2
            elif zone == "Impar" and self.winner != 0 and self.winner % 2 != 0:
                win_amount += amount * 2

        self.balance += win_amount
        
        # Registrar estadística: Si el retorno es mayor a 0, se cuenta como ronda ganada
        if win_amount > 0:
            self.wins += 1
        else:
            self.losses += 1

    def draw_start_screen(self):
        self.screen.fill(BG_COLOR)
        
        title = self.font_title.render("RULETA CASINO PRO", True, GOLD)
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))
        
        subtitle = self.font_med.render("Ingresa tu saldo inicial para jugar:", True, WHITE)
        self.screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 250))
        
        # Caja de texto
        input_rect = pygame.Rect(WIDTH//2 - 150, 300, 300, 60)
        pygame.draw.rect(self.screen, DARK_GRAY, input_rect)
        pygame.draw.rect(self.screen, GOLD, input_rect, 3)
        
        # Cursor parpadeante
        cursor = "|" if time.time() % 1 > 0.5 else ""
        txt_surface = self.font_large.render(f"${self.input_text}{cursor}", True, WHITE)
        self.screen.blit(txt_surface, (input_rect.x + 20, input_rect.y - 5))
        
        btn_txt = self.font_small.render("Presiona ENTER para iniciar", True, GRAY)
        self.screen.blit(btn_txt, (WIDTH//2 - btn_txt.get_width()//2, 380))
        
        pygame.display.flip()

    def draw_game(self):
        self.screen.fill(BG_COLOR)
        
        # --- RULETA ---
        rotated_wheel = pygame.transform.rotate(self.wheel_surface, self.angle)
        wheel_rect = rotated_wheel.get_rect(center=(250, 250))
        self.screen.blit(rotated_wheel, wheel_rect.topleft)
        pygame.draw.polygon(self.screen, GOLD, [(450, 250), (470, 240), (470, 260)])
        
        # --- TABLERO ---
        for zone, rect in self.board_zones.items():
            if zone == "0": color = GREEN
            elif zone.isdigit(): color = get_number_color(int(zone))
            elif zone == "Rojo": color = RED
            elif zone == "Negro": color = BLACK
            else: color = BG_COLOR
            
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, WHITE, rect, 1)
            
            txt = self.font_small.render(zone, True, WHITE)
            self.screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))
            
            if zone in self.bets:
                pygame.draw.circle(self.screen, GOLD, rect.center, 15)
                pygame.draw.circle(self.screen, WHITE, rect.center, 15, 2)
                val_txt = self.font_small.render(str(self.bets[zone]), True, BLACK)
                self.screen.blit(val_txt, (rect.centerx - val_txt.get_width()//2, rect.centery - val_txt.get_height()//2))

        # --- PANEL DE ESTADÍSTICAS Y SALDO ---
        # 1. Saldo Actual
        bal_txt = self.font_title.render(f"Saldo: ${self.balance}", True, WHITE)
        self.screen.blit(bal_txt, (550, 30))
        
        # 2. Ganancia / Pérdida
        profit = self.balance - self.initial_balance
        if profit > 0:
            prof_txt = f"Ganancia: +${profit}"
            prof_color = GREEN
        elif profit < 0:
            prof_txt = f"Pérdida: -${abs(profit)}"
            prof_color = RED
        else:
            prof_txt = "Neto: $0"
            prof_color = GRAY
            
        profit_render = self.font_med.render(prof_txt, True, prof_color)
        self.screen.blit(profit_render, (550, 90))
        
        # 3. Rondas Ganadas / Perdidas
        stats_txt = self.font_med.render(f"Rondas Ganadas: {self.wins}  |  Perdidas: {self.losses}", True, GOLD)
        self.screen.blit(stats_txt, (550, 130))

        # --- INTERFAZ INFERIOR (UI) ---
        for val in self.chip_values:
            rect = self.ui_zones[f"chip_{val}"]
            color = GOLD if val == self.current_chip else GRAY
            pygame.draw.circle(self.screen, color, rect.center, 30)
            pygame.draw.circle(self.screen, WHITE, rect.center, 30, 3)
            chip_txt = self.font_med.render(f"${val}", True, BLACK)
            self.screen.blit(chip_txt, (rect.centerx - chip_txt.get_width()//2, rect.centery - chip_txt.get_height()//2))

        spin_rect = self.ui_zones["btn_spin"]
        spin_color = GREEN if len(self.bets) > 0 and not self.spinning else GRAY
        pygame.draw.rect(self.screen, spin_color, spin_rect, border_radius=10)
        spin_txt = self.font_med.render("GIRAR", True, WHITE)
        self.screen.blit(spin_txt, (spin_rect.centerx - spin_txt.get_width()//2, spin_rect.centery - spin_txt.get_height()//2))

        # --- ZOOM / GANADOR ---
        if self.winner is not None and self.show_winner_timer > 0:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            
            win_color = get_number_color(self.winner)
            pygame.draw.circle(self.screen, win_color, (WIDTH//2, HEIGHT//2), 100)
            pygame.draw.circle(self.screen, GOLD, (WIDTH//2, HEIGHT//2), 100, 5)
            
            win_txt = self.font_large.render(str(self.winner), True, WHITE)
            self.screen.blit(win_txt, (WIDTH//2 - win_txt.get_width()//2, HEIGHT//2 - win_txt.get_height()//2))
            
            msg = self.font_med.render("¡NÚMERO GANADOR!", True, GOLD)
            self.screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 140))

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            
            if self.state == "START_SCREEN":
                self.draw_start_screen()
            elif self.state == "PLAYING":
                self.update()
                self.draw_game()
                
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = RouletteGame()
    game.run()