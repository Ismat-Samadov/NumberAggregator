from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
import random
import time

class CustomUserAgentMiddleware(UserAgentMiddleware):
   user_agents = [
       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
       'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
   ]

   def process_request(self, request, spider):
       request.headers['User-Agent'] = random.choice(self.user_agents)

class CustomRetryMiddleware(RetryMiddleware):
   def process_response(self, request, response, spider):
       if response.status in self.retry_http_codes:
           reason = response_status_message(response.status)
           time.sleep(2)  # Add delay before retry
           return self._retry(request, reason, spider) or response
       return response

class CustomDownloaderMiddleware:
   def process_request(self, request, spider):
       request.headers['Accept'] = 'application/json'
       request.headers['X-Requested-With'] = 'XMLHttpRequest'
       return None

