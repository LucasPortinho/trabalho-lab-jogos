import random
import config
from PPlay import window
from PPlay.sprite import Sprite

class Obstaculo:
    def __init__(self):
        self.cor_index = random.randint(0, len(config.CORES_JOGO) - 1)
        self.cor = config.CORES_JOGO[self.cor_index]
        
        self.sprite = Sprite(config.PORTAIS[self.cor_index])
        
        escala = config.ESCALAS_PORTAIS[self.cor_index]
        nova_largura = int(self.sprite.width * escala)
        nova_altura = int(self.sprite.height * escala)
        self.sprite.image = window.pygame.transform.scale(self.sprite.image, (nova_largura, nova_altura))
        self.sprite.width = nova_largura
        self.sprite.height = nova_altura
        
        self.width = self.sprite.width
        self.height = self.sprite.height
        
        self.x = config.LARGURA 
        self.y = config.OBSTACULO_Y_POS - self.height 
        self.sprite.set_position(self.x, self.y)
        
        self.velocidade = config.VELOCIDADE_INICIAL_OBSTACULO
        self.passou = False 

    def update(self, delta_time):
        self.x -= self.velocidade * delta_time
        self.sprite.set_position(self.x, self.y)

    def draw(self, janela):
        self.sprite.draw()

    def esta_fora_tela(self):
        return self.x + self.width < 0