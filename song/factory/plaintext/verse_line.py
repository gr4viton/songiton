import re
from models import ChordPoint, TextAbscissa, VerseLine


class VerseLineFactory:

    @classmethod
    def from_plaintext(cls, chord_line, text_line):
        chord_words = re.findall(r"\w+", chord_line)

        chord_points = [ChordPoint.from_x_letter(x=0, letter=word) for word in chord_words]
        text_abscissas = [TextAbscissa(text=text_line)]
        return VerseLine(chord_points=chord_points, text_abscissas=text_abscissas)
