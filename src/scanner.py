import datetime
from dataclasses import dataclass
from typing import Literal, Union
import sqlalchemy as sa
from db import engine, news_tbl

@dataclass
class Change:
    change_type: Literal["+", "-", "~"]  # added, removed or updated
    text: str

JSONType = Union[str, int, float, bool, None, dict[str, 'JSONType'], list['JSONType']]

class NewsScannerInterface:
    org = None  # Must override
    url = None  # Must override
    connector = engine.connect

    def __init__(self, **kwargs):
        if kwargs.get('connector'):
            self.connector = kwargs['connector']

    # Must override.
    def detect_changes(self) -> list[Change]:
        raise NotImplementedError()

    def get_last_content(self) -> JSONType:
        assert self.org
        with self.connector() as conn:
            stmt = sa.select([news_tbl.c.content]).where(news_tbl.c.org == self.org).order_by(sa.desc(news_tbl.c.dt_fetched)).limit(1)
            content_result = conn.execute(stmt).all()
            content = content_result[0][0] if content_result else None
        return content

    def save_content(self, content: JSONType):
        assert self.org and self.url
        with self.connector() as conn:
            now = datetime.datetime.now()
            stmt = news_tbl.insert().values(org=self.org, dt_fetched=now, url=self.url, content=content)
            conn.execute(stmt)
            conn.commit()
