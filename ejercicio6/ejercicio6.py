# -*- coding: utf-8 -*-

import tweepy, feedparser, datetime, shelve, pymongo, hashlib, os
from lxml import etree
from pymongo import MongoClient
from flask import Flask, session, flash, render_template, request,jsonify
app = Flask(__name__)

@app.route('/')
def cargaPagina():
	get=cargarRestaurantes()
	feeds=mostrarRSS()
	return render_template('index.html', get=get, feeds=feeds)

@app.route('/login', methods=['POST', 'GET'])
def login():
	session['url']=[]
	session['url'].insert(0,'index.html')
	error = None
	if request.method == 'POST':
		usuario=request.form['usuario']
		if valid_login(request.form['usuario'],request.form['contrasena']):
			session['usuario'] = request.form['usuario']
			session['contrasena'] =request.form['contrasena']
			return logueado()
		else:
			error = 'Usuario o contraseña invalida'
	return render_template('index.html', error=error)

@app.route('/registrar', methods=['POST', 'GET'])
def registrar():
	conectarBD()
	try:
		if shelf.has_key(request.form['usuario'].encode('utf-8')) == False:
			shelf[request.form['usuario'].encode('utf-8')] = {'usuario': request.form['usuario'].encode('utf-8') , 'contrasena': codificarContrasenha(request.form['contrasena'].encode('utf-8')).hexdigest()}
		else:
				shelf.close()
				return render_template('registrar.html')	
	finally:
		shelf.close()
	session['usuario'] =request.form['usuario']
	session['contrasena'] = request.form['contrasena']
	return logueado()

@app.route('/modificar', methods=['POST', 'GET'])
def modificar():
	shelf = shelve.open('usuarios.db')
	try:
		usuario=session['usuario'].encode('utf-8')
		us=shelf[usuario.encode('utf-8')]
		if(request.form['usuario'].encode('utf-8')== us['usuario']):
			if(request.form['contrasena'].encode('utf-8')!= us['contrasena']):
				us['contrasena'] = codificarContrasenha(request.form['contrasena'].encode('utf-8')).hexdigest()
				shelf[usuario.encode('utf-8')]=us
		else:
			if shelf.has_key(request.form['usuario'].encode('utf-8')) == False:
				if us['contrasena'] == codificarContrasenha(request.form['contrasena'].encode('utf-8')).hexdigest() :
					contrasenha=us['contrasena']
				else:
					contrasenha=codificarContrasenha(request.form['contrasena'].encode('utf-8')).hexdigest() 					
					del shelf[usuario]
					shelf[request.form['usuario'].encode('utf-8')] = {'usuario': request.form['usuario'].encode('utf-8') , 'contrasena': codificarContrasenha(request.form['contrasena'].encode('utf-8')).hexdigest()}
			else:
				shelf.close()
				return render_template('modificar.html')	
	finally:
		shelf.close()
	session['usuario'] =request.form['usuario']
	session['contrasena'] = request.form['contrasena']	
	return logueado()


def  valid_login(usuario, contrasenha):
	shelf = shelve.open('usuarios.db')
	contrasenha = codificarContrasenha(request.form['contrasena'].encode('utf-8'))
	if shelf.has_key(usuario.encode('utf-8')):
		if contrasenha.hexdigest() == shelf[usuario.encode('utf-8')].get('contrasena'):
			return True
		else:
			return False
	else:
		return False
	shelf.close()

@app.route('/redireccionar')
def redireccionar():
	pagina_direccionada = request.args.get('pagina')
	if pagina_direccionada == "registrar":
		return render_template('registrar.html')
	elif pagina_direccionada=='modificar':
		return render_template('modificar.html')
	else :
		return render_template('verDatos.html')

@app.route('/logueado')
def logueado():
	return render_template('logueado.html')

@app.route('/cerrarSesion')
def cerrarSesion():
	session.pop('usuario', None)
	session.pop('contrasena', None)
	session.pop('url', None)
	return render_template('index.html')

def codificarContrasenha(contrasenha):
	return hashlib.md5(contrasenha.encode('utf-8'))


@app.errorhandler(404)
def page_not_found(error):
    return "Página no encontrada", 404

app.secret_key = os.urandom(24)

#Contenido práctica 4

def conectarBD():
	try:
		conn=MongoClient ( 'localhost', 27017)
		db=conn.restaurantes
		print ("Connected successfully!!!")
	except (pymongo.errors.ConnectionFailure, e):
		print ("Could not connect to MongoDB: %s" % e) 
	return db 

@app.route('/info')
def infoRestaurant():
	return render_template('infoRestaurant.html', record=buscarRestaurante(request.args.get('identificador')))

def cargarRestaurantes():
	db=conectarBD()
	collection = db.restaurants
	get =collection.find()[:10]
	return get

def buscarRestaurante(identificador):
	db=conectarBD()
	collection = db.restaurants
	get =collection.find({"restaurant_id" : identificador})
	return get[0]

@app.route('/modificarRestaurante')
def modificarRestaurante():
	return render_template('modificarRestaurante.html', record=buscarRestaurante(request.args.get('identificador')))

@app.route('/modRestaurant', methods=['POST', 'GET'])
def modRestaurant():
	db=conectarBD()
	collection = db.restaurants 
	collection.update({"restaurant_id" : request.form['restaurant_id']}, { "address" : {"coord" : [ request.form['coordX'], request.form['coordY'] ],"building" : request.form['building'],"street" : request.form['street'],"zipcode" : request.form['zipcode']}	, "borough" : request.form['borough'], "cuisine" : request.form['cuisine'], "name" : request.form['name'],"restaurant_id" : request.form['restaurant_id']})
	return cargaPagina()

