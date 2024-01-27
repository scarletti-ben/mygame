

import pygame

class CardBuilder:
    folder = 'G:/Coding/assets_new/card/'
    scale = 1
    smooth = False
    attributes = [
        'faction',
        'mana',
        'banner',
        'rarity',
        'type']

    @classmethod
    def get_path(cls, attribute, value):
        """Get path from filesystem based on attribute and value"""
        return cls.folder + attribute + '/' + str(value) + '.png'
    
    @classmethod
    def get_image(cls, path, scale = None):
        """Load image from a given file path"""
        image = pygame.image.load(path).convert_alpha()
        scale = cls.scale if scale is None else scale
        if scale != 1:
            w = image.get_width() * scale
            h = image.get_height() * scale
            if cls.smooth:
                image = pygame.transform.smoothscale(image, [w,h])
            else:
                image = pygame.transform.scale(image, [w,h])
        return image
    
    @classmethod
    def get_personalised_surface(cls, card, scale = None):
        """Get a surface personalised for a particular card and attributes"""
        images = []
        for attribute in cls.attributes:
            value = getattr(card, attribute)
            path = cls.get_path(attribute, value)
            image = cls.get_image(path, scale)
            images.append(image)
        surface = images[0]
        for image in images[1:]:
            surface.blit(image, [0,0])
        return surface

if __name__ == '__main__':

    # ~ Imports and Initialisation
    import pygame, os, sys, random, itertools, numpy
    import typing, math, time, datetime, ctypes, string
    pygame.init()
    ctypes.windll.user32.SetProcessDPIAware()
    os.system('cls')
    # function prompt {"> "}
    
    # ~ Setup
    W = 1600
    H = 900
    FPS = 60
    CENTER = CX, CY = W // 2, H // 2
    GREY = [63,63,63]
    clock = pygame.time.Clock()
    display = pygame.display.set_mode([W,H], pygame.RESIZABLE)
    user_event = pygame.USEREVENT + 1
    font_name = "G:/Coding/Assets/Fonts/Monogram/monogram.ttf"
    font = pygame.font.Font(font_name, 26)

    card = lambda: 0
    card.rarity = 'rare'
    card.mana = 2
    card.faction = 'default'
    card.banner = 'default'
    card.type = 'skill'
    surface = CardBuilder.get_personalised_surface(card)
    rectangle = surface.get_rect(center = CENTER)

    path = "G:/Coding/Assets/Images/_main_11.png"
    base_surface = pygame.image.load(path).convert_alpha()
    base_width, base_height = base_surface.get_size()
    width = base_width * CardBuilder.scale
    height = base_height * CardBuilder.scale
    base_surface = pygame.transform.scale(base_surface, [width, height])
    base_rectangle = base_surface.get_rect(center = [W // 5, CY])

    # ~ Game Loop
    while True:
    
        display.fill(GREY)
        events = pygame.event.get()
        mouse = pygame.mouse.get_pos()

        display.blit(surface, rectangle)
        display.blit(base_surface, base_rectangle)

    
        for event in events:
            if event.type == pygame.QUIT: 
                quit()
            if event.type == pygame.KEYDOWN: ...
            if event.type == pygame.MOUSEBUTTONDOWN: ...  
            elif event.type == pygame.MOUSEBUTTONUP: ...
    
        pygame.display.flip()	
        clock.tick(FPS)