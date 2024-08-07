import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 400, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ball Chaos Simulation")

# Load sounds
boundary_sound = pygame.mixer.Sound('sounds/boundary_touch.wav')
escape_sound = pygame.mixer.Sound('sounds/escape.wav')

# Circle properties
circle_center = (width // 2, height // 2)
circle_radius = 190
gap_angle_start = 45  # degrees
gap_angle_end = 75  # degrees

# Speed factor
speed = 10

# Gravity constant
gravity = 0.1

# Function to generate velocity with a consistent speed
def generate_velocity(speed):
    angle = random.uniform(0, 2 * math.pi)  # Random direction
    vx = speed * math.cos(angle)
    vy = speed * math.sin(angle)
    return vx, vy

# Ball class
class Ball:
    def __init__(self, x, y, vx, vy, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = 10

    def update(self):
        # Apply gravity to the vertical velocity
        self.vy += gravity
        self.x += self.vx
        self.y += self.vy

        # Check for boundary bounce within the circle
        if not self.inside_circle():
            angle = math.atan2(self.y - circle_center[1], self.x - circle_center[0])
            angle = (angle + 2 * math.pi) % (2 * math.pi)  # Normalize angle to [0, 2*pi)
            if gap_angle_start_rad <= angle <= gap_angle_end_rad:
                escape_sound.play()
                return True  # Ball escaped
            else:
                # Reflect ball velocity when hitting the circle boundary
                distance = math.sqrt((self.x - circle_center[0]) ** 2 + (self.y - circle_center[1]) ** 2)
                nx = (self.x - circle_center[0]) / distance
                ny = (self.y - circle_center[1]) / distance
                dot = self.vx * nx + self.vy * ny
                self.vx -= 2 * dot * nx
                self.vy -= 2 * dot * ny

                # Reduce the magnitude of random changes to avoid rapid bouncing
                self.vx += random.uniform(-0.05, 0.05)
                self.vy += random.uniform(-0.05, 0.05)
                
                boundary_sound.play()

                # Move the ball slightly away from the boundary to prevent sticking
                overlap = circle_radius - math.sqrt((self.x - circle_center[0]) ** 2 + (self.y - circle_center[1]) ** 2)
                self.x += self.vx * overlap / (abs(self.vx) + 1e-6)  # Avoid division by zero
                self.y += self.vy * overlap / (abs(self.vy) + 1e-6)
        return False

    def inside_circle(self):
        distance = math.sqrt((self.x - circle_center[0]) ** 2 + (self.y - circle_center[1]) ** 2)
        return distance <= circle_radius - self.size

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

# Create initial ball at the middle of the top circle boundary with consistent speed
def create_ball():
    # Middle of the top edge of the circle
    start_x = circle_center[0]
    start_y = circle_center[1] - circle_radius + 10  # Slightly away from the edge
    
    vx, vy = generate_velocity(speed)
    return Ball(start_x, start_y, vx, vy,
                (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

balls = [create_ball()]

# Rotation speed of the gap (degrees per frame)
rotation_speed = 1

# Function to generate a random color
def generate_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Initial color of the circle
circle_color = generate_random_color()

# Main loop
running = True
while running:
    screen.fill((0, 0, 0))

    # Draw the grid
    grid_color = (50, 50, 50)
    for x in range(0, width, 20):
        pygame.draw.line(screen, grid_color, (x, 0), (x, height))
    for y in range(0, height, 20):
        pygame.draw.line(screen, grid_color, (0, y), (width, y))

    # Update gap angles
    gap_angle_start = (gap_angle_start + rotation_speed) % 360
    gap_angle_end = (gap_angle_end + rotation_speed) % 360
    gap_angle_start_rad = math.radians(gap_angle_start)
    gap_angle_end_rad = math.radians(gap_angle_end)

    # Change circle color
    circle_color = generate_random_color()

    # Draw the boundary circle with a gap
    for angle in range(0, 360):
        angle_rad = math.radians(angle)
        if gap_angle_start < gap_angle_end:
            if not (gap_angle_start <= angle <= gap_angle_end):
                x = int(circle_center[0] + circle_radius * math.cos(angle_rad))
                y = int(circle_center[1] + circle_radius * math.sin(angle_rad))
                pygame.draw.circle(screen, circle_color, (x, y), 2)
        else:
            if not (gap_angle_start <= angle or angle <= gap_angle_end):
                x = int(circle_center[0] + circle_radius * math.cos(angle_rad))
                y = int(circle_center[1] + circle_radius * math.sin(angle_rad))
                pygame.draw.circle(screen, circle_color, (x, y), 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    new_balls = []
    escaped_balls = []  # List to keep track of escaped balls

    for ball in balls:
        if ball.update():
            # Ball escaped through the gap, create exactly two new balls with consistent speed
            new_balls.append(create_ball())
            new_balls.append(create_ball())
            escaped_balls.append(ball)  # Track this ball as escaped
        else:
            ball.draw(screen)

    # Remove balls that have escaped
    balls = [ball for ball in balls if ball not in escaped_balls]
    balls.extend(new_balls)

    # Display ball count
    font = pygame.font.Font(None, 36)
    text = font.render(f"Balls: {len(balls)}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
