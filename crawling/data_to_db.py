import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.types import Integer, Text, String, DateTime, VARCHAR
from registered_car import registrated_car_crawler

def car_data_to_db(**kwargs):
    data = registrated_car_crawler()
    db_url = f'postgresql+psycopg2://{kwargs.get('name')}:{kwargs.get('password')}@{kwargs.get('host')}:{kwargs.get('port')}/{kwargs.get('db_name')}'
    engine = create_engine(db_url)

    data.to_sql(
        'registererd_car',
        engine,
        dtype={
            'region': VARCHAR(5),
            'count': Integer,
            'type': VARCHAR(5),
            'usage': VARCHAR(5),
            'date': DateTime,
        }
    )
