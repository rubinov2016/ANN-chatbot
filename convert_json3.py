import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

# Set up credentials for accessing Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('keys/chatbot-solent-79013b82a47d.json', scope)
gc = gspread.authorize(credentials)


# Open the Google Sheet by title or key
sheet_name = 'ChatbotSolent'
worksheet_name = 'Rules'  # Replace with the actual worksheet name
worksheet = gc.open(sheet_name).worksheet(worksheet_name)

# Get all values from the worksheet
data = worksheet.get_all_values()

# Convert data to a list of dictionaries
header = data[0]
json_data = {"intents": []}

for row in data[1:]:
    intent = {
        "tag": row[0],
        "patterns": row[1].split(";"),  # Assuming patterns are comma-separated
        "responses": row[2].split(";")  # Assuming responses are comma-separated
    }
    json_data["intents"].append(intent)

# Write JSON data to a file
with open('intents.json', 'w') as json_file:
    json.dump(json_data, json_file, indent=2)

print("Data successfully converted to JSON. Check 'intents.json'.")
