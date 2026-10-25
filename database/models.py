from sqlalchemy import Boolean, Column, Integer, Text

from .connect import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True, nullable=False)
    username = Column(Text, nullable=True)
    first_name = Column(Text, nullable=True)
    last_name = Column(Text, nullable=True)
    register_date = Column(Integer, nullable=True)
    access_level = Column(Integer, default=1, nullable=False)
    favorite_color = Column(Text, nullable=True)
    favorite_food = Column(Text, nullable=True)
    favorite_work = Column(Text, nullable=True)
    favorite_pet = Column(Text, nullable=True)

    @property
    def as_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Text, unique=True, nullable=False)
    message_id = Column(Integer, nullable=False)
    html = Column(Text, nullable=False)

    @property
    def as_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}


class Edit(Base):
    __tablename__ = "edits"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Text, nullable=False)
    message_id = Column(Integer, nullable=False)
    html = Column(Text, nullable=False)
    done = Column(Boolean, default=False, nullable=False)
    created_at = Column(Integer, nullable=False)

    @property
    def as_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
