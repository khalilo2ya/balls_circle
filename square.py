import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ball Chaos Simulation")

# Square boundary properties
square_center = (width // 2, height // 2)
square_size = 400  # Side length of the square
half_square_size = square_size // 2

# Gap properties
gap_width = 60
gap_start_x = square_center[0] - gap_width // 2
gap_end_x = square_center[0] + gap_width // 2

# Speed factor
speed = 3

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

        # Check for boundary bounce within the square
        if not self.inside_square():
            # Check if the ball escapes through the gap
            if gap_start_x <= self.x <= gap_end_x:
                if square_center[1] - half_square_size < self.y < square_center[1] + half_square_size:
                    return True  # Ball escaped through the gap
            
            # Reflect ball velocity when hitting the square boundary
            if self.x <= square_center[0] - half_square_size or self.x >= square_center[0] + half_square_size:
                self.vx = -self.vx
            if self.y <= square_center[1] - half_square_size or self.y >= square_center[1] + half_square_size:
                self.vy = -self.vy

        return False

    def inside_square(self):
        return (square_center[0] - half_square_size + self.size <= self.x <= square_center[0] + half_square_size - self.size and
                square_center[1] - half_square_size + self.size <= self.y <= square_center[1] + half_square_size - self.size)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

# Create initial ball at the middle of the top square boundary with consistent speed
def create_ball():
    # Middle of the top edge of the square
    start_x = square_center[0]
    start_y = square_center[1] - half_square_size + 10  # Slightly away from the edge
    
    vx, vy = generate_velocity(speed)
    return Ball(start_x, start_y, vx, vy,
                (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

balls = [create_ball()]

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

    # Draw the boundary square with a gap
    pygame.draw.rect(screen, (255, 165, 0), 
                     (square_center[0] - half_square_size, square_center[1] - half_square_size, square_size, square_size), 2)
    pygame.draw.rect(screen, (0, 0, 0), 
                     (gap_start_x, square_center[1] - half_square_size, gap_width, square_size), 0)  # Gap in the square

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
