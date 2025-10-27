from flask_socketio import SocketIO, emit
from app import db
from app.models import Message

socketio = SocketIO(cors_allowed_origins="*")

@socketio.on('join')
def handle_join(data):
    username = data.get('username')
    emit('receive_message', {'username': 'System', 'message': f'{username} joined the chat'}, broadcast=True)

@socketio.on('send_message')
def handle_message(data):
    username = data.get('username')
    message = data.get('message')

    # Save to DB
    msg = Message(username=username, message=message)
    db.session.add(msg)
    db.session.commit()

    # Broadcast to all clients
    emit('receive_message', {'username': username, 'message': message}, broadcast=True)
