from datetime import date
import logging
import pandas as pd
from sqlalchemy import Engine, create_engine


class DataLoader(object):
    def __init__(self, engine: Engine = None):
        self._logger = logging.getLogger(f"upload_to_database.DataLoader")
        self._engine = engine

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, value):
        self._logger = value

    @property
    def engine(self):
        return self._engine

    @engine.setter
    def engine(self, value):
        self._engine = value

    def set_mysql_engine(self, user_name, password, host, port, database) -> bool:
        try:
            engine = create_engine(
                f"mysql+mysqlconnector://{user_name}:{password}@{host}:{port}/{database}"
            )
            self._engine = engine

            return True
        except Exception as e:
            print(e)
            self._logger.exception(e)
            return False

    def upload_json_to_db(self, json_file_path, table_name, if_exists="replace") -> bool:
        try:
            # DataFrame 생성
            df = pd.read_json(json_file_path)

            # DataFrame을 MySQL 데이터베이스의 테이블로 저장
            df.to_sql(name=table_name, con=self.engine, if_exists=if_exists, index=False)

            return True
        except Exception as e:
            print(e)
            self._logger.exception(e)
            return False


if __name__ == "__main__":
    # MySQL 데이터베이스 연결 정보
    json_file_path = r".\product\results\tft_{table}s_{date}.json"
    username = "root"
    password = ""
    host = "localhost"
    port = "3306"
    database = "tftdb"

    date = str(date.today().strftime("%Y%m%d"))

    data_loader = DataLoader()
    data_loader.set_mysql_engine(username, password, host, port, database)

    # DataFrame을 MySQL 데이터베이스의 테이블로 저장
    table_names =[
        "player",
        "player_statistic",
        "matche",
        "match_player",
        "match_augment",
        "match_trait",
        "match_unit",
    ]
    select_tables = [table_names[1]]
    for table in select_tables:
        try:
           data_loader.upload_json_to_db(json_file_path.format(table=table, date=date), table, if_exists="append")
        except Exception as e:
            print(e)
