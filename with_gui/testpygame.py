import sys, pygame, time
pygame.init()

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
black = (0, 0, 0)
white = (255, 255, 255)
main_color = (180, 30, 20)

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Shroomraider")

menu_state = "main"
class text_Button_1():
    def __init__(self, x, y, text, s):
        text, capt = create_text(text, s, white)
        self.s = s
        self.capt = capt
        self.width = text.get_width()
        self.height = text.get_height()
        self.text = text
        self.rect = self.text.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.hovered = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            self.text, s = create_text(self.capt, self.s, main_color)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            self.hovered = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        if not self.rect.collidepoint(pos) and self.hovered == True:
            self.text, s = create_text(self.capt, self.s, white)
            self.hovered = False
            
        screen.blit(self.text, (self.rect.x, self.rect.y))

        return action

class text_Button():
    def __init__(self, x, y, text, s):
        text, capt = create_text(text, s, main_color)
        self.s = s
        self.capt = capt
        self.width = text.get_width()
        self.height = text.get_height()
        self.text = text
        self.rect = self.text.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.hovered = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            self.text, s = create_text(self.capt, self.s + 12, white)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            self.hovered = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        if not self.rect.collidepoint(pos) and self.hovered == True:
            self.text, s = create_text(self.capt, self.s, main_color)
            self.hovered = False
            
        screen.blit(self.text, (self.rect.x, self.rect.y))

        return action

def create_text(text, s, color):
    font = pygame.font.Font("Syne_Mono/SyneMono-Regular.ttf", size=s)
    return font.render(text, True, color), text

# Main menu buttons
play_btn = text_Button(128, 216, "Play", 60)
create_btn = text_Button(128, 288, "Create Levels", 60)
lb_btn = text_Button(128, 360, "Leaderboards", 60)
options_btn = text_Button(128, 432, "Options", 60)
quit_btn = text_Button(128, 504, "Quit", 60)

# Play menu buttons
create_plr_btn = text_Button_1(128, 140, "New Player", 48)

def _create_player(name, date):
    data = [name, date]
    with open(f"data/players/{name}.txt", "w", encoding="utf-8") as player_data:
        player_data.write("\n".join(data))

def preset_menu(heading, heading_size, heading_color):
    ...

def levels_menu():
    pygame.draw.rect(screen, (75, 75, 75), pygame.Rect(96, 48, 1024-192, 768-96), border_radius=32)
    text = create_text("Players", 60, white)[0]

    pygame.draw.rect(screen, white, pygame.Rect(128, 128, 768, 2))

    screen.blit(text, (128, 60))
    create_plr_btn.draw()

def create_menu():
    text = create_text("Create", 60, main_color)[0]
    top_bar = pygame.Surface((768, 2))
    top_bar.fill(main_color)
    screen.blit(top_bar, (128, 128))
    screen.blit(text, (128, 48))

def leaderboards_menu():
    text = create_text("Leaderboards", 60, main_color)[0]
    top_bar = pygame.Surface((768, 2))
    top_bar.fill(main_color)
    screen.blit(top_bar, (128, 128))
    screen.blit(text, (128, 48))

def options_menu():
    text = create_text("Options", 60, main_color)[0]
    top_bar = pygame.Surface((768, 2))
    top_bar.fill(main_color)
    screen.blit(top_bar, (128, 128))
    screen.blit(text, (128, 48))

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)

    if menu_state == "main":
        if play_btn.draw():
            menu_state = "play"
        elif create_btn.draw():
            menu_state = "create"
        elif lb_btn.draw():
            menu_state = "leaderboards"
        elif options_btn.draw():
            menu_state = "options"
        elif quit_btn.draw():
            sys.exit()

    if menu_state == "play":
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            menu_state = "main"
        levels_menu()

    if menu_state == "leaderboards":
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            menu_state = "main"
        leaderboards_menu()

    if menu_state == "create":
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            menu_state = "main"
        create_menu()

    if menu_state == "options":
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            menu_state = "main"
        options_menu()

    pygame.display.flip()