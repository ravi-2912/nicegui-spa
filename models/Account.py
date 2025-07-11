import os
from enum import Enum
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Boolean,
    Float,
    Enum as SQLAlchemyEnum,
)
from sqlalchemy.orm import relationship
from cryptography.fernet import Fernet
from dotenv import load_dotenv

from db.base import Base
from models.enums import PlatformType, AccountType, CurrencyType

load_dotenv()

ENCRYPTION_KEY = os.getenv("PASSWORD_ENCRYPTION_KEY")
if not ENCRYPTION_KEY:
    raise ValueError("ENCRYPTION_KEY not set in environment or .env file.")
fernet = Fernet(ENCRYPTION_KEY.encode())


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    login = Column(String, nullable=False)
    __password_encrypted = Column("password", String, nullable=False)
    type = Column(SQLAlchemyEnum(AccountType), nullable=False)
    platform = Column(SQLAlchemyEnum(PlatformType), nullable=False)
    path = Column(String, nullable=False)
    currency = Column(SQLAlchemyEnum(CurrencyType), nullable=True)
    starting_balance = Column(Float, nullable=True)
    current_balance = Column(Float, nullable=True)

    # Mt5 specific fields
    portable = Column(Boolean, nullable=False, default=True)
    server = Column(String, nullable=False)

    broker_id = Column(Integer, ForeignKey("brokers.id"), nullable=True)
    broker = relationship("Broker", back_populates="accounts")

    instruments = relationship("Instrument", backref="account")

    trades = relationship("Trade", back_populates="account")

    archived = Column(Boolean, nullable=False, default=False)

    is_valid = Column(Boolean, nullable=False, default=False)

    def __init__(self, **kwargs):
        password = kwargs.pop("password", None)
        super().__init__(**kwargs)
        if password is not None:
            self.password = password

    @property
    def password(self):
        if self.__password_encrypted:
            return fernet.decrypt(self.__password_encrypted.encode()).decode()
        return None

    @password.setter
    def password(self, value: str):
        if value:
            self.__password_encrypted = fernet.encrypt(value.encode()).decode()
        else:
            self.__password_encrypted = None
