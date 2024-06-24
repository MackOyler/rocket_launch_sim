import pygame
import sys
import math
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
EARTH_GRAVITY = 9.81  # m/s^2
MAX_THRUST = 1500000  # in Newtons
BURN_RATE = 500  # fuel burn rate in kg/s
TIME_STEP = 0.1  # simulation time step in seconds
TILT_STEP = 0.02  # Tilt step for left/right movement
MAX_TILT = 0.5  # Maximum tilt angle in radians (about 28.6 degrees)


# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rocket Launch Simulation")

class Rocket:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 60  # Start at the bottom of the screen, above the ground
        self.vx = 0
        self.vy = 0
        self.mass = 50000  # in kg
        self.fuel = 40000  # in kg
        self.thrust = 0  # Initial thrust is zero
        self.burn_rate = BURN_RATE
        self.angle = 0  # Angle of the rocket in radians
        self.launched = False  # Whether the rocket has been launched

    def launch(self):
        print("Launch method called")  # Debug print
        if not self.launched and self.fuel > 0:
            self.thrust = 1200000  # Initial thrust to counteract gravity
            self.launched = True
            print("Rocket launched!")  # Debug print

    def abort(self):
        self.__init__()  # Reset the rocket to its initial state

    def update(self):
        if self.launched:
            if self.fuel > 0 and self.thrust > 0:
                thrust_acceleration = self.thrust / self.mass
                self.fuel -= self.burn_rate * TIME_STEP
                self.mass -= self.burn_rate * TIME_STEP
                print(f"Thrust: {self.thrust}, Fuel: {self.fuel}, Mass: {self.mass}")  # Debug print
            else:
                thrust_acceleration = 0

            # Calculate acceleration
            ax = thrust_acceleration * math.sin(self.angle)
            ay = thrust_acceleration * math.cos(self.angle) - EARTH_GRAVITY
            print(f"Acceleration - ax: {ax}, ay: {ay}")  # Debug print

            # Update velocity and position
            self.vx += ax * TIME_STEP
            self.vy += ay * TIME_STEP
            self.x += self.vx * TIME_STEP
            self.y -= self.vy * TIME_STEP
            print(f"Velocity - vx: {self.vx}, vy: {self.vy}")  # Debug print
            print(f"Position - x: {self.x}, y: {self.y}")  # Debug print

            # Limit the rocket's vertical speed
            if self.vy < -100:
                self.vy = -100

        # Ensure the rocket doesn't go below the ground
        if self.y >= HEIGHT - 60:
            self.y = HEIGHT - 60
            self.vy = 0

        # Limit the rocket's horizontal position to stay on screen
        if self.x < 0:
            self.x = 0
            self.vx = 0
        elif self.x > WIDTH:
            self.x = WIDTH
            self.vx = 0

    def draw(self, screen, camera_offset):
            rocket_rect = pygame.Rect(0, 0, 20, 50)
            rocket_rect.center = (self.x, self.y + camera_offset)
            rocket_surface = pygame.Surface(rocket_rect.size, pygame.SRCALPHA)
            rocket_surface.fill(WHITE)
            rotated_rocket = pygame.transform.rotate(rocket_surface, -math.degrees(self.angle))
            rotated_rect = rotated_rocket.get_rect(center=rocket_rect.center)
            screen.blit(rotated_rocket, rotated_rect.topleft)

    def increase_thrust(self):
        if self.thrust < MAX_THRUST:
            self.thrust += 100000  # Increase thrust in larger increments
            print(f"Increased thrust: {self.thrust}")  # Debug print

    def decrease_thrust(self):
        if self.thrust > 0:
            self.thrust -= 100000  # Decrease thrust in larger increments
            print(f"Decreased thrust: {self.thrust}")  # Debug print
            
    def tilt_left(self):
        if self.angle < MAX_TILT:
            self.angle += TILT_STEP
            print(f"Tilted left: {math.degrees(self.angle)} degrees")  # Debug print

    def tilt_right(self):
        if self.angle > -MAX_TILT:
            self.angle -= TILT_STEP
            print(f"Tilted right: {math.degrees(self.angle)} degrees")  # Debug print

def draw_sky(screen, height):
    for i in range(height):
        color_value = min(255, max(0, 255 - int(i * 255 / height)))
        pygame.draw.line(screen, (color_value, color_value, 255), (0, i), (WIDTH, i))

def draw_stars(screen, height):
    for _ in range(50):
        x = random.randint(0, WIDTH)
        y = random.randint(0, height)
        pygame.draw.circle(screen, WHITE, (x, y), 2)

rocket = Rocket()

# Main game loop
running = True
camera_offset = 0  # Camera offset to follow the rocket

while running:
    pass

pygame.quit()
sys.exit()