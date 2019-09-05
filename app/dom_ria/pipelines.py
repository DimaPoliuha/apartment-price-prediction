from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from database_pg.models import ApartmentTable, create_table
from database_pg.utils import db_connect
from dom_ria.utils import serialize_price, serialize_geolocation


class DomRiaPipeline(object):
    def __init__(self):
        self.engine = db_connect()
        if not database_exists(self.engine.url):
            create_database(self.engine.url, encoding="utf8")

        create_table(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def open_spider(self, spider):
        self.session = self.Session()

    def close_spider(self, spider):
        self.session.close()
        self.engine.dispose()

    def process_item(self, item, spider):
        apartment = ApartmentTable()
        apartment.url = item["url"]
        apartment.title = item["title"]
        apartment.price_uah = serialize_price(item["price_uah"])
        apartment.price_usd = serialize_price(item["price_usd"])
        apartment.verified_price = item["verified_price"]
        apartment.verified_apartment = item["verified_apartment"]
        apartment.description = item["description"]
        apartment.region = item["region"]
        apartment.city = item["city"]
        apartment.district = item["district"]
        apartment.street = item["street"]
        apartment.building_number = item["building_number"]
        apartment.latitude = serialize_geolocation(item["latitude"])
        apartment.longitude = serialize_geolocation(item["longitude"])
        apartment.total_square = float(item["total_square"])
        apartment.living_square = float(item["living_square"])
        apartment.kitchen_square = float(item["kitchen_square"])
        apartment.room_count = int(item["room_count"])
        apartment.floor = int(item["floor"])
        apartment.floor_count = int(item["floor_count"])
        apartment.walls_material = item["walls_material"]
        apartment.heating = item["heating"]
        apartment.construction_year = item["construction_year"]
        apartment.apartment_type = item["apartment_type"]
        apartment.selling_type = item["selling_type"]
        apartment.creation_date = item["creation_date"]
        apartment.apartment_condition = item["apartment_condition"]
        apartment.centre_distance = item["centre_distance"]
        apartment.centre_distance_type = item["centre_distance_type"]
        apartment.images = item["images"]

        try:
            self.session.add(apartment)
            self.session.commit()
        except:
            self.session.rollback()
            raise

        return item
