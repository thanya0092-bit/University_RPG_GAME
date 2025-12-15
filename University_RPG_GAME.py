import pygame
pygame.init()

# --- Window ---
WIDTH, HEIGHT = 500, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("University RPG GAME")

clock = pygame.time.Clock()

# --- Load Assets ---
walkRight = [pygame.image.load('Images/R1.png'), pygame.image.load('Images/R2.png'), pygame.image.load('Images/R3.png')]
walkLeft  = [pygame.image.load('Images/L1.png'), pygame.image.load('Images/L2.png'), pygame.image.load('Images/L3.png')]
walkUp    = [pygame.image.load('Images/back.png'), pygame.image.load('Images/walk up1.png')]
walkDown  = [pygame.image.load('Images/standing1.png'), pygame.image.load('Images/walk down1.png')]
idleSprite = pygame.image.load('Images/standing1.png')

# ------------------------------------------------------------------------------------
# COLLISION RECTS (you may adjust these to match your background image furniture)
# ------------------------------------------------------------------------------------

bedroom_collisions = [ 
    pygame.Rect(180, 13, 160, 233),   # bed 
    pygame.Rect(333, 13, 147, 112),  # table right next to the bed 
    pygame.Rect(120, 13, 160, 161),  # table left next to the bed 
    pygame.Rect(10, 217, 50, 139),  # bookshelf 
    pygame.Rect(420, 250, 75, 170),  # desk/computer 
    pygame.Rect(397, 280, 21, 90),  #desk 
    pygame.Rect(15, 386, 51, 92),  # bottom left (plant) 
    pygame.Rect(411, 412, 72, 70),  # bottom right (plant) 
    pygame.Rect(29, 42, 76, 113),  #player not walk over the door 
    ]

livingroom_collisions = [ 
    pygame.Rect(296, 204, 101, 52),    # big table 
    pygame.Rect(386, 332, 110, 164),    # door and wall 
    pygame.Rect(90, 343, 200, 67),  # sofa 
    pygame.Rect(117, 246, 100, 52),  # small table 
    pygame.Rect(13, 294, 43, 77),  # left plant 
    pygame.Rect(13, 388, 29, 79),  # door to backyard 
    pygame.Rect(385, 344, 76, 37),  # door to bedroom 
    pygame.Rect(98, 5, 322, 182),  # tv and kitchan 
    pygame.Rect(420, 94, 69, 101),  # frezer 
    pygame.Rect(22, 34, 76, 116),  #front door 
    ]

frontyard_collisions = [
    pygame.Rect(199, 127, 100, 158),    # back door
    pygame.Rect(309, 327, 165, 110),  #bycle
    pygame.Rect(365, 431, 46, 45),  #bycle chain
    pygame.Rect(7, 280, 168, 27),  #left house wall
    pygame.Rect(322, 283, 168, 27),  #right house wall
]


# Door trigger area 
door_to_livingroom = pygame.Rect(30, 42, 76, 113)
door_to_bedroom = pygame.Rect(403, 325, 76, 37)
door_to_the_front = pygame.Rect(22, 34, 76, 116)
door_to_backyard = pygame.Rect(13, 388, 29, 79)
door_back_in_house = pygame.Rect(199, 127, 100, 158)

# Event tigger area
unlock_key = pygame.Rect(365, 431, 46, 45)


# --- Dialogue flag ---
font = pygame.font.SysFont("Arial", 20)


