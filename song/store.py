import os

import simplejson
from fastapi import HTTPException
# from structlog import get_logger
from models import Song


# logger = get_logger(__name__)


class SongStore:
    """Songs store.

    jsong_ensure_ascii - default False
    - on False store unicode to jsong file
    - normally JSON should contain only ascii chars - the utf8 is encoded via /u
    - though the jsong format can be sometimes read by humans - ergo use the utf8 in .jsong files by default
    """

    _path = "./store/"
    jsong_ensure_ascii = False
    jsong_indent = 2
    store = None

    def __init__(self):
        pass

    def put_song(self, song) -> bool:
        """Puts the song to db / disk - replaces if exist."""
        success = False
        fname = song.file_name
        fpath = os.path.join(self._path, fname)
        # if os.path.exists(fpath):
        #     raise HTTPException(status_code=409, detail="Song already exist")

        with open(fpath, "w") as fil:
            txt = song.json(ensure_ascii=self.jsong_ensure_ascii, indent=self.jsong_indent)
            fil.write(txt)

        success = True
        return success

    def load_songs(self):
        files = self.get_song_files(self._path)
        if not files:
            raise HTTPException(status_code=404, detail="No songs found")
        self.store = self.parse_songs_from_files(files)

    def parse_songs_from_files(self, files):
        songs = []
        for file in files:
            try:
                songs.append(Song.parse_file(file))
            except Exception as exc:
                print(f"Song loading error from file {file}.")
                print(exc)
        return songs

    def get_songs(self, language=None):
        if language:
            return list(filter(lambda song: song.language == language, self.store))
        return self.store

    def get_song_files(self, path):
        files = []
        for root, dirs, files in os.walk(path, topdown=False):
            files.extend([os.path.join(root, name) for name in files])
        return files
