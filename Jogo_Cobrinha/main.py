#Subir descer virar//Inicio do jogo, cores de fundo, desenvolvimento inicial

from turtle import Screen
from snake import Snake
from food import Food
from scoreboard import Scoreboard
import time

screen = Screen()
screen.setup(width=688, height=688)
screen.bgcolor("black")
screen.title("Alimente o Senhor Python 🐍")
screen.tracer(0)

snake = Snake()
food = Food()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")

game_is_on = True
while game_is_on:
    screen.update()
    time.sleep(0.1)
    snake.move()

    #Encontro do alimento com a cobrinha-metodo distancia
    # print("nom nom nom") apareceria no console quando encostasse na bolinha azul
    #snake extend = cobrinha crescer ao tocar o ponto azul
    if snake.head.distance(food) < 15:
        food.refresh()
        snake.extend()
        scoreboard.increase_score()
    #Detectar colisao na tela
    if snake.head.xcor() > 280 or snake.head.xcor() < -280 or snake.head.xcor() > 280 or snake.head.xcor() < -280:
        game_is_on = False
        scoreboard.game_over()


    #detectar colisao com a cauda a cabeca deve ser excluida para que o jogo nao finalize no inicio
    for segment in snake.segments:
        if segment == snake.head:
            pass
        elif snake.head.distance(segment) < 10:
            game_is_on = False
            scoreboard.game_over()
screen.exitonclick()
