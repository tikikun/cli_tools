from webbrowser import open

import feedparser
import typer
from bs4 import BeautifulSoup
from rich import print

app = typer.Typer()


@app.command()
def hello(name: str):
    print(f"Hello {name}")


@app.command()
def goodbye(name: str):
    print(f"goodbye {name}")


@app.command()
def get_news(limit: int = typer.Argument(10)):
    # Use a breakpoint in the code line below to debug your script.
    NewsFeed = feedparser.parse("https://vnexpress.net/rss/kinh-doanh.rss")
    entries = NewsFeed.entries
    index = 0
    for entry in entries:
        if index < limit:
            # prepare
            order = '[bold red]' + str(index + 1) + '[/bold red]'
            title = f'[link={entry.link}][green]' + entry.title + '[green][/link]'
            content = '[white]' + BeautifulSoup(entry.summary, features="html.parser").text + '[/white]'
            date = entry.published_parsed
            posted_date = ('Posted at:', str(date.tm_year) + '-' + str(date.tm_mon) + '-' + str(date.tm_mday), str(
                date.tm_hour).zfill(2) + ':' + str(date.tm_min).zfill(2))
            # print
            print('----***-----')
            print(*posted_date)
            print(order, title)
            print(content)

            index += 1
        else:
            break

    open_page(entries)


def open_page(entries: list):
    try:
        get_page = int(input('Do you want to open anything, type number of page \n'))
        open(entries[int(get_page) - 1].link)
    except ValueError:
        print("Input is not of int type , please retry")
        return open_page(entries)


if __name__ == '__main__':
    app()
