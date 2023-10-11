import datetime
from sqlalchemy import MetaData, Table, TIMESTAMP, Column, Integer, String

metadata = MetaData()

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, nullable=False),
    Column("password", String, nullable=False),
    Column("mail", String, nullable=False),
    Column("registration_date", TIMESTAMP, default=datetime.UTC),
    Column("role", Integer, nullable=False)
)

