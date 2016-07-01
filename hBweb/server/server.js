// importar
var express = require('express');
 
// instanciar
var app = express();
 
// ruteo
app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html' +'../app/index.html');
});
 
// escuchar
app.listen(9003);
 
console.log("Servidor Express escuchando en modo %s", app.settings.env);