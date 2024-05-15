import pytest

from sqlalchemy.exc import StatementError
from classes.errors import TransactionError
from database import Database
from models import TypeTransaction


# un user est créé dans seed avec l'id 1
def test_create_no_user_attach(db: Database, seed_user, transaction_factory):
    with pytest.raises(TransactionError, match="NoAccountAttach"):
        transaction_factory(12, amount=12, type=TypeTransaction.deposit)


def test_create_with_wrong_type(db: Database, seed_user, transaction_factory):
    with pytest.raises(TransactionError, match="NotATransactionType"):
        transaction_factory(1, amount=12, type="deposit2")


def test_create_with_amount_as_word(db: Database, seed_user, transaction_factory):
    with pytest.raises(StatementError):
        transaction_factory(1, amount="test", type=TypeTransaction.deposit)
