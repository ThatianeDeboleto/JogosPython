import random
from hangman_art import stages, logo
from hangman_words import lista_palavras
from replit import clear

print(logo)
final_jogo = False
vidas = len(stages) - 1

chosen_word = random.choice(lista_palavras)
word_length = len(chosen_word)

display = []
for _ in range(word_length):
    display += "_"

while not final_jogo:
    guess = input("Escolha uma letra: ").lower()

    #Use the clear() function imported from replit to clear the output between guesses.
    clear()

    if guess in display:
        print(f"Você já adivinhou!!! {guess}")

    for position in range(word_length):
        letras = chosen_word[position]
        if letras == guess:
            display[position] = letras
    print(f"{' '.join(display)}")

    if guess not in chosen_word:
        print(f"Você adivinhou {guess}, isso não está na palavra. Você perde uma vida.")
        vidas -= 1
        if vidas == 0:
            fim_de_jogo = True
            print("Você perdeu😟")
            print(f'Eiiiii, a solução é {chosen_word}.')
    if not "_" in display:
        final_do_jogo = True
    if not "_" in display:
        print("Você conseguiu😀!")

    print(stages[vidas])