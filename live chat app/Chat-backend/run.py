# run.py
from app import create_app, db
from flask_socketio import SocketIO
from app.models import User, Message
from flask_jwt_extended import decode_token

from app import create_app, db
from app.socket_events import socketio

app = create_app()
socketio = SocketIO(app, cors_allowed_origins="*")

online_users = set()

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('authenticate')
def handle_authenticate(data):
    token = data.get('token')
    if not token:
        return
    try:
        decoded = decode_token(token)
        user_id = decoded['sub']
        online_users.add(user_id)
        print(f"✅ User {user_id} authenticated via socket")
    except Exception as e:
        print("❌ Invalid token:", e)

@socketio.on('send_message')
def handle_send_message(data):
    token = data.get('token')
    content = data.get('content')
    if not token or not content:
        return
    try:
        decoded = decode_token(token)
        user_id = decoded['sub']
        message = Message(content=content, sender_id=user_id)
        db.session.add(message)
        db.session.commit()
        socketio.emit('new_message', message.to_dict())
    except Exception as e:
        print("Error sending message:", e)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# if __name__ == "__main__":
#     socketio.run(app, host="127.0.0.1", port=5000, debug=True)



app = create_app()

if __name__ == '__main__':
    socketio.init_app(app)
    socketio.run(app, debug=True)

