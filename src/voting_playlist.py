import asyncio
import json
import logging
import os

import tornado
from tornado.websocket import WebSocketHandler
from tornado.options import define, options, parse_command_line

from catalogue import Catalogue
from playlist import Playlist

define("port", default=8887, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")


song_catalogue = Catalogue()
playlist = Playlist(song_catalogue)


class DisplayHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("playlist.html")


class PlaylistHandler(tornado.web.RequestHandler):
    def get(self):
        self.write({"songs": playlist.get_ordered_list()})
        self.finish()


class SongsHandler(tornado.web.RequestHandler):
    def get(self):
        songs = song_catalogue.get_catalogue()
        self.write({"songs": songs})
        self.finish()


class AddSongsHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        songId = data["id"]
        playlist.add_song(songId)
        SongsDisplayHandler.send_updates({"songs":
                                          playlist.get_ordered_list()})
        self.write({"songs": playlist.get_ordered_list()})
        self.finish()


class SongsDisplayHandler(WebSocketHandler):
    waiters = set()

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        SongsDisplayHandler.waiters.add(self)

    def on_close(self):
        SongsDisplayHandler.waiters.remove(self)

    @classmethod
    def send_updates(cls, song_list):
        logging.info("sending message to %d waiters", len(cls.waiters))
        for waiter in cls.waiters:
            waiter.write_message(song_list)

    def on_message(self, message):
        parsed = tornado.escape.json_decode(message)
        song = parsed["id"]
        playlist.upvote_song(song)
        sorted_song_list = playlist.get_ordered_list()

        SongsDisplayHandler.send_updates({"songs": sorted_song_list})


async def main():

    parse_command_line()

    handlers = [
        (r'/', DisplayHandler),
        (r'/songs', SongsHandler),
        (r"/displaySongs", SongsDisplayHandler),
        (r"/addSong", AddSongsHandler),
        (r"/playlist", PlaylistHandler)

    ]

    app = tornado.web.Application(
        handlers=handlers,
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static")
    )

    app.listen(options.port)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
