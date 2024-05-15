import pytest
from sqlalchemy import text
from sqlalchemy.exc import NoResultFound

from bank import Account
from database import Database
from models import AccountsModel


def test_create(db: Database):
    acc = Account()
    acc.create(12)

    id_created = db.engine.connect().execute(text("SELECT last_insert_rowid()"))

    acc_in_db = (
        db.session.query(AccountsModel).filter(AccountsModel.balance == 12).one()
    )

    assert id_created.fetchone()[0] == acc_in_db.account_id


def test_update(db: Database):
    acc = Account()
    acc.update(1, balance=5)

    acc_in_db = (
        db.session.query(AccountsModel).filter(AccountsModel.account_id == 1).one()
    )

    assert acc_in_db.balance == 17


def test_delete(db: Database):
    acc = Account()
    acc.delete(1)

    with pytest.raises(NoResultFound):
        (db.session.query(AccountsModel).filter(AccountsModel.account_id == 1).one())
