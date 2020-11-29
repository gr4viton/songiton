from typing import Optional, List
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


class SectionCategory(str, Enum):
    verse = "verse"
    refrain = "refrain"
    intro = "intro"
    bridge = "bridge"
    outro = "outro"


class Section(BaseModel):
    category: SectionCategory
    verse_number: int
    lines: List[VerseLine]


class SongFormatVersion(str, Enum):
    version_0_0_1 = "version_0_0_1"


class Song(BaseModel):
    format_version: SongFormatVersion
    id: int
    slug: str  # snakeify the name
    name: str
    language: str
    author: str
    sections: List[Section]

    @property
    def file_name(self):
        return f"{self.slug}.jsong"
