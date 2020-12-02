import re
import operator
from enum import Enum
from collections import defaultdict
from typing import Optional, List
from itertools import zip_longest

from pydantic import BaseModel, Field


class LineCategory(str, Enum):
    chord = "chord"
    text = "text"


class Line(BaseModel):
    original_line: str = Field(
        None,
        tilte="Original line from plaintext."
    )
    category: Optional[LineCategory] = None
    verse_prefix_text: Optional[str] = Field(
        None,
        title="The text prefix of the line including spaces - sometimes containing the verse number or refrain sign 'R.'."
    )
    verse_letter: Optional[str] = Field(
        None,
        title="Character / string extracted from verse_prefix_text of the leading line of the verse, assigned to all lines in the verse."
    )
    verse_prefix_spaces: Optional[int] = Field(
        0,
        title="If the plaintext is detected to have prefix spaces for most of the lines, they are trimmed."
    )
    original_prefix_spaces: Optional[int] = Field(
        0,
        title="The count of prefix spaces of the original_line - not set by any other lines of the verse."
    )

    @property
    def line(self):
        """Return the working chars of the line.

        If prefix spaces are detected, they are trimmed.
        """
        if not self.category:
            # if category not assigned - we are not sure if to trim
            return self.original_line
        if self.category is LineCategory.chord:
            # if it is category chord - we actually can trim out chord words if they are written before the text starts
            return self.original_line
        if not self.verse_prefix_spaces:
            return self.original_line
        return self.original_line[self.verse_prefix_spaces:]

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
    selected_space_count: Optional[int] = None

    @classmethod
    def from_plaintext(cls, plaintext):
        txt_lines = plaintext.split("\n")
        lines = [Line(original_line=line) for line in txt_lines]
        inst = cls(lines=lines)
        inst.analyze()
        return inst

    def analyze(self):
        self._categorize_lines()
        self._detect_space_prefix()
        self._assign_verse()

    def _categorize_lines(self):
        """Naively categorize the lines."""
        for line in self.lines:
            if line.space_to_char_ratio > 1:
                line.category = LineCategory.chord
            else:
                line.category = LineCategory.text

    def _deduce_selected_space_count(self):
        """Check if lines are prefixed by some number of spaces."""
        occurrence_per_space_count = defaultdict(int)
        for line in self.text_lines:
            spaces_matches = re.findall(r"^ *", line.line)
            space_count = len(spaces_matches[0])
            line.original_prefix_spaces = space_count
            occurrence_per_space_count[space_count] += 1

        space_count_per_occurrence = defaultdict(list)
        for space_count, occurrence in occurrence_per_space_count.items():
            space_count_per_occurrence[occurrence].append(space_count)

            print(f"{space_count} spaces were in the text_lines {occurrence} times")

        max_count = max(space_count_per_occurrence.keys())
        most_frequent_space_counts = sorted(space_count_per_occurrence[max_count])
        # taking the smallest space_count with max occurances (if there are more of them)
        most_frequent_space_count = min(most_frequent_space_counts)
        return most_frequent_space_count

    def _detect_space_prefix(self):
        """Check if lines are prefixed by some number of spaces.

        Add the information about the prefix_space to the Lines.
        """
        if self.selected_space_count is None:
            self.selected_space_count = self._deduce_selected_space_count()

        for line in self.lines:
            line.verse_prefix_spaces = self.selected_space_count

    def _assign_verse(self):
        """Take in account the space_count and assign verse_letter from the text_lines."""
        if not self.selected_space_count:
            return

        for line in self.text_lines:
            line.verse_prefix_text = line.original_line[:self.selected_space_count]
        for line in self.text_lines:
            verse_word = line.verse_prefix_text.replace(" ", "")
            if not verse_word:
                continue
            verse_letter = verse_word.replace(".", "").replace(":", "")
            line.verse_letter = verse_letter

        current_verse_letter = "0"  # assign 0 to the lines without previous verse_letter
        for line in self.text_lines:
            if line.verse_letter is not None:
                current_verse_letter = line.verse_letter

            line.verse_letter = current_verse_letter

            print(line.verse_letter)
            print(line.line)

    @property
    def lines_without_empty(self):
        return list(filter(lambda lin: lin.is_empty==False, self.lines))

    @property
    def chord_lines(self):
        return self.get_lines_by_category(category=LineCategory.chord)

    @property
    def text_lines(self):
        return self.get_lines_by_category(category=LineCategory.text)

    def get_lines_by_category(self, category):
        return list(filter(lambda lin: lin.category is category, self.lines))

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
