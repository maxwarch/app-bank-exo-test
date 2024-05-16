from sqlalchemy import bindparam, insert, update
from sqlalchemy.orm.exc import NoResultFound
from src.classes.errors import TransactionError
from src.database import Database

from src.models import AccountsModel, TransactionsModel, TypeTransaction


class ObjData:
    pass


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
        self.account = ObjData()
        if account_id is not None:
            self.account.account_id = account_id
            self._refresh()

    def _refresh(self):
        try:
            self.account = self.session.get_one(
                AccountsModel,
                ident=self.account.account_id,
                bind_arguments={"account_id": self.account.account_id},
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
        self.transaction = ObjData()
        if transaction_id is not None:
            self.transaction.transaction_id = transaction_id
            self._refresh()

    def _refresh(self):
        try:
            self.transaction = self.session.get_one(
                TransactionsModel,
                ident=self.transaction.transaction_id,
                bind_arguments={"transaction_id": self.transaction.transaction_id},
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

        type_name = type.name if isinstance(type, TypeTransaction) else None

        if type_name in TypeTransaction or type_name is None:
            raise TransactionError("NotATransactionType")

        if amount == 0:
            raise TransactionError("AmountZero")

        if amount < 0:
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
