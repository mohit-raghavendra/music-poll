import json

from typing import List


class Catalogue:
    def __init__(self) -> None:

        with open('./static/catalogue.json') as f:
            data = json.loads(f.read())

        self.catalogue = dict(data["songs"])

    def get_catalogue(self) -> List[dict]:
        catalogue = [
            {"id": idx, "title": song}
            for idx, song in self.catalogue.items()
        ]

        return catalogue
