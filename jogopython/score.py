#-----------------------------------------------------------------
def existe_score():
    try:
        arquivo = open('score\score.txt', 'r')
        arquivo.close()
    except FileNotFoundError:
        arquivo = open('score\score.txt', 'w')
        arquivo.write('0')
        arquivo.close()
    return
#-----------------------------------------------------------------
def salvar_score(placar):
    arquivo = open('score\score.txt', 'w')
    arquivo.write(str(placar))
    arquivo.close()
    return
#-----------------------------------------------------------------
def le_score():
    arquivo = open('score\score.txt', 'r')
    score = arquivo.read()
    arquivo.close()
    return score
#-----------------------------------------------------------------
def limpa_score():
    arquivo = open('score\score.txt', 'w')
    arquivo.write('0')
    return