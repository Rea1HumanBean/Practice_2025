from service.random_developers import DevelopersData, Developer
from db.db_dev import DB


def fill_db_dev(count: int) -> None:
    for _ in range(count + 1):
        dev: Developer = DevelopersData.get_random_dev()
        DB().add_dev_to_db(dev)
