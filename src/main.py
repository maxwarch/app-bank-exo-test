from src.bank import Account, Transaction, TypeTransaction
from src.classes.errors import AccountError, TransactionError
from src.models import AccountsModel


class App:
    def __init__(self) -> None:
        pass

    def create_account(self, balance: float):
        acc = Account()
        acc.create(balance)
        return acc

    def action(self, account: Account, type: TypeTransaction, **kwargs):
        if type == TypeTransaction.deposit:
            return self.__deposit(account, **kwargs)

        if type == TypeTransaction.withdraw:
            return self.__withdraw(account, **kwargs)

        if type == TypeTransaction.transfer:
            return self.__transfer(account, **kwargs)

        raise TransactionError("NotATransactionType")

    def get_balance(self, account: Account) -> AccountsModel:
        account._refresh()
        return account.account

    def __transfer(
        self, account: Account = None, target: Account = None, amount: float = 0
    ):
        if target is None or (
            hasattr(target, "is_exist") and target.is_exist() is False
        ):
            raise AccountError("TargetAccountNotExist")

        if account is None or (
            hasattr(account, "is_exist") and account.is_exist() is False
        ):
            raise AccountError("AccountNotExist")

        if account == target:
            raise TransactionError("AccountAndTargetAreTheSame")

        withdraw, account = self.__withdraw(account, amount)
        deposit, target = self.__deposit(target, amount)
        return [(withdraw, account), (deposit, target)]

    def __deposit(self, account: Account, amount: float):
        account_data = account.account

        transaction = Transaction()
        transaction.create(
            account_id=account_data.account_id,
            amount=amount,
            type=TypeTransaction.deposit,
        )

        account.update(amount)

        return (transaction, account)

    def __withdraw(self, account: Account, amount: float):
        account_data = account.account

        if (account_data.balance - amount) < 0:
            raise TransactionError("InsufficientFunds")

        transaction = Transaction()
        transaction.create(
            account_id=account_data.account_id,
            amount=amount,
            type=TypeTransaction.withdraw,
        )

        account.update(-amount)

        return (transaction, account)
