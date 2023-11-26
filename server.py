import socketio
from flask import Flask, render_template
from gevent import monkey
from geventwebsocket.handler import WebSocketHandler
from gunicorn.app.base import BaseApplication
from werkzeug.serving import run_with_reloader

monkey.patch_all()

sio = socketio.Server(cors_allowed_origins='*')
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/socket.io/<path:remaining>')
def socketio_endpoint(remaining):
    # Handle Socket.IO requests directly through the Socket.IO server
    socketio_manage(request.environ, {'/': sio}, request)

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

class GunicornApp(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        for key, value in self.options.items():
            self.cfg.set(key, value)

    def load(self):
        return self.application

if __name__ == '__main__':
    options = {
        'bind': '0.0.0.0:5000',
        'workers': 1,
        'worker_class': 'geventwebsocket.gunicorn.workers.GeventWebSocketWorker',
        'timeout': 3600
    }

    run_with_reloader(GunicornApp(app, options).run)
