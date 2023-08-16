from typing import Optional
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    file: str = Field(index=True, default=None)

class Photo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    file_url: str

class UserPhotoLink(SQLModel, table=True):
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    photo_id: Optional[int] = Field(
        default=None, foreign_key="photo.id", primary_key=True
    )

class Challenge(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    challenge_name: str = Field(index=True)
    answer: set