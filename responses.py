from pydantic import BaseModel
from models import Song


class PutSongResponse(BaseModel):
    success: bool
    Song: Song
