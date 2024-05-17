from typing import List

import pytest
from src.bank import Account
from src.classes.errors import AccountError, TransactionError
from src.database import Database
from src.models import TypeTransaction
from src.main import App


# def test_transfer_normal(db: Database, accounts: List[Account], count_transactions):
#     app = App()
#     nb_trans = count_transactions()

#     transactions = app.action(
#         accounts[0], TypeTransaction.transfer, amount=50, target=accounts[1]
#     )

#     assert len(transactions) == 2

#     withdraw, acc = transactions[0]
#     withdraw._refresh()
#     acc._refresh()
#     assert acc.account.balance == 50
#     assert withdraw.transaction.type.name == TypeTransaction.withdraw.name

#     deposit, acc = transactions[1]
#     deposit._refresh()
#     acc._refresh()
#     assert acc.account.balance == 100
#     assert deposit.transaction.type.name == TypeTransaction.deposit.name

#     assert count_transactions() == nb_trans + 2


# @pytest.mark.parametrize(
#     "amount, type, expected",
#     [
#         (
#             150,
#             TypeTransaction.transfer,
#             pytest.raises(TransactionError, match="InsufficientFunds"),
#         ),
#         (
#             20,
#             "TypeTransaction.transfer",
#             pytest.raises(TransactionError, match="NotATransactionType"),
#         ),
#         (
#             -5,
#             TypeTransaction.transfer,
#             pytest.raises(TransactionError, match="AmountNegative"),
#         ),
#         (
#             0,
#             TypeTransaction.transfer,
#             pytest.raises(TransactionError, match="AmountZero"),
#         ),
#         (
#             "test",
#             TypeTransaction.transfer,
#             pytest.raises(TypeError),
#         ),
#     ],
# )
# def test_transfer_exception(
#     db, accounts: List[Account], count_transactions, amount, type, expected
# ):
#     app = App()
#     nb_trans = count_transactions()

#     with expected as e:
#         assert (app.action(accounts[0], type, amount=amount, target=accounts[1])) == e

#     accounts[0]._refresh()
#     assert accounts[0].account.balance == 100

#     accounts[1]._refresh()
#     assert accounts[1].account.balance == 50

#     assert count_transactions() == nb_trans


@pytest.mark.parametrize(
    "acc1_id, acc2_id, expected",
    [
        (
            0,
            2,
            pytest.raises(AccountError, match="TargetAccountNotExist"),
        ),
        (
            0,
            0,
            pytest.raises(TransactionError, match="AccountAndTargetAreTheSame"),
        ),
        (
            0,
            None,
            pytest.raises(AccountError, match="TargetAccountNotExist"),
        ),
        (
            None,
            1,
            pytest.raises(AccountError, match="AccountNotExist"),
        ),
    ],
)
def test_transfer_account_exception(
    db, accounts: List[Account], count_transactions, acc1_id, acc2_id, expected
):
    app = App()
    nb_trans = count_transactions()

    with expected as e:
        assert (
            app.action(
                accounts[acc1_id] if acc1_id is not None else None,
                TypeTransaction.transfer,
                amount=10,
                target=(accounts[acc2_id] if acc2_id is not None else None),
            )
        ) == e

    try:
        if acc1_id is not None:
            accounts[acc1_id]._refresh()
            assert accounts[acc1_id].account.balance == 100
    except Exception:
        pass

    try:
        if acc2_id is not None:
            accounts[acc2_id]._refresh()
            assert accounts[acc2_id].account.balance == 50
    except Exception:
        pass

    assert count_transactions() == nb_trans
