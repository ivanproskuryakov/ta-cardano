import pandas as pd

from sqlalchemy.orm import Session
from src.connector.db_connector import db_connect


class BaseRepository():
    connection = None
    entity = None

    def __init__(self):
        self.connection = db_connect()

    def find_all(self):
        session = Session(bind=self.connection)

        sql = session.query(self.entity) \
            .order_by(self.entity.id.asc()) \
            .statement

        df = pd.read_sql(
            sql=sql,
            con=self.connection
        )

        return df
