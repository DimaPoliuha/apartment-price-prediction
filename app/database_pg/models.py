from sqlalchemy import (
    Column,
    Integer,
    SmallInteger,
    String,
    DateTime,
    Float,
    Boolean,
    Text,
    ARRAY,
)
from sqlalchemy.ext.declarative import declarative_base
from database_pg.utils import Mixin

DeclarativeBase = declarative_base(cls=Mixin)


def create_table(engine):
    DeclarativeBase.metadata.create_all(engine, DeclarativeBase.metadata.tables.values(), checkfirst=True)


class ApartmentTable(DeclarativeBase):
    __tablename__ = "apartment"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    url = Column(String(240), nullable=False)
    title = Column(String(480))
    price_uah = Column(Integer, nullable=False)
    price_usd = Column(Integer, nullable=False)
    verified_price = Column(Boolean)
    verified_apartment = Column(Boolean)
    description = Column(Text)
    region = Column(String(240))
    city = Column(String(240))
    district = Column(String(240))
    street = Column(String(240))
    building_number = Column(String(40))
    latitude = Column(Float)
    longitude = Column(Float)
    total_square = Column(Float, nullable=False)
    living_square = Column(Float, nullable=False)
    kitchen_square = Column(Float, nullable=False)
    room_count = Column(SmallInteger, nullable=False)
    floor = Column(SmallInteger, nullable=False)
    floor_count = Column(SmallInteger, nullable=False)
    walls_material = Column(String(240))
    heating = Column(String(240))
    construction_year = Column(String(40))
    apartment_type = Column(String(120))
    selling_type = Column(String(120))
    creation_date = Column(DateTime)
    apartment_condition = Column(String(240))
    centre_distance = Column(String(120))
    centre_distance_type = Column(String(120))
    images = Column("images", ARRAY(String(240), dimensions=1))
