from src.main import App
from src.models import TypeTransaction


def main():
    app = App()

    acc = app.create_account(balance=12)
    app.action(acc, type=TypeTransaction.deposit, amount=10)

    # acc1 = Account(1)
    # acc2 = Account(2)
    # app.action(acc2, type=TypeTransaction.transfer, amount=10, target=acc1)


if __name__ == "__main__":
    main()
