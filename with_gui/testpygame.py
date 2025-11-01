import sys, pygame
pygame.init()

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
black = (0, 0, 0)
white = (255, 255, 255)
main_color = (10, 150, 230)

screen = pygame.display.set_mode((SCREEN_SIZE))

menu_state = "main"

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

play_btn = text_Button(144, 216, "Play", 60)
create_btn = text_Button(144, 288, "Create Levels", 60)
lb_btn = text_Button(144, 360, "Leaderboards", 60)
options_btn = text_Button(144, 432, "Options", 60)
quit_btn = text_Button(144, 504, "Quit", 60)

def levels_menu():
    ...

def menu_preset():
    ...

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
        levels_menu()
    if menu_state == "leaderboards":
        ...
    if menu_state == "create":
        ...
    if menu_state == "options":
        ...

    pygame.display.flip()