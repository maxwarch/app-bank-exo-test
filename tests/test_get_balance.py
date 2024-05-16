import datetime
from typing import List

import pytest
from src.bank import Account

from src.classes.errors import TransactionError

from src.database import Database
from src.models import TypeTransaction
from src.main import App


def test_get_balance_after_create(db: Database, count_transactions):
    app = App()
    nb_trans = count_transactions()

    acc = app.create_account(100)

    assert app.get_balance(acc).balance == 100
    assert nb_trans == count_transactions()


def test_get_balance_after_deposit(
    db: Database, accounts: List[Account], count_transactions
):
    app = App()
    nb_trans = count_transactions()

    transaction, acc = app.action(accounts[0], TypeTransaction.deposit, amount=50)

    assert app.get_balance(acc).balance == 150
    assert count_transactions() == nb_trans + 1


def test_get_balance_after_withdrawal(
    db: Database, accounts: List[Account], count_transactions
):
    app = App()
    nb_trans = count_transactions()

    transaction, acc = app.action(accounts[0], TypeTransaction.withdraw, amount=50)

    assert app.get_balance(acc).balance == 50
    assert count_transactions() == nb_trans + 1


def test_get_balance_after_transfer(
    db: Database, accounts: List[Account], count_transactions
):
    app = App()
    nb_trans = count_transactions()

    transactions = app.action(
        accounts[0], TypeTransaction.transfer, amount=50, target=accounts[1]
    )

    assert app.get_balance(transactions[0][1]).balance == 50
    assert app.get_balance(transactions[1][1]).balance == 100
    assert count_transactions() == nb_trans + 2
