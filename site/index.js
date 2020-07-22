var express = require('express');
const port = "3200";
const parser = require('body-parser');


//const { body,validationResult } = require('express-validator/check');
//const { sanitizeBody } = require('express-validator/filter');

var app = express();

app.use(express.static(__dirname + '/www'));
app.use(parser.urlencoded({extended: true}));

app.post('/upload', (req, res) => {
	console.log("Name: ", req.body.audio_name);
	console.log("Artist: ", req.body.artist_name);
	console.log("File: ", req.body.file)
	res.redirect("/");
});

app.listen(port);
console.log('working on port ' + port);
/*
body("audio_name", "Invallid Name").isLength({min: 2})
body("artist_name", "Invallid Artist").isLength({min: 2})
*/
