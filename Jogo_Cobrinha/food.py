#PONTO alimento para que a cobrinha cresca ao comer.

from turtle import Turtle
import random

class Food(Turtle):
# como se movera,como o ponto se comportara/cor
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_len=0.5, stretch_wid=0.5)
        self.color("blue")
        self.speed("fastest")
        self.refresh()

#para o ponto azul(comidinha) mudar de lugar
    def refresh(self):
        random_x = random.randint(-280, 280)
        random_y = random.randint(-280, 280)
        self.goto(random_x, random_y)



