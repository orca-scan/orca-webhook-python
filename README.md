# orca-webhook-python

Example of how to build an [Orca Scan WebHook](https://orcascan.com/docs/api/webhooks) endpoint in using [Python](https://www.python.org/) and [flask](https://github.com/pallets/flask) framework.

## Install

First ensure you have [Python](https://www.python.org/downloads/) installed:

```bash
# should return 3.7 or higher
python3 --version
```

Then execute the following:

```bash
# download this example code
git clone https://github.com/orca-scan/orca-webhook-python.git

# go into the new directory
cd orca-webhook-python

# create virtual environment and activate it
python3 -m venv orca && source ./orca/bin/activate

# upgrade pip to latest version
pip install --upgrade pip

# install dependencies
pip install -r requirements.txt
```

## Run

```bash
# activate virtual environment
source ./orca/bin/activate

# enable development features only for development
export FLASK_ENV=development

# start the project
flask run
```

Your WebHook receiver will now be running on port 5000.

You can emulate an Orca Scan WebHook using [cURL](https://dev.to/ibmdeveloper/what-is-curl-and-why-is-it-all-over-api-docs-9mh) by running the following:

```bash
curl --location --request POST 'http://127.0.0.1:5000' \
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

## How this example works

This [example](app.py) uses the [flask](https://github.com/pallets/flask) framework:

```python
# POST / handler
@app.route('/', methods=['POST'])
def index():
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
    return "ok\n"
```

## Troubleshooting

If you run into any issues not listed here, please [open a ticket](https://github.com/orca-scan/orca-webhook-python/issues).

## Examples in other langauges
* [orca-webhook-dotnet](https://github.com/orca-scan/orca-webhook-dotnet)

## History

For change-log, check [releases](https://github.com/orca-scan/orca-webhook-python/releases).

## License

&copy; Orca Scan, the [Barcode Scanner app for iOS and Android](https://orcascan.com).