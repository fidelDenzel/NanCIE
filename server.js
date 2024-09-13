// run it with "npm run start" or "node server.js"
const express = require('express');
const app = express();
const path = require('path');

// Serve static files from the current directory
app.use(express.static(path.join(__dirname)));

// Serve the index.html file on the root route
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// Handle requests to the room route and extract the roomHash
app.get('/room', (req, res) => {
  const roomHash = req.query.hash; // Get the roomHash from the URL query parameter
  // console.log(`Room Hash received: ${roomHash}`); // Logging roomHash to the console

  //for example : https://scaledrone.github.io/webrtc/index.html#315a9c
  console.log(`Client Address @ https://scaledrone.github.io/webrtc/index.html#${roomHash}`); 

  // Pass roomHash to the client, or use it however you need on the server side
  res.sendFile(path.join(__dirname, 'index.html')); // Serve the main HTML file
});

const PORT = 3005;
app.listen(PORT, () => {
  console.log(`Server is running at http://localhost:${PORT}`);
  
});

