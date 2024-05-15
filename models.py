import enum
from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Float,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class AccountsModel(Base):
    __tablename__ = "accounts"
    account_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    balance = Column(Float)
    time_created = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    time_updated = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.current_timestamp(),
    )


class TypeTransaction(enum.Enum):
    deposit = 1
    withdraw = 2
    transfer = 3

    @classmethod
    def has_value(cls, value):
        if value in cls._member_names_:
            return True
        elif value in cls.__members__.values():
            return True
        else:
            return False


class TransactionsModel(Base):
    __tablename__ = "transactions"
    transaction_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    account_id = Column(
        Integer, ForeignKey("accounts.account_id"), index=True, nullable=False
    )
    amount = Column(Float, nullable=False)
    type = Column(Enum(TypeTransaction))
    time_created = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
