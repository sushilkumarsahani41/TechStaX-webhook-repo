from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

# Set up MongoDB client and database
muri = os.getenv('MONGO_URI', 'your-default-mongo-uri-here')  # Use environment variables for credentials
client = MongoClient(muri)
db = client['github_webhooks']
collection = db['events']

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/webhook', methods=['POST'])
def handle_webhook():
    if request.method == 'POST':
        data = request.json
        event_type = request.headers.get('X-GitHub-Event')

        event = None  # Initialize event as None

        try:
            # Handle the 'push' event
            if event_type == 'push':
                event = {
                    "author": data['pusher']['name'],
                    "to_branch": data['ref'].split('/')[-1],
                    "timestamp": datetime.utcnow(),
                    "type": "push"
                }

            # Handle the 'pull_request' event
            elif event_type == 'pull_request':
                if data['action'] == 'closed' and data['pull_request']['merged']:
                    # Handle the 'merge' event within the pull request
                    event = {
                        "author": data['pull_request']['user']['login'],
                        "from_branch": data['pull_request']['head']['ref'],
                        "to_branch": data['pull_request']['base']['ref'],
                        "merged_by": data['pull_request']['merged_by']['login'],
                        "timestamp": datetime.utcnow(),
                        "type": "merge"
                    }
                else:
                    # Normal pull request event
                    event = {
                        "author": data['pull_request']['user']['login'],
                        "from_branch": data['pull_request']['head']['ref'],
                        "to_branch": data['pull_request']['base']['ref'],
                        "timestamp": datetime.utcnow(),
                        "type": "pull_request"
                    }

            # If event is valid, store it in MongoDB
            if event:
                collection.insert_one(event)
                return jsonify({"status": "success"}), 200
            else:
                return jsonify({"status": "unsupported event type", "event_type": event_type}), 400

        except KeyError as e:
            return jsonify({"status": "error", "message": f"Missing key: {str(e)}"}), 400


# API to fetch events for the frontend
@app.route('/get_events', methods=['GET'])
def get_events():
    events = list(collection.find().sort("timestamp", -1).limit(10))
    for event in events:
        event['_id'] = str(event['_id'])  # Convert ObjectId to string for JSON
    return jsonify(events)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
