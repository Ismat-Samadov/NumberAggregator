# items.py
from scrapy import Item, Field

class AutoNetItem(Item):
    car_id = Field()
    title = Field()
    price = Field() 
    engine_capacity = Field()
    year = Field()
    mileage = Field()
    make = Field()
    model = Field()
    city = Field()
    color = Field()
    barter = Field()
    credit = Field()
    phone1 = Field()
    phone2 = Field()
    is_salon = Field()
    transmission = Field()
    drive_type = Field()
    description = Field()
    created_at = Field()
    raw_data = Field()