import telajogo
import menu
import pygame
import score

telajogo.limpa_tela()
score.existe_score()
placar = 0
tempo = 0
jogar = 1
while True:
    opc = menu.menu(placar, tempo)
    if opc == 1:
        resultado = telajogo.jogar()
        placar = resultado[0]
        tempo = resultado[1]
        scr = score.le_score()
        scr = int(scr)
        if placar > scr:
            score.salvar_score(placar)
    elif opc == 2:
        pygame.quit()  # encerra o pygame e sai do shell
        break
    elif opc == 3:
        score.limpa_score()
