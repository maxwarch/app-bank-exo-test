import pytest
from sqlalchemy import bindparam

from models import AccountsModel


@pytest.fixture
def get_account_factory(db):
    def get_account(account_id):
        return (
            db.session.query(AccountsModel)
            .filter(AccountsModel.account_id == bindparam("account_id", account_id))
            .one()
        )

    return get_account
