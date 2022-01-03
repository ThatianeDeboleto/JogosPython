from turtle import Turtle
ALIGNMENT = "center"
FONT = ("Times", 18, "normal")

class Scoreboard(Turtle):
#penup retira linha branca do modo turtle do meio da tela
    def __init__(self):
        super().__init__()
        self.score = 0
        self.color("yellow")
        self.penup()
        self.goto(0, 270)
        self.hideturtle()
        self.update_scoreboard()

    def update_scoreboard(self):
        self.write(f"Placar 🐍: {self.score}", align=ALIGNMENT, font=FONT)

    def game_over(self):
        self.goto(0, 0)
        self.write("VOCÊ PERDEU!!!", align=ALIGNMENT, font=FONT)

    def increase_score(self):
        self.score += 1
        self.clear()
        self.update_scoreboard()
