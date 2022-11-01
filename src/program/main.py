import urllib.request

import typer
from rich import print

from handlers.database_handler import SqliteHandler
from handlers.news_handler import FeedHandler, TrendHandler

app = typer.Typer()
db_handler = SqliteHandler("local_app.db")


def input_rss(rss_link: str):
    """
    input-rss [rss_link] | input rss into the database
    """
    feed_title = FeedHandler(feed_url=rss_link).title
    db_handler.insert_feed(feed_title, rss_link)


@app.command()
def rss():
    """
    Feed manager
    """
    feeds = db_handler.get_feeds()
    db_handler.list_feeds()
    print('---------------')
    print("""
    Here is your option list of action
    1. input rss
    2. remove rss
    3. exit
    
    """)
    option = input('My choice:')
    match option:
        case '1':
            print("[green]Input new rss into database[/green]")
            rss_link = input("PLease provide the rss link:")
            input_rss(rss_link)
        case '2':
            print("[green]Remove rss from data[/green]")
            rss_order = input("Which one you want to remove, give id number:")
            feed_url = feeds[int(rss_order) - 1][1]
            db_handler.delete_feed(feed_url)
            print(f"Deleted {feed_url} from the feeds database")
        case '3':
            return
        case other:
            print("Not valid value,stop here")
            return


@app.command()
def get_news(limit: int = typer.Argument(10)):
    """
    Get news from current feed
    """
    feeds: list = db_handler.get_feeds()
    db_handler.list_feeds()
    feed_index = int(input("Type your order of feed to get \n"))
    feed_handler: FeedHandler = FeedHandler(feeds[feed_index - 1][1], limit_page=limit)
    feed_handler.get_news()


@app.command()
def get_trends(limit_page: int = typer.Argument(10)):
    """
    Get trending news
    """
    print("""
    Here is your option list of countries
    1. VN
    2. SG
    3. US

    """)
    option = input('My choice:')
    match option:
        case '1':
            trend_hand = TrendHandler(limit_page, "VN")
            trend_hand.get_top_trends()
            trend_hand.get_articles()
        case '2':
            trend_hand = TrendHandler(limit_page, "SG")
            trend_hand.get_top_trends()
            trend_hand.get_articles()
        case '3':
            trend_hand = TrendHandler(limit_page, "US")
            trend_hand.get_top_trends()
            trend_hand.get_articles()
        case other:
            print("Not valid value,stop here")
            return


@app.command()
def my_ip():
    """
    Get your ip
    """
    my_ip_address = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    print('Here is your ip address:', my_ip_address)


def main():
    app()


if __name__ == '__main__':
    main()
