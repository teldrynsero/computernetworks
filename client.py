import pygame
from network import Network
import pickle
pygame.font.init()

# CLIENT: Using Pygame, create graphical interface
# for the actual rock-papper-scissors game.

# Set up Pygame window appearance
width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rock Paper Scissors")

# Appearance of buttons
class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("georgia", 40)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

# Draws window depending on different game states
def redrawWindow(win, game, p):

    win.fill((250,229,212))

    # Waiting on another player to connect
    if not(game.connected()):
        font = pygame.font.SysFont("georgia", 60)
        text = font.render("Waiting for opponent...", 1, (121,173,29))
        win.blit(text, (50,200))
    else: # 2 players connected, ready to play
        #font = pygame.font.SysFont("georgia", 30)
        #text_p1 = font.render(f"Player 1 Wins: {game.wins[0]}", 1, (79, 184, 157))
        #text_p2 = font.render(f"Player 2 Wins: {game.wins[1]}", 1, (79, 184, 157))
        #text_ties = font.render(f"Ties: {game.ties}", 1, (79, 184, 157))

        # Position for Player 1 Wins text
        #win.blit(text_p1, (50, 50))

        # Position for Ties text
        #win.blit(text_ties, (width // 2 - text_ties.get_width() // 2, 50))

        # Position for Player 2 Wins text
        #win.blit(text_p2, (width - text_p2.get_width() - 50, 50))

        font = pygame.font.SysFont("georgia", 60)
        text = font.render("You", 1, (35,186,196))
        win.blit(text, (80, 200))

        text = font.render("Opponent", 1, (196,35,57))
        win.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (79,184,157))
            text2 = font.render(move2, 1, (79,184,157))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (79,184,157))
            elif game.p1Went:
                text1 = font.render("Move made", 1, (79,184,157))
            else:
                text1 = font.render("Waiting...", 1, (79,184,157))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (79,184,157))
            elif game.p2Went:
                text2 = font.render("Move made", 1, (79,184,157))
            else:
                text2 = font.render("Waiting...", 1, (79,184,157))

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)


    pygame.display.update()

# Make the buttons for each move option
btns = [Button("Rock", 50, 500, (115,197,222)), Button("Scissors", 250, 500, (232,175,70)), Button("Paper", 450, 500, (235,117,207))]

# Client communicates with server to update game state
# using player ID and play input
def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", (player + 1))

    while run:
        clock.tick(60) # 60 FPS
        try:
            game = n.send("get")
        except Exception as e:
            run = False
            print(f"Error receiving player data: {e}")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            test = game.winner()
            font = pygame.font.SysFont("georgia", 90)
            if (test == 1 and player == 1) or (test == 0 and player == 0):
                text = font.render("You Won!", 1, (41,214,64))
            elif test == -1:
                text = font.render("Tie Game!", 1, (163,100,196))
            else:
                text = font.render("You Lost...", 1, (171,29,55))

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))

            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player)


# Main menu, what players see first when game opened
def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((250,229,212))
        font = pygame.font.SysFont("georgia", 60)
        text = font.render("Click to Play!", 1, (121,173,29))
        win.blit(text, (160,200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

# Keep displaying menu screen until clicked
while True:
    menu_screen()
