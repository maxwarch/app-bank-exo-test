from bank import Account, Transaction, TypeTransaction
from classes.errors import TransactionError


class App:
    def __init__(self) -> None:
        pass

    def deposit(self, account: Account, amount: float, type: TypeTransaction):
        if account.balance < 0 and amount > 0:
            raise TransactionError("InsuffisantAmout")

        return Transaction().create(
            account_id=account.account_id, amount=amount, type=type
        )


# if __name__ == "__main__":
#     pass
