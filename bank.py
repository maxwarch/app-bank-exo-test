from sqlalchemy import bindparam, insert, update
from sqlalchemy.orm.exc import NoResultFound
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
    def __init__(self, account_id: int = None) -> None:
        super().__init__()
        self.account = None
        if account_id is not None:
            self._refresh(account_id)

    def _refresh(self, account_id: int) -> AccountsModel:
        try:
            self.account = self.session.get_one(
                AccountsModel,
                ident=account_id,
                bind_arguments={"account_id": account_id},
            )
        except NoResultFound:
            self.account = None

    def create(self, balance: float) -> AccountsModel:
        query = insert(AccountsModel).values(balance=balance).returning(AccountsModel)

        with self.db.engine.connect() as conn:
            acc = conn.execute(query)
            self.account = acc.one_or_none()
            conn.commit()

    def update(self, balance: float):
        query = (
            update(AccountsModel)
            .where(AccountsModel.account_id == self.account.account_id)
            .values(balance=AccountsModel.balance + balance)
            .returning(AccountsModel)
        )
        with self.db.engine.connect() as conn:
            acc = conn.execute(query)
            self.account = acc.one_or_none()
            conn.commit()

    def delete(self):
        self.session.query(AccountsModel).filter(
            AccountsModel.account_id == self.account.account_id
        ).delete()
        self.commit()


class Transaction(Bank):
    def __init__(self, transaction_id: int = None) -> None:
        super().__init__()
        self.transaction = None
        if transaction_id is not None:
            self._refresh(transaction_id)

    def _refresh(self, transaction_id: int):
        try:
            self.transaction = self.session.get_one(
                TransactionsModel,
                ident=transaction_id,
                bind_arguments={"transaction_id": transaction_id},
            )
        except NoResultFound:
            self.transaction = None

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

        if not (amount > 0):
            raise TransactionError("AmountNegative")

        query = (
            insert(TransactionsModel)
            .values(account_id=account_id, amount=amount, type=type)
            .returning(TransactionsModel)
        )

        with self.db.engine.connect() as conn:
            trans = conn.execute(query)
            self.transaction = trans.one_or_none()
            conn.commit()
