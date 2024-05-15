import pytest

from bank import Transaction


@pytest.fixture
def transaction_factory():
    def create_transaction(account_id, amount, type):
        trans = Transaction()
        trans.create(account_id, amount, type)
        return trans.transaction

    return create_transaction
