import scrapy
from urllib.parse import urljoin
from scrapy.utils.project import get_project_settings
from dom_ria.items import ApartmentItem
from dom_ria.utils import (
    parse_page,
    parse_apartment_condition,
    parse_centre_distance,
    parse_images_urls,
)


class DomRiaSpider(scrapy.Spider):
    name = "apartments"
    domain = "https://dom.ria.com"
    allowed_domains = ["dom.ria.com"]
    start_urls = ["https://dom.ria.com/prodazha-kvartir/?page=1"]
    settings = get_project_settings()
    custom_settings = {
        "ROBOTSTXT_OBEY": True,
        "DOWNLOAD_DELAY": "0.25",
        # 'FEED_URI': 'dataset/data.json',
        "FEED_EXPORT_ENCODING": "utf-8",
        "ITEM_PIPELINES": {"dom_ria.pipelines.DomRiaPipeline": 300},
    }
    limit = 20000
    count = 0

    def parse(self, response):
        apartments_links = response.css(".wrap_desc .mb-10 .mb-0 a::attr(href)").extract()
        for link in apartments_links:
            yield scrapy.Request(urljoin(self.domain, link), callback=self.parse_inner_page)

        next_page = response.css( "#pagination .pager .next a::attr(href)").extract_first()
        if next_page is not None and self.count < self.limit:
            next_page_url = urljoin(self.domain, next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_inner_page(self, response):
        initial_data = parse_page(response.body.decode("utf-8"))
        verified_fields = response.css(".mb-15 .ml-30 span::text").extract()
        apartment_info_keys = response.css("#description .unstyle .mt-15 .label::text").extract()
        apartment_info_values = response.css("#description .unstyle .mt-15 .indent::text").extract()
        apartment_info = {key.strip(): value.strip() for key, value in zip(apartment_info_keys, apartment_info_values)}
        additional_info = {item["groupName"]: item["items"] for item in initial_data["secondaryParams"]}

        apartment = ApartmentItem()
        apartment["url"] = initial_data["absoluteUrl"]
        apartment["title"] = response.css(".finalPage h1::text").extract_first()
        apartment["price_uah"] = initial_data["priceArr"]["3"]
        apartment["price_usd"] = initial_data["priceArr"]["1"]
        apartment["verified_price"] = True if "Перевірена ціна" in verified_fields else False
        apartment["verified_apartment"] = True if "Перевірена квартира" in verified_fields else False
        apartment["description"] = response.css("#descriptionBlock::text").extract_first()
        apartment["region"] = initial_data["state_name"]
        apartment["city"] = initial_data["city_name"]
        apartment["district"] = initial_data["district_name"]
        apartment["street"] = initial_data["street_name"]
        if "building_number_str" in initial_data:
            apartment["building_number"] = initial_data["building_number_str"]
        else:
            apartment["building_number"] = None
        if "latitude" in initial_data:
            apartment["latitude"] = initial_data["latitude"]
        else:
            apartment["latitude"] = None
        if "longitude" in initial_data:
            apartment["longitude"] = initial_data["longitude"]
        else:
            apartment["longitude"] = None
        apartment["total_square"] = initial_data["total_square_meters"]
        apartment["living_square"] = initial_data["living_square_meters"]
        apartment["kitchen_square"] = initial_data["kitchen_square_meters"]
        apartment["room_count"] = initial_data["mainCharacteristics"]["baseInfo"]["p1"]["value"]
        apartment["floor"] = initial_data["floor"]
        apartment["floor_count"] = initial_data["floors_count"]
        apartment["walls_material"] = initial_data["wall_type"]
        apartment["heating"] = apartment_info["Отопление"] if "Отопление" in apartment_info else None
        apartment["construction_year"] = apartment_info["Год постройки"] if "Год постройки" in apartment_info else None
        apartment["apartment_type"] = initial_data["mainCharacteristics"]["dashes"][-1]
        apartment["selling_type"] = apartment_info["Тип предложения"] if "Тип предложения" in apartment_info else None
        apartment["creation_date"] = initial_data["publishing_date"]
        if "характеристика помещения" in additional_info:
            apartment["apartment_condition"] = parse_apartment_condition(additional_info["характеристика помещения"])
        else:
            apartment["apartment_condition"] = None
        if "до центра города" in additional_info:
            apartment["centre_distance"], apartment["centre_distance_type"] = \
                parse_centre_distance(additional_info["до центра города"])
        else:
            apartment["centre_distance"], apartment["centre_distance_type"] = None, None
        apartment["images"] = parse_images_urls(initial_data["photos"])
        self.count += 1
        yield apartment
