from src.webbrowser_py.URL import URL
from typing import List, Tuple
from src.webbrowser_py.Constants import Constants


def show(body: str) -> None:
    in_tag: bool = False
    for ch in body:
        if ch == "<":
            in_tag = True
        elif ch == ">":
            in_tag = False
        elif not in_tag:
            print(ch, end="")


def load(url: URL) -> None:
    body: str = url.request()
    show(body)

def layout(text: str) -> List[Tuple[int, int, str]]:
    layout_list: List[Tuple[int, int, str]] = []
    cursor_x, cursor_y = Constants.HSTEP, Constants.VSTEP
    
    for ch in text:
        layout_list.append((cursor_x, cursor_y, ch))
        cursor_x += Constants.HSTEP
        if cursor_x > Constants.BROWSER_WIDTH - Constants.HSTEP:
            cursor_x = Constants.HSTEP
            cursor_y += Constants.VSTEP
            
    return layout_list
    
def lex(body: str) -> str:
    text: str = ""
    in_tag: bool = False
    for ch in body:
        if ch == "<":
            in_tag = True
        elif ch == ">":
            in_tag = False
        elif not in_tag:
            text += ch
    return text