from webbrowser import open

import feedparser
from bs4 import BeautifulSoup
from rich import print
from rich.panel import Panel

class FeedHandler:
    def __init__(self, feed_url: str = "https://vnexpress.net/rss/kinh-doanh.rss", limit_page: int = 10):
        print('Use this fee_url:', feed_url, 'limit page:', limit_page, 'as default')
        self.payload = feedparser.parse(feed_url)
        self.title = self.payload.feed.title
        self.entries = self.payload.entries
        self.feed_url = feed_url
        self.limit_page = limit_page

    def get_news(self):
        limit_page: int = self.limit_page
        entries: list = self.entries

        index = 0
        for entry in entries:
            if index < limit_page:
                # prepare
                order = '[bold red]' + str(index + 1) + '[/bold red]'
                title = f'[link={entry.link}][green]' + entry.title + '[green][/link]'
                content = BeautifulSoup(entry.summary, features="html.parser").text
                date = entry.published_parsed
                posted_date = ('Posted at:', str(date.tm_year) + '-' + str(date.tm_mon) + '-' + str(date.tm_mday), str(
                    date.tm_hour).zfill(2) + ':' + str(date.tm_min).zfill(2))
                # print
                print('----***-----')
                print(*posted_date)
                print(order, title)
                print(Panel(content))

                index += 1
            else:
                break

        self.open_page(entries)

    def open_page(self, entries: list):
        try:
            get_page = input('Do you want to open anything, type number of page, type "no" to stop \n')
            if get_page == 'no':
                return
            else:
                open(entries[int(get_page) - 1].link)
        except ValueError:
            print("Input is not of int type , please retry")
            return self.open_page(entries)
