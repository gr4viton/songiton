from typing import Optional, List

from fastapi import FastAPI

from pydantic import BaseModel
from enum import Enum


class Chord(BaseModel):
    letter: str


class ChordPoint(BaseModel):
    x: float
    chord: Chord


class TextAbscissa(BaseModel):
    text: str
    x_min: float = 0
    x_max: float = 1
    voice_name: str = None


class VerseLine(BaseModel):
    chord_points: List[ChordPoint]  # chord_line
    text_abscissas: List[TextAbscissa]  # text_abscissas


class SectionCategory(Enum):
    verse = "verse"
    refrain = "refrain"
    intro = "intro"
    bridge = "bridge"
    outro = "outro"


class Section(BaseModel):
    category: SectionCategory
    verse_number: int
    lines: List[VerseLine]


class Song(BaseModel):
    name: str
    language: str
    author: str
    sections: List[Section]


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/songs/{item_id}", response_model=List[Song])
def get_songs(item_id: int, q: Optional[str] = None):
    return [Song()]

