from sqlalchemy.orm import sessionmaker
from database_pg.models import ApartmentTable
from database_pg.utils import db_connect

engine = db_connect()
Session = sessionmaker(bind=engine)


def get_count_apartments():
    session = Session()
    query = session.query(ApartmentTable).count()
    session.close()
    return query


def get_apartments_list(limit: int = None, offset: int = None) -> list:
    session = Session()
    apartments_list = []
    if limit is None and offset is None:
        query = session.query(ApartmentTable).order_by(ApartmentTable.creation_date.desc())
    elif limit is None:
        query = session.query(ApartmentTable).order_by(ApartmentTable.creation_date.desc()).offset(offset)
    elif offset is None:
        query = session.query(ApartmentTable).order_by(ApartmentTable.creation_date.desc()).limit(limit)
    else:
        query = session.query(ApartmentTable).order_by(ApartmentTable.creation_date.desc()).offset(offset).limit(limit)
    session.close()
    for apartment in query:
        apartments_list.append(apartment.as_dict())
    return apartments_list


def get_count_col():
    return len(ApartmentTable.__table__.columns)


def get_prices_usd():
    session = Session()
    query = session.query(ApartmentTable.price_usd).all()
    session.close()
    return query


def get_total_squares():
    session = Session()
    query = session.query(ApartmentTable.total_square).all()
    session.close()
    return query


def get_living_squares():
    session = Session()
    query = session.query(ApartmentTable.living_square).all()
    session.close()
    return query


def get_kitchen_squares():
    session = Session()
    query = session.query(ApartmentTable.kitchen_square).all()
    session.close()
    return query


def get_floors():
    session = Session()
    query = session.query(ApartmentTable.floor).all()
    session.close()
    return query


def get_floor_counts():
    session = Session()
    query = session.query(ApartmentTable.floor_count).all()
    session.close()
    return query


def get_images_urls():
    session = Session()
    query = session.query(ApartmentTable.images).all()
    session.close()
    return query


def get_heating_types():
    session = Session()
    # query = session.query(ApartmentTable.heating).distinct()
    query = session.execute("SELECT heating, count(*) FROM apartment GROUP BY heating")
    session.close()
    return query


def get_cities():
    session = Session()
    # query = session.query(ApartmentTable.heating).distinct()
    query = session.execute("SELECT city, count(*) FROM apartment GROUP BY city")
    session.close()
    return query


def get_regions():
    session = Session()
    # query = session.query(ApartmentTable.heating).distinct()
    query = session.execute("SELECT region, count(*) FROM apartment GROUP BY region")
    session.close()
    return query


def get_walls_material():
    session = Session()
    # query = session.query(ApartmentTable.heating).distinct()
    query = session.execute("SELECT walls_material, count(*) FROM apartment GROUP BY walls_material")
    session.close()
    return query
