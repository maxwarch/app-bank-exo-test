import pytest

from src.bank import Transaction
from src.models import TransactionsModel


@pytest.fixture
def transaction_factory():
    def create_transaction(account_id, amount, type):
        trans = Transaction()
        trans.create(account_id, amount, type)
        return trans.transaction

    return create_transaction


@pytest.fixture
def count_transactions(db):
    def count():
        return db.session.query(TransactionsModel).count()

    return count
