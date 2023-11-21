var http = require('http');
var fs = require('fs');
var io = require('socket.io')(http);

var app = http.createServer(function(request,response){
    var url = request.url;
    if(request.url == '/'){
      url = '/index.html';
    }
    if(request.url == '/favicon.ico'){
      return response.writeHead(404);
    }
    response.writeHead(200);
    response.end(fs.readFileSync(__dirname + url));
 
});

io.on('connection', function(socket) {
	/*
	socket.on('login', function(data) {
		console.log('Client logged-in:\n name:' + data.name + '\n userid: ' + data.userid);
		socket.name = data.name;
		socket.userid = data.userid;
		io.emit('login', data.name);
	});

	socket.on('chat', function(data) {
		console.log('Message from %s: %s', socket.name, data.msg);
		var msg = {
			from: {
				name: socket.name,
				userid: socket.userid
			},
			msg: data.msg
		};

		socket.broadcast.emit('chat', msg);
	});

	socket.on('forceDisconnect', function() {
		socket.disconnect();
	});

	socket.on('disconnect', function() {
		console.log('user disconnected: ' + socket.name);
	}); */
	console.log('a user connected');
});

app.listen(3000);
