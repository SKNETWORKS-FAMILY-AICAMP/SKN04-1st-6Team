from data_to_db import car_data_to_db, faq_data_to_db

USERNAME = 'postgres'
PASSWORD = '1234'
HOST = 'localhost'
PORT = 5432
DB_NAME = 'postgres'

car_data_to_db(name=USERNAME, password=PASSWORD, host=HOST, port=PORT, db_name=DB_NAME)
faq_data_to_db(name=USERNAME, password=PASSWORD, host=HOST, port=PORT, db_name=DB_NAME)
