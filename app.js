const express = require('express');
var app = express();
var http = require('http').createServer(app);
var io = require('socket.io')(http);
const spawn =  require('child_process').spawn;

app.use(express.static('public'));

app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
});

io.on('connection', function(socket) {

  socket.on('login', function(data) {
    console.log('Client logged-in:\n name:' + data.name + '\n userid: ' + data.userid);

    socket.name = data.name;
    socket.userid = data.userid;

    io.emit('login', data.name );
  });
  
  socket.on('chat', function(data) {
    console.log('Message from %s: %s', socket.name, data.msg);
    console.log('Timestamp: %s', new Date(data.timestamp).toLocaleString());
    var msg = {
      from: {
        name: socket.name,
        userid: socket.userid
      },
      msg: data.msg,
      timestamp: data.timestamp,
      group: data.group
    };

 //    const pythonProcess = spawn('python', ['./test.py', data.msg]);
 //    pythonProcess.stdout.on('data', (data) => {
	// console.log("Message from python server:" + data);
	
	// var rec = {
	// 	group: msg.group,
	// 	participant: socket.userid,
	// 	recommendation: data.toString('utf-8')
	// };
	// console.log(rec);
	// //console.log(socket);
	// io.emit('rec', rec);
 //    }); 

    socket.broadcast.emit('chat', msg);
  });

  // force client disconnect from server
  socket.on('forceDisconnect', function() {
    socket.disconnect();
  })

  socket.on('disconnect', function() {
    console.log('user disconnected: ' + socket.name);
  });
});


http.listen(3000, function(){
  console.log('listening on *:3000');
});
