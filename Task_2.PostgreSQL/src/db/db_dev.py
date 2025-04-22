import psycopg

from model.model_Developer import Developer
from conf.conf_db import DB_SETTINGS


class DB:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DB, cls).__new__(cls)
            cls._instance.conn = psycopg.connect(**DB_SETTINGS)
        return cls._instance

    def add_dev_to_db(self, dev: Developer) -> None:
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO developers(name, department, geolocation, last_known_ip, is_available)
                    VALUES(%s, %s, POINT(%s, %s), %s, %s)
                    """,
                    (
                        dev.full_name,
                        dev.department,
                        dev.geolocation[0],
                        dev.geolocation[1],
                        str(dev.last_known_ip),
                        dev.is_available

                    )
                )
            self.conn.commit()
        except Exception as e:
            print(f"[ERROR] {e}")