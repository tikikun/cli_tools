
import typer
import os
print(os.getcwd())
from rich import print

from handlers.database_handler import SqliteHandler
from handlers.news_handler import FeedHandler, TrendHandler

app = typer.Typer()
db_handler = SqliteHandler("local_app.db")


@app.command()
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
def get_trends():
    """
    Get trending news
    """
    print("""
    Here is your option list of countries
    1. VN
    2. SG
    3. US

    """)
    trend_handler = TrendHandler()
    option = input('My choice:')
    match option:
        case '1':
            trend_handler.get_top_trends("VN")
        case '2':
            trend_handler.get_top_trends("SG")
        case '3':
            trend_handler.get_top_trends("US")
        case other:
            print("Not valid value,stop here")
            return


def main():
    app()


if __name__ == '__main__':
    main()
