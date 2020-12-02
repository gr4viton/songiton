from pydantic import BaseModel
from song.factory.plaintext.line_stats import LineStore
from song.factory.plaintext.verse_line import VerseLineFactory
from song.factory.plaintext.section_category import SectionCategoryFactory
from models import Song, Section, SectionCategory, SongFormatVersion


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

        # generate verse_lines
        sections = []
        verse_lines = []
        line_pairs = store.get_line_pairs()
        for i, line_pair in enumerate(line_pairs):
            chord_line, text_line = line_pair
            verse_line = VerseLineFactory.from_plaintext(chord_line.line, text_line.line)
            verse_lines.append(verse_line)
            verse_code = text_line.verse_code

            save_section = False
            if i+1 < len(line_pairs):
                next_line = line_pairs[i+1]
                next_line_is_new_verse = next_line[1].is_leading_line
                if next_line_is_new_verse:
                    save_section = True
            else:
                # this is last line_pair
                save_section = True

            if save_section:
                section = Section(
                    category=SectionCategoryFactory.from_verse_code(verse_code),
                    verse_code=verse_code,
                    lines=verse_lines,
                )
                sections.append(section)

                # empty the list to store only verse_lines of the next verse
                verse_lines = []


        song = Song(
            format_version=SongFormatVersion.v0_1_0,
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
