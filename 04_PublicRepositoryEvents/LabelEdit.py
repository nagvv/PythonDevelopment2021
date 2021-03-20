import tkinter as tk

class InputLabel(tk.Label):
    def __init__(self, master=None):
        tk.Label.__init__(self, master, takefocus=1, anchor='w')
        self.configure(text='test')
        self.bind('<FocusIn>', self.on_focus_in)
        self.bind('<FocusOut>', self.on_focus_out)
        self.bind("<Button-1>", lambda event: self.focus_set())
        self.bind('<Escape>', lambda event: master.focus_set())

    def on_focus_in(self, event):
        self.configure(relief='solid')

    def on_focus_out(self, event):
        self.configure(relief='flat')

class App(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.label = InputLabel(self)
        self.label.grid(row=0, column=0, sticky='nwe')
        self.exitButton = tk.Button(self, text='Quit', command=self.quit, height=1, width=8)
        self.exitButton.grid(row=1, column=0, sticky='se')

if __name__ == "__main__":
    window = tk.Tk()
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)
    app = App(window)
    app.grid(row=0, column=0, sticky='nsew')
    window.title("InputLabel")
    window.mainloop()
