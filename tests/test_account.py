import pytest

from bank import Account
from database import Database
from models import AccountsModel

INIT_BALANCE = 5899


def test_create(db: Database):
    acc = Account()
    acc.create(5899)

    assert acc.account.account_id == 1
    assert acc.account.balance == INIT_BALANCE


def test_get(db):
    assert Account(1).account.account_id == 1


def test_update(db: Database):
    acc = Account(1)
    acc.update(balance=5)

    assert acc.account.balance == INIT_BALANCE + 5


def test_delete(db: Database):
    Account(1).delete()

    assert (
        db.session.query(AccountsModel)
        .filter(AccountsModel.account_id == 1)
        .one_or_none()
    ) is None
