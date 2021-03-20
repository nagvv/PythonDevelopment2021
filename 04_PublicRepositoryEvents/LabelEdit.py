import tkinter as tk
from tkinter import font

class InputLabel(tk.Label):
    def __init__(self, master=None):
        tk.Label.__init__(self, master, takefocus=1, anchor='w')
        self.bind('<FocusIn>', self.on_focus_in)
        self.bind('<FocusOut>', self.on_focus_out)
        self.bind("<Button-1>", self.on_mouse_click)
        self.bind('<Escape>', lambda event: master.focus_set())
        self.bind('<KeyPress>', self.on_key_press)
        self.text = tk.StringVar(self)
        self.configure(textvariable=self.text)
        self.font = font.Font(family=self['font'], size=14) # default font
        self.configure(font=self.font)
        self.cursor = tk.Frame(bg='black')
        self.cursor_pos = 0
        self.draw_cursor()

    def draw_cursor(self):
        h = self.font.metrics('linespace')
        y_pos = h + int(str(self['pady'])) + int(str(self['bd']))
        x_pos = self.font.measure(self.text.get()[:self.cursor_pos]) + int(str(self['padx'])) + int(str(self['bd']))
        self.cursor.place(anchor='sw', height=h, width=3, x=x_pos, y=y_pos)

    def on_mouse_click(self, event):
        self.focus_set()
        pos = 0
        for i in range(1, len(self.text.get()) + 1):
            bx = self.font.measure(self.text.get()[:i]) + int(str(self['padx'])) + int(str(self['bd']))
            if bx > event.x:
                break
            pos += 1
        self.cursor_pos = pos
        self.draw_cursor()

    def on_focus_in(self, event):
        self.configure(relief='solid')

    def on_focus_out(self, event):
        self.configure(relief='flat')

    def on_key_press(self, event):
        if event.keysym == 'Left':
            self.cursor_pos = max(0, self.cursor_pos - 1)
        if event.keysym == 'Right':
            self.cursor_pos = min(len(self.text.get()), self.cursor_pos + 1)
        if event.keysym == 'Home':
            self.cursor_pos = 0
        if event.keysym == 'End':
            self.cursor_pos = len(self.text.get())
        if event.keysym == 'Delete' and len(self.text.get()) > self.cursor_pos:
            self.text.set(self.text.get()[:self.cursor_pos] + self.text.get()[self.cursor_pos + 1:])
        if event.keysym == 'BackSpace' and self.cursor_pos > 0:
            self.text.set(self.text.get()[:self.cursor_pos - 1] + self.text.get()[self.cursor_pos:])
            self.cursor_pos -= 1
        if event.char.isprintable() and event.char:
            self.text.set(self.text.get()[:self.cursor_pos] + event.char + self.text.get()[self.cursor_pos:])
            self.cursor_pos += 1
        self.draw_cursor()

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
