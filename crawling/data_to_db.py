import psycopg2
from sqlalchemy import create_engine, text
from sqlalchemy.types import Integer, Text, String, DateTime, VARCHAR
from registered_car import registrated_car_crawler
from faq.kia_faq import kia_faq_crawl
from faq.hyundai_faq import hyundai_crawler
import pandas as pd


def create_db_engine(**kwargs):
    db_url = f'postgresql+psycopg2://{kwargs.get('name')}:{kwargs.get('password')}@{kwargs.get('host')}:{kwargs.get('port')}/{kwargs.get('db_name')}'
    engine = create_engine(db_url)
    return engine

def faq_data_to_db(**kwargs):
    kia_faq_df = kia_faq_crawl()
    hyundat_faq_df = hyundai_crawler()
    engine = create_db_engine(**kwargs)
    car_corp_df = pd.DataFrame({'id': [hyundat_faq_df['id'].values[0], kia_faq_df['id'].values[0]], 'corp_name': ['현대', '기아']})
    
    with engine.connect() as con:
        con.execute(text('DROP TABLE IF EXISTS car_corp CASCADE;'))
        con.execute(text('DROP TABLE IF EXISTS car_faq CASCADE;'))
        con.commit()

    car_corp_df.to_sql(
        'car_corp',
        engine,
        if_exists='replace',
        dtype={
            'id': VARCHAR(2),
            'corp_name': VARCHAR(10)
        }
    )
   
    faq_df = pd.concat([kia_faq_df, hyundat_faq_df])

    faq_df.to_sql(
        'car_faq',
        engine,
        if_exists='replace',
        dtype={
            'id': VARCHAR(2),
            'question': Text,
            'answer': Text
        }
    )
    with engine.connect() as con:
        con.execute(text('ALTER TABLE car_corp ADD CONSTRAINT car_corp_record_pk PRIMARY KEY (id);'))
        con.commit()
    with engine.connect() as con:
        con.execute(text('ALTER TABLE car_faq ADD CONSTRAINT car_faq_record_fk FOREIGN KEY (id) REFERENCES car_corp (id);'))
        con.commit()

def car_data_to_db(**kwargs):
    data = registrated_car_crawler()
    engine = create_db_engine(**kwargs)
    
    with engine.connect() as con:
        con.execute(text('DROP TABLE IF EXISTS registererd_car CASCADE;'))
        con.commit()
    
    data.to_sql(
        'registererd_car',
        engine,
        if_exists='replace',
        dtype={
            'region': VARCHAR(5),
            'count': Integer,
            'type': VARCHAR(5),
            'usage': VARCHAR(5),
            'date': DateTime,
        }
    )
