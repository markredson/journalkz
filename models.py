from typing import Annotated
from sqlmodel import SQLModel, Field


class Type_Of_Article(SQLModel, table = True):
    id: int | None = Field(default = None, primary_key = True)
    type_of_article: str = Field(index=True)

class Type_Of_User(SQLModel, table = True):
    id: int | None = Field(default = None, primary_key = True)
    type_of_user: str = Field(index = True)

class User(SQLModel, table = True):
    id: int | None = Field(default = None, primary_key = True)
    lastName: str = Field(index = True)
    firstName: str = Field(index = True)
    birthdate: str
    country: str = Field(index = True)
    phone_number: int
    email: str = Field(index = True)
    type_of_user_id: int | None = Field(default=None, index=True)

class Article(SQLModel, table = True):
    id: int | None = Field(default = None, primary_key = True)
    title: str
    text: str
    date: str
    views: int
    author_id: int
    type_of_article_id: int

class Article_Images(SQLModel, table = True):
    id: int | None = Field(default = None, primary_key = True)
    article_images_image: str
    article_images_id: str

class Liked_Article(SQLModel, table = True):
    id: int | None = Field(default = None, primary_key = True)
    article_id: int | None = Field(default=None, index=True)
    user_id: int | None = Field(default=None, index=True)

class View_User(SQLModel, table = True):
    id: int | None = Field(default = None, primary_key = True)
    user_id: int | None = Field(default=None, index=True)
    article_id: int | None = Field(default=None, index=True)

