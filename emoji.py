__author__ = "Tin Tomašić"

from coroutine import coroutine
from types import SimpleNamespace
from logzero import logger
from json import loads
from requests import Session
from config import get_configuration
from configparser import ConfigParser


class EmojiHandler:
    """ Used for streaming emoji from external API
    """

    def __init__(self, pattern: str = None) -> None:
        """ Initializes EmojiHandler with specified search query

        Parameters
        ----------
        pattern - pattern to search for in emoji unicode name
        """
        self.emojis: list = []
        self.pattern: str = pattern
        self.config: ConfigParser = get_configuration()
        self.parse_json = self.parse_json()
        self.grep = self.grep()
        self.sink = self.sink()

    def start_stream(self) -> None:
        """ Starts streaming emoji data from external API
        """
        uri: str = self.config["API"]["uri"]
        key: str = self.config["API"]["key"]
        url: str = f"{uri}?access_key={key}"
        headers: dict = {'content-type': 'application/json'}

        with Session().get(url=url, headers=headers, stream=True) as resp:
            for chunk in resp.iter_content():
                if chunk:
                    for byte in chunk:
                        self.parse_json.send(byte)

        self.parse_json.close()

    @coroutine
    def parse_json(self) -> None:
        """ Collects streaming data and parses JSON Emoji objects
        """
        buffer: str = ""
        try:
            while True:
                byte: int = yield
                buffer: str = "{" if chr(byte) == "{" else "".join([buffer, chr(byte)])

                if chr(byte) == "}" and buffer[0] == "{":
                    emoji: SimpleNamespace = loads(buffer, object_hook=lambda d: SimpleNamespace(**d))
                    if self.pattern:
                        self.grep.send(emoji)
                    else:
                        self.sink.send(emoji)
                    buffer: str = ""
        except GeneratorExit:
            pass

    @coroutine
    def grep(self) -> None:
        """ Filters Emoji objects according to the given pattern
        """
        try:
            while True:
                emoji: SimpleNamespace = yield
                try:
                    if self.pattern in emoji.unicodeName:
                        self.sink.send(emoji)
                except AttributeError:
                    logger.debug(f"Given emoji does not contain unicode name ({emoji})")
        except GeneratorExit:
            pass

    @coroutine
    def sink(self):
        """ Sink coroutine; saves Emoji objects to internal emoji collection """
        try:
            while True:
                emoji: SimpleNamespace = yield
                self.emojis.append(emoji)
        except GeneratorExit:
            pass
