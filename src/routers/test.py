from src.crud.air_scraper import get_air_info
from src.schemas.base import DATE

print(get_air_info("重庆", "东京", DATE(year="2025", month="6", day="10")))