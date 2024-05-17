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


@pytest.mark.parametrize(
    "amount, type, expected",
    [
        (
            150,
            TypeTransaction.withdraw,
            pytest.raises(TransactionError, match="InsufficientFunds"),
        ),
        (
            20,
            "TypeTransaction.withdraw",
            pytest.raises(TransactionError, match="NotATransactionType"),
        ),
        (
            -5,
            TypeTransaction.withdraw,
            pytest.raises(TransactionError, match="AmountNegative"),
        ),
        (
            0,
            TypeTransaction.withdraw,
            pytest.raises(TransactionError, match="AmountZero"),
        ),
        (
            "test",
            TypeTransaction.withdraw,
            pytest.raises(TypeError),
        ),
    ],
)
def test_withdraw_exception(
    db, accounts: List[Account], count_transactions, amount, type, expected
):
    app = App()
    nb_trans = count_transactions()

    with expected as e:
        assert (app.action(accounts[0], type, amount=amount)) == e

    accounts[0]._refresh()
    assert accounts[0].account.balance == 100
    assert nb_trans == count_transactions()
