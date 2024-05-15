from sqlalchemy import bindparam
from bank import Account
from database import Database
from models import AccountsModel, TypeTransaction
from main import App


def user(db):
    return (
        db.session.query(AccountsModel)
        .filter(AccountsModel.account_id == bindparam("account_id", 1))
        .one()
    )


def test_deposit_normal(db: Database, seed_user: Account, transaction_factory):
    app = App()
    app.deposit(seed_user, 120, TypeTransaction.deposit)

    seed_user = user()
