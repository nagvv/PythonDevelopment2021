import tkinter as tk
from random import shuffle

WINDOW_MIN_WIDTH = 200
WINDOW_MIN_HEIGHT = 200
CONTROL_BUTTON_WIDTH = 5
CONTROL_BUTTON_HEIGHT = 1
CONTROL_BUTTON_PAD = 5
NUM_BUTTON_WIDTH = 10
NUM_BUTTON_HEIGHT = 2

class App(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        for i in range(4):
            self.columnconfigure(i, weight=1)
            self.rowconfigure(i + 1, weight=1)
        self.emptyCell = (0, 0)
        self.createControlButtons()
        self.createNumButtons()
        self.newGame()

    def createControlButtons(self):
        self.newButton = tk.Button(self, text='New', command=self.newGame, height=CONTROL_BUTTON_HEIGHT, width=CONTROL_BUTTON_WIDTH)
        self.newButton.grid(row=0, column=0, columnspan=2, pady=CONTROL_BUTTON_PAD)
        self.exitButton = tk.Button(self, text='Exit', command=self.quit, height=CONTROL_BUTTON_HEIGHT, width=CONTROL_BUTTON_WIDTH)
        self.exitButton.grid(row=0, column=2, columnspan=2, pady=CONTROL_BUTTON_PAD)

    def createNumButtons(self):
        for i in range(1, 16):
            def getOnClick(i):
                def tiedOnClick():
                    return self.onClick(i)
                return tiedOnClick
            setattr(self, f'numButton{i}', tk.Button(self, text=str(i), command=getOnClick(i), height=NUM_BUTTON_HEIGHT, width=NUM_BUTTON_WIDTH))

    def newGame(self):
        positions = [i for i in range(16)] # 0 - empty cells, others are number cells with corresponding numbers
        shuffle(positions) # TODO: check solvability and if not rotate numbers
        for pos, i in enumerate(positions):
            row = 1 + pos // 4
            col = pos % 4
            if i == 0:
                self.emptyCell = (col, row)
                continue
            getattr(self, f'numButton{i}').grid(row=row, column=col, sticky='nsew')

    def onClick(self, i):
        info = getattr(self, f'numButton{i}').grid_info()
        pos = (info['column'], info['row'])
        if self.emptyCell == (pos[0] + 1, pos[1]) or \
           self.emptyCell == (pos[0] - 1, pos[1]) or \
           self.emptyCell == (pos[0], pos[1] + 1) or \
           self.emptyCell == (pos[0], pos[1] - 1):
            getattr(self, f'numButton{i}').grid(row=self.emptyCell[1], column=self.emptyCell[0], sticky='nsew')
            self.emptyCell = pos

if __name__ == "__main__":
    window = tk.Tk()
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)
    app = App(window)
    app.grid(row=0, column=0, sticky='nsew')
    window.title("Game 15")
    window.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
    window.mainloop()
