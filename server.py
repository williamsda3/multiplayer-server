import socketio
import eventlet
from flask_cors import CORS

eventlet.monkey_patch()

sio = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(sio)

# Use CORS
CORS(app)

# Dictionary to store moves from each player
player_moves = {}

@sio.event
def connect(sid, environ):
    print('Client connected:', sid)

@sio.event
def disconnect(sid):
    print('Client disconnected:', sid)

@sio.event
def send_move(sid, data):
    print(f'Received move from client {sid}: {data}')

    # Store the move for the player
    player_moves[sid] = data

    # Check if moves from both players are available
    if len(player_moves) == 2:
        # Determine the result based on the game logic (customize this part)
        result = determine_game_result(player_moves)

        # Emit the result to both players
        for player_sid, move in player_moves.items():
            sio.emit('show_result', {'move': move, 'result': result}, room=player_sid)

        # Clear stored moves for the next round
        player_moves.clear()

def determine_game_result(moves):
    # Customize this function based on your game logic
    # For example, you can compare moves and return the result
    # (e.g., 'player1_wins', 'player2_wins', 'draw')
    # This is a placeholder logic; you need to adapt it to your game rules.
    return 'result_placeholder'

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)
