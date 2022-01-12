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
    response["text"] = text
    response["callid"] = callid
    response["calldetails"] = calldetails
    response["action"] = dict()

    result = pred.result(text)

    if result.get("domain")=="dvm" and result.get("entities").get("person_name"):
        response["action"]["command"] = "hangup"
        response["action"]["value"] = True
        response["action"]["identifiedData"] = dict()
        response["action"]["identifiedData"]["domain"] = "dvm"
        response["action"]["identifiedData"]["intent"] = ""
        response["action"]["identifiedData"]["entities"] = result.get("entities")

    return jsonify(response)
