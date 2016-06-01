"""
from pymongo import MongoClient


client = MongoClient(const.MONGODB)

db = client['local']
collection = db['local']
startlog = db.startup_log
startlog.find_one()
"""

from pymongo import Connection
import constantes.py as const
 
def mongomanager():
 
 conex = Connection(const.MONGODB)
 
 def databases():
  print "Control de BD's , Que deseas hacer?"
  entrada = raw_input("- [1]Visualizar BD's | [2]Crear BD's | [3]Borrar BD's | [4]Home -> ")
  if entrada == '1':
   var = conex.database_names()
   print var
   databases()
  elif entrada == '2':
   name = raw_input("Nombre de la BD que quieres crear -> ")
   global db 
   db = conex.name
   databases()
  elif entrada == '3':
   delname = raw_input("Nombre de la BD que quieres eliminar -> ")
   conex.drop_database(delname)
   databases()
  elif entrada == '4':
   mongomanager()
  else:
   print "Error\n"
   mongomanager()
 
 def collections():
  print "Control de Colecciones , que deseas hacer?"
  entrada = raw_input("- [1]Visualizar colecciones | [2]Crear coleccion | [3]Home -> ")
  if entrada == '1':
   var = db.collection_names()
   print var
   collections()
  elif entrada == '2':
   global collectname 
   collectname = raw_input("Nombre de la coleccion que quieres crear -> ")
   collect = db.collectname
   collections()
  elif entrada == '3':
   mongomanager()
  else:
   print "error\n"
   mongomanager()
 
 def documents():
  print "Control de Documentos , que deseas hacer?"
  entrada = raw_input("[1]Crear documento | [2]Busqueda de documentos | [3]Eliminar documento | [4]Home -> ")
  if entrada == '1':
   #Escriba el contenido de esta manera "name":"sanko" por ejemplo.
   document = raw_input("Escriba el contenido del doc => ")
   collectname.insert({"name":"sankito"})
   documents()
  elif entrada == '2':
   content = raw_input("Parametros del contenido -> ")
   var = collectname.find(content)
   print var
   documents()
  elif entrada == '3':
   choosedel = raw_input("Desea vaciar el documento(1) o borrar algo especifico(2) -> ")
   if choosedel == '1':
    collectname.drop()
    documents()
   elif choosedel == '2':
    delcontent = raw_input("Parametros del borrado -> ")
    collectname.remove(delcontent)
    documents()
   else:
    print "error\n"
    documents()
  else:
   print "error\n"
   mongomanager()
 
 entrada = raw_input("PyMongo Manager => Exit(0) | Control BD's(1) | Control Colecciones(2) | Control de Documentos(3) -> ")
 if entrada == '0':
  exit
 elif entrada == '1':
  databases()
 elif entrada == '2':
  collections()
 elif entrada == '3':
  documents()
 else:
  print "Error\n"
  mongomanager()
 
mongomanager()