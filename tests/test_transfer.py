from typing import List

import pytest
from src.bank import Account
from src.classes.errors import TransactionError
from src.database import Database
from src.models import TypeTransaction
from src.main import App


def test_transfer_normal(db: Database, accounts: List[Account], count_transactions):
    app = App()
    nb_trans = count_transactions()

    transactions = app.action(
        accounts[0], TypeTransaction.transfer, amount=50, target=accounts[1]
    )

    assert len(transactions) == 2

    withdraw, acc = transactions[0]
    withdraw._refresh()
    acc._refresh()
    assert acc.account.balance == 50
    assert withdraw.transaction.type.name == TypeTransaction.withdraw.name

    deposit, acc = transactions[1]
    deposit._refresh()
    acc._refresh()
    assert acc.account.balance == 100
    assert deposit.transaction.type.name == TypeTransaction.deposit.name

    assert count_transactions() == nb_trans + 2


def test_transfer_insufficient_funds(
    db: Database, accounts: List[Account], count_transactions
):
    app = App()
    nb_trans = count_transactions()

    with pytest.raises(TransactionError, match="InsufficientFunds"):
        app.action(
            accounts[0], TypeTransaction.transfer, amount=150, target=accounts[1]
        )

    accounts[0]._refresh()
    assert accounts[0].account.balance == 100

    accounts[1]._refresh()
    assert accounts[1].account.balance == 50

    assert count_transactions() == nb_trans


def test_transfer_zero_amount(
    db: Database, accounts: List[Account], count_transactions
):
    app = App()
    nb_trans = count_transactions()

    with pytest.raises(TransactionError, match="AmountZero"):
        app.action(accounts[0], TypeTransaction.transfer, amount=0, target=accounts[1])

    accounts[0]._refresh()
    assert accounts[0].account.balance == 100

    accounts[1]._refresh()
    assert accounts[1].account.balance == 50

    assert count_transactions() == nb_trans


def test_transfer_negative_amount(
    db: Database, accounts: List[Account], count_transactions
):
    app = App()
    nb_trans = count_transactions()

    with pytest.raises(TransactionError, match="AmountNegative"):
        app.action(
            accounts[0], TypeTransaction.transfer, amount=-20, target=accounts[1]
        )

    accounts[0]._refresh()
    assert accounts[0].account.balance == 100

    accounts[1]._refresh()
    assert accounts[1].account.balance == 50

    assert count_transactions() == nb_trans
