import tkinter as tk

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
        self.createControlButtons()
        self.createNumButtons()

    def createControlButtons(self):
        self.newButton = tk.Button(self, text='New', height=CONTROL_BUTTON_HEIGHT, width=CONTROL_BUTTON_WIDTH)
        self.newButton.grid(row=0, column=0, columnspan=2, pady=CONTROL_BUTTON_PAD)
        self.exitButton = tk.Button(self, text='Exit', command=self.quit, height=CONTROL_BUTTON_HEIGHT, width=CONTROL_BUTTON_WIDTH)
        self.exitButton.grid(row=0, column=2, columnspan=2, pady=CONTROL_BUTTON_PAD)

    def createNumButtons(self):
        for i in range(1, 16):
            btn_name = f'numButton{i}'
            row = 1 + i // 4
            col = i % 4
            setattr(self, btn_name, tk.Button(self, text=str(i), height=NUM_BUTTON_HEIGHT, width=NUM_BUTTON_WIDTH))
            getattr(self, btn_name).grid(row=row, column=col, sticky='nsew')

if __name__ == "__main__":
    window = tk.Tk()
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)
    app = App(window)
    app.grid(row=0, column=0, sticky='nsew')
    window.title("Game 15")
    window.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
    window.mainloop()
