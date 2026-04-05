from flask import Flask, request
import requests
import json
import sys

app = Flask(__name__)

@app.route('/orca-webhook-out', methods=['POST'])
def webhook_out():
    data = request.get_json(silent=True)

    if not data:
        return 'Bad Request', 400

    # debug purpose: show in console raw data received
    print('Request received:\n' + json.dumps(data, indent=2), flush=True)

    # get the name of the event that triggered this request (rows:add, rows:update, rows:delete, test)
    event = data.get('___orca_event')

    # get the name of the sheet this event impacts
    sheet_name = data.get('___orca_sheet_name')

    # get the email of the user who performed the action (empty if not HTTPS)
    user_email = data.get('___orca_user_email')

    # NOTE:
    # orca system fields start with ___
    # you can access the value of each field using the field name (data['Name'], data['Barcode'], data['Location'])

    if event == 'rows:add':
        pass  # TODO: do something when a row has been added
    elif event == 'rows:update':
        pass  # TODO: do something when a row has been updated
    elif event == 'rows:delete':
        pass  # TODO: do something when a row has been deleted
    elif event == 'test':
        pass  # TODO: do something when the user in the web app hits the test button

    return 'OK', 200

@app.route('/trigger-webhook-in', methods=['GET'])
def trigger_webhook_in():
    # The following example adds a new row to a sheet, setting the value of Barcode, Name, Quantity and Description
    # TODO: change url to https://api.orcascan.com/sheets/{id}
    response = requests.post('https://httpbin.org/post', json={
        '___orca_action': 'add',
        'Barcode': '0123456789',
        'Name': 'New 1',
        'Quantity': 12,
        'Description': 'Add new row example'
    })

    print(response.text, flush=True)
    return 'OK', 200

if __name__ == '__main__':
    app.run(port=8888)
