import json
from flask import Flask, request, jsonify
from src.json_utils import get_json_file

app = Flask(__name__)
app.url_map.strict_slashes = False

BILLS_PATH = './data/bills_info.json'

def save_json(json_content, path):
  with open(path, 'w') as bills_file:  
    bills_file.write(json.dumps(json_content))

@app.get("/bills")
def get_bills():
  return jsonify(get_json_file(path=BILLS_PATH))

@app.post("/bills")
def add_bill():
  if request.is_json:
    bill = request.get_json()
    bill_list = get_json_file(path=BILLS_PATH)

    # Added an autogenerated id.
    bill['id'] = len(bill_list) + 1
    bill_list.append(bill)

    # Save the bill into the JSON file.
    save_json(bill_list, path=BILLS_PATH)
    return bill, 201
    
  return {"error": "Request must be JSON"}, 415

@app.delete("/bills/<bill_id>")
def delete_bill(bill_id):
  # Filter the bill id sent
  bill_list = list(filter(lambda bill: str(bill['id']) != str(bill_id), get_json_file(path=BILLS_PATH)))

  # Save the bill id
  save_json(bill_list, path=BILLS_PATH)
  return "Deleted {}".format(bill_id), 201