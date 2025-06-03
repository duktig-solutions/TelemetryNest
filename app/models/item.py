from pydantic import BaseModel
from app.lib.CassConn import CassConn
from typing import Union


class Item(BaseModel):
    last_update_timestamp: Union[str, None] = None
    user_id: Union[str, None] = None
    item_id: int
    item_count: int
    description: Union[str, None] = None
    price: float


class ItemUpdate(BaseModel):
    item_count: int
    description: str
    price: float


class ItemModel:
    conn = ''
    table = 'products'

    def __init__(self) -> None:
        self.conn = CassConn()

    def create(self, item: Item):
        self.conn.insert(self.table, item)

    def update(self, item: ItemUpdate, where):
        self.conn.update(self.table, item, where)

    def get_one_by_where(self, where):
        return self.conn.get_one(self.table, where)

    def get_all_by_where(self, where):
        return self.conn.get_all(self.table, where)
