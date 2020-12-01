from enum import Enum
from typing import Optional, List
from itertools import zip_longest

from pydantic import BaseModel




class LineCategory(str, Enum):
    chord = "chord"
    text = "text"


class Line(BaseModel):
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


class LineStore(BaseModel):
    lines: List[Line]

    @classmethod
    def from_plaintext(cls, plaintext):
        txt_lines = plaintext.split("\n")
        lines = [Line(line=line) for line in txt_lines]
        inst = cls(lines=lines)
        inst.analyze()
        return inst

    def analyze(self):
        for line in self.lines:
            if line.space_to_char_ratio > 1:
                line.category = LineCategory.chord
            else:
                line.category = LineCategory.text

    @property
    def lines_without_empty(self):
        return list(filter(lambda lin: lin.is_empty==False, self.lines))
        return self.list

    # @property
    # def lines_without_starting_empty(self):
    #     # skip the starting empty lines
    #     for i, line in enumerate(self.lines):
    #         if not line.is_empty:
    #             first_non_empty_index = i
    #             break
    #     return self.lines[first_non_empty_index:]

    @property
    def first_line_is_empty(self):
        return self.lines[0].is_empty

    @property
    def first_line_is_chord(self):
        return self.lines[0].category is not LineCategory.chord

    @property
    def lines_are_zigzag(self):
        """True if there are no 2 linest with the same category next to each other."""
        last_line_category = self.lines[0].category
        for line in self.lines[1:]:
            if line.is_empty:
                continue

            if line.category is last_line_category:
                return False

            last_line_category = line.category
        return True

    @staticmethod
    def _group_by_two(lst):
        return list(zip_longest(*(iter(lst),) * 2))

    def get_line_pairs(self):
        lines = self.lines_without_empty
        if len(lines) % 2 == 1:
            lines = self.lines

        if len(lines) % 2 == 1:
            print("lines count is odd")

        return self._group_by_two(lines)
