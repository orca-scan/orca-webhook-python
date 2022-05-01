# import flask framework
from flask import Flask, request
import requests
import json

# create a flask app instance
app = Flask(__name__)

# POST / handler
@app.route('/orca-webhook-out', methods=['POST'])
def webhook_out():
    if request.method == 'POST':
        data = request.get_json()

        # dubug purpose: show in console raw data received
        print("Request received: \n"+json.dumps(data, sort_keys=True, indent=4))

        # get the name of the action that triggered this request (add, update, delete, test)
        action = data["___orca_action"]

        # get the name of the sheet this action impacts
        sheet_name = data["___orca_sheet_name"]

        # get the email of the user who preformed the action (empty if not HTTPS)
        user_email = data["___orca_user_email"]

        # NOTE:
        # orca system fields start with ___
        # you can access the value of each field using the field name (data["Name"], data["Barcode"], data["Location"])

        if action == "add":
            # TODO: do something when a row has been added
            pass
        elif action == "update":
            # TODO: do something when a row has been updated
            pass
        elif action == "delete":
            # TODO: do something when a row has been deleted
            pass
        elif action == "test":
            # TODO: do something when the user in the web app hits the test button
            pass
        
    # always return a 200 (ok)
    return "ok"

# Trigger Webhook In
@app.route('/trigger-webhook-in', methods=['GET'])
def trigger_webhook_in():
    # the following example adds a new row to a sheet, setting the value of Barcode, Name, Quantity and Description
    # TODO: change url to https://api.orcascan.com/sheets/{id}
    response = requests.post('https://httpbin.org/post', json={ 
            "___orca_action": "add",
            "Barcode": "0123456712",
            "Name": "New 1",
            "Quantity": 12,
            "Description": "Add new row example"
        })
    if response.ok:
        print(response.content)
    return "ok"
