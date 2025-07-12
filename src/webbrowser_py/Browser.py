import tkinter
import src.webbrowser_py.utils as utils
from src.webbrowser_py.Constants import Constants
from src.webbrowser_py.URL import URL

WIDTH, HEIGHT = 800, 600

class Browser:
    def __init__(self) -> None:
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=Constants.BROWSER_WIDTH,
            height=Constants.BROWSER_HEIGHT,
        )
        self.scroll = 0
        self.window.bind("<Down>", self.on_scroll)
        self.layout_list = []
        self.canvas.pack()
    
    def on_scroll(self, event: tkinter.Event) -> None:
        if event.keysym == "Down":
            self.scroll += Constants.VSTEP
        elif event.keysym == "Up":
            self.scroll -= Constants.VSTEP
        self.draw()
    
    def draw(self) -> None:
        self.canvas.delete("all")
        for x, y, ch in self.layout_list:
            if y > self.scroll + Constants.BROWSER_HEIGHT:
                continue
            if y + Constants.VSTEP < self.scroll:
                continue
            self.canvas.create_text(
                x, y - self.scroll, text=ch
            )
            
        
    def load(self, url: URL) -> None:
        body: str = url.request()
        text: str = utils.lex(body)
        self.layout_list = utils.layout(text)
        self.draw()
        tkinter.mainloop()
        