import re
from typing import Optional
from itertools import izip_longest

from models import Song, ChordPoint, TextAbscissa, VerseLine
from pydantic import BaseModel
from enum import Enum


class VerseLineFactory:

    @classmethod
    def from_plaintext(chord_line, text_line):
        pass
        chord_words = re.findall(r"\w+", chord_line)
        __import__('pudb').set_trace()

        chord_points = [ChordPoint.from_x_letter(0, word) for word in chord_words]
        text_abscissas = [TextAbscissa(text=text_line)]
        return VerseLine(chord_points, text_abscissas)


class LineCategory(str, Enum):
    chord = "chord"
    text = "text"


class LineStats(BaseModel):
    line: str
    category: Optional[LineCategory] = None

    @property
    def non_space_count(self):
        return len(self.line.replace(" ", ""))

    @property
    def space_count(self):
        return len(self.line) - self.non_space_count

    @property
    def space_to_char_ratio(self):
        """

        If there is a lot of spaces the ratio is high.
        If there is a lot of chars the ratio is low.
        """
        if not self.non_space_count:
            return 0
        return self.space_count / self.non_space_count

    @property
    def is_empty(self):
        return not bool(self.line.replace(" ", ""))



class SongFactory:

    @classmethod
    def from_plaintext(cls, txt):
        """

        In future, also try to use NN to learn the individual lines of the plaintext songs,
        then use it to analyze new songs
        """
        naive = True
        if naive:
            song = cls.naive_parser(txt)
        return song

    @classmethod
    def naive_parser(cls, txt):
        """

        First categorize lines
        - detect via short words with longer spaces = chord_line
        - detect via known chord words

        Then create verses
        - detect via enumeration prefixes `1.` + `R:`
        - detect via empty line

        Then analyze lines to assing chord position.
        """
        txt_lines = txt.split("\n")

        stats = LinesStats(lines=txt_lines)

class LinesStats(BaseModel):
    lines: List[LineStats]
        lines = [LineStats(line=line) for line in txt_lines]
        for line in lines:
            if line.space_to_char_ratio > 1:
                line.category = LineCategory.chord
            else:
                line.category = LineCategory.text

        # remove the empty lines from the beginning
        old_lines = list(lines)
        for i, line in enumerate(old_lines):
            if not line.is_empty:
                first_non_empty_index = i
                break
        lines = old_lines[first_non_empty_index:]

        # first line has to be chords in this naive approach
        if lines[0].category is not LineCategory.chord:
            raise RuntimeError("Naive parser error - first line not chords")

        for i in range(1, len(lines)):
            if lines[i].is_empty:
                lines[i-1].next_is_empty = True
                if i + 1 < len(lines):
                    lines[i+1].previous_is_empty = True
            if line
        # we need to have

        izip_longest(*(iter(range(10)),) * 3)

        # check if the line categories are zigzag
        last_line_category = lines[0].category
        for line in lines[1:]:
            if line.is_empty:
                continue

            if line.category is last_line_category:
                raise RuntimeError("Naive parser error - line categories not zigzag")

            last_line_category = line.category

        print("line categories are switching per each line, yay")
        print("not detecting multiple verses for now")
        # the indentation should be removed before the following step!

        non_empty_lines = list(filter(lambda lin: not lin.is_empty, lines))
        for two_lines in zip(non_empty_lines, 2):
            chord_line, text_line = two_lines
            verse_line = VerseLineFactory.from_plaintext(chord_line, text_line)

        # VerseLine(
        #     chord_points=

        # verse_start_line_indexes = []
        # for i, line in enumerate(lines):
        #     pat = r"\d\..+"
        #     match = re.search(pat, line)
        #     if match:
        #         verse_start_line_indexes.append(i)
