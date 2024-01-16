
# Download json from Google Sheet
def download_json(credentials_name, sheet_name, worksheet_name, json_path):
    import gspread
    import json
    from oauth2client.service_account import ServiceAccountCredentials

    # Set up credentials for accessing Google Sheets
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_name, scope)
    gc = gspread.authorize(credentials)
    worksheet = gc.open(sheet_name).worksheet(worksheet_name)

    # Get all values from the worksheet
    data = worksheet.get_all_values()

    # Convert data to a list of dictionaries
    header = data[0]
    json_data = {"intents": []}

    for row in data[1:]:
        intent = {
            "tag": row[1],
            "patterns": row[2].split(";"),
            "responses": row[3].split(";")
        }
        json_data["intents"].append(intent)

    # Write JSON data to a file
    with open(json_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=2)

    print(f"Data successfully converted to JSON. Check {json_path}")


def load_json(filename):
    import json
    with open(filename, 'r') as file:
        return json.load(file)

# Load json file and parse it by delimiter ';'
def load_and_format_json(filename):
    json_data = load_json(filename)
    formatted_data = []
    for intent in json_data["intents"]:
        tag = intent["tag"]
        patterns = '; '.join(intent["patterns"])
        responses = '; '.join(intent["responses"])
        formatted_data.append([tag, patterns, responses])
    return formatted_data


# Merge two json files
def merge_json_data(json_path_1, json_path_2, json_path_merged):
    import json
    json_data_1 = load_json(json_path_1)
    json_data_2 = load_json(json_path_2)

    merged_data = {}

    # Process data from the first JSON file
    for intent in json_data_1["intents"]:
        tag = intent["tag"]
        merged_data[tag] = {
            "patterns": set(intent["patterns"]),
            "responses": set(intent["responses"])
        }

    # Process data from the second JSON file
    for intent in json_data_2["intents"]:
        tag = intent["tag"]
        if tag in merged_data:
            merged_data[tag]["patterns"].update(intent["patterns"])
            merged_data[tag]["responses"].update(intent["responses"])
        else:
            merged_data[tag] = {
                "patterns": set(intent["patterns"]),
                "responses": set(intent["responses"])
            }

    formatted_data = [{"tag": tag, "patterns": list(content["patterns"]), "responses": list(content["responses"])}
                      for tag, content in merged_data.items()]
    merged_json = {"intents": formatted_data}

    with open(json_path_merged, "w") as file:
        json.dump(merged_json, file, indent=2)


# Upload json file in  Google Sheet
def upload_json(credentials_name, sheet_name, worksheet_name, json_path):
    import gspread
    import json
    from oauth2client.service_account import ServiceAccountCredentials

    # Set up credentials for accessing Google Sheets
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_name, scope)
    client = gspread.authorize(credentials)

    worksheet = client.open(sheet_name).worksheet(worksheet_name)
    worksheet.clear()

    data = load_and_format_json(json_path)
    headers = ["Tag", "Patterns", "Responses"]
    data.insert(0, headers)  # Add headers at the beginning

    # Use a single request to append all rows
    worksheet.append_rows(data)

    print("Sheet updated successfully.")

if __name__ == "__main__":
    credentials_name = 'keys/chatbot-solent-79013b82a47d.json'
    sheet_name = 'ChatbotSolent'
    worksheet_name = 'Merged'
    worksheet_name_upload = 'Rules_uploaded'
    json_path_google = 'Test_json_files/intents_google.json'
    json_path_initial = 'intents.json'
    json_path_merged = 'intents.json'
    # Comment functions that you don't need to run
    #download_json(credentials_name=credentials_name, sheet_name=sheet_name, worksheet_name=worksheet_name, json_path=json_path_google)
    #merge_json_data(json_path_1=json_path_google, json_path_2=json_path_initial, json_path_merged=json_path_merged)
    upload_json(credentials_name=credentials_name, sheet_name=sheet_name,worksheet_name=worksheet_name_upload, json_path=json_path_merged)
