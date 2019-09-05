import re
import json
from urllib.parse import urljoin
from typing import Tuple, Union

"""
Serializers
"""


def serialize_price(price: str) -> int:
    return int("".join(re.findall(r"\d+", price)))


def serialize_geolocation(coordinate: str) -> Union[None, float]:
    if not coordinate:
        return None
    else:
        return float(coordinate)


"""
Parsers
"""


def parse_page(content: str):
    all_data = re.search(r"__INITIAL_STATE__={.*};", content, re.DOTALL).group()
    return json.loads(all_data[18:-1])["dataForFinalPage"]["realty"]


def parse_apartment_condition(content: list) -> str:
    for item in content:
        if "состояние квартиры" in item:
            return item.replace("состояние квартиры: ", "")


def parse_centre_distance(content: list) -> Tuple[str, str]:
    distance = content[0].replace("удаленность: ", "")
    distance_type = content[-1].replace("как добираться: ", "")
    return distance, distance_type


def parse_images_urls(content: list) -> list:
    base_url = "https://cdn.riastatic.com/photosnew/"
    urls = []
    for item in content:
        url = item["beautifulUrl"]
        url = url.replace(".", "f.")
        urls.append(urljoin(base_url, url))
    return urls
