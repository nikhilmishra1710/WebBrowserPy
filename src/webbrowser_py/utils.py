import tkinter
import tkinter.font
from typing import List, Literal, Tuple

from webbrowser_py.Constants import Constants


class Text:
    def __init__(self, text: str) -> None:
        self.text = text
        
class Tag:
    def __init__(self, name: str) -> None:
        self.name = name

class Layout:
    def __init__(self, tokens: List[Text | Tag]) -> None:
        self.display_list: List[Tuple[float, float, str, tkinter.font.Font]] = []
        self.cursor_x = Constants.HSTEP
        self.cursor_y = Constants.VSTEP
        self.size = Constants.FONT_SIZE
        self.weight: Literal['normal', 'bold'] = "normal"
        self.style: Literal['roman', 'italic'] = "roman"
        self.line = []

        for token in tokens:
            self.token_handler(token)
            
    def token_handler(self, token: Text | Tag) -> None:
        if isinstance(token, Text):
            for word in token.text.split():
                self.text_handler(word)
        elif isinstance(token, Tag):
            self.tag_handler(token)
    
    def flush(self) -> None:
        if not self.line:
            return

        metrics = [font.metrics() for _, _, font in self.line]
        max_ascent = max([metric["ascent"] for metric in metrics])
        baseline = self.cursor_y + max_ascent * 1.25
        
        for x, word, font in self.line:
            y = baseline - font.metrics("ascent")
            self.display_list.append((x, y, word, font))
            
        max_descent = max([metric["descent"] for metric in metrics])
        self.cursor_y = baseline + max_descent * 1.25
        self.cursor_x = Constants.HSTEP
        self.line = []        
    
    def text_handler(self, word: str) -> None:
        font = tkinter.font.Font(
            size=self.size,
            weight=self.weight,
            slant=self.style
        )
        
        w = font.measure(word)
        #self.display_list.append((self.cursor_x, self.cursor_y, word, font))
        self.line.append((self.cursor_x, word, font))
        self.cursor_x += w + font.measure(" ")
        
        if self.cursor_x + w > Constants.BROWSER_WIDTH - Constants.HSTEP:
            print("Flushing line due to width limit")
            print(f"{self.line}")
            self.flush()
            
    def tag_handler(self, tag: Tag) -> None:
        if tag.name == "i":
            self.style = "italic"
        elif tag.name == "b":
            self.weight = "bold"
        elif tag.name == "/i":
            self.style = "roman"
        elif tag.name == "/b":
            self.weight = "normal"
        elif tag.name == "small":
            self.size -= 2
        elif tag.name == "/small":
            self.size += 2
    
def lex(body: str) -> List[Text | Tag]:
    out: List[Text | Tag] = []
    buffer: str = ""
    in_tag: bool = False
    for ch in body:
        if ch == "<":
            in_tag = True
            if buffer:
                out.append(Text(buffer))
            buffer = ""
        elif ch == ">":
            in_tag = False
            out.append(Tag(buffer))
            buffer = ""
        else:
            buffer += ch
    if not in_tag and buffer:
        out.append(Text(buffer))
    return out