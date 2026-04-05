# orca-webhook-python

Connect [Orca Scan](https://orcascan.com) to your own system using webhooks. When a user scans a barcode and adds, updates, or deletes a row, Orca Scan sends the data to your server in real-time - no polling, no manual exports.

This Python example shows you how to:

- **Receive scan data** from Orca Scan as it happens ([Webhook Out](https://orcascan.com/guides/updating-your-system-data-when-a-barcode-is-scanned-da8bbe42))
- **Push data back** into Orca Scan from your own system ([Webhook In](https://orcascan.com/guides/updating-orca-scan-data-from-your-system-4b249706))

## Quick start

```bash
git clone https://github.com/orca-scan/orca-webhook-python.git
cd orca-webhook-python
pip install -r requirements.txt
python server.py
```

Server runs on port **8888**.

## Receiving data from Orca Scan (Webhook Out)

When a barcode is scanned and a row changes, Orca Scan sends a `POST` request to `/orca-webhook-out` with the row data as JSON. You can use this to sync inventory to your database, trigger alerts, update dashboards — whatever your workflow needs.

Every request includes these system fields:

| Field | Description |
|---|---|
| `___orca_event` | `rows:add`, `rows:update`, `rows:delete`, or `test` |
| `___orca_sheet_name` | The sheet that triggered the event |
| `___orca_user_email` | Email of the user _(HTTPS only)_ |

All other fields match your sheet column names exactly _(case and space sensitive)_.

The full docs cover additional events like [import](https://orcascan.com/guides/updating-your-system-data-when-a-barcode-is-scanned-da8bbe42#what-information-does-orca-scan-send-when-i-import-data), [clear](https://orcascan.com/guides/updating-your-system-data-when-a-barcode-is-scanned-da8bbe42#what-information-does-orca-scan-send-when-i-clear-data), and [security headers](https://orcascan.com/guides/updating-your-system-data-when-a-barcode-is-scanned-da8bbe42#security).

### Test with cURL

```bash
curl -X POST 'http://127.0.0.1:8888/orca-webhook-out' \
-H 'Content-Type: application/json' \
-d '{
    "___orca_event": "rows:add",
    "___orca_sheet_name": "Vehicle Checks",
    "___orca_user_email": "hidden@requires.https",
    "___orca_row_id": "5cf5c1efc66a9681047a0f3d",
    "Barcode": "4S3BMHB68B3286050",
    "Make": "SUBARU",
    "Model": "Legacy",
    "Model Year": "2011",
    "Vehicle Type": "PASSENGER CAR",
    "Plant City": "Lafayette",
    "Trim": "Premium",
    "Location": "52.2034823, 0.1235817",
    "Notes": "Needs new tires"
}'
```

### Test with Orca Scan

Expose your local server with [localtunnel](https://github.com/localtunnel/localtunnel):

```bash
npx localtunnel --port 8888
```

Then [add the tunnel URL as your Webhook Out endpoint](https://orcascan.com/guides/capture-barcode-scan-events-with-webhooks-da8bbe42#how-to-set-up-a-webhook-out-url) in the Orca Scan web app and hit **Test**.

> Webhooks are fire-and-forget — they are not retried regardless of HTTP response.

## Pushing data into Orca Scan (Webhook In)

Need to update Orca Scan from your own system? Hit `GET /trigger-webhook-in` to push a row into a sheet via the [Webhook In API](https://orcascan.com/guides/updating-orca-scan-data-from-your-system-4b249706).

To connect it to your sheet, update the URL in [server.py](server.py):

```
https://api.orcascan.com/sheets/{id}
```

See the [REST API docs](https://orcascan.com/guides/barcode-scanning-rest-api-f09a21c3) for all available endpoints.

## Examples in other languages

| Language | Repository |
|---|---|
| Node.js | [orca-webhook-node](https://github.com/orca-scan/orca-webhook-node) |
| C# | [orca-webhook-dotnet](https://github.com/orca-scan/orca-webhook-dotnet) |
| Go | [orca-webhook-go](https://github.com/orca-scan/orca-webhook-go) |
| Java | [orca-webhook-java](https://github.com/orca-scan/orca-webhook-java) |
| PHP | [orca-webhook-php](https://github.com/orca-scan/orca-webhook-php) |

## Help

[Chat to us live](https://orcascan.com/#chat) if you run into any issues.

## License

&copy; Orca Scan, the [Barcode Scanner app for iOS and Android](https://orcascan.com).

## Install

First ensure you have [Python](https://www.python.org/downloads/) installed:

**macOS or Linux**
```bash
# should return 3.7 or higher
python3 --version
```

**Windows**
```bash
# should return 3.7 or higher
python --version
```

Then execute the following:

```bash
# download this example code
git clone https://github.com/orca-scan/orca-webhook-python.git

# go into the new directory
cd orca-webhook-python
```
**macOS or Linux**
```bash
# create virtual environment and activate it
python3 -m venv orca && source ./orca/bin/activate
```
**Windows**
```bash
# create virtual environment and activate it
python -m venv orca && source ./orca/scripts/activate
```
**All**
```bash
# upgrade pip to latest version
python -m pip install --upgrade pip

# install dependencies
pip install -r requirements.txt
```

## Run

**macOS or Linux**
```bash
# activate virtual environment
source ./orca/bin/activate
```
**Windows**
```bash
# activate virtual environment
source ./orca/scripts/activate
```
**All**
```bash
# enable development features only for development
export FLASK_ENV=development

# start the project
flask run -p 5000 
```

Your WebHook receiver will now be running on port 5000.

You can emulate an Orca Scan WebHook using [cURL](https://dev.to/ibmdeveloper/what-is-curl-and-why-is-it-all-over-api-docs-9mh) by running the following:

```bash
curl --location --request POST 'http://127.0.0.1:5000/orca-webhook-out' \
--header 'Content-Type: application/json' \
--data-raw '{
    "___orca_action": "add",
    "___orca_sheet_name": "Vehicle Checks",
    "___orca_user_email": "hidden@requires.https",
    "___orca_row_id": "5cf5c1efc66a9681047a0f3d",
    "Barcode": "4S3BMHB68B3286050",
    "Make": "SUBARU",
    "Model": "Legacy",
    "Model Year": "2011",
    "Vehicle Type": "PASSENGER CAR",
    "Plant City": "Lafayette",
    "Trim": "Premium",
    "Location": "52.2034823, 0.1235817",
    "Notes": "Needs new tires"
}'
```
### Important things to note

1. Only Orca Scan system fields start with `___`
2. Properties in the JSON payload are an exact match to the  field names in your sheet _(case and space)_
3. WebHooks are never retried, regardless of the HTTP response

## Example

This [example](app.py) uses the [flask](https://github.com/pallets/flask) framework:

### WebHook Out 

[Orca Scan WebHook Out](https://orcascan.com/docs/api/webhooks)

```python
# POST / handler
@app.route('/orca-webhook-out', methods=['POST'])
def webhook_out():
    if request.method == 'POST':
        data = request.get_json()

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
```

### WebHook In 

[Orca Scan WebHook In](https://orcascan.com/guides/how-to-update-orca-scan-from-your-system-4b249706)

```python
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
```

Use `http://127.0.0.1:5000/trigger-webhook-in` to trigget the in webhook and send the request.

## Test server locally against Orca Cloud

To expose the server securely from localhost and test it easily against the real Orca Cloud environment you can use [Secure Tunnels](https://ngrok.com/docs/secure-tunnels#what-are-ngrok-secure-tunnels). Take a look at [Ngrok](https://ngrok.com/) or [Cloudflare](https://www.cloudflare.com/).

```bash
ngrok http 5000
```

## Troubleshooting

If you run into any issues not listed here, please [open a ticket](https://github.com/orca-scan/orca-webhook-python/issues).

## Examples in other langauges
* [orca-webhook-dotnet](https://github.com/orca-scan/orca-webhook-dotnet)
* [orca-webhook-python](https://github.com/orca-scan/orca-webhook-python)
* [orca-webhook-go](https://github.com/orca-scan/orca-webhook-go)
* [orca-webhook-java](https://github.com/orca-scan/orca-webhook-java)
* [orca-webhook-php](https://github.com/orca-scan/orca-webhook-php)
* [orca-webhook-node](https://github.com/orca-scan/orca-webhook-node)

## History

For change-log, check [releases](https://github.com/orca-scan/orca-webhook-python/releases).

## License

&copy; Orca Scan, the [Barcode Scanner app for iOS and Android](https://orcascan.com).
