from django.conf.urls import url
from . import views           # This line is new!

app_name = "wish_list_app"
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^create$', views.create_wish, name = "create_wish"),
    url(r'^add$', views.add_wish, name = "add_wish"),
  
  	url(r'^join/(?P<number>\d+)$', views.join_wish, name = "join_wish"),
  	url(r'^(?P<number>\d+)$', views.show_wish, name = "show_wish"),

    url(r'^delete/(?P<number>\d+)$', views.delete, name="delete"),
    url(r'^confirm_delete/(?P<number>\d+)$', views.confirm_delete, name ="confirm_delete"),

    url(r'^remove/(?P<number>\d+)$', views.remove, name="remove"),
    url(r'^confirm_remove/(?P<number>\d+)$', views.confirm_remove, name ="confirm_remove"),

  	url(r'^clear$', views.clear, name="clear"),
   
    ]