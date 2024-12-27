import scrapy
import json
from urllib.parse import unquote
from ..items import AutoNetItem

class AvtonetSpider(scrapy.Spider):
   name = "avtonet"
   allowed_domains = ["autonet.az"]
   base_url = "https://autonet.az/api/items/searchItem"
   x_auth_token = "00028c2ddcc1ca6c32bc919dca64c288bf32ff2a"

   def start_requests(self):
       yield scrapy.Request(
           "https://autonet.az/items",
           callback=self.parse_tokens,
           meta={'dont_redirect': True, 'handle_httpstatus_list': [301, 302]},
           dont_filter=True
       )

   def parse_tokens(self, response):
       cookies = response.headers.getlist('Set-Cookie')
       xsrf_token = next(
           (unquote(c.decode().split(';')[0].split('=')[1]) 
            for c in cookies if b'XSRF-TOKEN' in c),
           ''
       )

       headers = {
           "Accept": "application/json",
           "X-Authorization": self.x_auth_token,
           "X-XSRF-TOKEN": xsrf_token,
           "X-Requested-With": "XMLHttpRequest",
           "Referer": "https://autonet.az/items"
       }

       for page in range(1, 237):
           yield scrapy.Request(
               f"{self.base_url}?page={page}",
               callback=self.parse_items,
               headers=headers,
               cookies={'XSRF-TOKEN': xsrf_token},
               meta={'dont_redirect': True, 'page': page},
               errback=self.handle_error,
               dont_filter=True
           )

   def parse_items(self, response):
       try:
           data = json.loads(response.text)
           if "data" not in data:
               self.logger.warning(f"No data in response for page {response.meta.get('page')}")
               return

           for car_data in data["data"]:
               yield AutoNetItem(
                   car_id=car_data.get('id'),
                   title=car_data.get('title'),
                   price=car_data.get('price'),
                   engine_capacity=car_data.get('engine_capacity'),
                   year=car_data.get('buraxilis_ili'),
                   mileage=car_data.get('yurus'),
                   make=car_data.get('make'),
                   model=car_data.get('model'),
                   city=car_data.get('cityName'),
                   color=car_data.get('rengi'),
                   barter=car_data.get('barter') == 1,
                   credit=car_data.get('kredit') == 1,
                   phone1=car_data.get('phone1'),
                   phone2=car_data.get('phone2'),
                   is_salon=car_data.get('isSalon') == 1,
                   transmission=car_data.get('suret_qutusu'),
                   drive_type=car_data.get('oturuculuk'),
                   description=car_data.get('information'),
                   created_at=car_data.get('created_at'),
                   raw_data=car_data
               )
       except json.JSONDecodeError as e:
           self.logger.error(f"JSON decode error on page {response.meta.get('page')}: {str(e)}")
       except Exception as e:
           self.logger.error(f"Error processing page {response.meta.get('page')}: {str(e)}")

   def handle_error(self, failure):
       self.logger.error(f"Request failed: {failure.value}")