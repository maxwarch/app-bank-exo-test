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


@pytest.mark.parametrize(
    "amount, type, expected",
    [
        (
            100,
            "TypeTransaction.deposit",
            pytest.raises(TransactionError, match="NotATransactionType"),
        ),
        (
            0,
            TypeTransaction.deposit,
            pytest.raises(TransactionError, match="AmountZero"),
        ),
        (
            -10,
            TypeTransaction.deposit,
            pytest.raises(TransactionError, match="AmountNegative"),
        ),
    ],
)
def test_deposit_exception(
    db, accounts: List[Account], count_transactions, amount, type, expected
):
    app = App()
    nb_trans = count_transactions()
    init_balance = accounts[0].account.balance

    with expected as e:
        assert (app.action(accounts[0], type, amount=amount)) == e

    accounts[0]._refresh()
    assert accounts[0].account.balance == init_balance
    assert nb_trans == count_transactions()
