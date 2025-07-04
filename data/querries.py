from typing import List
import pandas as pd
from sqlalchemy import func

from models import Account, Broker, Instrument
from db.get_session import get_session
from utils.case_converter import snake_to_title


def get_all_items_from_account() -> pd.DataFrame:
    with get_session() as session:
        data = []
        query = (
            session.query(
                Account.id,
                Account.name,
                Account.login,
                Account.type,
                Account.platform,
                Account.path,
                Account.portable,
                Account.server,
                Account.currency,
                Account.balance,
                Account.archived,
                Broker.name.label("broker"),
                func.count(Instrument.id).label("instrument_count"),
            )
            .outerjoin(Broker, Account.broker_id == Broker.id)
            .outerjoin(Instrument, Instrument.account_id == Account.id)
            .group_by(Account.id, Broker.name)
        )
        accounts: List[Account] = query.all()
        for acc in accounts:
            data.append(
                {
                    "ID": acc.id,
                    "Name": acc.name,
                    "Broker": acc.broker,
                    "Currency": acc.currency,
                    "Login": acc.login,
                    "Type": acc.type,
                    "Platform": acc.platform,
                    "Server": acc.server,
                    "Path": acc.path,
                    "Instruments #": acc.instrument_count,
                    "Balance": acc.balance,
                    "Archived": acc.archived,
                }
            )
        df = pd.DataFrame(data)
        try:
            df.set_index(
                "ID",
                inplace=True,
            )
        except KeyError:
            pass
        return df


def get_all_items_from_table(table, fields) -> pd.DataFrame:
    with get_session() as session:
        items = session.query(table).all()
        data = []
        for item in items:
            data.append({**{snake_to_title(field): getattr(item, field) for field in fields}})
        df = pd.DataFrame(data)
        try:
            df.set_index(
                "ID",
                inplace=True,
            )
        except KeyError:
            pass
        return df
