from bank import Account, Transaction, TypeTransaction
from classes.errors import TransactionError


class App:
    def __init__(self) -> None:
        pass

    def create_account(self, **kwargs):
        acc = Account()
        acc.create(**kwargs)
        return acc

    def action(self, account: Account, type: TypeTransaction, **kwargs):
        if type == TypeTransaction.deposit:
            return self.__deposit(account, **kwargs)

        return account

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
