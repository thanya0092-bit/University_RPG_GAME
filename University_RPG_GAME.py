import pygame
import random
pygame.init()

# --- Window ---
WIDTH, HEIGHT = 500, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("University RPG GAME")
clock = pygame.time.Clock()

# Toggle hitbox debug drawing (False to hide hit boxes)
DEBUG_HITBOXES = False

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
    pygame.Rect(333, 13, 147, 145),  # table right next to the bed
    pygame.Rect(120, 13, 160, 161),  # table left next to the bed 
    pygame.Rect(10, 217, 50, 139),  # bookshelf 
    pygame.Rect(420, 250, 75, 170),  # desk/computer 
    pygame.Rect(397, 280, 21, 90),  #desk 
    pygame.Rect(15, 386, 51, 92),  # bottom left (plant) 
    pygame.Rect(411, 412, 72, 70),  # bottom right (plant) 
    pygame.Rect(29, 42, 76, 113),  #player not walk over the door 
    ]

livingroom_collisions = [ 
    pygame.Rect(296, 204, 101, 85),    # big table 
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
backyard_collisions = [
    pygame.Rect(214, 26, 241, 253),    # tree
    pygame.Rect(380, 380, 106, 79),  #plant
    pygame.Rect(13, 399, 81, 84),  #back door
]
metro_collisions = [
    pygame.Rect(1, 1, 144, 290),    # left building
    pygame.Rect(319, 2, 181, 302),    # right building
    pygame.Rect(174, 187, 122, 99),    # metro gate
    pygame.Rect(373, 276, 67, 137),    # old man
    pygame.Rect(256, 376, 71, 40),    # grocery bag
]
metro2_collisions = [
    pygame.Rect(1, 1, 144, 290),    # left building
    pygame.Rect(319, 2, 181, 302),    # right building
    pygame.Rect(174, 187, 122, 99),    # metro gate
    pygame.Rect(373, 276, 67, 137),    # old man
]
bustop_collisions = [
    pygame.Rect(127, 45, 33, 88),    # the guy
    pygame.Rect(247, 149, 42, 141),    # busstop sing
    pygame.Rect(299, 161, 198, 114),    # busstop
    pygame.Rect(412, 282, 32, 32),    # busstop
    pygame.Rect(230, 363, 121, 66),    # bus
    pygame.Rect(360, 412, 79, 85),    # bus
    pygame.Rect(268, 336, 27, 12),    # bus
    pygame.Rect(342, 378, 45, 25),    # bus
    pygame.Rect(281, 438, 57, 36),    # bus
    pygame.Rect(183, 108, 40, 46),    # scooter
    pygame.Rect(217, 71, 29, 59),    # scooter
    pygame.Rect(91, 48, 35, 64),    # wall
    pygame.Rect(449, 271, 48, 90),    # bin
    pygame.Rect(4, 369, 58, 126),    # Lbuilding
    pygame.Rect(64, 397, 66, 98),    # Lbuilding
    pygame.Rect(131, 449, 44, 46),   #plant
]
university_collisions = [
    pygame.Rect(9, 5, 487, 161),    # building
    pygame.Rect(9, 179, 127, 160),    # buliding2
    pygame.Rect(148, 264, 24, 44),    # buliding3
    pygame.Rect(262, 176, 41, 74),    # buliding4
    pygame.Rect(9, 356, 167, 55),    # left plant
    pygame.Rect(7, 424, 94, 23),    # left plant
    pygame.Rect(7, 460, 34, 17),    # left plant
    pygame.Rect(150, 183, 106, 72),    # uni door
    pygame.Rect(314, 177, 178, 47),    # right plant
    pygame.Rect(329, 238, 154, 20),    # right plant
    pygame.Rect(378, 259, 67, 17),    # right plant
    pygame.Rect(229, 248, 38, 80),    # student
]
university2_collisions = [
    pygame.Rect(9, 5, 487, 161),    # building
    pygame.Rect(9, 179, 127, 160),    # buliding2
    pygame.Rect(148, 264, 24, 44),    # buliding3
    pygame.Rect(262, 176, 41, 74),    # buliding4
    pygame.Rect(9, 356, 167, 55),    # left plant
    pygame.Rect(7, 424, 94, 23),    # left plant
    pygame.Rect(7, 460, 34, 17),    # left plant
    pygame.Rect(150, 183, 106, 72),    # uni door
    pygame.Rect(314, 177, 178, 47),    # right plant
    pygame.Rect(329, 238, 154, 20),    # right plant
    pygame.Rect(378, 259, 67, 17),    # right plant
]
hallway_collisions = [
    pygame.Rect(20, 8, 59, 131),
    pygame.Rect(45, 145, 43, 13),
    pygame.Rect(94, 17, 62, 173),
    pygame.Rect(167, 89, 53, 111),
    pygame.Rect(217, 210, 82, 124),
    pygame.Rect(302, 224, 54, 131),
    pygame.Rect(364, 81, 128, 224),
    pygame.Rect(387, 313, 47, 32),
    pygame.Rect(442, 355, 57, 24),
    pygame.Rect(11, 311, 29, 20),
    pygame.Rect(11, 334, 48, 166),
    pygame.Rect(69, 341, 30, 15),
    pygame.Rect(72, 363, 43, 135),
    pygame.Rect(129, 380, 26, 120),
    pygame.Rect(166, 402, 34, 97),
    pygame.Rect(209, 417, 28, 82),
    pygame.Rect(246, 439, 18, 61),
    pygame.Rect(270, 452, 24, 48),
    pygame.Rect(300, 467, 24, 29),
    pygame.Rect(331, 480, 35, 18),
]
classroom_collisions = [
    pygame.Rect(20, 8, 59, 131),
    pygame.Rect(45, 145, 43, 13),
    pygame.Rect(94, 17, 62, 173),
    pygame.Rect(167, 89, 53, 111),
    pygame.Rect(364, 81, 128, 224),
    pygame.Rect(387, 313, 47, 32),
    pygame.Rect(442, 355, 57, 24),
    pygame.Rect(11, 311, 29, 20),
    pygame.Rect(11, 334, 48, 166),
    pygame.Rect(69, 341, 30, 15),
    pygame.Rect(72, 363, 43, 135),
    pygame.Rect(129, 380, 26, 120),
    pygame.Rect(166, 402, 34, 97),
    pygame.Rect(209, 417, 28, 82),
    pygame.Rect(246, 439, 18, 61),
    pygame.Rect(270, 452, 24, 48),
    pygame.Rect(300, 467, 24, 29),
    pygame.Rect(331, 480, 35, 18),
    pygame.Rect(190, 204, 65, 126),
    pygame.Rect(130, 119, 78, 151),
    pygame.Rect(266, 142, 82, 128),
    pygame.Rect(275, 276, 77, 20),
    pygame.Rect(322, 301, 51, 19),   
]


# Door trigger area 
door_to_livingroom = pygame.Rect(30, 42, 76, 113)
door_to_bedroom = pygame.Rect(403, 325, 76, 37)
door_to_the_front = pygame.Rect(22, 34, 76, 116)
door_to_backyard = pygame.Rect(13, 388, 29, 79)
door_back_in_houseF = pygame.Rect(199, 127, 100, 158)
door_back_in_houseB = pygame.Rect(13, 399, 81, 84)
metro_gate = pygame.Rect(223, 201, 40, 59)
uni_door = pygame.Rect(150, 183, 106, 72)



# Event tigger area
unlock_key = pygame.Rect(365, 431, 46, 45)
get_key = pygame.Rect(214, 26, 241, 253)
old_man = pygame.Rect(373, 276, 67, 137)
grocery_bag = pygame.Rect(256, 376, 71, 40)
bus = pygame.Rect(268, 336, 27, 12)
friend = pygame.Rect(127, 45, 33, 88)
senior = pygame.Rect(229, 248, 38, 80)
michelon = pygame.Rect(234, 246, 30, 52)
pascalle = pygame.Rect(324, 280, 20, 36)
way = pygame.Rect(415, 438, 69, 22)
michelon2 = pygame.Rect(190, 204, 65, 126)


# --- Dialogue flag ---
font = pygame.font.SysFont("Arial", 20)

# --- All text ---
key_event_choice = ["a: Look around for your key.",
    "b: Walk toward the station.",
    "c: Call your mom to ask about the key."
]
try_to_get_key = ["Try to get the key.", "Leave him alone."]
talk_to_Leo = [ "Leo, are you planning a jailbreak or just vibing?",
    "I will open the door AND let you ignore it.",
    "Key for treats? Final offer.",
    "The fate of my schedule rests in your paws."
]
old_man_event = ["Help the old man pick up his belongings.",
    "Ignore the old man and continue your way."
]
friend_event = ["Use a phone to call a mechanic for your classmate.",
    "Ignore classmate and continue your way."
]
wanna_walk = ["Walk to university.",
    "Try something else."
]
senior_event = ["Answer the senior's question.",
    "Try to use items to pass."
]
talk_to_michelon = ["Ask Michelon a way to the classroom.",
    "Try something else."
]
talk_to_pascalle = ["Ask Pascalle for a way to the classroom.",
    "Try something else."
]
find_the_way = ["Walking around and looking for classroom.",
    "Use items."
]


quiz_questions = [
    {
        "question": "I’m tall when I’m young and short when I’m old. What am I?",
        "options": ["a.) A candle", "b.) A pencil", "c.) A tree"],
        "answer": "a.) A candle"
    },
    {
        "question": "What can travel around the world while staying in the same spot?",
        "options": ["a.) A stamp", "b.) A satellite", "c.) The moon"],
        "answer": ["a", "a stamp", "stamp"]
    },
    {
        "question": "What has hands but can’t clap?",
        "options": ["a.) A statue", "b.) A clock", "c.) A robot"],
        "answer": "b.) A clock"
    },
    {
        "question": "What gets wetter the more it dries?",
        "options": ["a.) A towel", "b.) A sponge", "c.) A cloud"],
        "answer": "a.) A towel"
    },
    {
        "question": "What has many keys but can’t open a single lock?",
        "options": ["a.) A janitor", "b.) A piano", "c.) A keyboard"],
        "answer": "a.) Footsteps"
    },
    {
        "question": "The more you take, the more you leave behind. What am I?",
        "options": ["a.) Footsteps", "b.) Memories", "c.) Time"],
        "answer": "a.) Footsteps"
    },
    {
        "question": "What belongs to you, but other people use it more than you do?",
        "options": ["a.) My money", "b.) My name", "c.) My phone"],
        "answer": "b.) My name"
    },
    {
        "question": "What has a face and two hands but no arms or legs?",
        "options": ["a.) A robot", "b.) A clock", "c.) A card"],
        "answer": "b.) A clock"
    },
    {
        "question": "What can you catch but not throw?",
        "options": ["a.) A ball", "b.) A cold", "c.) A butterfly"],
        "answer": "b.) A cold"
    },
    {
        "question": "What comes down but never goes up?",
        "options": ["a.) Rain", "b.) Age", "c.) Shadows"],
        "answer": "a.) Rain"
    }
]

# ---------------------------------- SOUND EFFECTS ----------------------------------
def start_background_music(background_file):
    """Start looping background music."""
    # Initialize mixer only if not already done
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    pygame.mixer.music.load(background_file)
    pygame.mixer.music.set_volume(0.02)  # 0.0 = mute, 1.0 = full volume
    pygame.mixer.music.play(-1)  # Loop forever (-1 means infinite loop)


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
    # Split title into two lines
    title_lines = [
        "You wake up late! Hurry up and go to school!",
        "Choose 2 items before leaving!"
    ]
    # Render each line separately
    for i, line in enumerate(title_lines):
        title_surface = font.render(line, True, (0, 0, 0))
        win.blit(title_surface, (50, 20 + i*30))  # adjust spacing with i*30
    # Items list
    for i, item in enumerate(available_items):
        color = (0, 0, 0)
        if i == current_index:
            color = (0, 0, 255)  # highlight
        text_surface = font.render(item, True, color)
        win.blit(text_surface, (50, 80 + i*30))  # shifted down to avoid overlap
    # Chosen items
    chosen_text = font.render(f"Chosen: {', '.join(selected_items)}", True, (0, 150, 0))
    win.blit(chosen_text, (50, 400))


def draw_selected_menu(win, font, selected_items, unlock_index, text):
    # ------- Draw semi-transparent bottom box -------
    box_x = 20
    box_y = 320
    box_width = 460
    box_height = 160
    pygame.draw.rect(win, (230, 230, 230), (box_x, box_y, box_width, box_height))
    pygame.draw.rect(win, (0, 0, 0), (box_x, box_y, box_width, box_height), 3)
    # ------- Title -------
    title = font.render(text, True, (0, 0, 0))
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
    # For final screens (game over / win) don't draw debug boxes or the player
    if game_state in ("game over", "game won"):
        pygame.display.update()
        return
    if DEBUG_HITBOXES:
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
            pygame.draw.rect(win, (0, 255, 0), door_back_in_houseF, 2)
            pygame.draw.rect(win, (0, 255, 0), unlock_key, 2)
        elif game_state == "backyard":
            pygame.draw.rect(win, (0, 255, 0), door_back_in_houseB, 2)
            pygame.draw.rect(win, (0, 255, 0), get_key, 2)
        elif game_state == "metro_station":
            pygame.draw.rect(win, (0, 255, 0), metro_gate, 2)
            pygame.draw.rect(win, (0, 255, 0), old_man, 2)
        elif game_state == "busstop":
            pygame.draw.rect(win, (0, 255, 0), bus, 2)
            pygame.draw.rect(win, (0, 255, 0), friend, 2)
        elif game_state == "university":
            pygame.draw.rect(win, (0, 255, 0), senior, 2)
            pygame.draw.rect(win, (0, 255, 0), uni_door, 2)
        elif game_state == "hallway":
            pygame.draw.rect(win, (0, 255, 0), michelon, 2)
            pygame.draw.rect(win, (0, 255, 0), pascalle, 2)
            pygame.draw.rect(win, (0, 255, 0), way, 2)
        elif game_state == "classroom":
            pygame.draw.rect(win, (0, 255, 0), michelon2, 2)

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
        (start_button.centerx - text.get_width() // 2,
        start_button.centery - text.get_height() // 2)
    )
    pygame.display.update()


# ------------------------------------------------------------------------------------
# MAIN LOOP
# ------------------------------------------------------------------------------------
student = Player(350, 177, 96, 96)
run = True
items_chosen = False
unlock_bycle = False
key_get = False
help_old_man = False
ov_chipkaart = True
cash = True
help_friend = False
answered_senior = False
time_limit = 45 #minutes

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
                    start_background_music("Images/backgroundmusic.mp3")
                    background = pygame.image.load("Images/bedroom.png")
                    collisions = bedroom_collisions
                    student.x, student.y = 350, 177
                    game_state = "tutorial"
        # -------- TIME UP --------
        elif game_state == "time up":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = "game over"
        # --------- Tutorial ---------
        elif game_state == "tutorial":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = "bedroom"
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
                        game_state = "use_keys"
                        unlock_bycle = True
                    # Otherwise wrong item
                    else:
                        time_limit -= 2
                        if time_limit <= 0:
                            game_state = "time up"
                        else:
                            game_state = "wrong_item"
                    unlock_index = 0

                            # KEY EVENT
# ------------------------------------------------------------------------------------
        elif game_state == "wrong_item":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    unlock_index = (unlock_index + 1) % len(key_event_choice)
                elif event.key == pygame.K_UP:
                    unlock_index = (unlock_index - 1) % len(key_event_choice)
                elif event.key == pygame.K_RETURN:
                    chosen_choice = key_event_choice[unlock_index]
                    if chosen_choice == "a: Look around for your key.":
                        game_state = "frontyard"
                    elif chosen_choice == "b: Walk toward the station.":
                        time_limit -= 12
                        if time_limit <= 0:
                            game_state = "time up"
                        else:
                            game_state = "walk_to_station"
                    elif chosen_choice == "c: Call your mom to ask about the key.":
                        if "Phone" in selected_items:
                            time_limit -= 5
                            if time_limit <= 0:
                                game_state = "time up"
                            else:
                                game_state = "call_mom"
                        else:
                            game_state = "don't have a phone"
                    unlock_index = 0
        elif game_state == "try to get key":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    unlock_index = (unlock_index + 1) % len(try_to_get_key)
                elif event.key == pygame.K_UP:
                    unlock_index = (unlock_index - 1) % len(try_to_get_key)
                elif event.key == pygame.K_RETURN:
                    chosen_choice = try_to_get_key[unlock_index]
                    if chosen_choice == "Try to get the key.":
                        time_limit -= 5
                        if time_limit <= 0:
                            game_state = "time up"
                        else:
                            game_state = "Get key from Leo"
                    elif chosen_choice == "Leave him alone.":
                        game_state = "backyard"
                    unlock_index = 0
        elif game_state == "use_keys" and unlock_bycle:
                background = pygame.image.load('Images/metrostation.png')
                collisions = metro_collisions
                student.x, student.y = 10, 245
                game_state = "metro_station"
        elif game_state == "walk_to_station":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                background = pygame.image.load('Images/metrostation.png')
                collisions = metro_collisions
                student.x, student.y = 10, 245
                game_state = "metro_station"
        elif game_state == "call_mom":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = "frontyard"
        elif game_state == "Get key from Leo":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    unlock_index = (unlock_index + 1) % len(talk_to_Leo)
                elif event.key == pygame.K_UP:
                    unlock_index = (unlock_index - 1) % len(talk_to_Leo)
                elif event.key == pygame.K_RETURN:
                    chosen_choice = talk_to_Leo[unlock_index]
                    if chosen_choice == "Leo, are you planning a jailbreak or just vibing?":
                        time_limit -= 2
                        if time_limit <= 0:
                            game_state = "time up"
                        else:
                            game_state = "Leo still ignore you"
                    elif chosen_choice == "I will open the door AND let you ignore it.":
                        time_limit -= 2
                        if time_limit <= 0:
                            game_state = "time up"
                        else:
                            game_state = "Leo still ignore you"
                    elif chosen_choice == "Key for treats? Final offer.":
                        game_state = "Leo give you the key"
                    elif chosen_choice == "The fate of my schedule rests in your paws.":
                        time_limit -= 2
                        if time_limit <= 0:
                            game_state = "time up"
                        else:
                            game_state = "Leo still ignore you"
                    unlock_index = 0
        elif game_state == "Leo still ignore you":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = "backyard"
        elif game_state == "Leo give you the key":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                background = pygame.image.load('Images/backyard2.png')
                collisions = backyard_collisions
                selected_items.append("Keys")
                key_get = True
                game_state = "backyard"
        elif game_state == "don't have a phone":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = "frontyard"

                            # OLD MAN EVENT
# ------------------------------------------------------------------------------------
        elif game_state == "check-in metro":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    unlock_index = (unlock_index + 1) % len(selected_items)
                elif event.key == pygame.K_UP:
                    unlock_index = (unlock_index - 1) % len(selected_items)
                elif event.key == pygame.K_RETURN:
                    chosen_item = selected_items[unlock_index]
                    if chosen_item in ["OV-chipkaart", "Metro ticket", "Cash"]:
                        background = pygame.image.load('Images/busstop.png')
                        collisions = bustop_collisions
                        student.x, student.y = 21, 42
                        game_state = "busstop"
                        if chosen_item == "OV-chipkaart":
                            ov_chipkaart = False
                        elif chosen_item == "Metro ticket":
                            selected_items.remove("Metro ticket")
                        elif chosen_item == "Cash":
                            cash = False
                    else:
                        time_limit -= 2
                        if time_limit <= 0:
                            game_state = "time up"
                        else:
                            game_state = "can not not check-in metro"
                    unlock_index = 0
        elif game_state == "talk to old man":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    unlock_index = (unlock_index + 1) % len(old_man_event)
                elif event.key == pygame.K_UP:
                    unlock_index = (unlock_index - 1) % len(old_man_event)
                elif event.key == pygame.K_RETURN:
                    chosen_choice = old_man_event[unlock_index]
                    if chosen_choice == "Help the old man pick up his belongings.":
                        time_limit -= 5
                        if time_limit <= 0:
                            game_state = "time up"
                        else:
                            game_state = "help old man"
                    elif chosen_choice == "Ignore the old man and continue your way.":
                        game_state = "metro_station"
                    unlock_index = 0
        elif game_state == "help old man":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                background = pygame.image.load('Images/metrostation2.png')
                collisions = metro2_collisions
                student.x, student.y = 300, 333
                selected_items.append("Metro ticket")
                game_state = "metro_station"
                help_old_man = True
        elif game_state == "can not not check-in metro":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = "metro_station"

                            # FRIEND EVENT
# ------------------------------------------------------------------------------------
        elif game_state == "check-in bus":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    unlock_index = (unlock_index + 1) % len(selected_items)
                elif event.key == pygame.K_UP:
                    unlock_index = (unlock_index - 1) % len(selected_items)
                elif event.key == pygame.K_RETURN:
                    chosen_item = selected_items[unlock_index]
                    if chosen_item == "OV-chipkaart":
                        if ov_chipkaart:
                            background = pygame.image.load('Images/university.png')
                            collisions = university_collisions
                            student.x, student.y = 83, 400
                            game_state = "university"
                        else:
                            time_limit -= 3
                            if time_limit <= 0:
                                game_state = "time up"
                            else:
                                game_state = "don’t have enough money"
                    elif chosen_item == "Cash":
                        if cash:
                            background = pygame.image.load('Images/university.png')
                            collisions = university_collisions
                            student.x, student.y = 83, 400
                            game_state = "university"
                        else:
                            time_limit -= 3
                            if time_limit <= 0:
                                game_state = "time up"
                            else:
                                game_state = "don’t have enough money"
                    else:
                        time_limit -= 3
                        if time_limit <= 0:
                            game_state = "time up"
                        else:
                            game_state = "can not not check-in bus"
                    unlock_index = 0
        elif game_state == "can not not check-in bus":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = "wanna walk?"
        elif game_state == "talk to friend":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = "talk to friend2"
        elif game_state == "talk to friend2":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    unlock_index = (unlock_index + 1) % len(friend_event)
                elif event.key == pygame.K_UP:
                    unlock_index = (unlock_index - 1) % len(friend_event)
                elif event.key == pygame.K_RETURN:
                    chosen_choice = friend_event[unlock_index]
                    if chosen_choice == "Use a phone to call a mechanic for your classmate.":
                        if "Phone" in selected_items:
                            time_limit -= 7
                            if time_limit <= 0:
                                game_state = "time up"
                            else:
                                game_state = "help friend"
                        else:
                            time_limit -= 2
                            if time_limit <= 0:
                                game_state = "time up"
                            else:
                                game_state = "don't have phone"
                    elif chosen_choice == "Ignore classmate and continue your way.":
                        game_state = "busstop"
                    unlock_index = 0
        elif game_state == "don't have phone":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = "busstop"
        elif game_state == "don’t have enough money":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = "wanna walk?"
        elif game_state =="wanna walk?":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    unlock_index = (unlock_index + 1) % len(wanna_walk)
                elif event.key == pygame.K_UP:
                    unlock_index = (unlock_index - 1) % len(wanna_walk)
                elif event.key == pygame.K_RETURN:
                    chosen_choice = wanna_walk[unlock_index]
                    if chosen_choice == "Walk to university.":
                        time_limit -= 15
                        if time_limit <= 0:
                            game_state = "time up"
                        game_state = "walk to university"
                    if chosen_choice == "Try something else.":
                        game_state = "busstop"
                    unlock_index = 0
        elif game_state == "don’t have enough money":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = "busstop"
        elif game_state == "walk to university":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                background = pygame.image.load('Images/university.png')
                collisions = university_collisions
                student.x, student.y = 83, 400
                game_state = "university"
        elif game_state == "help friend":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                help_friend = True
                background = pygame.image.load('Images/university.png')
                collisions = university_collisions
                student.x, student.y = 83, 400
                game_state = "university"

                            # SENIOR EVENT
# ------------------------------------------------------------------------------------
        elif game_state == "talk to senior":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    unlock_index = (unlock_index + 1) % len(senior_event)
                elif event.key == pygame.K_UP:
                    unlock_index = (unlock_index - 1) % len(senior_event)
                elif event.key == pygame.K_RETURN:
                    chosen_choice = senior_event[unlock_index]
                    if chosen_choice == "Answer the senior's question.":
                        time_limit -= 3
                        if time_limit <= 0:
                            game_state = "time up"
                        else:
                            game_state = "answer senior"
                    elif chosen_choice == "Try to use items to pass.":
                        game_state = "item_use_senior"
        elif game_state == "answer senior":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    unlock_index = (unlock_index + 1) % len(question_data["options"])
                elif event.key == pygame.K_UP:
                    unlock_index = (unlock_index - 1) % len(question_data["options"])
                elif event.key == pygame.K_RETURN:
                    chosen_choice = question_data["options"][unlock_index]
                    if chosen_choice == question_data["answer"]:
                        game_state = "pass senior"
                    else:
                        time_limit -= 3
                        if time_limit <= 0:
                            game_state = "time up"
                        else:
                            game_state = "wrong answer"
                    unlock_index = 0
        elif game_state == "wrong answer":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = "university"
        elif game_state == "pass senior":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                answered_senior = True
                background = pygame.image.load('Images/university2.png')
                collisions = university2_collisions
                game_state = "university"
        elif game_state == "item_use_senior":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    unlock_index = (unlock_index + 1) % len(selected_items)
                elif event.key == pygame.K_UP:
                    unlock_index = (unlock_index - 1) % len(selected_items)
                elif event.key == pygame.K_RETURN:
                    chosen_item = selected_items[unlock_index]
                    if chosen_item == "Cash" and cash:
                        game_state = "pass sinior"
                    else:
                        time_limit -= 3
                        if time_limit <= 0:
                            game_state = "time up"
                        else:
                            game_state = "wrong answer"
                    unlock_index = 0

                            # HALLWAY EVENT
# ------------------------------------------------------------------------------------
        elif game_state == "talk to michelon":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    unlock_index = (unlock_index + 1) % len(talk_to_michelon)
                elif event.key == pygame.K_UP:
                    unlock_index = (unlock_index - 1) % len(talk_to_michelon)
                elif event.key == pygame.K_RETURN:
                    chosen_item = talk_to_michelon[unlock_index]
                    if chosen_item == "Ask Michelon a way to the classroom.":
                        time_limit -= 10
                        if time_limit <= 0:
                            game_state = "time up"
                        else:
                            game_state = "communicate with michelon"
                    elif chosen_item == "Try something else.":
                        game_state = "hallway"
                    unlock_index = 0
        elif game_state == "communicate with michelon":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                background = pygame.image.load('Images/classroom.png')
                collisions = classroom_collisions
                student.x, student.y = 390,360
                game_state = "classroom"
        elif game_state == "talk to pascalle":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    unlock_index = (unlock_index + 1) % len(talk_to_pascalle)
                elif event.key == pygame.K_UP:
                    unlock_index = (unlock_index - 1) % len(talk_to_pascalle)
                elif event.key == pygame.K_RETURN:
                    chosen_item = talk_to_pascalle[unlock_index]
                    if chosen_item == "Ask Pascalle for a way to the classroom.":
                        time_limit -= 15
                        if time_limit <= 0:
                            game_state = "time up"
                        else:
                            game_state = "communicate with pascalle"
                    elif chosen_item == "Try something else.":
                        game_state = "hallway"
                    unlock_index = 0
        elif game_state == "communicate with pascalle":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                background = pygame.image.load('Images/classroom.png')
                collisions = classroom_collisions
                student.x, student.y = 390,370
                game_state = "classroom"
        elif game_state == "find the way":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    unlock_index = (unlock_index + 1) % len(find_the_way)
                elif event.key == pygame.K_UP:
                    unlock_index = (unlock_index - 1) % len(find_the_way)
                elif event.key == pygame.K_RETURN:
                    chosen_item = find_the_way[unlock_index]
                    if chosen_item == "Walking around and looking for classroom.":
                        time_limit -= 7
                        if time_limit <= 0:
                            game_state = "time up"
                        else:
                            game_state = "look for classroom"
                    elif chosen_item == "Use items.":
                        game_state = "item_use_hallway"
                    unlock_index = 0
        elif game_state == "look for classroom":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                background = pygame.image.load('Images/classroom.png')
                collisions = classroom_collisions
                student.x, student.y = 390,360
                game_state = "classroom"
        elif game_state == "item_use_hallway":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    unlock_index = (unlock_index + 1) % len(selected_items)
                elif event.key == pygame.K_UP:
                    unlock_index = (unlock_index - 1) % len(selected_items)
                elif event.key == pygame.K_RETURN:
                    chosen_item = selected_items[unlock_index]
                    if chosen_item == "Phone":
                        time_limit -= 2
                        if time_limit <= 0:
                            game_state = "time up"
                        else:
                            game_state = "use phone to find classroom"
                    else:
                        time_limit -= 4
                        if time_limit <= 0:
                            game_state = "time up"
                        else:
                            game_state = "can't find classroom"
                    unlock_index = 0
        elif game_state == "use phone to find classroom":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                background = pygame.image.load('Images/classroom.png')
                collisions = classroom_collisions
                student.x, student.y = 390,360
                game_state = "classroom"
        elif game_state == "can't find classroom":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = "hallway"

                            # CLASSROOM EVENT
# ------------------------------------------------------------------------------------
        elif game_state == "need laptop":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if "Laptop" in selected_items:
                    game_state = "game won"
                else:
                    game_state = "game over"
        elif game_state == "game won":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                background = pygame.image.load('Images/winning.png')
                win.blit(background, (0, 0))
                pygame.display.update()
                pygame.time.delay(2000) 
                run = False  # show image for 2 seconds (optional)
        elif game_state == "game over":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                background = pygame.image.load('Images/gameover.png')
                win.blit(background, (0, 0))
                pygame.display.update()
                pygame.time.delay(2000) 
                run = False


    # =====================================================
    # ---------------- NORMAL GAMEPLAY --------------------
    # =====================================================

    if game_state in ("bedroom", "livingroom", "frontyard", "backyard", 
        "metro_station", "busstop", "university", "hallway", "classroom"):
        keys = pygame.key.get_pressed()
        student.moving = False

        if not keys[pygame.K_e]:
            can_interact = True
        if keys[pygame.K_a]:
            student.direction = "left"
            student.moving = True
            move_player(student, -student.vel, 0)
        elif keys[pygame.K_d]:
            student.direction = "right"
            student.moving = True
            move_player(student, student.vel, 0)
        elif keys[pygame.K_w]:
            student.direction = "up"
            student.moving = True
            move_player(student, 0, -student.vel)
        elif keys[pygame.K_s]:
            student.direction = "down"
            student.moving = True
            move_player(student, 0, student.vel)

        # DOOR LOGIC
        player_rect = pygame.Rect(student.x, student.y, student.width, student.height)
        if game_state == "bedroom" and player_rect.colliderect(door_to_livingroom):
            if keys[pygame.K_e] and not items_chosen and can_interact:
                game_state = "item_select"
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
            elif player_rect.colliderect(door_to_the_front):
                if keys[pygame.K_e] and can_interact:
                    can_interact = False
                    background = pygame.image.load('Images/frontyard.png')
                    collisions = frontyard_collisions
                    game_state = "frontyard"
                    student.x, student.y = 210, 300
            elif player_rect.colliderect(door_to_backyard):
                if keys[pygame.K_e] and can_interact:
                    can_interact = False
                    background = pygame.image.load('Images/backyard.png')
                    collisions = backyard_collisions
                    game_state = "backyard"
                    student.x, student.y = 131, 353
        if game_state == "frontyard":
            if player_rect.colliderect(door_back_in_houseF):
                if keys[pygame.K_e] and can_interact:
                    can_interact = False
                    background = pygame.image.load('Images/livingroom.png')
                    collisions = livingroom_collisions
                    game_state = "livingroom"
                    student.x, student.y = 25, 160
            if player_rect.colliderect(unlock_key):
                if keys[pygame.K_e] and not unlock_bycle:
                    game_state = "item_use"
        if game_state == "backyard":
            if player_rect.colliderect(door_back_in_houseB):
                if keys[pygame.K_e] and can_interact:
                    can_interact = False
                    background = pygame.image.load('Images/livingroom.png')
                    collisions = livingroom_collisions
                    game_state = "livingroom"
                    student.x, student.y = 20, 380
            elif player_rect.colliderect(get_key) and not key_get:
                if keys[pygame.K_e] and can_interact:
                    can_interact = False
                    game_state = "try to get key"
        if game_state == "metro_station":
            if player_rect.colliderect(metro_gate):
                if keys[pygame.K_e] and can_interact:
                    can_interact = False
                    game_state = "check-in metro"
            elif player_rect.colliderect(old_man) and not help_old_man:
                if keys[pygame.K_e] and can_interact:
                    can_interact = False
                    game_state = "talk to old man"
        if game_state == "busstop":
            if player_rect.colliderect(bus):
                if keys[pygame.K_e] and can_interact:
                    can_interact = False
                    game_state = "check-in bus"
            elif player_rect.colliderect(friend) and not help_friend:
                if keys[pygame.K_e] and can_interact:
                    can_interact = False
                    game_state = "talk to friend"
        if game_state == "university":
            if player_rect.colliderect(senior) and not answered_senior:
                if keys[pygame.K_e] and can_interact:
                    can_interact = False
                    question_data = random.choice(quiz_questions)
                    game_state = "talk to senior"
            elif player_rect.colliderect(uni_door) and answered_senior:
                if keys[pygame.K_e] and can_interact:
                    can_interact = False
                    background = pygame.image.load('Images/hallway.png')
                    collisions = hallway_collisions
                    game_state = "hallway"
                    student.x, student.y = 106, 206
        if game_state == "hallway":
            if player_rect.colliderect(michelon):
                if keys[pygame.K_e] and can_interact:
                    can_interact = False
                    game_state = "talk to michelon"
            elif player_rect.colliderect(pascalle):
                if keys[pygame.K_e] and can_interact:
                    can_interact = False
                    game_state = "talk to pascalle"
            elif player_rect.colliderect(way):
                if keys[pygame.K_e] and can_interact:
                    can_interact = False
                    game_state = "find the way"
        if game_state == "classroom":
            if player_rect.colliderect(michelon2):
                if keys[pygame.K_e] and can_interact:
                    can_interact = False
                    game_state = "need laptop"


    # =====================================================
    # ---------------- DRAWING ----------------------------
    # =====================================================

    # SPECIAL MENUS MUST DRAW BEFORE BACKGROUND OVERWRITE
    if game_state == "start_menu":
        draw_start_menu()
        continue
    elif game_state == "tutorial":
        # ensure bedroom background is shown behind the tutorial box
        win.blit(background, (0, 0))
        draw_text_box(win, "Tutorial: You have 45 minutes to get to the university."
        "\nUse WASD to move and press E to interact."
        "\nPress ENTER to continue.", font)
        pygame.display.update()
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
        draw_selected_menu(win, font, selected_items, unlock_index, "Choose item to unlock bicycle:")
        pygame.display.update()
        continue
    elif game_state == "item_use_senior":
        draw_selected_menu(win, font, selected_items, unlock_index, "Choose item to use on the senior:")
        pygame.display.update()
        continue
    elif game_state == "wrong_item":
        draw_selected_menu(win, font, key_event_choice, unlock_index, "No key? What would you do?")
        pygame.display.update()
        continue
    elif game_state == "get_key":
        draw_text_box(win, f"It took you couple minutes, but you finally got the keys.\nPress ENTER to continue.", font)
        pygame.display.update()
        continue
    elif game_state == "walk_to_station":
        draw_text_box(win, f"Walking to the station cost you 12 minutes.\nPress ENTER to continue.", font)
        pygame.display.update()
        continue
    elif game_state == "call_mom":
        draw_text_box(win, f"Mom: 'Key? I saw Leo playing with it.\nGo find him, maybe?", font)
        pygame.display.update()
        continue
    elif game_state == "try to get key":
        draw_selected_menu(win, font, try_to_get_key, unlock_index, "It looks like Leo has the keys with him. What would you do?")
        pygame.display.update()
        continue
    elif game_state == "Get key from Leo":
        draw_selected_menu(win, font, talk_to_Leo, unlock_index, "Choose what to say so Leo gives you the keys.")
        pygame.display.update()
        continue
    elif game_state == "Leo still ignore you":
        draw_text_box(win, f"Leo looks at you… and ignores you.\nPress ENTER to continue.", font)
        pygame.display.update()
        continue
    elif game_state == "Leo give you the key":
        draw_text_box(win, f"Leo looks at you… and drops the keys.\nPress ENTER to continue.", font)
        pygame.display.update()
        continue
    elif game_state == "check-in metro":
        draw_selected_menu(win, font, selected_items, unlock_index, "Choose item to check-in metro:")
        pygame.display.update()
        continue
    elif game_state == "don't have a phone":
        draw_text_box(win, f"You don't have a phone with you.", font)
        pygame.display.update()
        continue
    elif game_state == "talk to old man":
        draw_selected_menu(win, font, old_man_event, unlock_index, "Old man: 'Please help me pick up these things.'")
        pygame.display.update()
        continue
    elif game_state == "help old man":
        draw_text_box(win, f"The old man gives you a one-time metro ticket"
        "\nin return for your kindness. You lose 5 minutes."
            "\nPress ENTER to continue.", font)
        pygame.display.update()
        continue
    elif game_state == "can not not check-in metro":
        draw_text_box(win, f"You can not use this item to check-in metro."
            "\nPress ENTER to continue.", font)
        pygame.display.update()
        continue
    elif game_state == "talk to friend":
        draw_text_box(win, f"Classmate: 'Hey! I think my scooter broke down,"
            "\nI forgot my phone. Can you call a mechanic for me?'"
            "\nPress ENTER to continue.", font)
        pygame.display.update()
        continue
    elif game_state == "talk to friend2":
        draw_selected_menu(win, font, friend_event, unlock_index, "What would you do?")
        pygame.display.update()
        continue
    elif game_state == "don't have phone":
        draw_text_box(win, f"You don’t have a phone either. You feel sorry for him."
            "\nbut you have to continue on your way."
            "\nPress ENTER to continue.", font)
        pygame.display.update()
        continue
    elif game_state == "wanna walk?":
        draw_selected_menu(win, font, wanna_walk, unlock_index, "Do you want to walk to university?")
        pygame.display.update()
        continue
    elif game_state == "check-in bus":
        draw_selected_menu(win, font, selected_items, unlock_index, "Choose item to check-in bus:")
        pygame.display.update()
        continue
    elif game_state == "don’t have enough money":
        draw_text_box(win, f"You don't have enough money to check-in."
            "\nPress ENTER to continue.", font)
        pygame.display.update()
        continue
    elif game_state == "can not not check-in bus":
        draw_text_box(win, f"You can not use this item to check-in bus."
            "\nPress ENTER to continue.", font)
        pygame.display.update()
        continue
    elif game_state == "walk to university":
        draw_text_box(win, f"It took you 15 minutes."
         "\nBut you finally arrived at the university."
        "\nPress ENTER to continue.", font)
        pygame.display.update()
        continue
    elif game_state == "help friend":
        draw_text_box(win, f"You call a mechanic for your classmate."
         "\nHe offers you a ride to the university."
        "\nIt took you 7 minutes. Press ENTER to continue.", font)
        pygame.display.update()
        continue
    elif game_state == "talk to senior":
        draw_selected_menu(win, font, senior_event, unlock_index, "Senior: 'Not so fast! answer my question to pass!'")
        pygame.display.update()
        continue
    elif game_state == "answer senior":
        draw_selected_menu(win, font, question_data["options"], unlock_index, question_data["question"])
        pygame.display.update()
        continue
    elif game_state == "pass senior":
        draw_text_box(win, f"Senior: 'Alright! You may pass.'\nPress ENTER to continue.", font)
        pygame.display.update()
        continue
    elif game_state == "wrong answer":
        draw_text_box(win, f"Senior shake head: 'Nah ah! Try again later.'\nPress ENTER to continue.", font)
        pygame.display.update()
        continue
    elif game_state == "item_use_senior":
        draw_selected_menu(win, font, selected_items, unlock_index, "Choose item to use on the senior:")
        pygame.display.update()
        continue
    elif game_state == "talk to michelon":
        draw_selected_menu(win, font, talk_to_michelon, unlock_index, "Michelon: 'Hey! Need help?'")
        pygame.display.update()
        continue
    elif game_state == "communicate with michelon":
        draw_text_box(win, f"After 10 minutes of conversation,"
        "\nyou finally get directions to the classroom."
        "\nPress ENTER to continue.", font)
        pygame.display.update()
        continue
    elif game_state == "talk to pascalle":
        draw_selected_menu(win, font, talk_to_pascalle, unlock_index, "Pascalle: 'Hi there! Can I help you?'")
        pygame.display.update()
        continue
    elif game_state == "communicate with pascalle":
        draw_text_box(win, f"After 15 minutes of chat,"
        "\nYou finally get directions to the classroom."
        "\nPress ENTER to continue.", font)
        pygame.display.update()
        continue
    elif game_state == "find the way":
        draw_selected_menu(win, font, find_the_way, unlock_index, "How would you find the classroom?")
        pygame.display.update()
        continue
    elif game_state == "look for classroom":
        draw_text_box(win, f"You wander the hallways for 7 minutes,"
        "\nBut eventually find the classroom."
        "\nPress ENTER to continue.", font)
        pygame.display.update()
        continue
    elif game_state == "item_use_hallway":
        draw_selected_menu(win, font, selected_items, unlock_index, "Choose item to find the classroom:")
        pygame.display.update()
        continue
    elif game_state == "use phone to find classroom":
        draw_text_box(win, f"You use your phone's school app to find the classroom."
        "\nPress ENTER to continue.", font)
        pygame.display.update()
        continue
    elif game_state == "can't find classroom":
        draw_text_box(win, f"You can’t seem to find the classroom with this item."
        "\nPress ENTER to continue.", font)
        pygame.display.update()
        continue
    elif game_state == "need laptop":
        draw_text_box(win, f"Michelon: 'You need a laptop to get in classroom.'\nPress ENTER to continue.", font)
        pygame.display.update()
        continue
    elif game_state == "game won":
        draw_text_box(win, f"Congratulations! You made it to class on time!"
        "\nPress ENTER to continue.", font)
        pygame.display.update()
        continue
    elif game_state == "game over":
        draw_text_box(win, f"Game Over! You didn't make it to class on time."
        "\nPress ENTER to continue.", font)
        pygame.display.update()
        continue
    win.blit(background, (0, 0))
    redrawGameWindow()