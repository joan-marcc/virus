import pygame
import random

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
WIDTH = 1200
HEIGHT = 900

# Colores
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128, 100)

# Clase para representar a los círculos
class Circle:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.infected = False
        self.infected_time = 0
        self.speed = random.randint(1, 3)
        self.direction = random.choice([-1, 1]), random.choice([-1, 1])

    def update(self):
        self.x += self.speed * self.direction[0]
        self.y += self.speed * self.direction[1]

        # Rebotar en los bordes de la ventana
        if self.x <= self.radius or self.x >= WIDTH - self.radius:
            self.direction = -self.direction[0], self.direction[1]
        if self.y <= self.radius or self.y >= HEIGHT - self.radius:
            self.direction = self.direction[0], -self.direction[1]

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

# Crear la ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulación de Infectados")

# Lista de círculos
circles = []

# Crear círculo inicial infectado
x = random.randint(50, WIDTH - 50)
y = random.randint(50, HEIGHT - 50)
circle = Circle(x, y, 10, RED)
circle.infected = True
circle.infected_time = pygame.time.get_ticks()
circles.append(circle)

# Crear círculos no infectados
for _ in range(99):
    x = random.randint(50, WIDTH - 50)
    y = random.randint(50, HEIGHT - 50)
    circle = Circle(x, y, 10, GREEN)
    circles.append(circle)

# Variables de tiempo
clock = pygame.time.Clock()

# Variables para la gráfica
infected_count = 1
healthy_count = 9

# Fuente de texto
font = pygame.font.Font(None, 20)

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Actualizar el estado de los círculos
    current_time = pygame.time.get_ticks()
    for circle in circles:
        if circle.infected and current_time - circle.infected_time >= 5000:
            circle.infected = False
            circle.color = GREEN

        circle.update()

    # Verificar colisiones y propagar infección
    for i, circle1 in enumerate(circles):
        if circle1.infected:
            for j, circle2 in enumerate(circles):
                if not circle2.infected and i != j:
                    distance = ((circle1.x - circle2.x) ** 2 + (circle1.y - circle2.y) ** 2) ** 0.5
                    if distance <= circle1.radius + circle2.radius:
                        circle2.infected = True
                        circle2.color = RED
                        circle2.infected_time = pygame.time.get_ticks()

    # Contar la cantidad de infectados y sanos
    infected_count = sum(circle.infected for circle in circles)
    healthy_count = sum(not circle.infected for circle in circles)

    # Limpiar la pantalla
    screen.fill(BLACK)

    # Dibujar los círculos en la pantalla
    for circle in circles:
        circle.draw()

    # Dibujar la gráfica semitransparente
    pygame.draw.rect(screen, GRAY, (10, 10, 150, 60))
    text1 = font.render(f"Infectados: {infected_count}", True, RED)
    text2 = font.render(f"Sanos: {healthy_count}", True, GREEN)
    screen.blit(text1, (20, 20))
    screen.blit(text2, (20, 40))

    # Actualizar la ventana
    pygame.display.flip()

    # Controlar la velocidad de actualización
    clock.tick(60)

# Cerrar Pygame
pygame.quit()

