
from django.urls import path,include
from . import views
app_name = "store"
urlpatterns = [
    path('', views.ProductView, name="product"),
    path('login', views.LoginView, name="login" )
]

