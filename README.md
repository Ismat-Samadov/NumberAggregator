# Number Aggregator

A web scraping project built with Scrapy to collect car listings data from various automobile marketplaces.

## Features

- Data collection from multiple sources
- Automatic authentication handling
- PostgreSQL database integration
- Rate limiting and retry mechanisms 
- Error handling and logging

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/NumberAggregator.git
cd NumberAggregator
```

2. Create virtual environment and activate it
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables in `.env`
```
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=your_db_port
```

## Usage

Run specific spider:
```bash
scrapy crawl avtonet
```

## Project Structure

```
NumberAggregator/
├── .env                      # Environment variables
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
└── number_aggregator/        # Main project directory
    ├── __init__.py
    ├── items.py             # Data models
    ├── middlewares.py       # Custom middlewares
    ├── pipelines.py         # Data processing pipelines
    ├── settings.py          # Project settings
    └── spiders/             # Spider implementations
        ├── __init__.py
        └── avtonet.py       # Autonet.az spider
```

## Spiders

### Avtonet Spider
- Source: autonet.az
- Data: Car listings
- Features:
  - Dynamic token extraction
  - Pagination handling
  - Response validation
  - Error recovery

## Database Schema

```sql
CREATE TABLE autonet_az (
    id SERIAL PRIMARY KEY,
    car_id INTEGER,
    make TEXT,
    model TEXT,
    price NUMERIC,
    engine_capacity INTEGER,
    year INTEGER,
    mileage INTEGER,
    description TEXT,
    city TEXT,
    barter BOOLEAN,
    credit BOOLEAN,
    phone1 TEXT,
    phone2 TEXT,
    color INTEGER,
    transmission INTEGER,
    drive_type INTEGER,
    created_at TIMESTAMP,
    raw_data JSONB,
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Requirements

- Python 3.8+
- PostgreSQL
- Scrapy
- psycopg2-binary
- python-dotenv

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
