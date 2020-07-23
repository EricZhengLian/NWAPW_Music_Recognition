const express = require('express');
const port = 3200;
const parser = require('body-parser');
var app = express();

const http = require('http').Server(app);
const io = require('socket.io')(http);


app.use(express.static(__dirname + '/www'));
app.use(parser.urlencoded({extended: true}));

app.post('/upload', (req, res) => {
	error = "";
	console.log("Name: ", req.body.audio_name);
	if(req.body.file == undefined) error = "Please provide a file. "
	if(req.body.artist_name.length < 3) error = "Artist name too short";
	if(req.body.audio_name.length < 3) error = "Track title too short";
	console.log("Artist: ", req.body.artist_name);
	console.log("File: ", req.body.file);
	res.redirect("/");
});

io.on('connection', (socket) => {
	console.log(socket);
});
http.listen(port);
console.log('working on port ' + port);
