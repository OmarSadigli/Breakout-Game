import pygame
from pygame.locals import *

pygame.init()

screen_width = 800
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout Game")

# ----- DEFAULTS -----
BG_COLOR = "#0b3954"
PADDLE_COLOR = "#087e8b"
BALL_COLOR = "#bfd7ea"
BLOCK_COLORS = ["#ffe66d", "#ff6b6b", "#c81d25"]
TEXT_COLOR = "#f7fff7"
FONT = pygame.font.SysFont("Constantia", 30)

cols = 6
rows = 6
clock = pygame.time.Clock()
fps = 60
live_ball = False
game_over = False


# ------- PUT TEXT ON SCREEN-------- #
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


# ------- WALL CLASS -------- #
class Wall:
    def __init__(self):
        self.blocks = []
        self.width = screen_width // cols
        self.height = 45

    def create_wall(self):
        for row in range(rows):
            # reset the block row list
            block_row = []
            for col in range(cols):
                # generate x and y positions for each block and create a rectangle from that
                block_x = col * self.width
                block_y = row * self.height
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                # assign block strength based on row
                if row < 2:
                    strength = 3
                elif row < 4:
                    strength = 2
                elif row < 6:
                    strength = 1

                # create a list at this point to store the rect and colour data
                block_individual = [rect, strength]
                # append that individual block to the block row
                block_row.append(block_individual)
            # append the row to the full list of blocks
            self.blocks.append(block_row)

    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                # assign a colour based on block strength
                if block[1] == 3:
                    block_color = BLOCK_COLORS[2]
                elif block[1] == 2:
                    block_color = BLOCK_COLORS[1]
                elif block[1] == 1:
                    block_color = BLOCK_COLORS[0]
                pygame.draw.rect(screen, block_color, block[0])
                pygame.draw.rect(screen, BG_COLOR, block[0], 6)


# ------- PADDLE CLASS -------- #
class Paddle:
    def __init__(self):
        self.reset()

    def move(self):
        # reset movement direction
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
            self.direction = 1

    def draw(self):
        pygame.draw.rect(screen, PADDLE_COLOR, self.rect)

    def reset(self):
        # define paddle variables
        self.height = 20
        self.width = int(screen_width / cols)
        self.x = int((screen_width / 2) - (self.width / 2))
        self.y = screen_height - (self.height * 2)
        self.speed = 10
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.direction = 0
        self.game_over = 0


# --------- BALL CLASS ---------- #
class Ball:
    def __init__(self, x, y):
        self.reset(x, y)

    def draw(self):
        pygame.draw.circle(
            screen,
            BALL_COLOR,
            (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad),
            self.ball_rad
        )

    def move(self):
        # collision threshold
        collision_thresh = 5
        # start of with the assumption that the wall has been destroyed compeletely
        wall_destroyed = True
        row_count = 0
        for row in wall.blocks:
            item_count = 0
            for item in row:
                # check collision
                if self.rect.colliderect(item[0]):
                    # check if collision was from above
                    if abs(self.rect.bottom - item[0].top) < collision_thresh and self.speed_y > 0:
                        self.speed_y *= -1
                        # check if collision was from below
                    if abs(self.rect.top - item[0].bottom) < collision_thresh and self.speed_y < 0:
                        self.speed_y *= -1
                    # check if collision was from left
                    if abs(self.rect.right - item[0].left) < collision_thresh and self.speed_x > 0:
                        self.speed_x *= -1
                        # check if collision was from right
                    if abs(self.rect.left - item[0].right) < collision_thresh and self.speed_x < 0:
                        self.speed_x *= -1

                    # reduce the block's strength by doing damage to it
                    if wall.blocks[row_count][item_count][1] > 1:
                        wall.blocks[row_count][item_count][1] -= 1
                    else:
                        wall.blocks[row_count][item_count][0] = (0, 0, 0, 0) # these zeros means x=0| y=0| width=0|
                        # height=0. so we are making block invisible we are not deleting it

                # check if block still exists in which case the wall is not destroyed
                if wall.blocks[row_count][item_count][0] != (0, 0, 0, 0):
                    wall_destroyed = False
                # increase item counter
                item_count += 1
            # increase row counter
            row_count += 1
        # after iterating through all the blocks, check if the wall is destroyed
        if wall_destroyed:
            self.game_over = 1



        # check for collision with walls
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x *= -1
        if self.rect.top < 0:
            self.speed_y *= -1
        if self.rect.bottom > screen_height:
            self.game_over = -1

        # check for collision with paddle
        if self.rect.colliderect(paddle):
            # check if colliding from the top
            if abs(self.rect.bottom - paddle.rect.top) < collision_thresh and self.speed_y > 0:
                self.speed_y *= -1
                self.speed_x += paddle.direction
                if self.speed_x > self.speed_max:
                    self.speed_x = self.speed_max
                elif self.speed_x < 0 and self.speed_x < -self.speed_max:
                    self.speed_x = -self.speed_max
            else:
                self.speed_x *= -1


        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.game_over

    def reset(self, x, y):
        self.ball_rad = 10
        self.x = x - self.ball_rad
        self.y = y
        self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed_x = 4
        self.speed_y = -4
        self.speed_max = 5
        self.game_over = 0


# create wall
wall = Wall()
wall.create_wall()

# create paddle
paddle = Paddle()

# create ball
ball = Ball(paddle.x + (paddle.width // 2), paddle.y - paddle.height)

run = True
while run:
    clock.tick(fps)
    screen.fill(BG_COLOR)

    # draw all objects
    wall.draw_wall()
    paddle.draw()
    ball.draw()

    if live_ball:
        paddle.move()
        game_over = ball.move()
        if game_over != 0:
            live_ball = False

    # print player instructions on screen while game is not active
    if not live_ball:
        if game_over == 0:
            draw_text("hit space key to start the game", FONT, TEXT_COLOR, 200, screen_height // 2 + 100)
        elif game_over == 1:
            draw_text("you won!!!", FONT, TEXT_COLOR, 300, screen_height // 2 + 50)
            draw_text("hit space key to start the game", FONT, TEXT_COLOR, 200, screen_height // 2 + 100)
        else:
            draw_text("you lose... :(", FONT, TEXT_COLOR, 300, screen_height // 2 + 50)
            draw_text("hit space key to start the game", FONT, TEXT_COLOR, 200, screen_height // 2 + 100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and live_ball == False:
            live_ball = True
            ball.reset(paddle.x + (paddle.width // 2), paddle.y - paddle.height)
            paddle.reset()
    pygame.display.update()
pygame.quit()