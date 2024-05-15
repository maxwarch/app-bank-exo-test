import pytest
from sqlalchemy import bindparam

from bank import Account
from database import Database
from models import AccountsModel, Base


@pytest.fixture(scope="module")
def db():
    db = Database("sqlite:///data_test.sqlite")
    if not db.engine.url.get_backend_name() == "sqlite":
        raise RuntimeError("Use SQLite backend to run tests")

    Base.metadata.create_all(db.engine)
    # yield db
    try:
        yield db
    finally:
        Base.metadata.drop_all(db.engine)


@pytest.fixture(scope="module")
def seed_user(db) -> Account:
    acc = Account()
    acc.create(100)

    return acc.account
    # return (
    #     db.session.query(AccountsModel)
    #     .filter(AccountsModel.account_id == bindparam("account_id", 1))
    #     .one()
    # )
