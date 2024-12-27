from pathlib import Path
import os
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(env_path)

BOT_NAME = "number_aggregator"
SPIDER_MODULES = ["number_aggregator.spiders"]
NEWSPIDER_MODULE = "number_aggregator.spiders"

ROBOTSTXT_OBEY = False
COOKIES_ENABLED = True
DOWNLOAD_DELAY = 1

ITEM_PIPELINES = {
    "number_aggregator.pipelines.PostgresPipeline": 300,
}

# Database settings
POSTGRES_PIPELINE_ENABLED = True
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

DEFAULT_REQUEST_HEADERS = {
    "Accept": "application/json",
    "X-Requested-With": "XMLHttpRequest"
}

DOWNLOADER_MIDDLEWARES = {
    'number_aggregator.middlewares.CustomUserAgentMiddleware': 400,
    'number_aggregator.middlewares.CustomRetryMiddleware': 500,
    'number_aggregator.middlewares.CustomDownloaderMiddleware': 600,
}