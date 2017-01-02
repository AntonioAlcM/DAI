#-*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import Context
from restaurantes.forms import FormRestaurantes
from restaurantes.models import cliente_de_mongo
from django.http import JsonResponse
from django.core import serializers
import json
from bson import json_util
import tweepy

def index(request):
    return render(request, 'index.html')
@login_required
def redireccionar(request):	
	return render(request,'registrarRestaurante.html')
@login_required	
def modificarRestaurante(request):
	db=cliente_de_mongo.restaurantes
	collection=db.restaurants
	get =collection.find()[:10]
	context=Context({'coleccion':get})
	return render(request,'modificarRestaurante.html', context)

def test(request):
    return render(request,'test.html', {})
@login_required		   
def registrarRestaurante(request):
	if request.method == 'POST':
		form = FormRestaurantes(request.POST)		
		if form.is_valid():
			username = form.cleaned_data['Name']
			return crearRestaurant(request,form)
		else:
			print("Los errores son: ", form.errors.as_data())
	else:
		form = FormRestaurantes()
		return render(request, 'index.html')
@login_required
def crearRestaurant(request,form):
	db=cliente_de_mongo.restaurantes
	collection=db.restaurants
	if collection.find({"restaurant_id" : form.cleaned_data['Restaurante_id']}).count()==0:
		collection.insert({ "address" : {"coord" :  [form.cleaned_data['AdressCoordX'],  form.cleaned_data['AdressCoordY'] ],"building" :  form.cleaned_data['AdressBuilding'],"street" :  form.cleaned_data['AdressStreet'],"zipcode" : form.cleaned_data['AdressZipcode']}	, "borough" : form.cleaned_data['Borough'], "cuisine" : form.cleaned_data['Cuisine'], "name" : form.cleaned_data['Name'],"restaurant_id" : form.cleaned_data['Restaurante_id']})
		return buscarRestaurante(request,form.cleaned_data['Restaurante_id'])
	else:
		return render(request,'existeRestaurante.html')
@login_required
def buscarRestaurante(request,identificador):
	db=cliente_de_mongo.restaurantes
	collection=db.restaurants
	get =collection.find({"restaurant_id" : identificador})
	context=Context({'record':get[0]})
	return  render(request,'infoRestaurant.html', context)
@login_required
def modificarUnRestaurante(request,identificador):
	db=cliente_de_mongo.restaurantes
	collection=db.restaurants
	get =collection.find({"restaurant_id" : identificador})
	context=Context({'record':get[0]})
	return  render(request,'modificar.html', context)
@login_required	
def buscadorDeRestaurantes(request):
	if request.method == "POST":
		db=cliente_de_mongo.restaurantes
		collection=db.restaurants
		busqueda=request.POST['search']
		if collection.find({"restaurant_id" : busqueda}).count() > 0:
			get = collection.find({"restaurant_id" : busqueda})
			context=Context({'coleccion':get})
			return  render(request,'busqueda.html', context)
		elif collection.find({"name" : busqueda}).count() > 0:
			get = collection.find({"name" : busqueda})
			context=Context({'coleccion':get})
			return  render(request,'busqueda.html', context)
		elif collection.find({"borough" : busqueda}).count() > 0:
			get = collection.find({"borough" : busqueda})
			context=Context({'coleccion':get})
			return  render(request,'busqueda.html', context)
		elif collection.find({"cuisine" : busqueda}).count() > 0:
			get = collection.find({"cuisine" : busqueda})
			context=Context({'coleccion':get})
			return  render(request,'busqueda.html', context)
		elif collection.find({"address.street" : busqueda }).count() > 0:
			get = collection.find({"address.street" : busqueda })
			context=Context({'coleccion':get})
			return  render(request,'busqueda.html', context)
		else:
			return index(request)
	else:
		return index(request)
@login_required	
def redireccionarBuscarRestaurante(request):	
	return render(request,'buscarRestaurante.html')

@login_required	
def devuelve_filas(request):
	desde = request.GET['fila']
	db=cliente_de_mongo.restaurantes
	collection=db.restaurants
	lista = []
	filas = collection.find().skip(int(desde)).limit(10)
	for record in filas:
		diccionario={}
		diccionario["addres"]=record['address']['street']
		diccionario["borough"]=record['borough']
 		diccionario["cuisine"]=record['cuisine']
 		diccionario["name"]=record['name']
 		diccionario["restaurant_id"]=record['restaurant_id']
 		diccionario["coord"]=record['address']['coord']
 		diccionario["zipcode"]=record['address']['zipcode']
 		lista.append(diccionario)
	return  JsonResponse(lista, safe=False)

@login_required	
def redireccionarMapa(request):
	return render(request,'mapa.html')


@login_required	
def devuelve_coordenadas(request):
	db=cliente_de_mongo.restaurantes
	collection=db.restaurants 
	coordenadas=[]
	for record in collection.find().limit(100):
		coordenadas.append(record['address']['coord'])
	return JsonResponse(coordenadas, safe=False)
@login_required	
def redireccionarEstadistica(request):
	return render(request, 'estadistica.html')

@login_required	
def devuelve_informacion(request):
	db=cliente_de_mongo.restaurantes
	collection=db.restaurants
	score2011=[]
	score2012=[]
	score2013=[]
	score2014=[]
	grado2011=[]
	grado2012=[]
	grado2013=[]
	grado2014=[]
	datos=[]
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
	datos.append(score2011)
	datos.append(score2012)
	datos.append(score2013)
	datos.append(score2014)
	datos.append(grado2011)
	datos.append(grado2012)
	datos.append(grado2013)
	datos.append(grado2014)
	return JsonResponse(datos,safe=False)

@login_required	
def redireccionarTwitter(request):
	return render(request, 'busquedaTwitter.html')
@login_required	
def buscarTwitter(request):
	busquedaTwitter=request.POST['search']
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
	context=Context({'tweets':tweets})
	return render(request,'busquedaTwitter.html', context)
@login_required
def modRestaurante(request):
	if request.method == 'POST':
		db=cliente_de_mongo.restaurantes
		collection=db.restaurants
		collection.update({"restaurant_id" : request.POST['restaurant_id']}, { "address" : {"coord" : [ request.POST['coordX'], request.POST['coordY'] ],"building" : request.POST['building'],"street" : request.POST['street'],"zipcode" : request.POST['zipcode']}	, "borough" : request.POST['borough'], "cuisine" : request.POST['cuisine'], "name" : request.POST['name'],"restaurant_id" : request.POST['restaurant_id']})
	return buscarRestaurante(request, request.POST['restaurant_id'])


