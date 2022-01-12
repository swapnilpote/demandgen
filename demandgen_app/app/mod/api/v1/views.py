from flask import Blueprint, request, jsonify
from app import logging

from app.mod.module.predict import Predict
pred = Predict()

logger = logging.getLogger(__name__)

blueprint_demandgen = Blueprint("flask", __name__)


@blueprint_demandgen.route("/predict", methods=["POST"])
def predict():
    # Request data
    text = request.json.get("text")
    callid = request.json.get("callid")
    calldetails = request.json.get("calldetails")

    # Response data
    response = dict()
    response["calldetails"] = calldetails

    pred.result(text)

    return jsonify(response)
