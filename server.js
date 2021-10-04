const { response } = require("express");
var express = require( "express" );
var app = express();
app.use( express.static( "./public" ) );
var http = require('http').Server(app);

app.use(express.urlencoded());
app.use(express.json());

app.post('/', function(req, res){
    var msg = req.body.msg;
    console.log("python: " + msg);
    global.globalString = msg;
});

app.get('/Data', function(req,res) {
    if (globalString !== NULL){
        // make some calls to database, fetch some data, information, check state, etc...
        var dataToSendToClient = {'message': globalString};
        // convert whatever we want to send (preferably should be an object) to JSON
        var JSONdata = JSON.stringify(dataToSendToClient);
        res.send(JSONdata);
    } else{
        console.log('Message is empty');
    }
 });

http.listen(3000, function(){
console.log('listening...');
});