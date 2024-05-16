import datetime
from typing import List

import pytest
from src.bank import Account
from src.classes.errors import TransactionError
from src.database import Database
from src.models import TypeTransaction
from src.main import App


def test_withdraw_normal(db: Database, accounts: List[Account], count_transactions):
    app = App()
    nb_trans = count_transactions()

    transaction, account = app.action(accounts[0], TypeTransaction.withdraw, amount=50)

    account._refresh()
    assert account.account.balance == 50

    transaction._refresh()
    assert transaction.transaction is not None

    assert transaction.transaction.type.name == TypeTransaction.withdraw.name
    assert type(transaction.transaction.time_created) is datetime.datetime
    assert count_transactions() == nb_trans + 1


def test_withdraw_insufficient_funds(
    db: Database, accounts: List[Account], count_transactions
):
    app = App()
    nb_trans = count_transactions()

    with pytest.raises(TransactionError, match="InsufficientFunds"):
        app.action(accounts[0], TypeTransaction.withdraw, amount=120)

    accounts[0]._refresh()
    assert accounts[0].account.balance == 100
    assert nb_trans == count_transactions()


def test_withdraw_zero_amount(
    db: Database, accounts: List[Account], count_transactions
):
    app = App()
    nb_trans = count_transactions()

    with pytest.raises(TransactionError, match="AmountZero"):
        app.action(accounts[0], TypeTransaction.withdraw, amount=0)

    accounts[0]._refresh()
    assert accounts[0].account.balance == 100
    assert nb_trans == count_transactions()


def test_withdraw_negative_amount(
    db: Database, accounts: List[Account], count_transactions
):
    app = App()
    nb_trans = count_transactions()

    with pytest.raises(TransactionError, match="AmountNegative"):
        app.action(accounts[0], TypeTransaction.withdraw, amount=-20)

    accounts[0]._refresh()
    assert accounts[0].account.balance == 100
    assert nb_trans == count_transactions()
