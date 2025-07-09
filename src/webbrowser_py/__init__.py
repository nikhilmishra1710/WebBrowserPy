import sys

from src.webbrowser_py.URL import URL
from src.webbrowser_py.utils import load


def main():
    print(sys.argv)
    if len(sys.argv) < 2:
        print("usage: poetry run <url>")
    else:
        load(URL(sys.argv[1]))
