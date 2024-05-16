import datetime
from typing import List

import pytest
from bank import Account
from classes.errors import TransactionError
from database import Database
from models import TransactionsModel, TypeTransaction
from main import App


def test_deposit_normal(db: Database, accounts: List[Account]):
    app = App()
    transaction, account = app.action(accounts[0], TypeTransaction.deposit, amount=120)

    assert account.account.balance == 220
    assert transaction.transaction.type == TypeTransaction.deposit
    assert type(transaction.transaction.time_created) is datetime.datetime

    transaction._refresh()
    assert transaction.transaction is not None


def test_deposit_negative(db: Database, accounts: List[Account]):
    app = App()

    nb_trans = db.session.query(TransactionsModel).count()

    with pytest.raises(TransactionError, match="AmountNegative"):
        app.action(accounts[0], TypeTransaction.deposit, amount=-120)

    accounts[0]._refresh()
    assert accounts[0].account.balance == 220
    assert nb_trans == db.session.query(TransactionsModel).count()


def test_deposit_zero(db: Database, accounts: List[Account]):
    app = App()

    nb_trans = db.session.query(TransactionsModel).count()

    with pytest.raises(TransactionError, match="AmountZero"):
        app.action(accounts[0], TypeTransaction.deposit, amount=0)

    accounts[0]._refresh()
    assert accounts[0].account.balance == 220
    assert nb_trans == db.session.query(TransactionsModel).count()
