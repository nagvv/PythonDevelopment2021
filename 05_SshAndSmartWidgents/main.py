import tkinter as tk
import re
from os import linesep

class Textual(tk.Text):
    def __init__(self, master=None):
        tk.Text.__init__(self, master=master)
        self.repr = []
        self.bind('<KeyRelease>', self.parse)
        self.event_add('<<changed>>', 'None')

    line_re = r'^\[(?P<coords>[ \-\.\d]+)\] *(<(?P<bwidth>\d+(\.\d+)?)( *\((?P<bcolor>\d+, *\d+, *\d+)\))?>)? *(\((?P<fcolor>\d+, *\d+, *\d+)\))? *$'
    def checkLine(self, line):
        assert(type(line) is str)
        m = re.match(self.line_re, line) # type: re.Match
        if m is None:
            return None
        coords = tuple(map(float, m['coords'].split()))
        if len(coords) != 4:
            return None
        bwidth = m['bwidth']
        if bwidth is None:
            bwidth = 2.0 # default width
        bwidth = float(bwidth)
        if bwidth < 0.0:
            return None
        bcolor = m['bcolor']
        if bcolor is None:
            bcolor = '0, 0, 0'
        bcolor = tuple(map(int, bcolor.split(',')))
        if min(bcolor) < 0 or max(bcolor) > 255:
            return None
        fcolor = m['fcolor']
        if fcolor is None:
            fcolor = '255, 255, 255'
        fcolor = tuple(map(int, fcolor.split(',')))
        if min(fcolor) < 0 or max(fcolor) > 255:
            return None
        return coords, bwidth, bcolor, fcolor

    def parse(self, event):
        if not self.edit_modified():
            return
        self.edit_modified(arg=False)
        # clean up everything
        self.repr = []
        for tag in self.tag_names():
            self.tag_delete(tag)
        # parse text
        lines = self.get('1.0', tk.END).splitlines()
        for idx, line in enumerate(lines):
            res = self.checkLine(line)
            if res is None:
                self.tag_add(f'{idx}', f'{idx + 1}.0', f'{idx + 1}.end')
                self.tag_configure(f'{idx}', background='red')
                continue
            self.repr.append((idx, res))
        self.event_generate('<<changed>>')

    def addObject(self, x0, y0, x1, y1):
        line = f'[{x0} {y0} {x1} {y1}] <2.0 (0, 0, 0)> (255, 255, 255)'
        if self.compare("end-1c", "!=", "1.0") and self.get('end-1c', 'end') != linesep:
            self.insert('end', linesep)
        self.insert('end', line)

    def moveObject(self, idx, x0, y0, x1, y1):
        oldline = self.get(f'{idx + 1}.0', f'{idx + 1}.end').split(']')[1]
        self.delete(f'{idx + 1}.0', f'{idx + 1}.end')
        self.insert(f'{idx + 1}.0', f'[{x0} {y0} {x1} {y1}]' + oldline)

class App(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.textField = Textual(self)
        self.textField.grid(row=0, column=0, sticky='nsew')
        self.textField.bind('<<changed>>', self.update_canvas)
        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=0, column=1, sticky='nsew')
        self.canvas.bind('<Button-1>', self.interact_on)
        self.canvas.bind('<ButtonRelease-1>', self.interact_off)
        self.target = None
        self.idmap = {}

    def update_canvas(self, event):
        self.canvas.delete('all')
        self.target = None
        self.idmap = {}
        for tid, obj in self.textField.repr:
            cid = self.canvas.create_oval(
                *obj[0], # coords
                width=obj[1], # border width
                outline='#%02x%02x%02x' % obj[2], # border color
                fill='#%02x%02x%02x' % obj[3] # fill color
            )
            self.idmap[cid] = tid

    def interact_on(self, event):
        self.canvas.bind('<Motion>', self.mouse_move)
        tgt = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        if tgt:
            tgt = tgt[-1]
            self.target = ('move', tgt, event.x, event.y)
            return
        tgt = self.canvas.create_oval(
            event.x, event.y, event.x, event.y,
            width=2.0,
            outline='#000000',
            fill='#ffffff'
        )
        self.target = ('resize', tgt, event.x, event.y)

    def interact_off(self, event):
        self.canvas.unbind('<Motion>')
        if self.target == None:
            return
        if self.target[0] == 'resize':
            self.textField.addObject(*self.canvas.coords(self.target[1]))
        if self.target[0] == 'move':
            self.textField.moveObject(self.idmap[self.target[1]], *self.canvas.coords(self.target[1]))
        self.target = None
        self.textField.parse(None) # synchronize

    def mouse_move(self, event):
        if self.target == None:
            return
        if self.target[0] == 'move':
            tgt, x_old, y_old  = self.target[1:]
            self.canvas.move(tgt, event.x - x_old, event.y - y_old)
            self.target = ('move', tgt, event.x, event.y)
        if self.target[0] == 'resize':
            tgt, x0, y0 = self.target[1:]
            self.canvas.coords(tgt, x0, y0, event.x, event.y)

if __name__ == "__main__":
    window = tk.Tk()
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)
    app = App(window)
    app.grid(row=0, column=0, sticky='nsew')
    window.title("InputLabel")
    window.mainloop()
