from datetime import timedelta
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import (
    Float,
    Column,
    String,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    Enum as SQLAlchemyEnum,
)
from sqlalchemy.orm import relationship

from db.base import Base
from models.enums import (
    OrderType,
    DirectionType,
    ExitReasonType,
    TradeStatusType,
    TradingMindState,
    TradeSuccessProbabilityType,
)


class Trade(Base):
    __tablename__ = "trades"
    id = Column(Integer, primary_key=True)
    trade_id = Column(String, nullable=False)

    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    account = relationship("Account", back_populates="trades")
    symbol_id = Column(String, ForeignKey("symbols.id"), nullable=False)
    symbol = relationship("Symbol", back_populates="trades")
    instrument_id = Column(Integer, ForeignKey("instruments.id"), nullable=False)
    instrument = relationship("Instrument", back_populates="trades")
    strategy_id = Column(Integer, ForeignKey("strategies.id"), nullable=True)
    strategy = relationship("Strategy", back_populates="trades")

    status = Column(SQLAlchemyEnum(TradeStatusType), nullable=False)

    risk = Column(Float, nullable=False)

    direction = Column(SQLAlchemyEnum(DirectionType), nullable=False)
    order_type = Column(SQLAlchemyEnum(OrderType), nullable=False)
    lots = Column(Float, nullable=False)
    units = Column(Integer, nullable=False)
    entry_price = Column(Float, nullable=False)
    stop_loss_pips = Column(Float, nullable=True)
    take_profit_pips = Column(Float, nullable=True)
    stop_loss_price = Column(Float, nullable=True)
    take_profit_price = Column(Float, nullable=True)
    open_time = Column(DateTime, nullable=False)
    exit_time = Column(DateTime, nullable=True)
    exit_price = Column(Float, nullable=True)

    probability = Column(SQLAlchemyEnum(TradeSuccessProbabilityType), nullable=False)
    mindstate = Column(SQLAlchemyEnum(TradingMindState), nullable=False)

    _duration_seconds = Column(Integer, nullable=True)
    tags = Column(String, nullable=True)
    reward_risk = Column(Float, nullable=True)
    exit_reason = Column(SQLAlchemyEnum(ExitReasonType), nullable=True)
    exit_reason_details = Column(String, nullable=True)
    # comments = Column(String, nullable=True)

    actual_pnl = Column(Float, nullable=True)
    actual_reward_risk = Column(Float, nullable=True)
    starting_balance = Column(Float, nullable=True)
    ending_balance = Column(Float, nullable=True)
    validated_from_backtest = Column(Boolean, nullable=False, default=False)

    # ids returned by the MT5 or CT5

    @hybrid_property
    def duration(self) -> timedelta:
        return timedelta(seconds=self._duration_seconds)

    @duration.setter
    def duration(self, value: timedelta):
        self._duration_seconds = int(value.total_seconds())

    @duration.expression
    def duration(cls):
        return cls._duration_seconds
