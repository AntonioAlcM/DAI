#-*- coding: utf-8 -*-
from django import forms
import urllib, json
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.bootstrap import InlineField
from django.core.exceptions import ValidationError 
class FormRestaurantes(forms.Form):
	Name=forms.CharField(max_length=100, help_text='100 carácteres máximo.',error_messages={'necesario': 'Introducir tu nombre'})
	Restaurante_id=forms.CharField()
	Cuisine=forms.CharField()
	Borough=forms.CharField()
	AdressBuilding=forms.CharField()
	AdressCoordX=forms.FloatField()
	AdressCoordY=forms.FloatField()
	AdressStreet=forms.CharField()
	AdressZipcode=forms.IntegerField()
	def clean(self):
		direccion_final=""
		direccion=str(self.cleaned_data.get('AdressStreet'))
		trocitos=direccion.split()
		for i in trocitos:
			direccion_final+=str(i)+('+')
			url = "https://maps.googleapis.com/maps/api/geocode/json?address="+str(direccion_final)+"&components=postal_code:"+str(self.cleaned_data.get('AdressZipcode'))+"|locality:"+str(self.cleaned_data.get('Borough'))+"&key=AIzaSyDEICkYChmmm--Uq6ket7gMWDHfjrIx0-Y"		
			print url
			response = urllib.urlopen(url)
			data = json.loads(response.read())
			print data['results'][0]['address_components'][0]
			print "\n",data['status']
			if data['status'] != 'OK':
				raise ValidationError(u'%s Dirección y código postal no coincide')
			return self.cleaned_data
	def __init__(self, *args, **kwargs):
		super(FormRestaurantes, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Registrar',css_class='btn btn-warning'))
		self.helper.layout = Layout(
		InlineField('Name', css_class='input-xlarge'),
  		InlineField('Restaurante_id', css_class='input-xlarge'),
  		InlineField('Cuisine', css_class='input-xlarge'),
  		InlineField('Borough', css_class='input-xlarge'),
  		InlineField('AdressBuilding', css_class='input-xlarge'),
  		InlineField('AdressCoordX', css_class='input-xlarge'),
  		InlineField('AdressCoordY', css_class='input-xlarge'),
  		InlineField('AdressStreet', css_class='input-xlarge'),
  		InlineField('AdressZipcode', css_class='input-xlarge'))






#class FormRestaurantes(forms.Form):
	#Name=forms.CharField(label='Name',max_length=100, help_text='100 carácteres máximo.',error_messages={'necesario': 'Introducir tu nombre'})
	#Restaurante_id=forms.CharField(label='Restaurante_id')
	#Cuisine=forms.CharField(label='Cuisine')
	#Borough=forms.CharField(label='Borough')
	#AdressBuilding=forms.CharField(label='Adress building')
	#AdressCoordX=forms.FloatField(label='Adress coordX')
	#AdressCoordY=forms.FloatField(label='Adress coordY')
	#AdressStreet=forms.CharField(label='Adress street')
	#AdressZipcode=forms.IntegerField(label='Adress zipcode')