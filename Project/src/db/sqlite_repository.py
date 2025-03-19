from abc import ABC
from datetime import datetime, time
from typing import List
import sqlite3
import logging
import json

from src.utils.interfaces import IMedicationRepository
from src.utils.user_return_schedule_data import UserReturnScheduleData

logging.basicConfig(level=logging.DEBUG)


class SQLiteMedicationRepository(IMedicationRepository, ABC):

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._conn = None
        self._cursor = None

        self._connect()
        self.__create_tables()

    def __del__(self):
        if self._conn:
            self._conn.close()
            self._conn = None
            self._cursor = None

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__del__()

    def _connect(self):
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._cursor = self._conn.cursor()

    def __create_tables(self) -> None:
        self._cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT
        )"""
        )

        self._cursor.execute(
            """CREATE TABLE IF NOT EXISTS medication (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            drugs_name TEXT UNIQUE
        )"""
        )
        self._conn.commit()

    def _add_medication(self, name_medication) -> None:
        try:
            self._cursor.execute(
                "INSERT OR IGNORE INTO medication (drugs_name) VALUES (?)",
                (name_medication,),
            )
            self._conn.commit()
        except Exception as e:
            logging.error(e)
            self._conn.rollback()
            raise

    def add_schedule_taking_medication(
        self,
        user_id: int,
        name_pills: str,
        first_day: datetime,
        last_day: datetime | None,
        daily_schedule: list[time],
    ) -> None:
        try:
            medication_id = self._get_medication_id(name_pills)
            daily_schedule_str = json.dumps(daily_schedule, default=str)

            if not medication_id:
                self._add_medication(name_pills)
                medication_id = self._get_medication_id(name_pills)

            if not self.get_user(user_id):
                self._add_user(user_id)

            table_name = f"user_{user_id}_medications"
            self._create_user_schedule_table(table_name)

            logging.info(
                f"Добавление расписания {datetime.today().strftime('%d.%m.%Y %H:%M')} "
                f": user_id={user_id}, "
                f"name_pills={name_pills}, "
                f"first_day={first_day}, "
                f"last_day={last_day}, "
                f"daily_schedule={daily_schedule}"
            )

            self._cursor.execute(
                f"""
                INSERT INTO {table_name} (user_id, medication_id, first_day, last_day, daily_schedule)
                VALUES (?, ?, ?, ?, ?)""",
                (user_id, medication_id, first_day, last_day, daily_schedule_str),
            )
            self._conn.commit()
        except Exception as e:
            logging.error(f"Ошибка при добавлении расписания: {e}")
            self._conn.rollback()
            raise

    def _create_user_schedule_table(self, table_name: str) -> None:
        try:
            self._cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_day TEXT,
                    last_day TEXT,
                    user_id INTEGER,
                    medication_id INTEGER,
                    daily_schedule TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (medication_id) REFERENCES medication(id)
                )
            """
            )
            self._conn.commit()

        except Exception as e:
            logging.error(f"Ошибка при создании таблицы {table_name}: {e}")
            self._conn.rollback()
            raise

    def get_user_schedule(self, user_id, schedule_id) -> UserReturnScheduleData | None:
        table_name = f"user_{user_id}_medications"

        try:
            self._cursor.execute(
                f"""
                SELECT medication.drugs_name AS name_medication, 
                       {table_name}.daily_schedule, 
                       {table_name}.first_day, 
                       {table_name}.last_day
                FROM {table_name}
                JOIN medication ON {table_name}.medication_id = medication.id
                WHERE {table_name}.id = ?""",
                (schedule_id,),
            )

            row = self._cursor.fetchone()

            if row:
                columns = ["name_medication", "daily_schedule", "first_day", "last_day"]

                row_dict = dict(zip(columns, row))

                result = UserReturnScheduleData(**row_dict)
                return result

            return None
        except Exception as e:
            logging.error(e)
            self._conn.rollback()
            raise

    def get_user_id_schedule(self, user_id: int) -> int | None:
        table_name = f"user_{user_id}_medications"
        try:
            self._cursor.execute(f"SELECT id FROM {table_name}")
            result = self._cursor.fetchall()
            return result if result else None
        except Exception as e:
            logging.error(f"Error fetching schedule IDs for user {user_id}: {e}")
            raise

    def get_user_next_takings(self, user_id: int) -> List[UserReturnScheduleData]:
        table_name = f"user_{user_id}_medications"
        results = []

        try:
            self._cursor.execute(
                f"""
                SELECT medication.drugs_name AS name_medication, 
                       {table_name}.daily_schedule, 
                       {table_name}.first_day, 
                       {table_name}.last_day
                FROM {table_name}
                JOIN medication ON {table_name}.medication_id = medication.id
                WHERE {table_name}.user_id = ?""",
                (user_id,),
            )

            rows = self._cursor.fetchall()

            if rows:
                columns = ["name_medication", "daily_schedule", "first_day", "last_day"]

                for row in rows:
                    row_dict = dict(zip(columns, row))

                    result = UserReturnScheduleData(**row_dict)
                    results.append(result)
            return results

        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            self._conn.rollback()
            raise

    def _get_medication_id(self, name_pills: str) -> int | None:
        self._cursor.execute(
            """SELECT id FROM medication WHERE drugs_name = ?""", (name_pills,)
        )
        result = self._cursor.fetchone()
        return result[0] if result else None

    def get_user(self, user_id) -> bool:
        self._cursor.execute("SELECT COUNT(*) FROM users WHERE id  = ?", (user_id,))
        result = self._cursor.fetchone()
        return result[0] > 0

    def _add_user(self, user_id) -> None:
        self._cursor.execute("INSERT INTO users VALUES (?)", (user_id,))
        self._conn.commit()
