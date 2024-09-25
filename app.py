from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# Set up MongoDB client and database
muri = 'mongodb+srv://devsahanisushilkumar:YF4Gpgtg0CBoikFX@cluster0.71cay.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
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
            event = {
                "author": data['pull_request']['user']['login'],
                "from_branch": data['pull_request']['head']['ref'],
                "to_branch": data['pull_request']['base']['ref'],
                "timestamp": datetime.utcnow(),
                "type": "pull_request"
            }

        # Handle the 'merge' event (if needed)
        elif event_type == 'merge':
            event = {
                "author": data['merge_commit']['committer']['name'],
                "from_branch": data['pull_request']['head']['ref'],
                "to_branch": data['pull_request']['base']['ref'],
                "timestamp": datetime.utcnow(),
                "type": "merge"
            }

        # If event is valid, store it in MongoDB
        if event:
            collection.insert_one(event)
            return jsonify({"status": "success"}), 200

        # For unsupported event types
        return jsonify({"status": "unsupported event type", "event_type": event_type}), 400


# API to fetch events for the frontend
@app.route('/get_events', methods=['GET'])
def get_events():
    events = list(collection.find().sort("timestamp", -1).limit(10))
    for event in events:
        event['_id'] = str(event['_id'])  # Convert ObjectId to string for JSON
    return jsonify(events)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
