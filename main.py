from typing import Optional, List

from fastapi import FastAPI
from models import Song
from responses import PutSongResponse
from song_store import SongStore


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}


# @app.get("/song/{item_id}", response_model=List[Song])
# def get_song(item_id: int, q: Optional[str] = None):
#     return [Song()]


@app.put("/song", response_model=Song)
def put_song(song: Song):
    store = SongStore()
    success = store.put_song(song)
    return song


@app.get("/songs", response_model=List[Song])
def get_songs(language: Optional[str] = None):
    store = SongStore()
    store.load_songs()
    return store.get_songs(language=language)
