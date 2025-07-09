from src.webbrowser_py.URL import URL


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
