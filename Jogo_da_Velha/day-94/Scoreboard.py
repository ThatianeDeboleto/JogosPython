from turtle import Turtle

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.lives = 3
        with open("data.txt") as file:
            self.high_score = int(file.read())
        self.high_score = 0
        self.color("MintCream")
        self.penup()
        self.hideturtle()
        self.goto(-290,270)
        self.RefreshScore()

    def RefreshScore(self):
        self.clear()
        score = f"Pontuação: {self.score}. Pontuação máxima: {self.high_score}.   Você tem {self.lives} vidas restantes!"
        self.write(arg=score,align="left", font=("Arial", 15, "bold"), move=False)

    def RemoveLife(self):
        self.lives -= 1
        self.RefreshScore()

    def GameOver(self, Reason):
        self.goto(0, -240)
        if Reason == "Vidas":
            self.write("Você não possui mais vidas! Você perdeu!!", align="center", font=('Arial', 20, 'bold'), move=False)
        elif Reason == "Won":
            self.write("Você eliminou todos os alienígenas!!!", align="center", font=('Arial', 20, 'bold'), move=False)
        elif Reason == "Invasão":
            self.write("Os alienígenas pousaram! Fim de jogo!!", align="center", font=('Arial', 20, 'bold'), move=False)
        if self.score > self.high_score:
            self.high_score = self.score
            with open("data.txt", "w") as file:
                file.write(str(self.high_score))

    def Reset(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open("data.txt", "w") as file:
                file.write(str(self.high_score))
        self.score = 0
        self.RefreshScore()