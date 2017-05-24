from django.conf.urls import url
from . import views

urlpatterns = [

	#user index
	url(r'^$', views.index, name= 'index'),
	url(r'^signup$', views.create_signup, name = "signup"),
	url(r'^login$', views.login, name= "login"),
	url(r'logout$', views.destroy, name= "logout" ),
	# latest secrets
	url(r'^secrets$', views.show, name= "show"),
	url(r'^secrets/create$', views.create_secrets, name="create_secrets"),
	url(r'^secrets/delete_secrets$', views.delete_secrets, name='delete_secrets'),
	url(r'^secrets/like$', views.like_recent, name="secret_like"),
	url(r'^secrets/un_like$', views.un_like_recent, name="secret_un_like"),
	# most populair
	url(r'^secrets/populair$', views.populair, name="populair"),
	url(r'^secrets/delete_secrets_pop$', views.delete_secrets_pop, name='delete_secrets_pop'),
	url(r'^secrets/like_pop$', views.like_pop, name="secret_like_pop"),
	url(r'^secrets/un_like_pop$', views.un_like_pop, name="secret_un_like_pop"),
]