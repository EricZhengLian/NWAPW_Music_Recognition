const port = 3200;

const express 		= require('express');
const path 			= require('path');
const formidable	= require('formidable');
const fs 			= require('fs');
const cookieParser 	= require('cookie-parser');
const spawn 		= require("child_process");

var app = express();

const http 	= require('http').Server(app);
const io 	= require('socket.io')(http);


app.use(express.static(__dirname + '/www'));
app.use(cookieParser());
//app.use(parser.urlencoded({extended: true}));

var users = {};
users = JSON.parse(fs.readFileSync('users.json'));
console.log(users);

function Save()
{
	console.log("saving");
	fs.writeFileSync('users.json', JSON.stringify(users));
}
setInterval(Save, 10000)

app.post('/compare', (req, res) => {
	const form = new formidable.IncomingForm();
	form.parse(req, function(err, fields, files){
		var userID = fields.userID;
		console.log("user " + userID + " has uploaded a file for comparison. ");
		if(users[userID] == undefined)
		{
			return; //the user doesn't exist. they shouldn't be uploading stuff
		}
		users[userID]["uploads"].push({"name": path.basename(files.file.name), "complete": false, "match": "", "confidence": 0});
		var oldPath = files.file.path;
		var newPath = path.join(__dirname, "comparisons/" + path.basename(files.file.name));
		var rawData = fs.readFileSync(oldPath);
        fs.writeFile(newPath, rawData, function(err){
            if(err) console.log(err);
            return console.log("Successfully uploaded");
        });
        

        var process = spawn.spawn('python3', ['../core/onCompare.py', path.basename(files.file.name), userID])
        console.log("A wild process has appeared!")
        process.stdout.on('data', function(data)
        {
        	//console.log(data.toString())
        	console.log("got data");
        	console.log(data.toString())
        	try{
				var asJson = JSON.parse(data.toString());
	        	console.log("Got file upload data from user " + asJson.userID);
				var upload = users[asJson.userID]["uploads"][0]
				for(var i in users[asJson.userID]["uploads"])
					if(users[asJson.userID]["uploads"][i]["name"] == asJson.fileName) upload = users[asJson.userID]["uploads"][i]
				console.log("Upload: " + upload); //upload is what we want to modify
				upload["complete"] = asJson.complete;
				upload["match"] = asJson.match;
				upload["confidence"] = asJson.confidence;
        	}
        	catch{
        		console.log("Not JSON data")
        		return;
        	}
        	
        	//users[asJson.userID]["uploads"][]
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
		socket.emit("sendUserUploads", users[userID]["uploads"]);
	});

});



http.listen(port);
console.log('working on port ' + port);
