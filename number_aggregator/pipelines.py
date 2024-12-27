# pipelines.py
from dotenv import load_dotenv
import os
import psycopg2
import json
from scrapy.exceptions import NotConfigured

class PostgresPipeline:
    def __init__(self, db_settings):
        self.db_settings = db_settings

    @classmethod
    def from_crawler(cls, crawler):
        load_dotenv()
        if not crawler.settings.getbool('POSTGRES_PIPELINE_ENABLED'):
            raise NotConfigured
        return cls(db_settings={
            'dbname': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'), 
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT')
        })

    def open_spider(self, spider):
        self.conn = psycopg2.connect(**self.db_settings)
        self.cur = self.conn.cursor()
        self.create_table()
        spider.logger.info("Database connected successfully")

    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS autonet_az (
                id SERIAL PRIMARY KEY,
                car_id INTEGER,
                title TEXT,
                price NUMERIC,
                engine_capacity INTEGER,
                year INTEGER,
                mileage INTEGER,
                make TEXT,
                model TEXT,
                city TEXT,
                color INTEGER,
                barter BOOLEAN,
                credit BOOLEAN,
                phone1 TEXT,
                phone2 TEXT,
                is_salon BOOLEAN,
                transmission INTEGER,
                drive_type INTEGER,
                description TEXT,
                created_at TIMESTAMP,
                raw_data JSONB
            )
        """)
        self.conn.commit()

    def process_item(self, item, spider):
        try:
            raw_data = item['raw_data']
            self.cur.execute("""
                INSERT INTO autonet_az (
                    car_id, title, price, engine_capacity, year, mileage,
                    make, model, city, color, barter, credit, phone1, phone2,
                    is_salon, transmission, drive_type, description, created_at, raw_data
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                raw_data.get('id'),
                raw_data.get('title'),
                raw_data.get('price'),
                raw_data.get('engine_capacity'),
                raw_data.get('buraxilis_ili'),
                raw_data.get('yurus'),
                raw_data.get('make'),
                raw_data.get('model'),
                raw_data.get('cityName'),
                raw_data.get('rengi'),
                raw_data.get('barter') == 1,
                raw_data.get('kredit') == 1,
                raw_data.get('phone1'),
                raw_data.get('phone2'),
                raw_data.get('isSalon') == 1,
                raw_data.get('suret_qutusu'),
                raw_data.get('oturuculuk'),
                raw_data.get('information'),
                raw_data.get('created_at'),
                json.dumps(raw_data)
            ))
            self.conn.commit()
        except Exception as e:
            spider.logger.error(f"Error saving item {raw_data.get('id')}: {str(e)}")
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()