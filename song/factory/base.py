
from song.factory.plaintext.base import SongFactoryPlaintext


class SongFactory:

    @classmethod
    def from_plaintext(cls, plaintext):
        """

        In future, also try to use NN to learn the individual lines of the plaintext songs,
        then use it to analyze new songs
        """
        factory = SongFactoryPlaintext(naive=True)
        song = factory.get_song(plaintext=plaintext)
        return song
