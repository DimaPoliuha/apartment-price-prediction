import settings
import json
from flask import Flask, request, jsonify, render_template, redirect
from services.records_service import process_records
from services.statistics_service import process_statistics
from services.price_prediction_service import PricePredictionService

price_prediction_service = PricePredictionService()

ALLOWED_EXTENSIONS = {"json"}

web_app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@web_app.route("/api/v1/statistics")
def statistics_api():
    return jsonify(process_statistics())


@web_app.route("/api/v1/records")
def records_api():
    limit = request.args.get("limit")
    offset = request.args.get("offset")
    return jsonify(process_records(limit, offset))


@web_app.route("/api/v1/price/predict")
def price_prediction_page():
    return render_template('price_predict.html')


@web_app.route("/api/v1/price/predict", methods=['POST'])
def price_prediction_api():
    if 'file' not in request.files:
        print('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        print('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        params = json.load(file)
        if "model" not in params or "features" not in params:
            print('Specify all params in file')
            return redirect(request.url)
        predict = price_prediction_service.predict(params["model"], params["features"])
        output = {
            "price USD": predict
        }
        return jsonify(output)
    return redirect(request.url)


if __name__ == "__main__":
    web_app.run()
