"""ejercicio7 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
    """
from django.conf.urls import url, include
from django.contrib import admin
from registration.backends.simple.views import RegistrationView
from django.contrib.auth.views import (password_reset, password_reset_done,
    	password_reset_confirm, 
    	password_reset_complete,
    # these are the two new imports
    password_change,
    password_change_done,
    )

# Create a new class that redirects the user to the index page, if successful at logging
class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
	   return '/restaurantes/'

urlpatterns = [
	url(r'^restaurantes/', include('restaurantes.urls')),
	url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
	url(r'^accounts/', include('registration.backends.simple.urls')),
	url(r'^accounts/password/change/$', password_change, {
			'template_name': 'registration/password_change_form.html'}, 
			name='password_change'),
	url(r'^accounts/password/change/done/$', password_change_done, 
			{'template_name': 'registration/password_change_done.html'},
			name='password_change_done'),
	url(r'^admin/', admin.site.urls),
	]
