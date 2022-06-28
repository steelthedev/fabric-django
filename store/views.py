import datetime
from urllib import response
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


def AddProducts(request):
    if request.method == "POST":
        sku = request.POST["sku"]
        title = request.POST["title"]
        nodeName = request.POST["nodeName"]
        image = request.POST["image"]
        price = request.POST["price"]
        weight = request.POST["weight"]
        status = request.POST["status"]

        print(nodeName)


        base_url = settings.BASE_URL
        path = f"api-product/v1/product/bulk/insert"
        url = base_url + path
        token = request.session["auth_token"]
        date =datetime.datetime.now()
        d=date.strftime("%m/%d/%Y, %H:%M:%S")
        headers ={
          
            "x-site-context":json.dumps({"stage":"sandbox", "channel":12, "account":"60ec78e9fb4cf000085cf0b9",  "date":d}),
            "Content-Type":"application/json"
        }

        body =[
                 {
                "sku": sku,
                "type": "ITEM",
                "nodeName":nodeName,
                "attributeValues": [
                {
                    "name": "title",
                    "value": title
                },
                  {
                    "name": "image",
                    "value": image
                },
                  {
                    "name": "price",
                    "value": price
                },
                  {
                    "name": "weight",
                    "value": weight
                },
                  {
                    "name": "status",
                    "value": "TRUE"
                }
                ],
            }
            ]
            

        response = requests.post(url, headers=headers, json = body)

        if response.status_code == 200:
            r = response.json()
            print(r)
    return render(request,'store/create_products.html')