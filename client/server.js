const jsonServer = require('json-server');
const server = jsonServer.create();
const router = jsonServer.router('db.json');
const middlewares = jsonServer.defaults();

// Set up the server
server.use(middlewares);
server.use(jsonServer.bodyParser); // Allows the POST body to be parsed
server.use(router);

// Start the server on port 5000
server.listen(5000, () => {
  console.log('JSON Server is running on http://localhost:5000');
});
