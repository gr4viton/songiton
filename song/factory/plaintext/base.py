from pydantic import BaseModel
from song.factory.plaintext.line_stats import LineStore
from song.factory.plaintext.verse_line import VerseLineFactory
from models import Song, Section


class SongFactoryPlaintext(BaseModel):
    naive: bool

    def get_song(self, plaintext):
        if self.naive:
            song = self.naive_parser(plaintext)
        return song

    @classmethod
    def naive_parser(cls, plaintext):
        """

        First categorize lines
        - detect via short words with longer spaces = chord_line
        - detect via known chord words

        Then create verses
        - detect via enumeration prefixes `1.` + `R:`
        - detect via empty line

        Then analyze lines to assing chord position.
        """
        store = LineStore.from_plaintext(plaintext)

        if store.first_line_is_empty:
            raise RuntimeError("Naive parser error - first line is empty")
        # first line has to be chords in this naive approach
        if store.first_line_is_chord:
            raise RuntimeError("Naive parser error - first line not chords")

        # check if the line categories are zigzag
        if not store.lines_are_zigzag:
            raise RuntimeError("Naive parser error - line categories not zigzag")

        print("line categories are switching per each line, yay")

        print("not detecting multiple verses for now")
        # the indentation should be removed before the following step!

        category_cls = Section.__fields__["category"].type_  # lol

        sections = []
        verse_lines = []
        verse_code = None
        for line_pair in store.get_line_pairs():
            chord_line, text_line = line_pair

            save_previous_verse = text_line.verse_code != verse_code and verse_code is not None
            if save_previous_verse:
                # first line_pair of a new verse (section)
                sections.append(Section(
                    category=category_cls.verse  # always verse for now
                    verse_code=verse_code,
                    lines=list(verse_lines),
                ))
                verse_lines = []

            verse_code = text_line.verse_code

            verse_line = VerseLineFactory.from_plaintext(chord_line.line, text_line.line)
            verse_lines.append(verse_line)
        else:
            # done if we get to the end of the iterable
            # save the last verse as section now
            sections.append(Section(
                category=category_cls.verse  # always verse for now
                verse_code=verse_code,
                lines=list(verse_lines),
            ))

        for verse_line in verse_lines:
            verse_code = text_line.verse_code

        format_version = Song.__fields__["format_version"].type_
        song = Song(
            format_version=format_version.v0_1_0,
            name="noha_v_dumku.lorem",
            slug="noha_v_dumku.lorem",
            author="SCRAPER",
            language="cz",
            sections=sections
        )
        return song

        # verse_start_line_indexes = []
        # for i, line in enumerate(lines):
        #     pat = r"\d\..+"
        #     match = re.search(pat, line)
        #     if match:
        #         verse_start_line_indexes.append(i)
