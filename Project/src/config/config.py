from ..db.sqlite_repository import SQLiteMedicationRepository
from ..utils.medication_schedule import MedicationSchedule


db_path = "data/medications.db"


repository = SQLiteMedicationRepository(db_path)
schedule_service = MedicationSchedule(repository)


TIME_PERIOD_HOURS = 1
