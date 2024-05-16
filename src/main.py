from src.bank import Account, Transaction, TypeTransaction
from src.classes.errors import TransactionError


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

        if type == TypeTransaction.withdraw:
            return self.__withdraw(account, **kwargs)

        if type == TypeTransaction.transfer:
            return self.__transfer(account, **kwargs)

        return account

    def __transfer(self, account: Account, target: Account, amount: float):
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


if __name__ == "__main__":
    app = App()

    app.create_account(amount=12)
