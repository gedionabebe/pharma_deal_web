import pyrebase
from django.shortcuts import render,redirect

from django.http import HttpResponse
import requests
from authentication import firebase
from datetime import datetime, timezone
import pytz,string,random


db = firebase.database

def post_create(request):

    if request.session['status'] == 'logged_in':
        if request.session['privilege'] == 'pharmacies':
            user = firebase.auth.refresh(request.session['refreshidtoken'])
            product_id = request.POST['product_id']
            product_name = request.POST['medicine']
            product_image = request.POST['url']
            distributor_id = request.POST['distributor']
            price = request.POST['cost']
            pharmacy_id = request.session["user_id"]
            distributor_number = db.child('Distributors').child('%s'%distributor_id).get(user['idToken']).val()['phone_number']
            pharmacy_number = db.child('Pharmacies').child('%s'%pharmacy_id).get(user['idToken']).val()['phone_number']
            pharmacy_name =  firebase.database.child('Pharmacies').child('%s'%pharmacy_id).get(user['idToken']).val()['name']
            distributor_name = db.child('Distributors').child('%s'%distributor_id).get(user['idToken']).val()['name']
            request_id = ''.join(random.choices(string.ascii_lowercase + string.digits,k=7))
            time_of_request = str(datetime.now(timezone.utc).astimezone(pytz.timezone('Africa/Addis_Ababa')))

            data = {'product_id':'%s'%product_id, 'product_name':'%s'%product_name, 'product_image':'%s'%product_image,
                    'distributor_id':'%s'%distributor_id, 'price':'%s'%price, 'pharmacy_id':'%s'%pharmacy_id,
                    'distributor_number':'%s'%distributor_number, 'pharmacy_number':'%s'%pharmacy_number, 'pharmacy_name':'%s'%pharmacy_name,
                    'distributor_name':'%s'%distributor_name, 'request_id':'req_00%s'%request_id, 'time_of_request':'%s'%time_of_request, 'status': "pending",
            }
            try:
                db.child('transaction').child('req_00%s'%request_id).set(data,user['idToken'])
                return redirect('/transaction/cart_check')
            except requests.HTTPError as e:
                print('first',e)
                return render(request, 'unauthorized.html')
        return redirect('/products/browse')
    return redirect('/authentication/')

def post_check(request):
    if request.session['status'] == 'logged_in':
        if request.session['privilege'] == 'distributors':
            user = firebase.auth.refresh(request.session['refreshidtoken'])
            distributor_id = request.session['user_id']
            try:
                dist_requests = db.child('transaction').order_by_child('distributor_id').equal_to('%s'%distributor_id).get(user['idToken']).val()
                return render(request,"post_check.htm",{'dist_requests': dist_requests})
            except requests.HTTPError as e:
                print('first',e)
                return render(request, 'unauthorized.html')
        return redirect('/products/browse')
    return redirect('/authentication/')

def accept(request):
    user = firebase.auth.refresh(request.session['refreshidtoken'])
    request_id = request.POST['request_id']
    try:
        db.child("transaction").child('%s'%request_id).update({'status':'accepted'},user['idToken'])
        return redirect('/transaction/post_check')
    except requests.HTTPError as e:
                print('first',e)
                return render(request, 'unauthorized.html')

def decline(request):
    user = firebase.auth.refresh(request.session['refreshidtoken'])
    request_id = request.POST['request_id']
    try:
        db.child("transaction").child('%s'%request_id).update({'status':'declined'},user['idToken'])
        return redirect('/transaction/post_check')
    except requests.HTTPError as e:
                print('first',e)
                return render(request, 'unauthorized.html')

def cart_check(request):

    if request.session['status'] == 'logged_in':
        if request.session['privilege'] == 'pharmacies':
            pharmacy_id = request.session['user_id']
            user = firebase.auth.refresh(request.session['refreshidtoken'])
            try:
                pharma_requests = db.child('transaction').order_by_child('pharmacy_id').equal_to('%s'%pharmacy_id).get(user['idToken']).val()
                return render(request,"cart_check.htm",{'pharma_requests': pharma_requests})
            except requests.HTTPError as e:
                print('first',e)
                return render(request, 'unauthorized.html')
        return redirect('/products/browse')
    return redirect('/authentication/')

   