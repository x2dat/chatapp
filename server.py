from flask import Flask, request
from flask_socketio import SocketIO, send

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Store messages (temporary storage)
messages = []

@app.route("/")
def home():
    return "Chat Server is Running!"

@socketio.on("message")
def handle_message(msg):
    print(f"Received: {msg}")
    messages.append(msg)  # Store messages
    send(msg, broadcast=True)  # Send message to all clients

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=10000)  # Use the correct port
