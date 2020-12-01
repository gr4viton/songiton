from pydantic import BaseModel
from models import Song


class PutSongFromPlaintextRequest(BaseModel):
    plaintext: str
