from models import SectionCategory


class SectionCategoryFactory:

    @classmethod
    def from_verse_code(cls, verse_code):

        if str(verse_code) == "0":
            return SectionCategory.intro
        if verse_code.isnumeric():
            return SectionCategory.verse
        if verse_code.upper() == "R":
            return SectionCategory.refrain
        if verse_code.lower() == "bridge":
            return SectionCategory.bridge

        return SectionCategory.verse
