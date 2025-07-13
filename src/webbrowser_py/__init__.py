import sys

from webbrowser_py.Browser import Browser
from webbrowser_py.URL import URL


def main():
    print(sys.argv)
    if len(sys.argv) < 2:
        print("usage: poetry run <url>")
    else:
        url = URL(sys.argv[1])
        browser = Browser()
        browser.load(url)
