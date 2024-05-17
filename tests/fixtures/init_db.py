from typing import List
import pytest

from src.bank import Account
from src.database import Database
from src.main import App
from src.models import Base


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


@pytest.fixture(scope="function")
def accounts(db) -> List[Account]:
    accounts_balance = [100, 50]
    accounts = []
    app = App()
    for balance in accounts_balance:
        acc = app.create_account(balance=balance)
        accounts.append(acc)

    acc = app.create_account(balance=50)
    accounts.append(acc)
    acc.delete()

    return accounts
