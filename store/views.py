
from multiprocessing import context
from wsgiref import headers
from django.shortcuts import redirect, render
import requests
import json
from django.contrib import messages
from django.conf import settings
# Create your views here.
def LoginView(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        account_id = request.POST["account_id"]

        if username and password and account_id:
           
            base_url = "https://sandbox.copilot.fabric.inc/"

            path = f"api-identity/auth/local/login"

            url = base_url + path

            body = {
                "username":username,
                "password":password,
                "accountId":account_id
            }

            response = requests.post(url, json=body)

            response_data = response.json()

            access_token = response_data["accessToken"]

            if access_token:
                request.session["auth_token"] = access_token
                
                messages.info(request,"Login successful")

                return redirect("store:login")
    return render(request, 'store/login.html')


def ProductView(request):

    base_url = settings.BASE_URL
    path = f"api-product/v1/product"
    url = base_url + path
    token = request.session["auth_token"]

    headers ={
        "Authorization":token
    }

    params = {
        "page":1,
        "size":1
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        response_data = response.json()
        products = response_data
        
    return render(request,'store/products.html',products)