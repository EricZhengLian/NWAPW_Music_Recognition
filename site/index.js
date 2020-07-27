const express = require('express');
const port = 3200;
//const parser = require('body-parser');
const path = require('path');
const formidable = require('formidable');
const fs = require('fs');
const cookieParser = require('cookie-parser');
const spawn = require("child_process");
var app = express();

const http = require('http').Server(app);
const io = require('socket.io')(http);


app.use(express.static(__dirname + '/www'));
app.use(cookieParser());
//app.use(parser.urlencoded({extended: true}));

var users = {}

app.post('/compare', (req, res) => {
	const form = new formidable.IncomingForm();
	form.parse(req, function(err, fields, files){
		var userID = fields.userID;
		console.log("user " + userID + " has uploaded a file for comparison. ");
		if(users[userID] == undefined)
		{
			return; //the user doesn't exist. they shouldn't be uploading stuff
		}
		users[userID]["uploads"].push({"name": path.basename(files.file.name), "complete": false});
		console.log(users[userID]);
		var oldPath = files.file.path;
		var newPath = path.join(__dirname, "comparisons/" + path.basename(files.file.name));
		var rawData = fs.readFileSync(oldPath);
        fs.writeFile(newPath, rawData, function(err){
            if(err) console.log(err);
            return console.log("Successfully uploaded");
        });
        

        var process = spawn.spawn('python3', ['examplescript.py'])
        process.stdout.on('data', function(data)
        {
        	console.log(data.toString())
        });
	});
	res.redirect("/");
});

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
	res.redirect("/");
});

io.on('connection', (socket) => {
	//console.log(socket);
	socket.on("userConnect", (userID) =>
	{
		console.log("user " + userID + " connected. ");
		if(users[userID] == undefined)
		{
			users[userID] = {"uploads": []};
		}
		//emit uploads from that user
		var sendingUploads = users[userID]["uploads"];
		console.log(sendingUploads);
		socket.emit("sendUserUploads", users[userID]["uploads"]);
	});

});
http.listen(port);
console.log('working on port ' + port);
