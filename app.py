__author__ = "Tin Tomašić"

from emoji import EmojiHandler
from flask import Flask, request, render_template
from config import get_configuration

app = Flask(__name__)


@app.route('/')
def index() -> str:
    """ Home page - used for displaying home page, along with possible search results

    Returns
    -------
    str - HTML template
    """
    query: str = request.args.get(key="query", default=None, type=str)
    if query:
        emoji_handler = EmojiHandler(query)
        emoji_handler.start_stream()
        return render_template("index.html", query=query, emojis=emoji_handler.emojis)
    else:
        return render_template("index.html", query=query, emojis=None)


# Driver
if __name__ == "__main__":
    config = get_configuration()
    port = int(config["DEFAULT"]["port"])
    host = config["DEFAULT"]["host"]

    app.run(host, port)
