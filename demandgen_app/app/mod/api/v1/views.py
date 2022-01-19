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
    print("Stage - 0")
    print({"text": text, "callid": callid, "calldetails": calldetails})
    print("-"*100)

    # Response data
    response = dict()
    response["text"] = text
    response["callid"] = callid
    response["calldetails"] = calldetails
    response["action"] = list(dict())

    result = pred.result(text)
    print("Stage - 1")
    print({"result": result})
    print("-"*100)

    if result.get("entities"):
        verified_entities = data_validation(calldetails, result.get("entities"))

    if result.get("domain")=="dvm" and result.get("entities") and result.get("entities").get("person_name"):
        if verified_entities.get("person_name_verified"):
            response["action"].append({"command": "hangup", "value": True})
        else:
            response["action"].append({"command": "hangup", "value": False})
            response["identifiedData"] = dict()
            response["identifiedData"]["domain"] = "dvm"
            response["identifiedData"]["intent"] = ""
            response["identifiedData"]["entities"] = result.get("entities")

    print("Stage - 2")
    print(response)
    print("="*100)

    return jsonify(response)


def data_validation(calldetails: dict, entities: dict):
    verified_entities = dict()
    if entities.get("person_name"):
        person_name = calldetails.get("fname") + " " + calldetails.get("lname")
        if entities.get("person_name").lower() == person_name.lower():
            verified_entities["person_name_verified"] = True
        else:
            verified_entities["person_name_verified"] = False

    return verified_entities
