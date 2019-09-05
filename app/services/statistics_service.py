import numpy as np
from database_pg.queries import (
    get_count_apartments, get_prices_usd, get_total_squares, get_count_col, get_living_squares, get_kitchen_squares,
    get_floors, get_floor_counts, get_images_urls, get_heating_types, get_cities, get_regions, get_walls_material
)


def process_statistics():
    prices = np.array(get_prices_usd())
    squares = np.array(get_total_squares())
    living_squares = np.array(get_living_squares())
    kitchen_squares = np.array(get_kitchen_squares())
    floors = np.array(get_floors())
    floor_counts = np.array(get_floor_counts())
    images_counts = np.array([len(item) for item in get_images_urls()])
    heating_types = {item[0] if item[0] is not None else "missing": item[1] for item in get_heating_types()}
    walls_materials = {item[0] if item[0] is not None else "missing": item[1] for item in get_walls_material()}
    cities = {item[0] if item[0] is not None else "missing": item[1] for item in get_cities()}
    regions = {item[0] if item[0] is not None else "missing": item[1] for item in get_regions()}
    output = {
        "apartments count": get_count_apartments(),
        "params per apartment": get_count_col(),
        "USD prices": {
            "mean": int(np.mean(prices)),
            "median": int(np.median(prices)),
            "std": int(np.std(prices)),
        },
        "total squares": {
            "mean": np.mean(squares),
            "median": np.median(squares),
            "std": np.std(squares),
        },
        "living squares": {
            "mean": np.mean(living_squares),
            "median": np.median(living_squares),
            "std": np.std(living_squares),
        },
        "kitchen squares": {
            "mean": np.mean(kitchen_squares),
            "median": np.median(kitchen_squares),
            "std": np.std(kitchen_squares),
        },
        "floor of apartments": {
            "mean": np.mean(floors),
            "median": np.median(floors),
            "std": np.std(floors),
        },
        "floor counts": {
            "mean": np.mean(floor_counts),
            "median": np.median(floor_counts),
            "std": np.std(floor_counts),
        },
        "images per apartment": {
            "mean": np.mean(images_counts),
            "median": np.median(images_counts),
        },
        "heating_types:": heating_types,
        "walls_materials": walls_materials,
        "cities": cities,
        "regions": regions
    }
    return output
