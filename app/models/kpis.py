from pydantic import BaseModel, field_validator, ConfigDict
from app.lib.CassConn import CassConn
from typing import Union
from datetime import datetime, timedelta
from cassandra.query import BatchStatement, ConsistencyLevel

import warnings

warnings.simplefilter("error")

class MyBaseModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed = True)


class Kpi(MyBaseModel):
    kpi_name: str
    timestamp: str
    # value: DoubleType
    value: float
    # value: Annotated[float, DoubleType]
    tags: Union[str, None] = None

    @field_validator('value')
    def validate_value(cls, value):

        # Add your timestamp validation here if needed
        return float(value)


class KPIs:
    conn = ''
    table = 'kpi_data'

    def __init__(self) -> None:
        self.conn = CassConn()

    def insert_batch(self, kpis):

        insert_kpi = self.conn.session.prepare(
            'INSERT INTO kpis (kpi_name, timestamp, tags, value) VALUES (?, ?, ?, ?)'
        )

        data = []
        for row in kpis:
            data.append(vars(row))

        batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
        for row in data:
            try:
                row['timestamp'] = datetime.strptime(row['timestamp'], "%Y-%m-%d %H:%M:%S")
                batch.add(insert_kpi, (row['kpi_name'], row['timestamp'], row['tags'], row['value']))
            except Exception as e:
                print('The cassandra error: {}'.format(e))

        self.conn.session.execute(batch)

    def insert_big_batch(self, kpis):

        insert_kpi = self.conn.session.prepare(
            'INSERT INTO kpis (kpi_name, timestamp, tags, value) VALUES (?, ?, ?, ?)'
        )

        data = []

        for row in kpis:
            data.append(vars(row))

            if len(data) >= 300:

                batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)

                for rec in data:
                    try:
                        rec['timestamp'] = datetime.strptime(rec['timestamp'], "%Y-%m-%d %H:%M:%S")
                        batch.add(insert_kpi, (rec['kpi_name'], rec['timestamp'], rec['tags'], rec['value']))
                    except Exception as e:
                        print('The cassandra error: {}'.format(e))

                self.conn.session.execute(batch)
                data = []

        if len(data) > 0:

            batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)

            for rec in data:
                try:
                    rec['timestamp'] = datetime.strptime(rec['timestamp'], "%Y-%m-%d %H:%M:%S")
                    batch.add(insert_kpi, (rec['kpi_name'], rec['timestamp'], rec['tags'], rec['value']))
                except Exception as e:
                    print('The cassandra error: {}'.format(e))

            self.conn.session.execute(batch)

    def fetch_last_days(self, kpi, days):

        # Get the current date and time
        current_date = datetime.now()

        # Calculate the date 7 days before
        seven_days_before = current_date - timedelta(days=days)

        # Convert the date to a string
        date_string = seven_days_before.strftime('%Y-%m-%d %H:%M:%S')

        return self.conn.get_by_query(
            "SELECT * FROM kpis " +
            "WHERE kpi_name = %s " +
            "AND timestamp >= %s " +
            "order by timestamp", [kpi, date_string])

    def fetch_last_(self):
        return self.conn.get_by_query(
            "SELECT * FROM kpis " +
            "WHERE kpi_name = 'kpi1' " +
            "AND timestamp >= '2024-06-01 00:00:00' " +
            "order by timestamp", [])
