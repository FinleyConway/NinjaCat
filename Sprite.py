import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self, spritePath, spriteType: str):
        pygame.sprite.Sprite.__init__(self)
        
        self.originalImage = pygame.image.load(spritePath).convert_alpha()
        self.image = self.originalImage
        self.rect = self.image.get_rect()
        
        self.isFlipX = False
        self.isFlipY = False
        
        self.spriteType = spriteType
        
    
    def update(self, deltaTime):
        pass
    
    def flip(self, horizontal = False, vertical = False):
        if (horizontal != self.isFlipX or vertical != self.isFlipY):
            self.isFlipX = horizontal
            self.isFlipY = vertical
            
            self.image = pygame.transform.flip(self.originalImage, horizontal, vertical)