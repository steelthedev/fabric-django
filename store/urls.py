
from django.urls import path,include
from . import views
app_name = "store"
urlpatterns = [
    path('', views.ProductView, name="product"),
    path('create-product', views.AddProducts, name="add_product"),
    path('login', views.LoginView, name="login" )
]

