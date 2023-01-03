import random
import pygame

score_red = 0
score_blue = 0

class Board(object):
    def __init__(self, side):
        self.side = side
        self.thickness = 15
        self.length = 100
        self.screen_size = 800
        self.direction = None

    def set_position(self):
        """ Sets the initial position of the board for both the players. """
        if self.side == "West":
            self.position = [15, int(self.screen_size / 2) - 50]
        elif self.side == "East":
            self.position = [self.screen_size - 30, int(self.screen_size / 2) - 50]

    def set_direction(self, direction=None):
        """ Changes board directions. """
        self.direction = direction

    def move(self):
        """ Moves the board without allowing it to go off screen. """
        if self.direction == "Up":
            self.position[1] -= 2
        if self.direction == "Down":
            self.position[1] += 2

        # returns board to screen if it goes off
        if self.position[1] < 0:
            self.position[1] = 0
        elif self.position[1] > self.screen_size - self.length:
            self.position[1] = int(self.screen_size - self.length)

    def check_collision_ball(self, ball_position):
        """ Checks if the ball is in a range of the position of the board. """
        if self.side == "West":
            if ball_position[1] in range(self.position[1], self.position[1] + 100) and ball_position[0] in range(
                    self.position[0] + 20, self.position[0] + 30):
                return True

        elif self.side == "East":
            if ball_position[1] in range(self.position[1], self.position[1] + 100) and ball_position[0] in range(
                    self.position[0] - 20, self.position[0] - 10):
                return True


class Ball(object):
    def __init__(self):
        self.screen_size = 800
        self.position = [int(self.screen_size / 2), int(self.screen_size / random.randint(2, 11))]
        self.radius = 20
        self.direction_x = "Left"
        self.direction_y = "Up"
        self.speed = 2

    def move(self):
        """ Move in x and y directions. """
        if self.direction_x == "Left":
            self.position[0] -= self.speed
        if self.direction_x == "Right":
            self.position[0] += self.speed
        if self.direction_y == "Up":
            self.position[1] -= self.speed
        if self.direction_y == "Down":
            self.position[1] += self.speed

            # bouncing the ball off the walls
        if self.position[1] < self.radius or self.position[1] > self.screen_size - self.radius:
            self.change_direction_y()

        return self.position

    def change_direction_y(self):
        """ Change ball movement in the y-direction. """
        if self.direction_y == "Up":
            self.direction_y = "Down"
        elif self.direction_y == "Down":
            self.direction_y = "Up"

    def change_direction_x(self):
        """ Change ball movement in the x-direction. """
        if self.direction_x == "Left":
            self.direction_x = "Right"
        elif self.direction_x == "Right":
            self.direction_x = "Left"

    def check_collision_side(self):
        """ Checks if a player fails to catch the ball and returns the winner. """
        if self.position[0] < self.radius:
            return "Blue"
        if self.position[0] > self.screen_size - self.radius:
            return "Red"
        return False


class Game(object):
    def __init__(self, window):
        self.game_over = False
        self.window = window
        self.no_hits = 0
        self.result = False

        # set instances of other classes
        self.board1 = Board("West")
        self.board1.set_position()
        self.board2 = Board("East")
        self.board2.set_position()
        self.ball = Ball()

    def handle_events(self):
        """ Pygame event handling. """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_over = True
                if event.key == pygame.K_UP:
                    self.board2.set_direction("Up")
                if event.key == pygame.K_DOWN:
                    self.board2.set_direction("Down")
                if event.key == pygame.K_w:
                    self.board1.set_direction("Up")
                if event.key == pygame.K_s:
                    self.board1.set_direction("Down")
            # Stop boards when when the keys are released
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.board2.set_direction()
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    self.board1.set_direction()

    def game_logic(self):
        """ Handling game logic and interactions between objects. """
        global score_red, score_blue

        # moves the ball, and the board if keys are pressed.
        self.board1.move()
        self.board2.move()
        self.ball_position = self.ball.move()

        # change direction of ball if it hits the board
        if self.board1.check_collision_ball(self.ball_position) or self.board2.check_collision_ball(self.ball_position):
            self.ball.change_direction_x()
            self.no_hits += 1

        # checks if a player fails to catch the ball
        self.result = self.ball.check_collision_side()

        # keeping track of score and ending the game.
        if self.result:
            self.game_over = True
            if self.result == "Red":
                score_red += 1
            elif self.result == "Blue":
                score_blue += 1

    def display(self):
        """ Handling pygame displays. """
        global score_red, score_blue

        self.window.fill((0, 0, 0))
        pygame.draw.rect(self.window, pygame.Color(255, 0, 0),
                         pygame.Rect(self.board1.position[0], self.board1.position[1], self.board1.thickness,
                                     self.board1.length))
        pygame.draw.rect(self.window, pygame.Color(0, 0, 255),
                         pygame.Rect(self.board2.position[0], self.board2.position[1], self.board2.thickness,
                                     self.board2.length))
        pygame.draw.circle(self.window, pygame.Color(0, 255, 0), self.ball.position, self.ball.radius)

        myfont = pygame.font.SysFont("Comic Sans MS", 30)

        # string formatting to show no of hits
        self.message(f"Current No of Hits: {self.no_hits}", (300, 15))
        self.message((f"Red : {score_red} | Blue : {score_blue} "), (300, 760))

        if self.game_over:
            self.message(f"{self.result} player wins! Press R to restart or ESC to quit", (150, 400))

        pygame.display.update()

    def message(self, text, position):
        """ A helper method that displays text on screen. """
        myfont = pygame.font.SysFont("Comis Sans MS", 30)
        textSurf = myfont.render(text, True, (255, 255, 255))
        self.window.blit(textSurf, position)

    def instructions(self):
        """ Instructions for which keys to press for each player. """
        global score_red, score_blue

        # only display instructions if this is the first time game is played.
        if score_red > 0 or score_blue > 0:
            start_game = True
        else:
            start_game = False
            self.window.fill((0, 0, 0))
            self.message(f"Welcome to 2 Player Pong!", (250, 150))
            self.message(f"Board Controls : ", (200, 250))
            self.message(f"Red Player (Left Side) : W and S", (200, 300))
            self.message(f"Blue Player (Right Side) : Up and Down", (200, 350))
            self.message(f"Press Space to start!", (300, 450))
            pygame.display.update()

        # wait for player to start the game
        while not start_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                    if event.key == pygame.K_SPACE:
                        start_game = True

    def restart(self):
        """ Method to restart the game if requested by the players.  """
        restart_game = False

        # wait for player input
        while not restart_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                    if event.key == pygame.K_r:
                        restart_game = True
                        main()


def main():
    """ Main game loop"""

    pygame.init()
    window = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Pong - 2 Players")

    game = Game(window)
    game_over = False

    game.instructions()

    while not game_over:
        game.handle_events()

        game.game_logic()

        game.display()

        # pairing the game_over variable with the one inside the class.
        game_over = game.game_over

    game.restart()

    pygame.quit()


if __name__ == "__main__":
    main()
