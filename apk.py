from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# In-memory storage for connections (for demonstration purposes)
connections = []

@app.route('/', methods=['GET', 'OPTIONS'])
def home():
     if request.method == 'OPTIONS':
        # Respond to preflight request
        response = jsonify({
            "message": "CORS preflight response",
            "allowed_methods": ["GET", "OPTIONS", "POST"]
        })
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "GET, OPTIONS, POST")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response, 200
     return jsonify({"message": "Welcome to the API!"}), 200

@app.route('/connect', methods=['POST'])
def connect_users():
    user_id = request.json.get('userId')
    connection_id = request.json.get('connectionId')
    
    if user_id and connection_id:
        connections.append((user_id, connection_id))
        return jsonify({"message": f"Connected {user_id} to {connection_id}"}), 200
    return jsonify({"error": "Invalid input"}), 400

@app.route('/disconnect', methods=['POST'])
def disconnect_users():
    user_id = request.json.get('userId')
    connection_id = request.json.get('connectionId')

    if user_id and connection_id in [conn[1] for conn in connections if conn[0] == user_id]:
        connections.remove((user_id, connection_id))
        return jsonify({"message": f"Disconnected {user_id} from {connection_id}"}), 200
    return jsonify({"error": "Connection not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
