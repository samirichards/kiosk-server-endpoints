import datetime
import sys
from flask import Flask, request, jsonify
import json
import mysql.connector
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

db = mysql.connector.connect(
    host="cmp408db.cd4gki5ztccc.eu-west-2.rds.amazonaws.com",
    user="admin",
    password="password101",
    database="cmp408main"
)

# Function to check if the API key is valid
def is_valid_api_key(api_key):
    cursor = db.cursor()
    query = "SELECT deviceID FROM registered_devices WHERE deviceAPIKey = %s"
    cursor.execute(query, (api_key,))
    result = cursor.fetchone()
    return result[0]


#Function to receive device feedback data
@app.route('/add_data', methods=['POST'])
def add_data():
    print('Run', file=sys.stderr, flush=True)
    # Parse the incoming JSON data
    data = request.get_json()

    # Validate the input
    if not data:
        print('No input data provided', file=sys.stderr, flush=True)
        return jsonify({'status': 'error', 'message': 'No input data provided'})
    api_key = data.get('api_key')
    if not api_key:
        print('No API Key provided', file=sys.stderr, flush=True)
        return jsonify({'status': 'error', 'message': 'No API key provided'})

    # Check if the API key is valid
    device_id = is_valid_api_key(api_key)
    if device_id == -1:
        print('Invalid API Key', file=sys.stderr, flush=True)
        return jsonify({'status': 'error', 'message': 'Invalid API key'})

    # Extract the other necessary data from the JSON
    record_value = data.get('record_value')
    if not record_value:
        print('No Record value provided', file=sys.stderr, flush=True)
        return jsonify({'status': 'error', 'message': 'No record value provided'})

    # Add the data to the database
    record_time = datetime.datetime.now()
    cursor = db.cursor()
    query = "INSERT INTO records (recordTime, recordValue, associatedDeviceID) VALUES (%s, %s, %s)"
    values = (record_time, record_value, device_id)
    cursor.execute(query, values)
    db.commit()

    print('Data added to database', file=sys.stdout)
    return jsonify({'status': 'success', 'message': 'Data added to the database'})

@app.route('/test')
def index():
    print('Welp, it wasn\'t that, file=sys.stderr', flush=True)
    return 'Hello again world!'

if __name__ == '__main__':
    app.run(debug=True)