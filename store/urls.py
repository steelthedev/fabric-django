
from django.urls import path,include
from . import views
app_name = "store"
urlpatterns = [
    path('login', views.LoginView, name="login" )
]

