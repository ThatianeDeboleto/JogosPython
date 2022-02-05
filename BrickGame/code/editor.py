import tkinter as tk
import random
import math
import copy

# Classe principal: herda da classe tk.Canvas
class Editor(tk.Canvas):
    linesNb = 20

    # Propriedades dos tijolos
    bricksWidth = 50
    bricksHeight = 20
    bricksNbByLine = 16
    bricksColors = {
        "r": "#e74c3c",
        "g": "#2ecc71",
        "b": "#3498db",
        "t": "#1abc9c",
        "p": "#9b59b6",
        "y": "#f1c40f",
        "o": "#e67e22",
    }

    # Propriedades da tela
    screenHeight = 500
    screenWidth = bricksWidth*bricksNbByLine

    # Este método cria a janela e carrega o nível.
    # Se o arquivo "X.txt" (com X o número do nível) existir, os tijolos
    # do nível são colocados na janela e os tijolos brancos correspondem a ".".
    # Se o arquivo não existir, a janela será preenchida com tijolos brancos.
    def __init__(self, root, level):
        tk.Canvas.__init__(self, root, bg="#ffffff", bd=0, highlightthickness=0, relief="ridge", width=self.screenWidth, height=self.screenHeight)
        self.level = level
        try:
            file = open(str(self.level)+".txt")
            bricks = list(file.read().replace("\n", ""))[:(self.bricksNbByLine*self.linesNb)]
            file.close()
        except IOError:
            bricks = []
        for i in range(self.bricksNbByLine*self.linesNb-len(bricks)):
            bricks.append(".")
        for i, j in enumerate(bricks):
            col = i%self.bricksNbByLine
            line = i//self.bricksNbByLine
            if j == ".":
                color = "#ffffff"
            else:
                color = self.bricksColors[j]
            self.create_rectangle(col*self.bricksWidth, line*self.bricksHeight, (col+1)*self.bricksWidth, (line+1)*self.bricksHeight, fill=color, width=2, outline="#ffffff")
        for i, j in enumerate(self.bricksColors.items()):
            self.create_rectangle(i*self.bricksWidth, self.screenHeight-self.bricksHeight, (i+1)*self.bricksWidth, self.screenHeight, fill=j[1], width=2, outline="#ffffff")
        self.pack()

    # Este método, chamado cada vez que o usuário deseja alterar a cor de um tijolo,
    # altera a cor dos tijolos e salva a nova grade no arquivo "X.txt"
    # (com X o número do nível) onde os tijolos brancos são substituídos por ".".
    def setColor(self, id, color):
        self.itemconfig(id, fill=color)
        
        content = ""
        for i in range(self.bricksNbByLine*self.linesNb):
            if i%self.bricksNbByLine == 0 and i != 0:
                content += "\n"
            brickColor = self.itemcget(i+1, "fill")
            brickId = [id for id, color in self.bricksColors.items() if color == brickColor]
            if brickId == []:
                content += "."
            else:
                content += brickId[0]
            
        file = open(str(self.level)+".txt", "w")
        file.write(content)
        file.close()


# Esta função é chamada quando o usuário clica com o botão esquerdo.
# Se o usuário clicar em um tijolo na parte inferior da tela,
# ele seleciona a cor do tijolo clicado.
# Se o usuário clicar em um tijolo no meio da tela,
# o tijolo clicado fica com a cor selecionada.
def eventsLeftClick(event):
    global editor

    id = event.widget.find_closest(event.x, event.y)[0]
    if id <= editor.bricksNbByLine*editor.linesNb:
        if hasattr(editor, "selectedColor"):
            editor.setColor(id, editor.selectedColor)
    else:
        editor.selectedColor = editor.itemcget(id, "fill")
        

# Esta função é chamada quando o usuário clica com o botão direito.
# O tijolo clicado fica branco.
def eventsRightClick(event):
    global editor

    id = event.widget.find_closest(event.x, event.y)[0]
    if id <= editor.bricksNbByLine*editor.linesNb:
        editor.setColor(id, "#ffffff")    


root = tk.Tk()
root.title("Editor")
root.resizable(0,0)
root.bind("<Button-1>", eventsLeftClick)
root.bind("<Button-3>", eventsRightClick)


editor = Editor(root, int(input("What is the level number? ")))
root.mainloop()