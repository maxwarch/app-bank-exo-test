import datetime
from typing import List

import pytest
from src.bank import Account

from src.classes.errors import TransactionError

from src.database import Database
from src.models import TypeTransaction
from src.main import App


def test_deposit_normal(db: Database, accounts: List[Account], count_transactions):
    app = App()
    nb_trans = count_transactions()

    transaction, account = app.action(accounts[0], TypeTransaction.deposit, amount=120)

    account._refresh()
    transaction._refresh()

    assert account.account.balance == 220
    assert transaction.transaction.type == TypeTransaction.deposit
    assert type(transaction.transaction.time_created) is datetime.datetime
    assert count_transactions() == nb_trans + 1
    assert transaction.transaction is not None


def test_deposit_negative(db: Database, accounts: List[Account], count_transactions):
    app = App()
    nb_trans = count_transactions()

    with pytest.raises(TransactionError, match="AmountNegative"):
        app.action(accounts[0], TypeTransaction.deposit, amount=-120)

    accounts[0]._refresh()
    assert accounts[0].account.balance == 100
    assert nb_trans == count_transactions()


def test_deposit_zero(db: Database, accounts: List[Account], count_transactions):
    app = App()
    nb_trans = count_transactions()

    with pytest.raises(TransactionError, match="AmountZero"):
        app.action(accounts[0], TypeTransaction.deposit, amount=0)

    accounts[0]._refresh()
    assert accounts[0].account.balance == 100
    assert nb_trans == count_transactions()
