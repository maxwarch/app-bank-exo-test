import pytest

from src.classes.errors import TransactionError
from src.database import Database
from src.models import TypeTransaction


def test_create_no_problem(db: Database, accounts, transaction_factory):
    trans = transaction_factory(1, amount=12, type=TypeTransaction.deposit)
    assert trans.transaction_id == 1


# un user est créé dans seed avec l'id 1
def test_create_no_user_attach(db: Database, accounts, transaction_factory):
    with pytest.raises(TransactionError, match="NoAccountAttach"):
        transaction_factory(12, amount=12, type=TypeTransaction.deposit)


def test_create_with_wrong_type(db: Database, accounts, transaction_factory):
    with pytest.raises(TransactionError, match="NotATransactionType"):
        transaction_factory(1, amount=12, type="deposit2")


def test_create_with_amount_as_word(db: Database, accounts, transaction_factory):
    with pytest.raises(TypeError):
        transaction_factory(1, amount="test", type=TypeTransaction.deposit)
