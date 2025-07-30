from typing import Annotated
from typing import List
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

from database import create_db_and_tables, get_session

from datetime import date

'''class Type_Of_Article(SQLModel, table = True):
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
    article_id: int | None = Field(default=None, index=True)'''

class Type_Of_Article(SQLModel, table = True):
    id: int | None = Field(default = None, index = True)
    type_of_article: str = Field(index = True)

class ArticleBase(SQLModel):
    title: str = Field(index = True)
    text: str 
    date_of_article: date = Field(index = True)
    views: int = Field(index = True)
    author_id: int = Field(index = True)
    type_article_id: int = Field(index = True)

class Article(ArticleBase, table = True):
    id: int = Field(index = True)

class ArticelPublic(ArticleBase):
    id: int 

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(ArticleBase):
    title: str | None = None
    text: str | None = None
    date_of_article: date | None = None
    views: int | None = None
    author_id: int | None = None
    type_article_id: int | None = None


class Type_Of_Article(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    type_of_article: str = Field(index=True)
    
    
class  Type_Of_User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    type_of_user: str = Field(index=True)
    

class UserBase(SQLModel):
    username: str = Field(index=True)
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    birth_date: date = Field(index=True)
    country: str = Field(index=True)
    phone_number: str = Field(index=True)
    email: str = Field(index=True)
    type_user_id: int = Field(index=True)
    

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password = str
    

class UserPublic(UserBase):
    id: int


class UserCreate(UserBase):
    password: str
    
    
class UserUpodate(UserBase):
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    birth_date: date | None = None
    country: str | None = None
    phone_number: str | None = None
    email: str | None = None
    type_user_id: int | None = None
    password: str | None = None
                      

class Article_Images(SQLModel, table = True):
    id: int | None = Field(default = None, index = True)
    image: str | None 
    article_id: int | None = Field(default = None, index = True)

class Liked_Article(SQLModel, table = True):
    id: int | None = Field(default = None, index = True)
    article_id | None = Field(default = None, index = True)
    user_id | None = Field(default = None, index = True)

class View_User(SQLModel, table = True):
    id: int | None = Field(default = None, index = True)
    user_id: int | None = Field(default = None, index = True)
    article_id: int | None = Field(default = None, index = True)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# ----------- USER ROUTES -----------

@app.post("/users/", response_model=User)
def create_user(*, session: Session = Depends(get_session), user: User):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.get("/users/", response_model=List[User])
def read_users(*, session: Session = Depends(get_session), offset: int = 0, limit: int = Query(default=100, le=100)):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users

@app.get("/users/{user_id}", response_model=User)
def read_user(*, session: Session = Depends(get_session), user_id: int):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.patch("/users/{user_id}", response_model=User)
def update_user(*, session: Session = Depends(get_session), user_id: int, user: User):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
def delete_user(*, session: Session = Depends(get_session), user_id: int):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}

# ----------- ARTICLE ROUTES -----------

@app.post("/articles/", response_model=Article)
def create_article(*, session: Session = Depends(get_session), article: Article):
    session.add(article)
    session.commit()
    session.refresh(article)
    return article

@app.get("/articles/", response_model=List[Article])
def read_articles(*, session: Session = Depends(get_session), offset: int = 0, limit: int = Query(default=100, le=100)):
    articles = session.exec(select(Article).offset(offset).limit(limit)).all()
    return articles

@app.get("/articles/{article_id}", response_model=Article)
def read_article(*, session: Session = Depends(get_session), article_id: int):
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@app.patch("/articles/{article_id}", response_model=Article)
def update_article(*, session: Session = Depends(get_session), article_id: int, article: Article):
    db_article = session.get(Article, article_id)
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    article_data = article.model_dump(exclude_unset=True)
    db_article.sqlmodel_update(article_data)
    session.add(db_article)
    session.commit()
    session.refresh(db_article)
    return db_article

@app.delete("/articles/{article_id}")
def delete_article(*, session: Session = Depends(get_session), article_id: int):
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    session.delete(article)
    session.commit()
    return {"ok": True}


