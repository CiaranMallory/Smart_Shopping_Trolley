
const { response } = require("express");
var express = require( "express" );
var app = express();
app.use( express.static( "./public" ) );
var http = require('http').Server(app);
const mysql = require('mysql')
const cors = require('cors');

app.use(express.urlencoded());
app.use(express.json());
app.use(cors())

// Create connection
const db = mysql.createConnection({
    host : 'localhost',
    user : 'root',
    password : '',
    database: 'smartshopper'
});

// Connect 
db.connect((err) => {
    if(err){
        throw err;
    }else{
        console.log('My sql connected');
    }
});

// Create table
app.get('/createtable/:username/:password', (req, res) => {
    let sql = `CREATE TABLE ${req.params.username}(id int AUTO_INCREMENT, password VARCHAR(255), date VARCHAR(255), PRIMARY KEY(id))`;
    let post = {password: `${req.params.password}`};
    let sql2 = `INSERT INTO ${req.params.username} SET ?`;
    db.query(sql, (err, result) => {
        if(err) throw err;
        return;
    });

    db.query(sql2, post, (err, result) => {
        if(err) throw err;
        res.json(result);
        return;
    });
});

// Search for user
app.get('/getuser/:username', (req, res) => {
    let sql = `SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '${req.params.username}'`;
    let query = db.query(sql, (err, result) => {
        if(err) throw err;
        //console.log(result);
        if(result.length === 0){
            res.json({userStatus: 0});
            return;
        } else {
            res.json({userStatus: 1});
            return;
        }
    });
});

// Search for users password
app.get('/getpassword/:username/:password', (req, res) => {
    let sql = `SELECT * FROM ${req.params.username} WHERE password = ${req.params.password}`;
    let query = db.query(sql, (err, result) => {
        if(err) throw err;
        //console.log(result);
        if(result.length === 0){
            res.json({passwordStatus: 0});
            return;
        } else {
            res.json({passwordStatus: 1});
            return;
        }
    });
});

// End Point for raspberry pi to send data to
app.post('/', function(req, res){
    var type = req.body.Type;
    var price = req.body.Price;
    //console.log("python: " + type);
    //console.log("python: " + price);
    global.globalType = type;
    global.globalPrice = price;
});

// End point for client to call to get item data
app.get('/Data', function(req, res) {
    var dataToSendToClient = {'Type': globalType, 'Price': globalPrice};
    // convert whatever we want to send (preferably should be an object) to JSON
    var JSONdata = JSON.stringify(dataToSendToClient);
    res.send(JSONdata);
});

// End point for client to send enable status to
app.post('/Enable', function(req, res){
    var Enable = req.body.Enable;
    //console.log("python: " + type);
    console.log(Enable);
    global.globalEnable = Enable;
});

// End point to send enable status to raspberry pi
app.get('/EnableStatus', function(req, res) {
    var dataToSendToClient = {'Enable': globalEnable};
    // convert whatever we want to send (preferably should be an object) to JSON
    var JSONdata = JSON.stringify(dataToSendToClient);
    res.send(JSONdata);
});

http.listen(3000, function(){
    console.log('Listening...');
});