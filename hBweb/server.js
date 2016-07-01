// importar
var express = require('express');
var path = require('path');
// instanciar
var app = express();
app.use(express.static(__dirname));
 
// ruteo
app.get('*', function(req, res){
  res.sendFile(path.join(__dirname + '/app/index.html'));
});
 
// escuchar
app.listen(9003);
 
console.log("Servidor Express escuchando en modo %s", app.settings.env);