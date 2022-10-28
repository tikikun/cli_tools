import typer
from rich import print

from handlers.database_handler import SqliteHandler
from handlers.news_handler import FeedHandler

app = typer.Typer()
db_handler = SqliteHandler("local_app.db")


@app.command()
def goodbye(name: str):
    print(f"goodbye {name}")


@app.command()
def input_rss(rss_link: str):
    feed_title = FeedHandler(feed_url=rss_link).title
    db_handler.insert_feed(feed_title, rss_link)


@app.command()
def rss():
    db_handler.list_feeds()


@app.command()
def get_news(limit: int = typer.Argument(10)):
    feeds: list = db_handler.get_feeds()
    db_handler.list_feeds()
    feed_index = int(input("Type your order of feed to get \n"))
    feed_handler: FeedHandler = FeedHandler(feeds[feed_index-1][1],limit_page=limit)
    feed_handler.get_news()


if __name__ == '__main__':
    app()
