import typer

from handlers.database_handler import SqliteHandler
from handlers.news_handler import FeedHandler

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
    db_handler.list_feeds()
    print('---------------')
    print("""
    Here is your option list of action, please type the number into 
    """)


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


if __name__ == '__main__':
    app()
