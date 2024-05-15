from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from classes.singleton_class import Singleton

SQLALCHEMY_DATABASE_URL = "sqlite:///data.sqlite"


class Database(metaclass=Singleton):
    def __init__(self, url: str = SQLALCHEMY_DATABASE_URL) -> None:
        self.engine = None
        self.session = self._gen_session(url)

    def _gen_engine(self, url: str):
        self.engine = create_engine(url)

    def _gen_session(self, url: str) -> Session:
        self._gen_engine(url)
        engine = self.engine

        Sess = sessionmaker(
            autocommit=False, autoflush=True, bind=engine, expire_on_commit=False
        )

        return Sess()
