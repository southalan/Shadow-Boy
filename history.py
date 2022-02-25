# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 22:55:42 2022

@author: Choripan
"""

def history_engine():
    
    pygame.init()
    screen_width=1024
    screen_height=768
    screen=pygame.display.set_mode((screen_width, screen_height))
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.display.update()
    pygame.display.set_caption("ShadowBoy")