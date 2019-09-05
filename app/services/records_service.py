import re
from typing import Union
from database_pg.queries import get_apartments_list


def process_records(limit: Union[str, int], offset: Union[str, int]):
    if (limit and not re.match(r"^\d+$", limit)) or not limit:
        limit = 10
    else:
        limit = int(limit)

    if (offset and not re.match(r"^\d+$", offset)) or not offset:
        offset = 0
    else:
        offset = int(offset)
    output = {
        "limit": limit,
        "offset": offset,
        "apartments": get_apartments_list(limit, offset)
    }
    return output
