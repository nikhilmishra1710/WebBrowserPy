import tkinter
from typing import List, Tuple

import webbrowser_py.utils as utils
from webbrowser_py.Constants import Constants
from webbrowser_py.URL import URL

WIDTH, HEIGHT = 800, 600

class Browser:
    def __init__(self) -> None:
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=Constants.BROWSER_WIDTH,
            height=Constants.BROWSER_HEIGHT,
        )
        self.scroll: float = 0
        self.window.bind("<Down>", self.on_scroll)
        self.window.bind("<Up>", self.on_scroll)
        self.layout_list: List[Tuple[float, float, str, tkinter.font.Font]] = []
        self.canvas.pack()
    
    def on_scroll(self, event: tkinter.Event) -> None:
        if event.keysym == "Down":
            self.scroll += Constants.VSTEP
        elif event.keysym == "Up":
            if self.scroll > 0:
                self.scroll -= Constants.VSTEP
        self.draw()
    
    def draw(self) -> None:
        self.canvas.delete("all")
        for x, y, ch, font in self.layout_list:
            if y > self.scroll + Constants.BROWSER_HEIGHT:
                continue
            if y + Constants.VSTEP < self.scroll:
                continue
            self.canvas.create_text(
                x, y - self.scroll, text=ch, font=font, anchor=tkinter.NW
            )
            
    def load(self, url: URL) -> None:
        body: str = url.request()
        tokens: List[utils.Text | utils.Tag] = utils.lex(body)
        self.layout_list = utils.Layout(tokens).display_list
        self.window.title(f"Web Browser - {url.scheme}://{url.host}{url.path}")
        self.draw()
        tkinter.mainloop()
        