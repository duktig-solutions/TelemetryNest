from typing import List, Union
from ..models import kpis as kpi_model

def fetch_last_kpis(kpi: Union[str, None], days: Union[int, None]):
    model = kpi_model.KPIs()
    return model.fetch_last_days(kpi, days)

def insert_kpis_batch(kpis: List[kpi_model.Kpi]):
    model = kpi_model.KPIs()
    model.insert_big_batch(kpis)
