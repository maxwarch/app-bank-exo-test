import pytest

from bank import Transaction


@pytest.fixture
def transaction_factory():
    def create_transaction(account_id, amount, type):
        return Transaction().create(account_id, amount, type)

    return create_transaction
