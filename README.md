# Apartment price prediction project

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required libraries in a separate virtualenv:
```bash
pip install -r requirements.txt
```
You need to create `.env` file in root directory with following code:
```
DB_CONNECTION="DB://USER:PASS@URL/dom_ria"
```

## Load data
You need to specify `LOAD_TYPE="crawler"` in `.env` file.
```bash
bash load.sh
```

## Train models
You need to specify `LOAD_TYPE="price_prediction"` in `.env` file.
```bash
bash load.sh
```

## Usage
To start server:
```bash
bash dev.sh
```

### Prediction template

```json
{
    "model": "nn",
    "features": {
        "verified_price": false,
        "city": "Киев",
        "district": "Центр",
        "total_square": 40,
        "living_square": 20,
        "kitchen_square": 10,
        "room_count": 2,
        "floor": 5,
        "floor_count": 8,
        "walls_material": "панель",
        "heating": "индивидуальное",
        "apartment_type": "Вторичное жилье"
    }
}
```
```
    "model": "decision_tree",
    "model": "lightgbm"
```