# ------------------------------------------------------------------------------------
# PLAYER CLASS
# ------------------------------------------------------------------------------------
class Player:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.vel = 5

        self.direction = "down"
        self.moving = False
        self.walkCount = 0

    def draw(self, win):
        if self.walkCount >= 12:
            self.walkCount = 0

        if self.moving:
            if self.direction == "left":
                frame = walkLeft[self.walkCount // 4]
            elif self.direction == "right":
                frame = walkRight[self.walkCount // 4]
            elif self.direction == "up":
                frame = walkUp[self.walkCount // 6]
            else:
                frame = walkDown[self.walkCount // 6]

            win.blit(frame, (self.x, self.y))
            self.walkCount += 1
        else:
            if self.direction == "left":
                win.blit(walkLeft[0], (self.x, self.y))
            elif self.direction == "right":
                win.blit(walkRight[0], (self.x, self.y))
            elif self.direction == "up":
                win.blit(walkUp[0], (self.x, self.y))
            else:
                win.blit(idleSprite, (self.x, self.y))


# ------------------------------------------------------------------------------------
# MOVE PLAYER WITH COLLISION CHECK
# ------------------------------------------------------------------------------------
def move_player(player, dx, dy):
    new_rect = pygame.Rect(player.x + dx + 30, player.y + dy + 70, 36, 26)

    # Check collision with furniture
    for obj in collisions:
        if new_rect.colliderect(obj):
            return  # stop movement
    player.x += dx
    player.y += dy

    # Clamp to window boundaries
    if player.x < 0:
        player.x = 0
    if player.y < 0:
        player.y = 0
    if player.x + player.width > WIDTH:
        player.x = WIDTH - player.width
    if player.y + player.height > HEIGHT:
        player.y = HEIGHT - player.height


def draw_text_box(surface, text, font, x=50, y=350, w=400, h=100):
    pygame.draw.rect(surface, (200,200,200), (x, y, w, h))
    pygame.draw.rect(surface, (0,0,0), (x, y, w, h), 2)
    lines = text.split("\n")
    for i, line in enumerate(lines):
        txt_surface = font.render(line, True, (0,0,0))
        surface.blit(txt_surface, (x+10, y+10 + i*25))


# --- Item selection state ---
choosing_items = False
available_items = [
    "OV-chipkaart", "Metro ticket", "Cash", "Phone",
    "Keys", "Book", "Pen", "Water bottle", "Snack", "Laptop"
]
selected_items = []
current_index = 0
unlock_index = 0

def draw_item_menu():
    win.fill((255, 255, 255))
    title = font.render("Choose 2 items before leaving!", True, (0,0,0))
    win.blit(title, (50, 20))

    for i, item in enumerate(available_items):
        color = (0, 0, 0)
        if i == current_index:
            color = (0, 0, 255)  # highlight
        text_surface = font.render(item, True, color)
        win.blit(text_surface, (50, 60 + i*30))

    chosen_text = font.render(f"Chosen: {', '.join(selected_items)}", True, (0,150,0))
    win.blit(chosen_text, (50, 400))


def draw_selected_item_menu(win, font, selected_items, unlock_index):
    # ------- Draw semi-transparent bottom box -------
    box_x = 20
    box_y = 320
    box_width = 460
    box_height = 160
    pygame.draw.rect(win, (230, 230, 230), (box_x, box_y, box_width, box_height))
    pygame.draw.rect(win, (0, 0, 0), (box_x, box_y, box_width, box_height), 3)
    # ------- Title -------
    title = font.render("Choose an item to use:", True, (0, 0, 0))
    win.blit(title, (box_x + 10, box_y + 10))
    # ------- Item List -------
    for i, item in enumerate(selected_items):
        color = (0, 0, 0)
        if i == unlock_index:
            color = (0, 0, 255)  # highlight current item
        text_surface = font.render(f"- {item}", True, color)
        win.blit(text_surface, (box_x + 20, box_y + 50 + i * 25))



# ------------------------------------------------------------------------------------
# DRAW WINDOW
# ------------------------------------------------------------------------------------
def redrawGameWindow():
    win.blit(background, (0, 0))
    player_rect = pygame.Rect(student.x, student.y, student.width, student.height)
    pygame.draw.rect(win, (0, 255, 0), player_rect, 2)
    # Draw collision boxes (debug)
    for obj in collisions:
        pygame.draw.rect(win, (255, 0, 0), obj, 2)

    # Draw door
    if game_state == "bedroom":
        pygame.draw.rect(win, (0, 255, 0), door_to_livingroom, 2)
    elif game_state == "livingroom":
        pygame.draw.rect(win, (0, 255, 0), door_to_bedroom, 2)
        pygame.draw.rect(win, (0, 255, 0), door_to_backyard, 2)
        pygame.draw.rect(win, (0, 255, 0), door_to_the_front, 2)
    elif game_state == "frontyard":
        pygame.draw.rect(win, (0, 255, 0), door_back_in_house, 2)
        pygame.draw.rect(win, (0, 255, 0), unlock_key, 2)
    student.draw(win)
    pygame.display.update()


def draw_start_menu():
    win.blit(start_bg, (0, 0))
    # Title
    win.blit(
        title_text,
        (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 6)
    )
    # Button hover
    mouse_pos = pygame.mouse.get_pos()
    color = BUTTON_HOVER if start_button.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(win, color, start_button, border_radius=10)
    text = button_font.render("Start", True, (255, 255, 255))
    win.blit(
        text,
        (
            start_button.centerx - text.get_width() // 2,
            start_button.centery - text.get_height() // 2
        )
    )
    pygame.display.update()


# ------------------------------------------------------------------------------------
# MAIN LOOP
# ------------------------------------------------------------------------------------
# --- START SCREEN ASSETS ---
start_bg = pygame.image.load("Images/startmenu.png")
start_bg = pygame.transform.scale(start_bg, (WIDTH, HEIGHT))

title_font = pygame.font.SysFont("Arial", 64)
button_font = pygame.font.SysFont("Arial", 32)

title_text = title_font.render("Race to University", True, (0, 0, 0))

button_width, button_height = 200, 60
button_x = WIDTH // 2 - button_width // 2
button_y = HEIGHT // 1.5
start_button = pygame.Rect(button_x, button_y, button_width, button_height)

BUTTON_COLOR = (50, 200, 50)
BUTTON_HOVER = (80, 255, 80)
game_state = "start_menu"
run = True

# --- START MENU BUTTON ---
button_width, button_height = 200, 60
button_x = WIDTH // 2 - button_width // 2
button_y = HEIGHT // 1.5
start_button = pygame.Rect(button_x, button_y, button_width, button_height)

BUTTON_COLOR = (50, 200, 50)
BUTTON_HOVER = (80, 255, 80)

can_interact = True
student = Player(350, 177, 96, 96)
run = True
items_chosen = False
unlock_bycle = False
while run:
    clock.tick(30)
    # ================== EVENTS ==================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # -------- START MENU --------
        elif game_state == "start_menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    game_state = "bedroom"
                    background = pygame.image.load("Images/bedroom.png")
                    collisions = bedroom_collisions
                    student.x, student.y = 350, 177

        # ---------------- ITEM SELECTION ----------------
        elif game_state == "item_select":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    current_index = (current_index + 1) % len(available_items)

                elif event.key == pygame.K_UP:
                    current_index = (current_index - 1) % len(available_items)

                elif event.key == pygame.K_RETURN:
                    # Pick item
                    choice = available_items[current_index]
                    if choice not in selected_items:
                        selected_items.append(choice)

                    # When 2 items chosen → show confirmation box
                    if len(selected_items) == 2:
                        game_state = "item_confirm"
                        items_chosen = True

        # ----------- CONFIRM LEAVING THE BEDROOM -----------  
        elif game_state == "item_confirm":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # move to livingroom
                background = pygame.image.load('Images/livingroom.png')
                collisions = livingroom_collisions
                student.x, student.y = 410, 208
                game_state = "livingroom"

        # ---------------- ITEM SELECTION ----------------
        if game_state == "item_use":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    unlock_index = (unlock_index + 1) % len(selected_items)

                elif event.key == pygame.K_UP:
                    unlock_index = (unlock_index - 1) % len(selected_items)

                elif event.key == pygame.K_RETURN:
                    chosen_item = selected_items[unlock_index]

                    # If the player has keys → success
                    if chosen_item == "Keys":
                        game_state = "unlock_success"
                    # Otherwise wrong item
                    else:
                        game_state = "wrong_item"
    # =====================================================
    # ---------------- NORMAL GAMEPLAY --------------------
    # =====================================================

    if game_state in ("bedroom", "livingroom", "frontyard"):
        keys = pygame.key.get_pressed()
        student.moving = False

        if not keys[pygame.K_e]:
            can_interact = True

        if keys[pygame.K_LEFT]:
            student.direction = "left"
            student.moving = True
            move_player(student, -student.vel, 0)

        elif keys[pygame.K_RIGHT]:
            student.direction = "right"
            student.moving = True
            move_player(student, student.vel, 0)

        elif keys[pygame.K_UP]:
            student.direction = "up"
            student.moving = True
            move_player(student, 0, -student.vel)

        elif keys[pygame.K_DOWN]:
            student.direction = "down"
            student.moving = True
            move_player(student, 0, student.vel)

        # DOOR LOGIC
        player_rect = pygame.Rect(student.x, student.y, student.width, student.height)

        if game_state == "bedroom" and player_rect.colliderect(door_to_livingroom):
            if keys[pygame.K_e] and not items_chosen and can_interact:
                game_state = "item_select"  # start item picking
            elif keys[pygame.K_e] and items_chosen and can_interact:
                can_interact = False
                background = pygame.image.load('Images/livingroom.png')
                collisions = livingroom_collisions
                game_state = "livingroom"
                student.x, student.y = 410, 208
        if game_state == "livingroom":
            if player_rect.colliderect(door_to_bedroom):
                if keys[pygame.K_e] and can_interact:
                    can_interact = False
                    background = pygame.image.load('Images/bedroom.png')
                    collisions = bedroom_collisions
                    game_state = "bedroom"
                    student.x, student.y = 40, 165
        if game_state == "livingroom":
            if player_rect.colliderect(door_to_the_front):
                if keys[pygame.K_e] and can_interact:
                    can_interact = False
                    background = pygame.image.load('Images/frontyard.png')
                    collisions = frontyard_collisions
                    game_state = "frontyard"
                    student.x, student.y = 210, 300
        if game_state == "frontyard":
            if player_rect.colliderect(door_back_in_house):
                if keys[pygame.K_e] and can_interact:
                    can_interact = False
                    background = pygame.image.load('Images/livingroom.png')
                    collisions = livingroom_collisions
                    game_state = "livingroom"
                    student.x, student.y = 25, 160
            if player_rect.colliderect(unlock_key):
                if keys[pygame.K_e] and not unlock_bycle:
                    game_state = "item_use"

    # =====================================================
    # ---------------- DRAWING ----------------------------
    # =====================================================

    # SPECIAL MENUS MUST DRAW BEFORE BACKGROUND OVERWRITE
    if game_state == "start_menu":
        draw_start_menu()
        continue

    elif game_state == "item_select":
        draw_item_menu()
        pygame.display.update()
        continue

    elif game_state == "item_confirm":
        draw_text_box(win, f"You selected: {selected_items[0]}, {selected_items[1]}\nPress ENTER to continue.", font)
        pygame.display.update()
        continue

    elif game_state == "item_use":
        draw_selected_item_menu(win, font, selected_items, unlock_index)
        pygame.display.update()
        continue

    # NORMAL ROOM RENDER
    win.blit(background, (0, 0))
    redrawGameWindow()



