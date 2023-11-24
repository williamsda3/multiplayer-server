const express = require('express');
const http = require('http');
const socketIO = require('socket.io');
const bodyParser = require('body-parser');

const app = express();
const server = http.createServer(app);
const io = socketIO(server);

const port = process.env.PORT || 3000;

// Middleware to parse JSON
app.use(bodyParser.json());

// Serve static files (if needed)
app.use(express.static('public'));

// Keep track of player moves
const playerMoves = {
  player1: null,
  player2: null,
};

// Endpoint to receive moves
app.post('/move', (req, res) => {
  const { player, move } = req.body;
  playerMoves[player] = move;

  // Broadcast moves to all connected clients
  io.emit('moves', playerMoves);

  res.json({ success: true });
});

// Socket.io connection handler
io.on('connection', (socket) => {
  console.log('A user connected');

  // Send current moves to the newly connected client
  socket.emit('moves', playerMoves);

  // Handle disconnection
  socket.on('disconnect', () => {
    console.log('User disconnected');
  });
});

// Start the server
server.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
