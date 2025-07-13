import tkinter
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
        self.display_list: List[Tuple[int, int, str, tkinter.font.Font]] = []
        self.cursor_x = Constants.HSTEP
        self.cursor_y = Constants.VSTEP
        self.size = Constants.FONT_SIZE
        self.weight: Literal['normal', 'bold'] = "normal"
        self.style: Literal['roman', 'italic'] = "roman"

        for token in tokens:
            self.token_handler(token)
            
    def token_handler(self, token: Text | Tag) -> None:
        if isinstance(token, Text):
            for word in token.text.split():
                self.text_handler(word)
        elif isinstance(token, Tag):
            self.tag_handler(token)
    
    def text_handler(self, word: str) -> None:
        font = tkinter.font.Font(
            size=16,
            weight=self.weight,
            slant=self.style,
        )
        
        w = font.measure(word)
        self.display_list.append((self.cursor_x, self.cursor_y, word, font))
        self.cursor_x += w + font.measure(" ")
        
        if self.cursor_x + w > Constants.BROWSER_WIDTH - Constants.HSTEP:
            self.cursor_y += font.metrics("linespace") * 1.25
            self.cursor_x = Constants.HSTEP
            
    def tag_handler(self, tag: Tag) -> None:
        if tag.name == "i":
            self.style = "italic"
        elif tag.name == "b":
            self.weight = "bold"
        elif tag.name == "/i":
            self.style = "roman"
        elif tag.name == "/b":
            self.weight = "normal"
    
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