#-*- coding: utf-8 -*-
from django import forms

class FormRestaurantes(forms.Form):
	Name=forms.CharField(label='Name',max_length=100, help_text='100 carácteres máximo.',error_messages={'necesario': 'Introducir tu nombre'})
	Restaurante_id=forms.CharField(label='Restaurante_id')
	Cuisine=forms.CharField(label='Cuisine')
	Borough=forms.CharField(label='Borough')
	AdressBuilding=forms.CharField(label='Adress building')
	AdressCoordX=forms.FloatField(label='Adress coordX')
	AdressCoordY=forms.FloatField(label='Adress coordY')
	AdressStreet=forms.CharField(label='Adress street')
	AdressZipcode=forms.IntegerField(label='Adress zipcode')