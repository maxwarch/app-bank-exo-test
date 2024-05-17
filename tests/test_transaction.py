from typing import List
import pytest

from src.bank import Account
from src.classes.errors import TransactionError
from src.database import Database
from src.models import TypeTransaction


def test_create_no_problem(db: Database, accounts: List[Account], transaction_factory):
    trans = transaction_factory(1, amount=12, type=TypeTransaction.deposit)
    assert trans.transaction_id == 1


@pytest.mark.parametrize(
    "account_id, amount, type, expected",
    [
        (
            100,
            20,
            TypeTransaction.deposit,
            pytest.raises(TransactionError, match="NoAccountAttach"),
        ),
        (
            1,
            20,
            "TypeTransaction.deposit",
            pytest.raises(TransactionError, match="NotATransactionType"),
        ),
        (
            1,
            -5,
            TypeTransaction.deposit,
            pytest.raises(TransactionError, match="AmountNegative"),
        ),
        (
            1,
            "salut",
            TypeTransaction.deposit,
            pytest.raises(TypeError),
        ),
    ],
)
def test_transaction_exception(
    db, accounts: List[Account], transaction_factory, account_id, amount, type, expected
):
    with expected as e:
        assert (transaction_factory(account_id, amount=amount, type=type)) == e
