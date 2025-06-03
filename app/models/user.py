from pydantic import BaseModel, Field, EmailStr, ConfigDict
from app.lib.CassConn import CassConn
import warnings

warnings.simplefilter("error")

class UserSchema(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "name": "The full name of the user",
                "email": "email@example.com",
                "password": "weakpassword"
            }
        }
    )

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "email": "email@example.com",
                "password": "weakpassword"
            }
        }
    )

class UserTest:
    email: str = ""
    password: str = ""


class User:
    conn = ''
    table = 'Users'

    def __init__(self) -> None:
        self.conn = CassConn()

    def fetch_user_by_where(self, where):
        return self.conn.get_one(self.table, where)

    def create(self, user: UserSchema):
        self.conn.insert(self.table, user)

    def update(self, user: UserSchema, where):
        self.conn.update(self.table, user, where)

    def get_all_by_where(self, where):
        return self.conn.get_all(self.table, where)
