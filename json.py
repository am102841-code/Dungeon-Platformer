import json

data = {"name": "Knight", "level": 1}
json_string = json.dumps(data)
print("JSON String:", json_string)

loaded_data = json.loads(json_string)
print("Loaded Data:", loaded_data)
