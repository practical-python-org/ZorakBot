import json

# Function to read data from JSON file
def read_json(file_path, category=None):
    with open(file_path, 'r') as f:
        if category:
            data = json.load(f)["server"][category]
        else:
            data = json.load(f)["server"]
    return data

# Function to write data to JSON file
def write_json(data, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


x = read_json('FAKE_DB_settings.json', 'info')
print(x)
