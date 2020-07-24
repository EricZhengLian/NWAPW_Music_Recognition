const express = require('express');
const port = 3200;
//const parser = require('body-parser');
const path = require('path');
const formidable = require('formidable');
const fs = require('fs');
var app = express();

const http = require('http').Server(app);
const io = require('socket.io')(http);


app.use(express.static(__dirname + '/www'));
//app.use(parser.urlencoded({extended: true}));

app.post('/upload', (req, res) => {
	//console.log("Name: ", req.body.audio_name);
	//console.log("Artist: ", req.body.artist_name);
	//console.log("File: ", req.body.file);
	const form = new formidable.IncomingForm();
	form.parse(req, function(err, fields, files)
	{
		console.log("Uploading file...");
		console.log(fields);
		var oldPath = files.file.path;
		var newPath = path.join(__dirname, "uploads/" + "TITLE " + fields.audio_name + " %%% " + path.basename(files.file.name));
		var rawData = fs.readFileSync(oldPath) 
        fs.writeFile(newPath, rawData, function(err){
            if(err) console.log(err);
            return console.log("Successfully uploaded");
        });
	});
	// if(req.body.file == undefined) error = "Please provide a file. "
	// if(req.body.artist_name.length < 3) error = "Artist name too short";
	// if(req.body.audio_name.length < 3) error = "Track title too short";
	res.redirect("/");
});

io.on('connection', (socket) => {
	//console.log(socket);
});
http.listen(port);
console.log('working on port ' + port);
