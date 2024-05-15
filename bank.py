from sqlalchemy import bindparam
from classes.errors import TransactionError
from database import Database

from models import AccountsModel, TransactionsModel, TypeTransaction


class Bank:
    def __init__(self) -> None:
        self.db = Database()
        self.session = self.db.session

    def commit(self):
        self.session.commit()

    def close(self):
        self.session.close()


class Account(Bank):
    def __init__(self) -> None:
        super().__init__()
        self.account = AccountsModel()

    def refresh(self, account_id: int) -> AccountsModel:
        return (
            self.db.session.query(AccountsModel)
            .filter(AccountsModel.account_id == bindparam("account_id", self.account_id))
            .one()
        )

    def create(self, balance: float):
        acc = AccountsModel(balance=balance)
        self.session.add(AccountsModel(balance=balance))
        self.session.flush()
        self.commit()
        return acc

    def update(self, id: int, balance: float):
        self.session.query(AccountsModel).filter(AccountsModel.account_id == id).update(
            {AccountsModel.balance: AccountsModel.balance + balance}
        )
        self.commit()

    def delete(self, id: int):
        self.session.query(AccountsModel).filter(
            AccountsModel.account_id == id
        ).delete()
        self.commit()


class Transaction(Bank):
    def check_account(self, id: int) -> bool:
        return (
            self.session.query(AccountsModel)
            .filter(AccountsModel.account_id == bindparam("account_id", id))
            .one_or_none()
            is not None
        )

    def create(self, account_id: int, amount: float, type: TypeTransaction):
        if not self.check_account(account_id):
            raise TransactionError("NoAccountAttach")

        if not TypeTransaction.has_value(type):
            raise TransactionError("NotATransactionType")

        self.session.add(
            TransactionsModel(account_id=account_id, amount=amount, type=type)
        )
        self.commit()
