from pydantic import BaseModel, field_validator, ConfigDict
from app.lib.CassConn import CassConn
from datetime import datetime, timedelta
from cassandra.query import BatchStatement, ConsistencyLevel
import warnings

warnings.simplefilter("error")

class MyBaseModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed = True)

class PredictedAlarm(MyBaseModel):
    operator_id: int
    date_prediction: str
    alert_sign: str
    element_id: int
    fault_description: str
    fault_id: int
    fault_name: str
    object: str
    probability: float
    severity: str

    @field_validator('alert_sign')
    def validate_alert_sign(cls, value):
        if value != 'YES' and value != 'NO':
            raise ValueError(f"Can be 'Yes' or 'NO'")

        return value

    @field_validator('severity')
    def validate_severity(cls, value):
        if value != 'CRITICAL' and value != 'MAJOR' and value != 'MINOR' and value != 'INFORMATION':
            raise ValueError(f"Can be 'CRITICAL', 'MAJOR', 'MINOR' or 'INFORMATION'")

        return value


class PredictedAlarms:
    conn = ''
    table = 'predicted_alarms'

    def __init__(self) -> None:
        self.conn = CassConn()

    def insert_big_batch(self, predicted_alarms):

        insert_predicted_alarm = self.conn.session.prepare(
            'INSERT INTO predicted_alarms (operator_id, date_prediction, alert_sign, element_id, fault_description, '
            'fault_id, fault_name, object, probability, severity) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        )

        data = []

        for row in predicted_alarms:
            data.append(vars(row))

            if len(data) >= 300:

                batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)

                for rec in data:
                    try:
                        rec['date_prediction'] = datetime.strptime(rec['date_prediction'], "%Y-%m-%d %H:%M:%S")
                        batch.add(insert_predicted_alarm, (
                            row['operator_id'], row['date_prediction'], row['alert_sign'],
                            row['element_id'], row['fault_description'], row['fault_id'],
                            row['fault_name'], row['object'], row['probability'], row['severity']
                        ))
                    except Exception as e:
                        print('The cassandra error: {}'.format(e))

                self.conn.session.execute(batch)
                data = []

        if len(data) > 0:

            batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)

            for rec in data:
                try:
                    rec['date_prediction'] = datetime.strptime(rec['date_prediction'], "%Y-%m-%d %H:%M:%S")
                    batch.add(insert_predicted_alarm, (
                        rec['operator_id'], rec['date_prediction'], rec['alert_sign'],
                        rec['element_id'], rec['fault_description'], rec['fault_id'],
                        rec['fault_name'], rec['object'], rec['probability'], rec['severity']
                    ))
                except Exception as e:
                    print('The cassandra error: {}'.format(e))

            self.conn.session.execute(batch)

    def fetch_last_days(self, days):

        # Get the current date and time
        current_date = datetime.now()

        # Calculate the date 7 days before
        days_before = current_date - timedelta(days=days)

        # Convert the date to a string
        date_string = days_before.strftime('%Y-%m-%d %H:%M:%S')

        print(date_string)

        return self.conn.get_by_query(
            "SELECT * FROM predicted_alarms " +
            "WHERE date_prediction >= %s " +
            "", [date_string])
    # order by date_prediction
