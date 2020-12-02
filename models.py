from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum


class Chord(BaseModel):
    letter: str


class ChordPoint(BaseModel):
    x: float
    chord: Chord

    @classmethod
    def from_x_letter(cls, x, letter):
        return cls(x=x, chord=Chord(letter=letter))


class TextAbscissa(BaseModel):
    text: str
    x_min: float = 0.0
    x_max: float = 1.0
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
    verse_code: str
    lines: List[VerseLine]


class SongFormatVersion(str, Enum):
    v0_0_1 = "v0.1.0"


class Song(BaseModel):
    format_version: SongFormatVersion
    # id: int
    # hash: str  # to calculate on creation
    name: str
    author: str
    language: str
    slug: Optional[str] = Field(
        None,
        title="The name of the song but with snake_case formatting."
    )
    sections: List[Section]

    @property
    def file_name(self):
        return f"{self.slug}.jsong"