@app.route('/buscadorDeRestaurantes', methods=['POST', 'GET'])
def buscadorDeRestaurantes():
	db=conectarBD()
	collection = db.restaurants
	busqueda=request.form['busqueda']
	if collection.find({"restaurant_id" : busqueda}).count() > 0:
		get = collection.find({"restaurant_id" : busqueda})
		return render_template('busqueda.html', get=get)
	elif collection.find({"name" : busqueda}).count() > 0:
		get = collection.find({"name" : busqueda})
		return render_template('busqueda.html', get=get)
	elif collection.find({"borough" : busqueda}).count() > 0:
		get = collection.find({"borough" : busqueda})
		return render_template('busqueda.html', get=get)
	elif collection.find({"cuisine" : busqueda}).count() > 0:
		get = collection.find({"cuisine" : busqueda})
		return render_template('busqueda.html', get=get)
	elif collection.find({"address.street" : busqueda }).count() > 0:
		get = collection.find({"address.street" : busqueda })
		return render_template('busqueda.html', get=get)
	else:
		return cargaPagina()

@app.route('/crearRestaurante', methods=['POST', 'GET'])
def crearRestaurante():
	return render_template('crearRestaurante.html')

@app.route('/crearRestaurant', methods=['POST', 'GET'])
def crearRestaurant():
	db=conectarBD()
	collection = db.restaurants 
	if collection.find({"restaurant_id" : request.form['restaurant_id']}).count()<=0:
		collection.insert({ "address" : {"coord" : [ request.form['coordX'], request.form['coordY'] ],"building" : request.form['building'],"street" : request.form['street'],"zipcode" : request.form['zipcode']}	, "borough" : request.form['borough'], "cuisine" : request.form['cuisine'], "name" : request.form['name'],"restaurant_id" : request.form['restaurant_id']})
		return render_template('infoRestaurant.html', record=buscarRestaurante(request.form['restaurant_id']))
	else:
		return render_template('crearRestaurante.html')

#Contenido practica 5
@app.route('/obtener_filas')
def devuelve_filas():
	db=conectarBD()
	collection = db.restaurants 
	desde = request.args.get('fila')
	filas = collection.find().skip(int(desde)).limit(10)
	nombres=[]
	calles=[]
	cocina=[]
	restaurant_id=[]
	borough=[]
	for record in filas:
		calles.append(record['address']['street'])
		borough.append(record['borough'])
		cocina.append(record['cuisine'])
		nombres.append(record['name'])
		restaurant_id.append(record['restaurant_id'])
	return jsonify( calles, borough, cocina,nombres, restaurant_id)

#contenido practica6

def mostrarRSS():
	feeds = feedparser.parse('http://estaticos.elmundo.es/elmundo/rss/portada.xml')
	return feeds
@app.route('/estadistica')
def verEstadistica():
	return render_template('estadistica.html')

@app.route('/obtener_informacion' )
def devuelve_informacion():
	db=conectarBD()
	collection = db.restaurants 
	score2011=[]
	score2012=[]
	score2013=[]
	score2014=[]
	grado2011=[]
	grado2012=[]
	grado2013=[]
	grado2014=[]
	i=0;
	for record in collection.find():
		for d in record["grades"]:
			if i < 100:

				if d['date'].year == 2011:
					score2011.append(d['score'])
				elif d['date'].year == 2012:
					score2012.append(d['score'])
				elif d['date'].year == 2013:
					score2013.append(d['score'])
				elif d['date'].year == 2014:
					score2014.append(d['score'])

				if d['date'].year == 2011:
					if d['grade']!='Not Yet Graded':
						grado2011.append(ord(d['grade'])-65)
				elif d['date'].year == 2012:
					if d['grade']!='Not Yet Graded':
						grado2012.append(ord(d['grade'])-65)
				elif d['date'].year == 2013:
					if d['grade']!='Not Yet Graded':
						grado2013.append(ord(d['grade'])-65)
				elif d['date'].year == 2014:
					if d['grade']!='Not Yet Graded':
						grado2014.append(ord(d['grade'])-65)
			i+=1
	return jsonify(score2011,score2012,score2013,score2014, grado2011,grado2012,grado2013,grado2014)

@app.route('/verMapa')
def verMapa():
	return render_template('mapa.html')


@app.route('/coordenadas')
def devuelve_coordenadas():
	db=conectarBD()
	collection = db.restaurants 
	coordenadas=[]
	for record in collection.find():
		coordenadas.append(record['address']['coord'])
	return jsonify(coordenadas)

@app.route('/Twitter')
def busquedaTwitter():
	return render_template('busquedaTwitter.html')

@app.route('/buscarTwitter', methods=['POST', 'GET'])
def buscarTwitter():
	busquedaTwitter=request.form['busquedaTwitter']
	print busquedaTwitter
	# Consumer keys and access tokens, used for OAuth
	consumer_key = 'OgC0wVydfZDZHbC6onEu2bbmn'
	consumer_secret = 'ymqHDavE3s3OBI9Y9BMfvlRT58fstgjueK2XJMquRkPgENDtnE'
	access_token = '806079390144757761-tHxKOGrI4iM4IgSUnjhmFscfnFC0FdS'
	access_token_secret = '0bBrvX9s6DwimawJQOSmmHYk5sGtYD4QyyjcnplSJQPJZ'
	# OAuth process, using the keys and tokens
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	# Creation of the actual interface, using authentication
	api = tweepy.API(auth)
	geocode="37.1722794,-3.5993356,150km"
	# https://dev.twitter.com/docs/api/1.1/get/search/tweets
	tweets = api.search(q=busquedaTwitter, count=200)
	# Mostramos los campos del objeto Tweet
	return render_template('busquedaTwitter.html', tweets=tweets)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
