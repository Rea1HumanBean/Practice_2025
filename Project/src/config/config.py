import os

from sqlalchemy.engine import URL
from dotenv import load_dotenv

load_dotenv()

port_str = os.getenv("DB_PORT")
port = int(port_str) if port_str and port_str.isdigit() else None


DATABASE_URL = URL.create(
    drivername=str(os.getenv("DB_DRIVER")),
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=port,
    database=os.getenv("DB_NAME"),
)

TIME_PERIOD_HOURS = 1
