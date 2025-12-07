from PPlay.keyboard import Keyboard
from PPlay import window
from PPlay.sprite import Sprite
import config

class Player:
    def __init__(self, janela):
        self.janela = janela
        
        self.cor_index = 0
        self.cor = config.CORES_JOGO[self.cor_index]
        
        self.sprites = [
            Sprite(config.BONECO_VERMELHO),
            Sprite(config.BONECO_VERDE),
            Sprite(config.BONECO_AZUL)
        ]
        
        # Escalar os sprites
        for sprite in self.sprites:
            nova_largura = int(sprite.width * config.ESCALA_PLAYER)
            nova_altura = int(sprite.height * config.ESCALA_PLAYER)
            sprite.image = window.pygame.transform.scale(sprite.image, (nova_largura, nova_altura))
            sprite.width = nova_largura
            sprite.height = nova_altura
        
        self.sprite_atual = self.sprites[self.cor_index]
        
        self.x = config.PLAYER_X_INICIAL
        self.y = config.PLAYER_Y_INICIAL
        self.sprite_atual.set_position(self.x, self.y)
        
        self.width = self.sprite_atual.width
        self.height = self.sprite_atual.height
        
        self.pode_trocar = True

    def update(self, teclado: Keyboard):
        if teclado.key_pressed("SPACE") and self.pode_trocar:
            self.mudar_cor()
            self.pode_trocar = False 
            return True  
        
        if not teclado.key_pressed("SPACE"):
            self.pode_trocar = True
            
        return False 

    def mudar_cor(self):
        self.cor_index = (self.cor_index + 1) % len(config.CORES_JOGO)
        self.cor = config.CORES_JOGO[self.cor_index]
        self.sprite_atual = self.sprites[self.cor_index]
        self.sprite_atual.set_position(self.x, self.y)

    def draw(self):
        self.sprite_atual.draw()

    def collides(self, obstaculo):
        return (self.x < obstaculo.x + obstaculo.width and
                self.x + self.width > obstaculo.x and
                self.y < obstaculo.y + obstaculo.height and
                self.y + self.height > obstaculo.y)