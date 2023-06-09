from typing import List
from catalogue import Catalogue


class Playlist:
    def __init__(self, catalogue: Catalogue) -> None:
        self.playlist = []
        self.song_catalogue = catalogue

    def get_ordered_list(self) -> List[dict]:
        sorted_list = sorted(self.playlist,
                             key=lambda k: k["upvotes"],
                             reverse=True
                             )

        return sorted_list

    def upvote_song(self, songId: int):
        for song in self.playlist:
            if song["id"] == int(songId):
                song["upvotes"] += 1

    def add_song(self, songId: int):

        present = False
        for song in self.playlist:
            if song["id"] == songId:
                present = True

        if not present:
            self.playlist.append(
                    {
                        "id": songId,
                        "title": self.song_catalogue.catalogue[songId],
                        "upvotes": 0
                    }
                )
