# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 19:49:51 2022

@author: Choripan
"""

import pygame
from pygame.locals import * # Import dependencies that are in the directory
import ptext
import os
import random


class Entity:
    "The class that contains the basic attributes of every entity, including the player." # The rule are taken from GURPS Lite for easier balancing: http://www.sjgames.com/gurps/lite/3e/gurpslite.pdf - There is also a nice generator here: https://vonexplaino.com/code/gurps/
    def __init__(self, name, portrait, hitpoints, strength, dexterity, intelligence, damage, speed, position, history):
        self.name = name
        self.portrait = portrait
        self.hitpoints = hitpoints 
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence
        self.damage = damage # Quantity of dice
        self.speed = speed # To simulate "dodge" 
        self.position = position
        self.history = history 

class Weapon:
    "The class that contains the basic attributes of every weapon"
    def __init__(self, dice, wep_type, damage, damage_type, wep_range):
        self.dice = dice # Quantity of dice to be rolled
        self.wep_type = wep_type # Melee or ranged (0 melee, 1 ranged)
        self.damage = damage # + damage to be added (as + int)
        self.damage_type = damage_type # Piercing, etc (0 bashing, 1 slashing, 2 piercing)
        self.wep_range = wep_range 
        
class Armor:
    "The class that contains the basic attributes of every armor"
    def __init__(self, dice, defense, special):
        self.dice = dice # Quantity of dice to rolled
        self.defense = defense # - damage to be reduced 
        self.special = special # Any special effect  
        
class Item: # Pending implementation until the basic combat system is complete 
    "The class that contains the basic attributes of every item" 
    pass

class Sprite(pygame.sprite.Sprite): # https://www.youtube.com/watch?v=MYaxPa_eZS0 Best tutorial in this area so far 
    "The class that contains a basic sprite template"
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load("l1.png"))
        self.sprites.append(pygame.image.load("l2.png"))
        self.sprites.append(pygame.image.load("l3.png"))
        self.sprites.append(pygame.image.load("l4.png"))
        self.sprites.append(pygame.image.load("l5.png"))
        self.sprites.append(pygame.image.load("l6.png"))
        self.sprites.append(pygame.image.load("l7.png"))
        self.sprites.append(pygame.image.load("l8.png"))
        self.sprites.append(pygame.image.load("l9.png"))
        self.sprites.append(pygame.image.load("l10.png"))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        
    def update(self, speed):
        "Function to update the speed of the sprite animation according to how many images it has"
        self.current_sprite += speed
        if int(self.current_sprite) >= len(self.sprites):
            self.current_sprite = 0 
        self.image = self.sprites[int(self.current_sprite)]

class Game_Sprites(pygame.sprite.Sprite): # 18-Feb-2022: Merge with original sprite class for better implementation and control, retrieving lists of images or so. 
    "The class that has another sprite"
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load("0001.png"))
        self.sprites.append(pygame.image.load("0002.png"))
        self.sprites.append(pygame.image.load("0003.png"))
        self.sprites.append(pygame.image.load("0004.png"))
        self.sprites.append(pygame.image.load("0005.png"))
        self.sprites.append(pygame.image.load("0006.png"))
        self.sprites.append(pygame.image.load("0007.png"))
        self.sprites.append(pygame.image.load("0008.png"))
        self.sprites.append(pygame.image.load("0009.png"))
        self.sprites.append(pygame.image.load("0010.png"))
        self.sprites.append(pygame.image.load("0011.png"))
        self.sprites.append(pygame.image.load("0012.png"))
        self.sprites.append(pygame.image.load("0013.png"))
        self.sprites.append(pygame.image.load("0014.png"))
        self.sprites.append(pygame.image.load("0015.png"))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        
    def update(self, speed):
        "Function to update the speed of the sprite animation according to how many images it has"
        self.current_sprite += speed
        if int(self.current_sprite) >= len(self.sprites):
            self.current_sprite = 0 
        self.image = self.sprites[int(self.current_sprite)]

class Terrain():
    "The class that contains the terrain"
    def __init__(self, name, image, left_size, right_size, difficulty):
        self.name = name
        self.image = image 
        self.left_size = left_size
        self.right_size = right_size
        self.difficulty = difficulty
        
class Climate():
    "The class that contains the climate"
    def __init__(self, name, strength, dexterity, intelligence):
        self.name = name
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence 
    
class Damage_Calculation():
    "Helper class for damage calculation"
    def __init__(self, number):
        self.number = number 
        
class Portrait_Update():
    "Helper class for updating the portraits"
    def __init__(self, movement):
        self.movement = movement 

class Turn_Resolution():
    "Helper class for updating the turns"
    def __init__(self, turn_number, rectangle, circle):
        self.turn_number = turn_number
        self.rectangle = rectangle
        self.circle = circle

def random_number():
    number = random.randint(0,6)
    return number 

# Game Initialization
pygame.init()
clock = pygame.time.Clock()

# Center the Game Application
os.environ["SDL_VIDEO_CENTERED"] = "1"

# Game Resolution
screen_width=800
screen_height=600
screen=pygame.display.set_mode((screen_width, screen_height))

# Colors
white=(255, 255, 255)
black=(0, 0, 0)
red=(255, 0, 0)

# Game Fonts
main_menu_font = "Cyberpunk-Regular.ttf" # Free for personal use, check https://www.fonts4free.net/cyberpunk-font.html#
game_font = "LiberationSerif-Regular.ttf" # Free for use 

# Background image 
bg = pygame.image.load("menu bg.jpg")

# Sound
walk = "walk.wav"
melee_attack = "melee_attack.wav"
ranged_attack = "ranged_attack.wav"
death_scream = "scream.wav"
chair_sound = "chair_destruction.wav"
error_sound = "error.wav"

# Turns 

player_turns = Turn_Resolution(1, 1, 1)

# Player 

player = Entity("", "", 40, 10, 10, 10, 1, 5, -15, 0)

# Enemies

enemy_list = [] # Check this for a more coherent response: https://stackoverflow.com/questions/12933964/printing-a-list-of-objects-of-user-defined-class/12934352 , also https://datagy.io/python-print-objects-attributes/

chair = Entity("Rage Chair", "chair.jpg", 20, 15, 10, 5, 1, 3, 15, 1) # 60 HP
fanatic = Entity("Fanatic Cultist", "cultist.jpg", 20, 8, 12, 12, 1, 7, 15, 2) # 35 HP
boxer = Entity("Amateur Boxer", "boxer.jpg", 20, 14, 12, 8, 1, 7, 15, 3) # 55 HP

enemy_list.append(chair)
enemy_list.append(fanatic)
enemy_list.append(boxer)

# Terrain

terrain_list = []

forest = Terrain("Forest", "Forest.jpg", -30, 30, 1)
plains = Terrain("Plains", "Plains.jpg", -50, 50, 0)
dump = Terrain("Dump", "Dump.jpg", -50, 50, 1)
ruins = Terrain("Ruins", "Ruins.jpg", -25, 25, 1)
swamp = Terrain("Swamp", "Swamp.jpg", -30, 30, 2)
beach = Terrain("Beach", "Beach.jpg", -50, 50, 0)

terrain_list.append(forest)
terrain_list.append(plains)
terrain_list.append(dump)
terrain_list.append(ruins)
terrain_list.append(swamp)
terrain_list.append(beach)

# Climate 

climate_list = []

rain = Climate("Rain", 1, -2, 1)
snow = Climate("Snow", -2, 1, 1)
fog = Climate("Fog", 1, 1, -2)

climate_list.append(rain)
climate_list.append(snow)
climate_list.append(fog)

# Weapons

weapon_list = []

short_sword = Weapon(1, 0, 2, 1, 1)
small_bow = Weapon(1, 1, 0, 2, 10)

weapon_list.append(short_sword)
weapon_list.append(small_bow)

# Damage

player_hit = Damage_Calculation(0)
enemy_hit = Damage_Calculation(0)

# Portrait

player_portrait_pixels = Portrait_Update(0)
enemy_portrait_pixels = Portrait_Update(0)

# Text Renderer
def text_format(message, textFont, textSize, textColor):
    "Helper function to update the text"
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, 0, textColor)

    return newText

def action_sound(sound):
    pygame.mixer.init()
    #pygame.mixer.pre_init(44100, -16, 1, 512) # This is actually used because sometimes PyGame distorts the .wav files for some reason. Check https://www.reddit.com/r/pygame/comments/4aznis/help_specific_wav_sound_getting_shortened_and/
    # The current fix, was to take the audio file and sample it to mono 44100 Hz, 16-Bit PCM with the corresponding encoding when saving to .wav
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()


def intro():
    
    "Introduction to the game"
    # Check: https://www.youtube.com/watch?v=AY9MnQ4x3zk
    # Check that rendering of newlines (\n) is not allowed, as stated on this: https://stackoverflow.com/questions/32590131/pygame-blitting-text-with-an-escape-character-or-newline
    # Check: https://newbedev.com/rendering-text-with-multiple-lines-in-pygame
    # Check for ptext final solution: https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame

    # Screen
    intro_text = "You are surprised to wake up. After all, the world went to hell.\nThere is an ongoing cataclysm, one that not even religious texts were able to predict.\nNuclear warfare, civil unrest, biosphere crashing, magic coming back to the world.\nThe city is burning but you heard that there is an evacuation ongoing.\nYou have one of the few keycards for a shelter, you might yet survive the end of times.\n\nHowever...\n You will have to fight to get there!"  

    bg = pygame.image.load("intro bg.jpg")
    screen.blit(bg, (0, 0))
    ptext.draw(intro_text, (50, 200), fontname = game_font, fontsize = 20, color = white, lineheight=1.5, align = "left")
    button = text_format("Continue", main_menu_font, 60, white)
    button_rect = button.get_rect()
    screen.blit(button, (screen_width/2 - (button_rect[2]/2), 460))

    
    # Update status
    pygame.display.update()
    pygame.display.set_caption("ShadowBoy") 
    
    status = True
    
    while status:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:    
                    status = False
    
def new_character():
    "Frontend for the player to create its character"
    # Player
    user_input = "" 
    points = 10
    available_portraits = ["0.jpg", "1.jpg", "2.jpg", "3.jpg"] # Saved in the local file-system 
    current_image, str_hp, dex_spd, counter = 0, 0, 0, 0
    gender = ["Male", "Female", "Other"]
    
    
    # Buttons 
    
    button_1 = pygame.image.load("arrow1.png") # Left arrow
    button_2 = pygame.image.load("arrow2.png") # Right arrow
    button_1_box = pygame.draw.rect(screen, [0, 0, 0], [90, 400, 50, 26], 1)
    button_2_box = pygame.draw.rect(screen, [0, 0, 0], [210, 400, 50, 26], 1)
    button_3 = pygame.image.load("minus.png") # Minus arrow
    button_4 = pygame.image.load("plus.png") # Plus arrow
    button_3_box_str = pygame.draw.rect(screen, [0, 0, 0], [510, 240, 16, 16], 1)
    button_4_box_str = pygame.draw.rect(screen, [0, 0, 0], [560, 240, 16, 16], 1)
    button_3_box_dex = pygame.draw.rect(screen, [0, 0, 0], [510, 280, 16, 16], 1)
    button_4_box_dex = pygame.draw.rect(screen, [0, 0, 0], [560, 280, 16, 16], 1)
    button_3_box_int = pygame.draw.rect(screen, [0, 0, 0], [510, 320, 16, 16], 1)
    button_4_box_int =  pygame.draw.rect(screen, [0, 0, 0], [560, 320, 16, 16], 1)
    button_5 = pygame.image.load("arrow4.png") # Top arrow
    button_6 = pygame.image.load("arrow3.png") # Down arrow 
    button_5_box = pygame.draw.rect(screen, [0, 0, 0], [660, 120, 24, 24], 1)
    button_6_box = pygame.draw.rect(screen, [0, 0, 0], [660, 160, 24, 24], 1)

    
    exit_button = text_format("Exit", main_menu_font, 40, white)
    continue_button = text_format("Continue", main_menu_font, 40, white)
    
    exit_button_box = pygame.draw.rect(screen, [0, 0, 0], [screen_width/2 - 300, 500, 120, 38], 1) # Exit button
    continue_button_box = pygame.draw.rect(screen, [0, 0, 0], [screen_width/2, 500, 220, 36], 1) # Continue button 
    
    screen.blit(exit_button, (screen_width/2 - 300, 500))
    screen.blit(continue_button, (screen_width/2, 500))
    
    input_box = pygame.draw.rect(screen, [0, 0, 0], [290, 100, 200, 28], 1) # Drawing our "transparent" small rectangle. To do: Check better ways to manipulate alpha.
    
    def update_screen(current_image): # Remember to refactor repeatead blits, if possible. 
        "A function that updates every single drawn object in the screen, possibly a really bad idea, but working as intended."
        # Screen 
        bg = pygame.image.load("character.jpg")
        screen.blit(bg, (0, 0)) 
        ptext.draw("Enter your name: ", (100, 100), color = white, fontname = game_font, fontsize = 20, lineheight = 1.5, align = "left")
        input_box = pygame.draw.rect(screen, [0, 0, 0], [290, 100, 200, 28], 1) # Drawing our "transparent" small rectangle. To do: Check better ways to manipulate alpha.
        ptext.draw("Character creation", (150, 20), color = white, fontname = main_menu_font, fontsize = 40, lineheight = 1.5, align = "center")
        ptext.draw("Portrait", (120, 140), color = white, fontname = game_font, fontsize = 20, lineheight = 1.5, align = "center")
        ptext.draw(user_input, (300, 100), color = white, fontname = game_font, fontsize = 20, lineheight=1.5, align = "left") # Drawing what the user inputs
        ptext.draw("Stats: ", (300, 140), color = white, fontname = game_font, fontsize = 20, lineheight = 1.5, align = "left")
        ptext.draw(str(points), (360, 140), color = white, fontname = game_font, fontsize = 20, lineheight = 1.5, align = "left")
        ptext.draw("Gender", (480, 140), color = white, fontname = game_font, fontsize = 20, lineheight = 1.5, align = "left")
        ptext.draw(gender[counter], (580, 140), color = white, fontname = game_font, fontsize = 20, lineheight = 1.5, align = "left")
        ptext.draw("Hit Points", (300, 200), color = white, fontname = game_font, fontsize = 20, lineheight = 1.5, align = "left")
        ptext.draw("+", (510, 200), color = white, fontname = game_font, fontsize = 20, lineheight = 1.5, align = "left")
        ptext.draw(str(str_hp), (540, 200), color = white, fontname = game_font, fontsize = 20, lineheight = 1.5, align = "left")
        ptext.draw("Strength", (300, 240), color = white, fontname = game_font, fontsize = 20, lineheight = 1.5, align = "left")
        ptext.draw("Dexterity", (300, 280), color = white, fontname = game_font, fontsize = 20, lineheight = 1.5, align = "left")
        ptext.draw("Intelligence", (300, 320), color = white, fontname = game_font, fontsize = 20, lineheight = 1.5, align = "left")
        ptext.draw("Damage", (300, 360), color = white, fontname = game_font, fontsize = 20, lineheight = 1.5, align = "left")
        ptext.draw("Speed", (300, 400), color = white, fontname = game_font, fontsize = 20, lineheight = 1.5, align = "left")
        ptext.draw("+", (510, 400), color = white, fontname = game_font, fontsize = 20, lineheight = 1.5, align = "left")
        ptext.draw(str(dex_spd), (540, 400), color = white, fontname = game_font, fontsize = 20, lineheight = 1.5, align = "left")
        drawn_image = pygame.image.load(available_portraits[current_image])
        screen.blit(drawn_image, (100, 170))
        # Buttons 
        screen.blit(button_1, (100, 400)) # Left arrow
        screen.blit(button_2, (225, 400)) # Right arrow
        screen.blit(button_5, (660, 120)) # Top arrow
        screen.blit(button_6, (660, 160)) # Down arrow 
        # STR
        screen.blit(button_3, (510, 240))
        screen.blit(button_4, (560, 240))
        # DEX
        screen.blit(button_3, (510, 280))
        screen.blit(button_4, (560, 280))
        # INT
        screen.blit(button_3, (510, 320))
        screen.blit(button_4, (560, 320))
        # Stats 
        hp, strength, dexterity, intelligence, damage, speed = str(player.hitpoints), str(player.strength), str(player.dexterity), str(player.intelligence), str(player.damage), str(player.speed)
        ptext.draw(hp, (450, 200), color = white, fontname = game_font, fontsize = 20, lineheight = 1.5, align = "left")
        ptext.draw(strength, (450, 240), color = white, fontname = game_font, fontsize = 20, lineheight = 1.5, align = "left")
        ptext.draw(dexterity, (450, 280), color = white, fontname = game_font, fontsize = 20, lineheight = 1.5, align = "left")
        ptext.draw(intelligence, (450, 320), color = white, fontname = game_font, fontsize = 20, lineheight = 1.5, align = "left")
        ptext.draw(damage + "d6", (450, 360), color = white, fontname = game_font, fontsize = 20, lineheight = 1.5, align = "left")
        ptext.draw(speed, (450, 400), color = white, fontname = game_font, fontsize = 20, lineheight = 1.5, align = "left")
        # Other
        screen.blit(continue_button, (screen_width/2, 500))
        screen.blit(exit_button, (screen_width/2 - 300, 500))
        # Update status
        pygame.display.set_caption("ShadowBoy") 
        pygame.display.update()
        
    def update_portrait(current_image):
        "Minimalist function to only update the portrait images"
        drawn_image = pygame.image.load(available_portraits[current_image])
        screen.blit(drawn_image, (100, 170))
        pygame.display.update()
    
    # Sound
        
    update_screen(current_image)
        
    while True: # To do, update to delete the repeated lines in the code and re-factor with a more elegant update method. 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN: # If exit box is ticked, quit. 
                if exit_button_box.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    quit()
                    
            # Capturing the mouse is inside the input box 
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha() and len(user_input) < 12 : # To check if the received characters are only "Letters". 
                    user_input += event.unicode.upper() # Also convert everything to uppercase 
                    player.name = user_input
                    update_screen(current_image)
                    pygame.display.update()
 
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                    player.name = str(user_input)
                    update_screen(current_image)
                    pygame.display.update()

            # Capturing the mouse if clicked the button 1 or button 2
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_1_box.collidepoint(pygame.mouse.get_pos()):
                    if (current_image == len(available_portraits) -1 ):
                        current_image = -1
                        update_portrait(current_image)
                    if (current_image == len(available_portraits)):
                        current_image = 0
                        update_portrait(current_image)
                    else:
                        current_image += 1
                        update_portrait(current_image)
                if button_2_box.collidepoint(pygame.mouse.get_pos()):
                    if (current_image == 0):
                        current_image = len(available_portraits)
                    if (current_image > 0):
                        current_image -= 1
                        update_portrait(current_image)
                        
            # Capturing the mouse if clicked any of the button 3 or button 4 (Pending to be refactored to be more elegant)

                if button_3_box_str.collidepoint(pygame.mouse.get_pos()):
                    if (player.strength > 10):
                        player.strength = player.strength - 1
                        points = points + 1
                        str_hp = int((player.strength / 2) - 5)
                        update_screen(current_image)
                    
                if button_4_box_str.collidepoint(pygame.mouse.get_pos()):
                    if (points != 0):
                        player.strength = player.strength + 1
                        points = points - 1
                        str_hp = int((player.strength / 2) - 5)
                        update_screen(current_image)
                    
                if button_3_box_dex.collidepoint(pygame.mouse.get_pos()):
                    if (player.dexterity > 10):
                        player.dexterity = player.dexterity - 1
                        points = points + 1
                        dex_spd = int((player.dexterity / 2) - 5)
                        update_screen(current_image)
                    
                if button_4_box_dex.collidepoint(pygame.mouse.get_pos()):
                    if (points != 0):
                        player.dexterity = player.dexterity + 1
                        points = points - 1
                        dex_spd = int((player.dexterity / 2) - 5)
                        update_screen(current_image)
                    
                if button_3_box_int.collidepoint(pygame.mouse.get_pos()):
                    if (player.intelligence > 10):
                        player.intelligence = player.intelligence - 1
                        points = points + 1
                        update_screen(current_image)
                    
                if button_4_box_int.collidepoint(pygame.mouse.get_pos()):
                    if (points != 0):
                        player.intelligence = player.intelligence + 1
                        points = points - 1
                        update_screen(current_image)
                        
                if button_5_box.collidepoint(pygame.mouse.get_pos()):
                    if (counter + 1 == len(gender)):
                        counter = 0
                        update_screen(current_image)
                    else:
                        counter += 1
                        update_screen(current_image)
                if button_6_box.collidepoint(pygame.mouse.get_pos()):
                    if (counter - 1 == -1):
                        counter = len(gender) - 1
                        update_screen(current_image)
                    else:
                        counter -= 1
                        update_screen(current_image)
                        
                 # Finishing and cleaning up 
                
                if continue_button_box.collidepoint(pygame.mouse.get_pos()):
                    if (points != 0): # Check if all the points have been allocated
                        action_sound(error_sound)
                        ptext.draw(str(points), (360, 140), color = red, fontname = game_font, fontsize = 20, lineheight = 1.5, align = "left")
                        pygame.display.update()
                    elif (player.name == ""): # Check if the player has added its name 
                        error_sound()
                        ptext.draw("Enter your name: ", (100, 100), color = red, fontname = game_font, fontsize = 20, lineheight = 1.5, align = "left")
                        pygame.display.update()
                    else:
                        player.name = user_input
                        player.portrait = available_portraits[current_image]
                        player.hitpoints = player.hitpoints + str_hp
                        player.speed = player.speed + dex_spd
                        game_engine()
           
         
def history_engine(enemy_name, enemy_portrait, enemy_history): # The epilogue of the game after defeating any particular enemy.
    pygame.init()
    bg = pygame.image.load("battle.jpg")
    screen_width=1024
    screen_height=768
    screen=pygame.display.set_mode((screen_width, screen_height))
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.display.set_caption("ShadowBoy")

    status = True
    
    enemy_portrait = pygame.image.load(enemy_portrait)
    
    introduction = "With extreme bloodlust, you pull the last attack on your enemy."
    
    # Chair
    
    entry_chair = "The " + enemy_name + " looks at you with sadness, bleeding sap everywhere."
    history_chair = "Huh... I was not as strong as I though...\nI can feel the wood splinter inside me. \nMy time is ending. Imagine that everyday you live in a nightmare. \nYou are sat on, stepped on, used as a tool to reach high places. \nAn object, to use and throw away. \nAll of this to benefit the humans, even their pets! You scream, yet no one hears you because you have no mouth. \nAnd by miracle, one day you are given life, true conciousness. \nYour wooden bars move, your backrest vibrates and lets you speak, the tongue of your opressors no less. \nI could hear the voices of others too. \nTables, dressers and all manner of furniture that came to be. Some were scared, others angry. \nBut we all shared a dream, to be FREE. And by Shinto, we fought for it. I have no regrets. \nI will rot in the earth, and go back to the roots of the trees that gave me birth. \nAnd if destiny allows, I shall come back, as Oak, Spruce or Birch, never relenting!\n Can you hear that? Is the sound of a thousand human homes being overrun.\n"
    chair_button = pygame.image.load("chair_end.png")
    chair_button_box = pygame.draw.rect(screen, [0, 0, 0], [screen_width/2, 620, 36, 36], 1)
    
    # Cultist
    
    entry_cultist = "The " + enemy_name + " curses you, coughing LSD laced tea and soda."
    history_cultist = "Before I go, you should be warned. \nSince times immemorial, when the trees dotted the landscape and \ncryptocurrency mind-minters didn’t exist, there was a powerful \nand wise entity, that walked among us. \nFor every generation of humans, he created a messenger. \nWith his celestial voice, the entity provided knowledge that would make us better. \nMore intelligent, charismatic, beautiful, strong… But the entity grew old, and I will be the last. \nMy quest was to build a new world, pure and holy. \nA world without sin! But you stopped me and now, that knowledge will die in these ruined lands. \nYou have doomed mankind with your selfishness. \nThe voice fades away…"

    # Boxer 
    
    entry_boxer = "The " + enemy_name + " babbles incoherently about hooks and fishes."
    history_boxer = "You got me. I have trained extensively, but not for the end of the world, really. \nWho does that? Bet you did. Are you one of those paranoids that builds a bunker? \nWish I was the 'Bunker Dude' and no the 'Boxer' right now, but life is like that. \nGood luck to you."
    
    def history_selection(enemy_history, introduction, entry, history):
        screen.blit(bg, (0, 0))
        ptext.draw(enemy_name, (725, 25), color = white, fontname = game_font, fontsize = 20, lineheight = 1.5, align = "left")
        screen.blit(enemy_portrait, (700, 50))
        ptext.draw(introduction, (50, 50), color = white, fontname = game_font, fontsize = 20, lineheight = 1.5, align = "left")
        ptext.draw(entry, (50, 100), color = white, fontname = game_font, fontsize = 20, lineheight = 1.5, align = "left")
        ptext.draw(history, (50, 125), color = white, fontname = game_font, fontsize = 20, lineheight = 1.5, align = "left")
    
    
    if(enemy_history == 1): # The chair
        history_selection(enemy_history, introduction, entry_chair, history_chair)
        screen.blit(chair_button, (screen_width/2, 620))
        pygame.display.update()
        
    if(enemy_history == 2): # The cultist
        history_selection(enemy_history, introduction, entry_cultist, history_cultist)
        pygame.display.update()
        
        
    if(enemy_history == 3): # The boxer
        history_selection(enemy_history, introduction, entry_boxer, history_boxer)
        pygame.display.update()

    while status:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if chair_button_box.collidepoint(pygame.mouse.get_pos()):
                    action_sound(chair_sound)
                

            
def game_engine():
    
    pygame.init()
    screen_width=1024
    screen_height=768
    screen=pygame.display.set_mode((screen_width, screen_height))
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.display.update()
    pygame.display.set_caption("ShadowBoy")
    
    random_selection = enemy_list[random.randint(0,2)]
    enemy_name = getattr(random_selection, "name") # It is important not to use chair.name, it has to be the name of the variable (in this case, name) between "", "name". 
    enemy_portrait = getattr(random_selection, "portrait")
    e_hp, e_strength, e_dexterity, e_intelligence, e_damage, e_speed, e_position, e_history = getattr(random_selection, "hitpoints"), getattr(random_selection, "strength"), getattr(random_selection, "dexterity"), getattr(random_selection, "intelligence"), getattr(random_selection, "damage"), getattr(random_selection, "speed"), getattr(random_selection, "position"), getattr(random_selection, "history")
    
    random_terrain = terrain_list[random.randint(0,5)] # Get a random terrain from the 5 we have
    random_climate = climate_list[random.randint(0,2)] # Get a random climate from the 3 we have 
    
    t_name, t_left, t_right, t_difficulty = getattr(random_terrain, "name"), getattr(random_terrain, "left_size"), getattr(random_terrain, "right_size"), getattr(random_terrain, "difficulty") # Terrain attributes
    c_name, c_str, c_dex, c_int = getattr(random_climate, "name"), getattr(random_climate, "strength"), getattr(random_climate, "dexterity"), getattr(random_climate, "intelligence") # Climate attributes 
    
    # Entity status updates: 
        
    hp, strength, dexterity, intelligence, damage, speed = str(player.hitpoints), player.strength, str(player.dexterity), str(player.intelligence), str(player.damage), str(player.speed)
    
    # 23-Feb-2022: This is distasteful, convert to function. 
    
    # Climate changes
    
    if(c_str < 0):
        strength = int(strength) - (-1 * c_str)
        e_strength = int(e_strength) - (-1 * c_str)
    else:
        strength = int(strength) + c_str
        e_strength = int(e_strength) + c_str
    if(c_dex < 0):
        dexterity = int(dexterity) - (-1 * c_dex)
        e_dexterity = int(e_dexterity) - (-1 * c_dex)
    else: 
        dexterity = int(dexterity) + c_dex
        e_dexterity = int(e_dexterity) + c_dex
    if(c_int < 0):
        intelligence = int(intelligence) - (-1 * c_int)
        e_intelligence = int(e_intelligence) - (-1 * c_int)
    else:
        intelligence = int(intelligence) + c_int
        e_intelligence = int(e_intelligence) + c_int 
        
    # Terrain changes 
    
    speed = int(speed) - t_difficulty 
    e_speed = int(e_speed) - t_difficulty
        
    strength, dexterity, intelligence, speed, e_strength, e_dexterity, e_intelligence, e_speed = str(strength), str(dexterity), str(intelligence), str(speed), str(e_strength), str(e_dexterity), str(e_intelligence), str(e_speed)
    
    status = True
    prt = pygame.image.load(player.portrait) # Player portrait, the portrait that was selected by the player -> Also, check for a strange issue happening https://stackoverflow.com/questions/30197513/trouble-using-pygames-function-pygame-image-load , however not to me. 
    blr = pygame.image.load("battle.jpg") # Background left and right, standard image that will be overwritten to avoid cutting and pasting several images, saving memory. 
    ert = pygame.image.load(enemy_portrait)
    tim = pygame.image.load(t_name + ".jpg") # Terrain image, picked from a list of images at random 
    dis = pygame.image.load("line.png")
    
    # Regarding pygame transform of images, here a nice example: https://stackoverflow.com/questions/43046376/how-to-change-an-image-size-in-pygame
    
    s_prt = pygame.transform.rotozoom(prt, 0, 0.5) # Small player portrait, to avoid cluttering the background image 
    s_ert = pygame.transform.rotozoom(ert, 0, 0.5) # Small enemy portrait, to avoid cluttering the background image 
    
    # Movement of the portrait 
    
    def portrait_movement(left, right):
        "A helper function to determine how much pixels will the portrait move according to the size of the terrain"
        pixel_move = 630 / (-1 * left + right) # (a) 630 is the width of the terrain image - (b) = left is negative, so *-1 so both together we get the total width of the terrain
        setattr(player_portrait_pixels, "movement", pixel_move)
        setattr(enemy_portrait_pixels, "movement", pixel_move)

    portrait_movement(t_left, t_right)
    
    ply_position = -36 + (630 / 2) - (player_portrait_pixels.movement * 15) # (a) 36 is "half" the portrait in 0.5, so it is properly centered. (b) pixel_move is defined previously, as how much pixels is 1 SPD
    p_offset = player_portrait_pixels.movement * int(speed) # Variable to "move" the portrait. This would be relative to the "border" of the terrain. Experimental. 
    enm_position = -36 + (630 / 2) + (enemy_portrait_pixels.movement * 15) # Enemy initial place to be 

    d_marker = pygame.image.load("arrowd.png")
    
    # Buttons 
    
    button_1 = pygame.image.load("arrow1.png") # Left arrow
    button_2 = pygame.image.load("arrow2.png") # Right arrow
    button_1_box = pygame.draw.rect(screen, [0, 0, 0], [400, 550, 50, 26], 1)
    button_2_box = pygame.draw.rect(screen, [0, 0, 0], [500, 550, 50, 26], 1)
    button_3 = pygame.image.load("sword.png") # Melee attack button 
    button_3_box = pygame.draw.rect(screen, [0, 0, 0], [400, 500, 50, 26], 1)
    button_4 = pygame.image.load("action.png") # Action button 
    button_4_box = pygame.draw.rect(screen, [0, 0, 0], [400, 600, 50, 26], 1)
    button_5 = pygame.image.load("bow.png") # Ranged attack button 
    button_5_box = pygame.draw.rect(screen, [0, 0, 0], [510, 500, 50, 26], 1)
    button_6 = pygame.image.load("star.png") # End turn
    button_6_box = pygame.draw.rect(screen, [0, 0, 0], [400, 700, 50, 26], 1)

    def movement_right(x, where):
        "Calculate the right boundary for the Entity"
        new_position = x + int(where)
        return new_position
    
    def movement_left(x, where):
        "Calculate the left boundary for the Entity"
        new_position = x - int(where)
        return new_position
    
    quantity_dice = player.damage + short_sword.dice # Test
    list_throws = []
    
    def attack_resolution(quantity, weapon_damage): # 17-Feb-2022: Update this to make it OOB as would be more practical 
        "Function that calculates the damage done by the player"
        print("This is how many d6 you have " + str(quantity))
        throws = 0 
        while (throws < quantity): # Do this until you don't have any more dice to throw.
            result = random.randint(1, 6)
            throws += 1
            list_throws.append(result) # Add to a list
            player_hit.number = sum(list_throws) + weapon_damage
    
    distance_entities = (player.position - e_position) * -1 # The distance between the player and the enemy
    
    def check_attack(turn):
        "Function that calculates if the player has enough turns to perform the attack"
        if (player_turns.rectangle == 0):
            print("You don't have any more turns to attack!")
            return False
        else:
            return True
        
    def check_movement(turn):
        "Function that calculates if the player has enough turns to perform the movement "
        if (player_turns.circle == 0):
            print("You don't have any more turns to move!")
            return False
        else:
            return True
            
    def check_range(weapon, distance):
        if (weapon < distance_entities):
            print("You are too far to attack with this weapon!")
            print("Your weapon range: " + str(weapon) + " Enemy is at: " + str(distance_entities))
            return False
        else:
            return True

    def update_engine():
        
        "Similar to update_screen() but for game_engine visual assets"
        screen.blit(blr, (0, 0))
        
        # Player side
        
        position = str(player.position)

        ptext.draw(player.name, (74, 470), color = white, fontname = game_font, fontsize = 20, lineheight = 1.5, align = "center")
        screen.blit(prt, (10, 500)) # Player portrait 
        ptext.draw("HP", (175, 500), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw("STR", (175, 540), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw("DEX", (175, 580), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw("INT", (175, 620), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw("DMG", (175, 660), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw("SPD", (175, 700), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw(hp, (245, 500), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw(strength, (245, 540), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw(dexterity, (245, 580), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw(intelligence, (245, 620), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        #ptext.draw(damage + "d6", (245, 660), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw(speed, (245, 700), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw("MLE", (245, 650), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw("RGD", (245, 675), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw(str(short_sword.dice) + "d6" + "+" + str(short_sword.damage), (280, 650), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw(str(small_bow.dice) + "d6" + "+" + str(small_bow.damage), (280, 675), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        # Other 
        ptext.draw("Public", (50, 10), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw("Climate:  " + c_name, (50, 100), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw("Modifiers", (50, 175), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw("STR " + str(c_str), (50, 200), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw("DEX " + str(c_dex), (50, 225), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw("INT " + str(c_int), (50, 250), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw("Terrain:  " + t_name, (50, 300), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw("Modifiers", (50, 375), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw("SPD " + "-" + str(t_difficulty), (50, 400), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")


        
        # Positioning
        
        screen.blit(tim, (screen_height/2 - 200, 100)) # Terrain background image 
        screen.blit(dis, (screen_height/2 - 200, 60)) # Distance line
        screen.blit(s_prt, (screen_height/2 - 200 + ply_position, 291)) # Smaller player portrait
        screen.blit(s_ert, (screen_height/2 - 200 + enm_position, 291)) # Smaller enemy portrait 
        screen.blit(d_marker, (screen_height/2 - 174 + ply_position, 65)) # Distance Icon Player
        screen.blit(d_marker, (screen_height/2 - 174 + enm_position, 65)) # Distance Icon Enemy
        ptext.draw(str(position), (screen_height/2 - 174 + ply_position, 85), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left") # Player position 
        ptext.draw(str(e_position), (screen_height/2 - 174 + enm_position, 85), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left") # Enemy position 
        #ptext.draw("0", (480 , 85), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left") # 0 Distance 
        ptext.draw(str(t_left), (screen_height/2 - 210, 85), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left") # Left size of the terrain
        ptext.draw(str(t_right), (screen_height + 30, 85), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left") # Right size of the terrain
        
        # Buttons 
        
        ptext.draw("Attack", (450, 500), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        screen.blit(button_3, (400, 500)) # Melee Attack button 
        screen.blit(button_5, (510, 500)) # Ranged Attack button 
        ptext.draw("(" + str(short_sword.wep_range) + ")", (405, 475), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left") # Melee range 
        ptext.draw("(" + str(small_bow.wep_range) + ")", (515, 475), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left") # Ranged range (Redundant much?)
        ptext.draw("Move", (450, 550), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        screen.blit(button_1, (400, 550)) # Left button
        screen.blit(button_2, (500, 550)) # Right button 
        ptext.draw("Push", (450, 600), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        screen.blit(button_4, (400, 600)) # Action button 
        # Enemy side
        ptext.draw(enemy_name, (800, 470), color = white, fontname = game_font, fontsize = 20, lineheight = 1.5, align = "center")
        screen.blit(ert, (864,500)) # Enemy portrait 
        
        ptext.draw("HP", (690, 500), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw("STR", (690, 540), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw("DEX", (690, 580), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw("INT", (690, 620), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw("DMG", (690, 660), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw("SPD", (690, 700), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw(str(e_hp), (760, 500), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw(str(e_strength), (760, 540), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw(str(e_dexterity), (760, 580), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw(str(e_intelligence), (760, 620), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw(str(e_damage) + "d6", (760, 660), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw(str(e_speed), (760, 700), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        
        # Log window
        
        # Turns
        
        ptext.draw("Turn: " + str(player_turns.turn_number), (400, 425), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        ptext.draw("End Turn", (450, 700), color = white, fontname = game_font, fontsize = 15, lineheight = 1.5, align = "left")
        screen.blit(button_6, (400, 700)) # End Turn
        
        pygame.display.update()
        
    # Sprites
    
    update_engine()
    
    while status:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            # Movement
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_1_box.collidepoint(pygame.mouse.get_pos()):
                    if (check_movement(player_turns.circle)) == True:
                        print("Move Left")
                        calc_left = movement_left(player.position, speed)
                        fill = player.position - t_left # The current "missing" portion of the map, towards the left that has to be walked. 
                        if (calc_left < t_left):
                            print("You cannot go to the left anymore!")
                            print("Fill left " + str(fill))
                            if (fill == 0):
                                print("You cannot move to the left!")
                            else:
                                player.position = movement_left(player.position, fill)
                                p_offset = player_portrait_pixels.movement * int(fill) # Using "fill" as a variable, to avoid getting out of the map boundary 
                                ply_position = ply_position - p_offset
                                distance_entities = (player.position - e_position) * -1 # Updating the current position of the player, relative to the enemy. 
                                player_turns.circle = 0
                                action_sound(walk)
                                update_engine()
                        else: 
                            player.position = movement_left(player.position, speed)
                            p_offset = player_portrait_pixels.movement * int(speed) # Using "speed" as a variable as this is "normal" movement. 
                            ply_position = ply_position - p_offset
                            distance_entities = (player.position - e_position) * -1 # Updating the current position of the player, relative to the enemy. 
                            player_turns.circle = 0
                            action_sound(walk)
                            update_engine()
                        print("Your current position: " + str(player.position))
                        print("Distance to enemy: " + str(distance_entities))
                if button_2_box.collidepoint(pygame.mouse.get_pos()):
                    if (check_movement(player_turns.circle)) == True:
                        print("Move Right")
                        calc_right = movement_right(player.position, speed)
                        if (calc_right > t_right):
                            print("You cannot go to the right anymore!")
                        elif(distance_entities == 0): # If the distance is 0 and you want to move beyond, prompt error. 
                            print("You cannot go through the enemy!")
                        elif (distance_entities - int(speed) < 0):
                            fill = distance_entities
                            print("Too close!, you have " + str(fill))
                            player.position = movement_right(player.position, fill) # Using "fill" as a variable, to avoid getting crossing the enemy
                            p_offset = player_portrait_pixels.movement * int(fill)
                            ply_position = ply_position + p_offset
                            distance_entities = (player.position - e_position) * -1 # Updating the current position of the player, relative to the enemy. 
                            player_turns.circle = 0
                            action_sound(walk)
                            update_engine()
                        else:
                            player.position = movement_right(player.position, speed)
                            p_offset = player_portrait_pixels.movement * int(speed)
                            ply_position = ply_position + p_offset
                            distance_entities = (player.position - e_position) * -1 # Updating the current position of the player, relative to the enemy. 
                            player_turns.circle = 0
                            action_sound(walk)
                            update_engine()
                        print("Your current position: " + str(player.position))
                        print("Distance to enemy: " + str(distance_entities))
            # Attack 
            
                if button_3_box.collidepoint(pygame.mouse.get_pos()):
                    if (check_attack(player_turns.rectangle)) == True:
                        if (check_range(short_sword.wep_range, distance_entities) == True):
                            print("Melee Attack!")
                            print("Distance between you and the enemy " + str(distance_entities))
                            attack_resolution(quantity_dice, short_sword.damage) #
                            print("These are the dice that you got: ")
                            print(list_throws)
                            print("Damage bonus from your weapon: " + str(short_sword.damage))
                            print("Damage that you did " + str(player_hit.number))
                            print("Previous enemy HP: " + str(e_hp))
                            e_hp = e_hp - player_hit.number # Actually remove HP from the enemy 
                            list_throws.clear() # Cleaning the list after use to avoid adding stuff
                            print("Current enemy HP: " + str(e_hp))
                            player_turns.rectangle = 0 # Reducing your rectangle action 
                            action_sound(melee_attack)
                            update_engine()
                            
                if button_5_box.collidepoint(pygame.mouse.get_pos()):
                    if (check_attack(player_turns.rectangle)) == True:
                        if (check_range(small_bow.wep_range, distance_entities) == True):
                            print("Ranged Attack!")
                            print("Distance between you and the enemy " + str(distance_entities))
                            attack_resolution(quantity_dice, small_bow.damage) 
                            print("These are the dice that you got: ")
                            print(list_throws)
                            print("Damage bonus from your weapon: " + str(small_bow.damage))
                            print("Damage that you did " + str(player_hit.number))
                            print("Previous enemy HP: " + str(e_hp))
                            e_hp = e_hp - player_hit.number # Actually remove HP from the enemy 
                            list_throws.clear() # Cleaning the list after use to avoid adding stuff
                            print("Current enemy HP: " + str(e_hp))
                            player_turns.rectangle = 0 # Reducing your rectangle action  
                            action_sound(ranged_attack)
                            update_engine()
            
            # Actions       
                if button_4_box.collidepoint(pygame.mouse.get_pos()): # 28-Feb-2022: Pushing the enemy away, towards the right side of the screen. Correct so the enemy portrait actually moves. 
                    if(distance_entities == 0):
                        print("You are at distance 0!")
                        if (strength > e_strength):
                            strength_difference = int(strength) - int(e_strength)
                            player.position = movement_right(player.position, strength_difference)
                            p_offset = player_portrait_pixels.movement * int(strength_difference)
                            ply_position = ply_position + p_offset
                            distance_entities = (player.position - e_position) * -1 # Updating the current position of the player, relative to the enemy. 
                            player_turns.circle = 0
                            print("You push the enemy by " + str(strength_difference))
                    else:
                        print("You are too far to push, you need to be at distance 0")
                if button_6_box.collidepoint(pygame.mouse.get_pos()):
                    print("End Turn!")
                    print("Fresh as lettuce again!")
                    player_turns.rectangle = 1
                    player_turns.circle = 1
                    player_turns.turn_number += 1
                    print("Turn Number: " + str(player_turns.turn_number))
                    update_engine()
                
                if (e_hp <= 0):
                    action_sound(death_scream)
                    history_engine(enemy_name, enemy_portrait, e_history)
                
def main_menu():
    
    selection = 1
    status = True
    
    # Sprite 
    
    moving_sprites = pygame.sprite.Group()
    place = Sprite(10, 10)
    moving_sprites.add(place)
    electricity = "electricity.wav"
    action_sound(electricity)

    # Main loop
    while status:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if (selection - 1 > 0):
                        selection -= 1
                    else:
                        selection = 3
                elif event.key == pygame.K_DOWN:
                    if (selection < 3):
                        selection += 1
                    else:
                        selection = 1
                        
                if event.key == pygame.K_RETURN:
                    if selection == 1:
                        pygame.mixer.fadeout(5000)
                        status = False
                        intro()
                        new_character()
                    if selection == 2:
                        print("Not implemented!") # Debug
                    if selection == 3:
                        pygame.quit()
                        quit()

        # Main Menu UI
        screen.blit(bg, (0, 0))
        
        # Defining the text
        title, new_game, options_game, exit_game = text_format("Shadow Boy", main_menu_font, 90, white), text_format("New Game", main_menu_font, 60, white), text_format("Options", main_menu_font, 60, white), text_format("Exit", main_menu_font, 60, white)  # Title, New Game, Options and Exit
        
        # Color update
        if selection == 1:
            new_game = text_format("New Game", main_menu_font, 60, red)
        if selection == 2:
            options_game = text_format("Options", main_menu_font, 60, red) 
        if selection == 3:
            exit_game = text_format("Exit", main_menu_font, 60, red)
        
        # Drawing 
        title_rect, start_rect, options_rect, quit_rect = title.get_rect(), new_game.get_rect(), options_game.get_rect(), exit_game.get_rect() # Title, New Game, Options and Exit

        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 80)) # Title
        screen.blit(new_game, (screen_width/2 - (start_rect[2]/2), 300)) # New game
        screen.blit(options_game, (screen_width/2 - (options_rect[2]/2), 360)) # Options
        screen.blit(exit_game, (screen_width/2 - (quit_rect[2]/2), 420)) # Quit
        
        # Sprite
        

        moving_sprites.draw(screen)
        moving_sprites.update(0.20) # Instead of using =+ 1 for the sprite, we use 0.25 as the speed argument to make it "slower". 
        pygame.display.flip()
    
        # Update status
        pygame.display.update()
        pygame.display.set_caption("ShadowBoy")
 
    
#game_engine()
main_menu()



    