from sqlalchemy.engine import URL

DATABASE_URL = URL.create(
    drivername="postgresql+asyncpg",
    username="postgres",
    password="2191",
    host="localhost",
    port=5432,
    database="schedule_medications"
)

LOG_LVL = 'INFO'

TIME_PERIOD_HOURS = 1
