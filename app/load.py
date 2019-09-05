import os
import settings
from scrapy.crawler import CrawlerProcess
from dom_ria.spiders.apartments import DomRiaSpider
from services.price_prediction_service import PricePredictionService


def load_crawler():
    process = CrawlerProcess()
    process.crawl(DomRiaSpider)
    process.start()


def main():
    load_type = os.getenv("LOAD_TYPE")
    if load_type == "crawler":
        load_crawler()
    elif load_type == "price_prediction":
        PricePredictionService()
    else:
        raise Exception("specify correct LOAD_TYPE in .env file")


if __name__ == "__main__":
    main()
