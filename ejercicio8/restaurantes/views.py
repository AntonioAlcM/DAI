#-*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import Context
from restaurantes.forms import FormRestaurantes
from restaurantes.models import cliente_de_mongo
from django.http import JsonResponse
from django.core import serializers
import json


def index(request):
    return render(request, 'index.html')
@login_required
def redireccionar(request):	
	return render(request,'registrarRestaurante.html')
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
def devuelve_filas(request):
	if request.method == 'GET':
		desde = request.GET['fila']
	db=cliente_de_mongo.restaurantes
	collection=db.restaurants
	filas = collection.find().skip(int(desde)).limit(10)
	context=Context({'record':filas})
	return  render(request,'infoRestaurant.html', context)