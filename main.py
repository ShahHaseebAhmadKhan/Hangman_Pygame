import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 1000, 800  # Adjusted size
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

# Load images
images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".jpg")
    image = pygame.transform.scale(image, (200, 200))  # Resize images to 200x200
    images.append(image)

# Game variables
hangman_status = 0
words = ["PYTHON", "JAVA", "JAVASCRIPT", "RUBY", "PHP", "HTML", "CSS"]
word = random.choice(words)
guessed = []

# Button variables
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 600  # Adjusted position
A = 65
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# Setup game loop
FPS = 60
clock = pygame.time.Clock()
run = True


def draw():
    win.fill(WHITE)

    # Draw title
    text = TITLE_FONT.render("HANGMAN", 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))

    # Draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 400))  # Adjusted position

    # Draw buttons
    for letter in letters:
        x, y, char, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(char, 1, BLACK)
            win.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    # Draw hangman
    win.blit(images[hangman_status], (300, 150))  # Adjusted position
    pygame.display.update()


def display_message(message):
    pygame.time.delay(1000)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    text_width = text.get_width()
    text_height = text.get_height()
    win.blit(text, (WIDTH / 2 - text_width / 2, HEIGHT / 2 - text_height / 2))
    pygame.display.update()
    pygame.time.delay(3000)


while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            for letter in letters:
                x, y, char, visible = letter
                if visible:
                    dist = ((x - mx) ** 2 + (y - my) ** 2) ** 0.5
                    if dist < RADIUS:
                        letter[3] = False
                        guessed.append(char)
                        if char not in word:
                            hangman_status += 1

    draw()

    won = True
    for letter in word:
        if letter not in guessed:
            won = False
            break

    if won:
        display_message("You WON!")
        break

    if hangman_status == 6:
        display_message("You LOST! The word was " + word)
        break

pygame.quit()
