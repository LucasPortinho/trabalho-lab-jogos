from PPlay.gameimage import GameImage

import PPlay as pplay

import config
import random
from player import Player
from obstacle import Obstaculo

def carregar_high_score():
    try:
        with open(config.ARQUIVO_HIGH_SCORE, "r") as f:
            return int(f.read())
    except (IOError, ValueError):
        return 0

def salvar_high_score(score):
    try:
        with open(config.ARQUIVO_HIGH_SCORE, "w") as f:
            f.write(str(int(score)))
    except IOError:
        print("Erro ao salvar high score.")

def menu(janela, teclado, high_score, background):
    background.draw()
    
    janela.draw_text("Correndo pela Aquarela", 
                     x=janela.width/2 - 250, y=150, 
                     size=50, color=config.BRANCO, font_name=config.ARQUIVO_FONTE)
    
    janela.draw_text(f"Recorde: {high_score}", 
                     x=janela.width/2 - 100, y=250, 
                     size=30, color=config.BRANCO, font_name=config.ARQUIVO_FONTE)
    
    janela.draw_text("Pressione [JOGAR] (Enter)", 
                     x=janela.width/2 - 150, y=350, 
                     size=30, color=config.VERDE, font_name=config.ARQUIVO_FONTE)
    
    if teclado.key_pressed("ENTER"):
        return config.JOGANDO
    return config.MENU

def game_over(janela, teclado, pontuacao_final, high_score, background):
    background.draw()
    
    janela.draw_text("GAME OVER", 
                     x=janela.width/2 - 150, y=150, 
                     size=60, color=config.VERMELHO, font_name=config.ARQUIVO_FONTE)
    
    janela.draw_text(f"Pontuação Final: {pontuacao_final}", 
                     x=janela.width/2 - 140, y=250, 
                     size=30, color=config.BRANCO, font_name=config.ARQUIVO_FONTE)
    
    janela.draw_text(f"Novo Recorde: {high_score}" if pontuacao_final == high_score else f"Recorde: {high_score}", 
                     x=janela.width/2 - 120, y=300, 
                     size=30, color=config.AZUL, font_name=config.ARQUIVO_FONTE)
    
    janela.draw_text("Pressione [R] para reiniciar", 
                     x=janela.width/2 - 170, y=400, 
                     size=30, color=config.VERDE, font_name=config.ARQUIVO_FONTE)
    
    if teclado.key_pressed("R"):
        return config.MENU
    return config.GAME_OVER

def jogar(janela, teclado, audios, background):
    jogador = Player(janela)
    obstaculos = []
    
    pontuacao = 0.0
    
    velocidade_atual = config.VELOCIDADE_INICIAL_OBSTACULO
    frequencia_spawn_atual = config.FREQUENCIA_SPAWN_INICIAL
    
    timer_spawn = 0.0
    timer_dificuldade = 0.0
    
    cor_fundo = config.CINZA_FUNDO

    while True:
        delta_time = janela.delta_time()
        
        if jogador.update(teclado):
            audios["mudar_cor"].play()

        pontuacao += 10 * delta_time 
        timer_spawn += delta_time
        timer_dificuldade += delta_time
        
        if timer_dificuldade > 5.0:
            velocidade_atual *= config.ACELERACAO_VELOCIDADE
            frequencia_spawn_atual *= config.REDUCAO_FREQUENCIA
            timer_dificuldade = 0.0
            
            cor_fundo = random.choice([config.VERMELHO, config.VERDE, config.AZUL])

        if timer_spawn > frequencia_spawn_atual:
            novo_obstaculo = Obstaculo()
            novo_obstaculo.velocidade = velocidade_atual
            obstaculos.append(novo_obstaculo)
            timer_spawn = 0.0
            
        for obs in obstaculos[:]:
            obs.update(delta_time)
            
            if jogador.collides(obs):
                if jogador.cor != obs.cor:
                    audios["falha"].play() 
                    return config.GAME_OVER, int(pontuacao)

            if obs.esta_fora_tela():
                obstaculos.remove(obs)
        
        background.draw()

        jogador.draw()
        for obs in obstaculos:
            obs.draw(janela)
            
        janela.draw_text(f"Pontuação: {int(pontuacao)}", 
                         x=10, y=10, 
                         size=24, color=config.BRANCO, font_name=config.ARQUIVO_FONTE)
        
        janela.update()

def main():
    janela = pplay.window.Window(config.LARGURA, config.ALTURA)
    janela.set_title("Correndo pela Aquarela")
    teclado = pplay.keyboard.Keyboard()
    
    background = GameImage(config.BACKGROUND)
    background.image = pplay.window.pygame.transform.scale(
        background.image, 
        (config.LARGURA, config.ALTURA)
    )
    background.width = config.LARGURA
    background.height = config.ALTURA
    background.set_position(0, 0)
    
    try:
        audios = {
            "mudar_cor": pplay.sound.Sound(config.AUDIO_MUDAR_COR),
            "falha": pplay.sound.Sound(config.AUDIO_FALHA),
            "recorde": pplay.sound.Sound(config.AUDIO_RECORDE)
        }
    except Exception as e:
        print(f"Erro ao carregar áudios: {e}")
        print("Certifique-se que os arquivos .ogg estão na pasta.")
        return

    high_score = carregar_high_score()
    game_state = config.MENU
    pontuacao_final = 0

    while True:
        if game_state == config.MENU:
            game_state = menu(janela, teclado, high_score, background)
            
        elif game_state == config.JOGANDO:
            game_state, pontuacao_final = jogar(janela, teclado, audios, background)
            
            if pontuacao_final > high_score:
                audios["recorde"].play() 
                high_score = pontuacao_final
                salvar_high_score(high_score)
                
        elif game_state == config.GAME_OVER:
            game_state = game_over(janela, teclado, pontuacao_final, high_score, background)
            
        janela.update()

if __name__ == "__main__":
    main()